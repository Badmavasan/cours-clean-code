"""Tests des regles metier officielles, sections M1 a M8 du cahier des charges.

Chacun de ces tests a ete ecrit ROUGE, avant la correction qu'il exige.
Le filet de inventaire/test_inventaire.py decrit ce que le code fait ;
ce fichier decrit ce que le code doit faire.
"""

from inventaire import cout_de_reapprovisionnement, references_en_alerte, retirer_du_stock


def article(**surcharges):
    valeurs = {"ref": "VIS-M6", "lib": "Vis M6", "q": 50, "pu": 2.0, "seuil": 10, "cat": "piece"}
    valeurs.update(surcharges)
    return valeurs


def test_m2_un_article_pile_au_seuil_est_en_alerte():
    assert references_en_alerte([article(q=10, seuil=10)]) == ["VIS-M6"]


def test_m5_la_remise_s_applique_a_partir_de_cent_unites_incluses():
    # seuil 40 donne une cible de 120, quantite 20 donne 100 unites commandees
    assert cout_de_reapprovisionnement(article(q=20, seuil=40, pu=1.0)) == 90.0


def test_m3_un_retrait_refuse_laisse_le_stock_inchange():
    stock = article(q=50)
    assert retirer_du_stock(stock, 51) is False
    assert stock["q"] == 50
