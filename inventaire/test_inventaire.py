"""Filet de tests du module de stock.

Ces tests decrivent ce que le code fait AUJOURD'HUI, pas ce qu'il devrait faire.
Quand le comportement observe contredit une regle metier, la regle concernee est
citee dans le nom du test et l'ecart est reporte dans RAPPORT-QUALITE.md.
"""

from inventaire import alerte, val


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
