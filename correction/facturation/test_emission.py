"""Ce que la separation rend possible : relancer un envoi sans consommer de numero."""

from datetime import date

import pytest

from facturation.abonnements import Abonnement
from facturation.facture import EmetteurDeFactures
from facturation.presentation import corps_de_la_facture

ABONNEMENT = Abonnement("Dupont SARL", "pro", 3, date(2019, 1, 1))


class PasserelleEnPanne:
    def envoyer_courriel(self, *_):
        raise ConnectionError("serveur mail injoignable")


def test_etablir_calcule_la_facture_sans_rien_envoyer(capsys):
    facture = EmetteurDeFactures().etablir(ABONNEMENT, date(2019, 3, 5))
    assert facture.numero == "FA-2019-0001"
    assert facture.montant_ht == 57.0
    assert capsys.readouterr().out == ""


def test_produire_le_texte_ne_fait_pas_avancer_le_compteur():
    emetteur = EmetteurDeFactures()
    facture = emetteur.etablir(ABONNEMENT, date(2019, 3, 5))
    corps_de_la_facture(facture, ABONNEMENT)
    corps_de_la_facture(facture, ABONNEMENT)
    assert emetteur.etablir(ABONNEMENT, date(2019, 3, 5)).numero == "FA-2019-0002"


def test_un_envoi_en_echec_se_relance_avec_la_meme_facture(capsys):
    emetteur = EmetteurDeFactures()
    facture = emetteur.etablir(ABONNEMENT, date(2019, 3, 5))
    passerelle_d_origine = emetteur.passerelle
    emetteur.passerelle = PasserelleEnPanne()
    with pytest.raises(ConnectionError):
        emetteur.envoyer(facture, ABONNEMENT, "compta@dupont.fr")
    emetteur.passerelle = passerelle_d_origine
    emetteur.envoyer(facture, ABONNEMENT, "compta@dupont.fr")
    assert "FA-2019-0001" in capsys.readouterr().out
    assert emetteur.etablir(ABONNEMENT, date(2019, 3, 5)).numero == "FA-2019-0002"
