import math

MINUTES_GRATUITES_STANDARD = 30
MINUTES_PAR_TRANCHE = 30
TARIF_PAR_TRANCHE = 1.50
PLAFOND_PAR_JOURNEE = 18.00
MINUTES_PAR_JOURNEE = 24 * 60


def _montant_des_tranches(duree_en_minutes):
    minutes_facturables = max(0, duree_en_minutes - MINUTES_GRATUITES_STANDARD)
    return math.ceil(minutes_facturables / MINUTES_PAR_TRANCHE) * TARIF_PAR_TRANCHE


def _plafond(duree_en_minutes):
    journees = max(1, math.ceil(duree_en_minutes / MINUTES_PAR_JOURNEE))
    return journees * PLAFOND_PAR_JOURNEE


def tarif(duree_en_minutes, est_abonne=False):
    montant = min(_montant_des_tranches(duree_en_minutes), _plafond(duree_en_minutes))
    if est_abonne:
        montant *= 0.60
    return round(montant, 2)
