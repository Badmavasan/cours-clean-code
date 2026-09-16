"""La regle de numerotation des factures. Acteur : la comptabilite."""

from datetime import date

PREFIXE_DE_NUMERO = "FA"


class Numeroteur:
    """Attribue des numeros sequentiels de la forme FA-<annee>-<compteur>."""

    def __init__(self) -> None:
        self.compteur = 0

    def suivant(self, emise_le: date) -> str:
        self.compteur += 1
        return f"{PREFIXE_DE_NUMERO}-{emise_le.year}-{self.compteur:04d}"
