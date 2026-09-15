"""Filet de tests du module de stock.

Ces tests decrivent ce que le code fait AUJOURD'HUI, pas ce qu'il devrait faire.
Quand le comportement observe contredit une regle metier, la regle concernee est
citee dans le nom du test et l'ecart est reporte dans RAPPORT-QUALITE.md.
"""

from inventaire import (
    ajouter_au_stock,
    classer_par_valeur,
    cout_de_reapprovisionnement,
    exporter_historique,
    generer_rapport,
    message_de_rotation,
    messages_de_diagnostic,
    references_en_alerte,
    retirer_du_stock,
    rotation_en_jours,
    valeur_du_stock,
    valeur_par_categorie,
)


def article(**surcharges):
    valeurs = {"ref": "VIS-M6", "lib": "Vis M6", "q": 50, "pu": 2.0, "seuil": 10, "cat": "piece"}
    valeurs.update(surcharges)
    return valeurs


# --- val ------------------------------------------------------------------


def test_val_d_un_stock_vide_vaut_zero():
    assert valeur_du_stock([]) == 0


def test_val_additionne_quantite_fois_prix():
    assert valeur_du_stock([article(q=2, pu=1.5), article(q=3, pu=2.0)]) == 9.0


def test_val_arrondit_au_centime():
    assert valeur_du_stock([article(q=3, pu=0.333)]) == 1.0


def test_val_ignore_une_quantite_nulle():
    assert valeur_du_stock([article(q=0, pu=5.0)]) == 0


def test_val_ignore_une_quantite_negative_au_lieu_de_la_soustraire():
    assert valeur_du_stock([article(q=-5, pu=2.0)]) == 0


# --- alerte ---------------------------------------------------------------


def test_alerte_signale_un_article_sous_son_seuil():
    assert references_en_alerte([article(q=5, seuil=10)]) == ["VIS-M6"]


def test_alerte_signale_un_article_pile_au_seuil():
    assert references_en_alerte([article(q=10, seuil=10)]) == ["VIS-M6"]


def test_alerte_ignore_un_article_au_dessus_du_seuil():
    assert references_en_alerte([article(q=11, seuil=10)]) == []


def test_alerte_ne_renvoie_que_les_references_concernees():
    articles = [article(ref="BAS", q=1, seuil=10), article(ref="HAUT", q=99, seuil=10)]
    assert references_en_alerte(articles) == ["BAS"]


# --- cout -----------------------------------------------------------------


def test_cout_est_nul_hors_alerte():
    assert cout_de_reapprovisionnement(article(q=50, seuil=10)) == 0


def test_cout_remonte_a_trois_fois_le_seuil():
    assert cout_de_reapprovisionnement(article(q=4, seuil=10, pu=2.0)) == 52.0


def test_cout_applique_la_remise_a_cent_unites():
    assert cout_de_reapprovisionnement(article(q=20, seuil=40, pu=1.0)) == 90.0


def test_cout_applique_la_remise_a_cent_une_unites():
    assert cout_de_reapprovisionnement(article(q=19, seuil=40, pu=1.0)) == 90.9


def test_cout_commande_pour_un_article_pile_au_seuil():
    assert cout_de_reapprovisionnement(article(q=10, seuil=10, pu=1.0)) == 20.0


# --- classer --------------------------------------------------------------


def test_classer_ordonne_de_la_plus_grosse_valeur_a_la_plus_petite():
    petit = article(ref="PETIT", q=1, pu=1.0)
    gros = article(ref="GROS", q=10, pu=100.0)
    moyen = article(ref="MOYEN", q=5, pu=10.0)
    classes = [a["ref"] for a in classer_par_valeur([petit, gros, moyen])]
    assert classes == ["GROS", "MOYEN", "PETIT"]


def test_classer_ne_reordonne_pas_la_liste_recue():
    origine = [article(ref="A", q=1), article(ref="B", q=9)]
    classer_par_valeur(origine)
    assert [a["ref"] for a in origine] == ["A", "B"]


# --- rot ------------------------------------------------------------------


def test_rot_donne_les_jours_de_stock_restants():
    assert rotation_en_jours(article(q=60), 30) == 60


def test_rot_arrondit_a_l_entier_inferieur():
    assert rotation_en_jours(article(q=14), 300) == 1


def test_rot_renvoie_zero_sans_vente_alors_que_la_regle_m7_exige_une_erreur():
    assert rotation_en_jours(article(q=50), 0) == 0


# --- par_cat --------------------------------------------------------------


def test_par_cat_ventile_la_valeur_par_categorie():
    articles = [
        article(cat="outil", q=2, pu=10.0),
        article(cat="outil", q=1, pu=5.0),
        article(cat="piece", q=4, pu=2.5),
    ]
    assert valeur_par_categorie(articles) == {"outil": 25.0, "piece": 10.0}


def test_par_cat_range_une_categorie_inconnue_dans_autre():
    assert valeur_par_categorie([article(cat="drone", q=1, pu=3.0)]) == {"autre": 3.0}


# --- mouv -----------------------------------------------------------------


def test_un_retrait_diminue_le_stock():
    a = article(q=50)
    assert retirer_du_stock(a, 10) is True
    assert a["q"] == 40


def test_un_ajout_augmente_le_stock():
    a = article(q=50)
    assert ajouter_au_stock(a, 10) is True
    assert a["q"] == 60


def test_un_retrait_superieur_au_stock_est_refuse():
    assert retirer_du_stock(article(q=50), 51) is False


def test_un_refus_laisse_le_stock_intact():
    a = article(q=50)
    retirer_du_stock(a, 51)
    assert a["q"] == 50


def test_une_quantite_nulle_ou_negative_est_refusee():
    a = article(q=50)
    assert retirer_du_stock(a, 0) is False
    assert retirer_du_stock(a, -3) is False
    assert a["q"] == 50


def test_le_journal_fourni_est_alimente():
    journal = []
    retirer_du_stock(article(q=50), 5, journal=journal)
    assert journal[0]["ref"] == "VIS-M6"
    assert journal[0]["q"] == 5


# --- rapport --------------------------------------------------------------


def test_rapport_utilise_la_date_fournie():
    assert generer_rapport([article()], date_du_rapport="2019-03-05")["date"] == "2019-03-05"


def test_rapport_compte_et_valorise_les_articles_retenus():
    res = generer_rapport([article(q=10, pu=10.0)], date_du_rapport="x")
    assert res["nb"] == 1
    assert res["valeur"] == 100.0


def test_rapport_ajoute_la_tva_de_vingt_pour_cent():
    assert generer_rapport([article(q=10, pu=10.0)], date_du_rapport="x")["ttc"] == 120.0


def test_rapport_ecarte_un_article_sans_stock():
    res = generer_rapport([article(q=0)], date_du_rapport="x")
    assert res["nb"] == 0
    assert res["valeur"] == 0


def test_rapport_ecarte_un_article_sans_prix():
    res = generer_rapport([article(pu=0)], date_du_rapport="x")
    assert res["nb"] == 0


def test_rapport_filtre_sur_la_categorie_demandee():
    articles = [article(ref="A", cat="outil"), article(ref="B", cat="piece")]
    assert generer_rapport(articles, categorie="outil", date_du_rapport="x")["nb"] == 1


def test_rapport_filtre_sur_une_quantite_minimale():
    articles = [article(ref="A", q=5), article(ref="B", q=500)]
    assert generer_rapport(articles, quantite_minimale=100, date_du_rapport="x")["nb"] == 1


def test_rapport_signale_un_article_pile_au_seuil():
    res = generer_rapport([article(q=10, seuil=10)], date_du_rapport="x")
    assert res["alertes"] == ["VIS-M6"]


def test_rapport_ne_modifie_aucun_article():
    a = article(q=50)
    generer_rapport([a], date_du_rapport="x")
    assert a["q"] == 50


# --- export_json ----------------------------------------------------------


def test_export_json_ecrit_le_rapport_et_renvoie_l_historique(tmp_path):
    chemin = tmp_path / "inv.json"
    historique = exporter_historique({"valeur": 12.5}, chemin=str(chemin), historique=[])
    assert historique == [{"valeur": 12.5}]
    assert chemin.read_text(encoding="utf-8") == '[{"valeur": 12.5}]'


# --- diagnostic, extrait du corps de rapport ------------------------------


def test_un_stock_vide_est_signale():
    assert messages_de_diagnostic([article(q=0)]) == ["stock vide VIS-M6"]


def test_un_prix_invalide_est_signale():
    assert messages_de_diagnostic([article(pu=0)]) == ["prix invalide VIS-M6"]


def test_un_article_sous_son_seuil_est_signale_avec_sa_quantite():
    messages = messages_de_diagnostic([article(q=5, seuil=10)])
    assert messages == ["ALERTE VIS-M6 : 5 restants"]


def test_moins_de_sept_jours_de_stock_est_une_rupture_imminente():
    assert message_de_rotation(article(q=10), 300) == "RUPTURE IMMINENTE VIS-M6"


def test_moins_de_trente_jours_de_stock_est_a_surveiller():
    assert message_de_rotation(article(q=100), 300) == "a surveiller VIS-M6"


def test_plus_de_trente_jours_de_stock_ne_dit_rien():
    assert message_de_rotation(article(q=1000), 300) is None


def test_une_periode_sans_vente_est_signalee():
    assert message_de_rotation(article(q=10), 0) == "aucune vente pour VIS-M6"
