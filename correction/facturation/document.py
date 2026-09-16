"""La facture en tant que donnee. Aucun comportement, aucune dependance."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Facture:
    numero: str
    client: str
    emise_le: date
    montant_ht: float
    montant_ttc: float
