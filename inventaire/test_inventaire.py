"""Filet de tests du module de stock.

Ces tests decrivent ce que le code fait AUJOURD'HUI, pas ce qu'il devrait faire.
Quand le comportement observe contredit une regle metier, la regle concernee est
citee dans le nom du test et l'ecart est reporte dans RAPPORT-QUALITE.md.
"""

from inventaire import (
    alerte,
    classer,
    cout,
    export_json,
    message_de_rotation,
    messages_de_diagnostic,
    mouv,
    par_cat,
    rapport,
    rot,
    val,
)


def article(**surcharges):
    valeurs = {"ref": "VIS-M6", "lib": "Vis M6", "q": 50, "pu": 2.0, "seuil": 10, "cat": "piece"}
    valeurs.update(surcharges)
    return valeurs


# --- val ------------------------------------------------------------------


def test_val_d_un_stock_vide_vaut_zero():
    assert val([]) == 0


def test_val_additionne_quantite_fois_prix():
    assert val([article(q=2, pu=1.5), article(q=3, pu=2.0)]) == 9.0


def test_val_arrondit_au_centime():
    assert val([article(q=3, pu=0.333)]) == 1.0


def test_val_ignore_une_quantite_nulle():
    assert val([article(q=0, pu=5.0)]) == 0


def test_val_ignore_une_quantite_negative_au_lieu_de_la_soustraire():
    assert val([article(q=-5, pu=2.0)]) == 0


# --- alerte ---------------------------------------------------------------


def test_alerte_signale_un_article_sous_son_seuil():
    assert alerte([article(q=5, seuil=10)]) == ["VIS-M6"]


def test_alerte_ignore_un_article_pile_au_seuil_alors_que_la_regle_m2_l_exige():
    assert alerte([article(q=10, seuil=10)]) == []


def test_alerte_ignore_un_article_au_dessus_du_seuil():
    assert alerte([article(q=11, seuil=10)]) == []


def test_alerte_ne_renvoie_que_les_references_concernees():
    articles = [article(ref="BAS", q=1, seuil=10), article(ref="HAUT", q=99, seuil=10)]
    assert alerte(articles) == ["BAS"]


# --- cout -----------------------------------------------------------------


def test_cout_est_nul_hors_alerte():
    assert cout(article(q=50, seuil=10)) == 0


def test_cout_remonte_a_trois_fois_le_seuil():
    assert cout(article(q=4, seuil=10, pu=2.0)) == 52.0


def test_cout_n_applique_pas_la_remise_a_cent_unites_alors_que_la_regle_m5_l_exige():
    assert cout(article(q=20, seuil=40, pu=1.0)) == 100.0


def test_cout_applique_la_remise_a_cent_une_unites():
    assert cout(article(q=19, seuil=40, pu=1.0)) == 90.9


def test_cout_est_nul_pour_un_article_pile_au_seuil():
    assert cout(article(q=10, seuil=10, pu=1.0)) == 0


# --- classer --------------------------------------------------------------


def test_classer_ordonne_de_la_plus_grosse_valeur_a_la_plus_petite():
    petit = article(ref="PETIT", q=1, pu=1.0)
    gros = article(ref="GROS", q=10, pu=100.0)
    moyen = article(ref="MOYEN", q=5, pu=10.0)
    classes = [a["ref"] for a in classer([petit, gros, moyen])]
    assert classes == ["GROS", "MOYEN", "PETIT"]


def test_classer_ne_reordonne_pas_la_liste_recue():
    origine = [article(ref="A", q=1), article(ref="B", q=9)]
    classer(origine)
    assert [a["ref"] for a in origine] == ["A", "B"]


# --- rot ------------------------------------------------------------------


def test_rot_donne_les_jours_de_stock_restants():
    assert rot(article(q=60), 30) == 60


def test_rot_arrondit_a_l_entier_inferieur():
    assert rot(article(q=14), 300) == 1


def test_rot_renvoie_zero_sans_vente_alors_que_la_regle_m7_exige_une_erreur():
    assert rot(article(q=50), 0) == 0


# --- par_cat --------------------------------------------------------------


def test_par_cat_ventile_la_valeur_par_categorie():
    articles = [
        article(cat="outil", q=2, pu=10.0),
        article(cat="outil", q=1, pu=5.0),
        article(cat="piece", q=4, pu=2.5),
    ]
    assert par_cat(articles) == {"outil": 25.0, "piece": 10.0}


def test_par_cat_range_une_categorie_inconnue_dans_autre():
    assert par_cat([article(cat="drone", q=1, pu=3.0)]) == {"autre": 3.0}


# --- mouv -----------------------------------------------------------------


def test_mouv_retire_la_quantite_demandee():
    a = article(q=50)
    assert mouv(a, 10) is True
    assert a["q"] == 40


def test_mouv_ajoute_la_quantite_demandee():
    a = article(q=50)
    assert mouv(a, 10, t="in") is True
    assert a["q"] == 60


def test_mouv_refuse_un_retrait_superieur_au_stock():
    assert mouv(article(q=50), 51) is False


def test_mouv_laisse_le_stock_negatif_apres_un_refus_alors_que_la_regle_m3_l_interdit():
    a = article(q=50)
    mouv(a, 51)
    assert a["q"] == -1


def test_mouv_refuse_une_quantite_nulle_ou_negative():
    a = article(q=50)
    assert mouv(a, 0) is False
    assert mouv(a, -3) is False
    assert a["q"] == 50


def test_mouv_refuse_un_type_de_mouvement_inconnu():
    a = article(q=50)
    assert mouv(a, 5, t="transfert") is False


def test_mouv_alimente_le_journal_fourni():
    journal = []
    mouv(article(q=50), 5, j=journal)
    assert journal[0]["ref"] == "VIS-M6"
    assert journal[0]["q"] == 5


# --- rapport --------------------------------------------------------------


def test_rapport_utilise_la_date_fournie():
    assert rapport([article()], d="2019-03-05")["date"] == "2019-03-05"


def test_rapport_compte_et_valorise_les_articles_retenus():
    res = rapport([article(q=10, pu=10.0)], d="x")
    assert res["nb"] == 1
    assert res["valeur"] == 100.0


def test_rapport_ajoute_la_tva_de_vingt_pour_cent():
    assert rapport([article(q=10, pu=10.0)], d="x")["ttc"] == 120.0


def test_rapport_ecarte_un_article_sans_stock():
    res = rapport([article(q=0)], d="x")
    assert res["nb"] == 0
    assert res["valeur"] == 0


def test_rapport_ecarte_un_article_sans_prix():
    res = rapport([article(pu=0)], d="x")
    assert res["nb"] == 0


def test_rapport_filtre_sur_la_categorie_demandee():
    articles = [article(ref="A", cat="outil"), article(ref="B", cat="piece")]
    assert rapport(articles, cat="outil", d="x")["nb"] == 1


def test_rapport_filtre_sur_une_quantite_minimale():
    articles = [article(ref="A", q=5), article(ref="B", q=500)]
    assert rapport(articles, seuil_min=100, d="x")["nb"] == 1


def test_rapport_omet_un_article_pile_au_seuil_de_ses_alertes():
    res = rapport([article(q=10, seuil=10)], d="x")
    assert res["alertes"] == []


def test_rapport_ne_modifie_aucun_article():
    a = article(q=50)
    rapport([a], d="x")
    assert a["q"] == 50


# --- export_json ----------------------------------------------------------


def test_export_json_ecrit_le_rapport_et_renvoie_l_historique(tmp_path):
    chemin = tmp_path / "inv.json"
    historique = export_json({"valeur": 12.5}, chemin=str(chemin), hist=[])
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
