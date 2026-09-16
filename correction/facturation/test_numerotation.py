"""La regle de numerotation se teste sans construire une seule facture."""

from datetime import date

from facturation.numerotation import Numeroteur


def test_le_premier_numero_porte_l_annee_et_le_compteur_sur_quatre_chiffres():
    assert Numeroteur().suivant(date(2019, 3, 5)) == "FA-2019-0001"


def test_les_numeros_se_suivent_sans_rupture():
    numeroteur = Numeroteur()
    numeros = [numeroteur.suivant(date(2019, 3, 5)) for _ in range(3)]
    assert numeros == ["FA-2019-0001", "FA-2019-0002", "FA-2019-0003"]
