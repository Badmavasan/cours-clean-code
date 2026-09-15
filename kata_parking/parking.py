import math


def tarif(duree_en_minutes):
    minutes_facturables = max(0, duree_en_minutes - 30)
    return math.ceil(minutes_facturables / 30) * 1.50
