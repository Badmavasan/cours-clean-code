import math

MINUTES_GRATUITES_STANDARD = 30
MINUTES_PAR_TRANCHE = 30
TARIF_PAR_TRANCHE = 1.50


def tarif(duree_en_minutes):
    minutes_facturables = max(0, duree_en_minutes - MINUTES_GRATUITES_STANDARD)
    return math.ceil(minutes_facturables / MINUTES_PAR_TRANCHE) * TARIF_PAR_TRANCHE
