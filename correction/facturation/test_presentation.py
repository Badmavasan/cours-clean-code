"""La presentation se teste sans numeroter ni envoyer."""

from datetime import date

from facturation.abonnements import Abonnement
from facturation.document import Facture
from facturation.presentation import corps_de_la_facture, objet_du_courriel

FACTURE = Facture("FA-2019-0042", "Dupont SARL", date(2019, 3, 5), 57.0, 68.4)
ABONNEMENT = Abonnement("Dupont SARL", "pro", 3, date(2019, 1, 1))


def test_l_objet_porte_le_numero_de_la_facture():
    assert objet_du_courriel(FACTURE) == "Votre facture FA-2019-0042"


def test_le_corps_affiche_les_deux_montants_avec_deux_decimales():
    corps = corps_de_la_facture(FACTURE, ABONNEMENT)
    assert "Montant HT    : 57.00" in corps
    assert "Montant TTC   : 68.40" in corps


def test_le_corps_rappelle_la_formule_et_le_nombre_de_postes():
    assert "Formule       : pro, 3 postes" in corps_de_la_facture(FACTURE, ABONNEMENT)
