import math

MINUTES_GRATUITES_STANDARD = 30
MINUTES_PAR_TRANCHE = 30
TARIF_PAR_TRANCHE = 1.50
PLAFOND_PAR_JOURNEE = 18.00
MINUTES_PAR_JOURNEE = 24 * 60
PART_PAYEE_PAR_UN_ABONNE = 0.60


def _montant_des_tranches(duree_en_minutes, est_electrique):
    gratuites = 60 if est_electrique else MINUTES_GRATUITES_STANDARD
    minutes_facturables = max(0, duree_en_minutes - gratuites)
    return math.ceil(minutes_facturables / MINUTES_PAR_TRANCHE) * TARIF_PAR_TRANCHE


def _plafond(duree_en_minutes):
    journees = max(1, math.ceil(duree_en_minutes / MINUTES_PAR_JOURNEE))
    return journees * PLAFOND_PAR_JOURNEE


def tarif(duree_en_minutes, est_abonne=False, est_electrique=False):
    montant = min(
        _montant_des_tranches(duree_en_minutes, est_electrique),
        _plafond(duree_en_minutes),
    )
    if est_abonne:
        montant *= PART_PAYEE_PAR_UN_ABONNE
    return round(montant, 2)
