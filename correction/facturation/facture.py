"""Emission des factures d'abonnement."""

from datetime import date, datetime

from facturation.abonnements import Abonnement
from facturation.document import Facture
from facturation.numerotation import Numeroteur
from facturation.passerelles import ClientSMTP
from facturation.presentation import corps_de_la_facture, objet_du_courriel
from facturation.tarifs import montant_hors_taxe, montant_toutes_taxes


class EmetteurDeFactures:
    """Orchestre l'emission : etablir la facture, puis l'envoyer."""

    def __init__(self) -> None:
        self.numeroteur = Numeroteur()
        self.passerelle = ClientSMTP()

    def etablir(
        self,
        abonnement: Abonnement,
        emise_le: date,
        code_promo: str | None = None,
        premiere_facture: bool = False,
    ) -> Facture:
        return Facture(
            numero=self.numeroteur.suivant(emise_le),
            client=abonnement.client,
            emise_le=emise_le,
            montant_ht=montant_hors_taxe(abonnement, code_promo, premiere_facture),
            montant_ttc=montant_toutes_taxes(abonnement, code_promo, premiere_facture),
        )

    def envoyer(self, facture: Facture, abonnement: Abonnement, adresse: str) -> None:
        self.passerelle.envoyer_courriel(
            adresse, objet_du_courriel(facture), corps_de_la_facture(facture, abonnement)
        )

    def emettre(
        self,
        abonnement: Abonnement,
        adresse: str,
        code_promo: str | None = None,
        premiere_facture: bool = False,
    ) -> Facture:
        facture = self.etablir(abonnement, datetime.now().date(), code_promo, premiere_facture)
        self.envoyer(facture, abonnement, adresse)
        return facture
