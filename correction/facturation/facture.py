"""Emission des factures d'abonnement."""

from datetime import date, datetime

from facturation.abonnements import Abonnement
from facturation.document import Facture
from facturation.numerotation import Numeroteur
from facturation.passerelles import ClientSMTP
from facturation.presentation import corps_de_la_facture, objet_du_courriel
from facturation.tarifs import montant_hors_taxe, montant_toutes_taxes


class EmetteurDeFactures:
    """Calcule, met en forme et envoie les factures."""

    def __init__(self) -> None:
        self.numeroteur = Numeroteur()
        self.passerelle = ClientSMTP()

    def emettre(
        self,
        abonnement: Abonnement,
        adresse: str,
        code_promo: str | None = None,
        premiere_facture: bool = False,
    ) -> Facture:
        emise_le = datetime.now().date()
        facture = Facture(
            numero=self.numeroteur.suivant(emise_le),
            client=abonnement.client,
            emise_le=emise_le,
            montant_ht=montant_hors_taxe(abonnement, code_promo, premiere_facture),
            montant_ttc=montant_toutes_taxes(abonnement, code_promo, premiere_facture),
        )
        self.passerelle.envoyer_courriel(
            adresse, objet_du_courriel(facture), corps_de_la_facture(facture, abonnement)
        )
        return facture
