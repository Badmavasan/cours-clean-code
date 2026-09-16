"""La presentation d'une facture. Acteur : la communication."""

from facturation.abonnements import Abonnement
from facturation.document import Facture


def objet_du_courriel(facture: Facture) -> str:
    return f"Votre facture {facture.numero}"


def corps_de_la_facture(facture: Facture, abonnement: Abonnement) -> str:
    return "\n".join(
        [
            f"Facture {facture.numero}",
            f"Client        : {facture.client}",
            f"Emise le      : {facture.emise_le.isoformat()}",
            f"Formule       : {abonnement.formule}, {abonnement.nombre_de_postes} postes",
            f"Montant HT    : {facture.montant_ht:.2f}",
            f"Montant TTC   : {facture.montant_ttc:.2f}",
        ]
    )
