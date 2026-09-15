"""Tests des regles metier officielles, sections M1 a M8 du cahier des charges.

Chacun de ces tests a ete ecrit ROUGE, avant la correction qu'il exige.
Le filet de inventaire/test_inventaire.py decrit ce que le code fait ;
ce fichier decrit ce que le code doit faire.
"""

from inventaire import references_en_alerte


def article(**surcharges):
    valeurs = {"ref": "VIS-M6", "lib": "Vis M6", "q": 50, "pu": 2.0, "seuil": 10, "cat": "piece"}
    valeurs.update(surcharges)
    return valeurs


def test_m2_un_article_pile_au_seuil_est_en_alerte():
    assert references_en_alerte([article(q=10, seuil=10)]) == ["VIS-M6"]
