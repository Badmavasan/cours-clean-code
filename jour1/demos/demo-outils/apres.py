"""Calcul du montant total d'une commande, taxes, remises et livraison incluses."""

from dataclasses import dataclass
from decimal import Decimal

TAUX_TVA_NORMAL = Decimal("0.200")
TAUX_TVA_REDUIT = Decimal("0.055")
TAUX_TVA_SUPER_REDUIT = Decimal("0.021")

TAUX_TVA_PAR_CATEGORIE = {
    "alimentaire": TAUX_TVA_REDUIT,
    "livre": TAUX_TVA_REDUIT,
    "presse": TAUX_TVA_SUPER_REDUIT,
    "medicament_rembourse": TAUX_TVA_SUPER_REDUIT,
}

QUANTITE_MINIMALE_REMISE_VOLUME = 10
REMISE_FIDELITE_PROFESSIONNEL = Decimal("0.05")
REMISE_VOLUME_PARTICULIER = Decimal("0.10")
REMISE_VOLUME_PROFESSIONNEL = Decimal("0.15")

SEUIL_FRANCO_DE_PORT = Decimal(50)
FRAIS_DE_PORT_STANDARD = Decimal("4.90")
SUPPLEMENT_LIVRAISON_EXPRESS = Decimal("9.90")

SEUIL_RISTOURNE_PROFESSIONNELLE = Decimal(1000)
TAUX_RISTOURNE_PROFESSIONNELLE = Decimal("0.02")


@dataclass(frozen=True)
class LigneCommande:
    """Un article et sa quantite dans une commande."""

    reference: str
    categorie: str
    prix_unitaire_hors_taxe: Decimal
    quantite: int


def taux_tva_applicable(categorie: str) -> Decimal:
    """Renvoie le taux de TVA de la categorie, le taux normal par defaut."""
    return TAUX_TVA_PAR_CATEGORIE.get(categorie, TAUX_TVA_NORMAL)


def taux_remise_ligne(quantite: int, est_professionnel: bool) -> Decimal:
    """Renvoie le taux de remise applicable a une ligne selon sa quantite."""
    if quantite >= QUANTITE_MINIMALE_REMISE_VOLUME:
        if est_professionnel:
            return REMISE_VOLUME_PROFESSIONNEL
        return REMISE_VOLUME_PARTICULIER
    if est_professionnel:
        return REMISE_FIDELITE_PROFESSIONNEL
    return Decimal(0)


def montant_ligne(ligne: LigneCommande, est_professionnel: bool) -> Decimal:
    """Calcule le montant taxes et remise comprises d'une seule ligne."""
    montant_hors_taxe = ligne.prix_unitaire_hors_taxe * ligne.quantite
    montant_taxe = montant_hors_taxe * (1 + taux_tva_applicable(ligne.categorie))
    return montant_taxe * (1 - taux_remise_ligne(ligne.quantite, est_professionnel))


def frais_de_livraison(montant_articles: Decimal, est_express: bool) -> Decimal:
    """Calcule les frais de port, gratuits au dela du seuil de franco de port."""
    if montant_articles < SEUIL_FRANCO_DE_PORT:
        return FRAIS_DE_PORT_STANDARD
    if est_express:
        return SUPPLEMENT_LIVRAISON_EXPRESS
    return Decimal(0)


def ristourne_professionnelle(montant: Decimal, est_professionnel: bool) -> Decimal:
    """Calcule la ristourne accordee aux professionnels sur les grosses commandes."""
    if est_professionnel and montant > SEUIL_RISTOURNE_PROFESSIONNELLE:
        return montant * TAUX_RISTOURNE_PROFESSIONNELLE
    return Decimal(0)


def total_commande(
    lignes: list[LigneCommande],
    est_professionnel: bool = False,
    est_livree: bool = True,
    est_express: bool = False,
) -> Decimal:
    """Calcule le montant total a payer pour une commande."""
    montant_articles = sum(
        (montant_ligne(ligne, est_professionnel) for ligne in lignes),
        start=Decimal(0),
    )
    montant = montant_articles - ristourne_professionnelle(
        montant_articles, est_professionnel
    )
    if est_livree:
        montant += frais_de_livraison(montant_articles, est_express)
    return montant.quantize(Decimal("0.01"))
