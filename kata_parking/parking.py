import math

MINUTES_GRATUITES_STANDARD = 30
MINUTES_GRATUITES_VEHICULE_ELECTRIQUE = 60
MINUTES_PAR_TRANCHE = 30
TARIF_PAR_TRANCHE = 1.50
PLAFOND_PAR_JOURNEE = 18.00
MINUTES_PAR_JOURNEE = 24 * 60
PART_PAYEE_PAR_UN_ABONNE = 0.60
DUREE_MAXIMALE_AVANT_FOURRIERE = 72 * 60
FORFAIT_DE_FOURRIERE = 250.00


class DureeInvalide(ValueError):
    """La duree de stationnement demandee n'a pas de sens."""


def _minutes_gratuites(est_electrique):
    if est_electrique:
        return MINUTES_GRATUITES_VEHICULE_ELECTRIQUE
    return MINUTES_GRATUITES_STANDARD


def _montant_des_tranches(duree_en_minutes, est_electrique):
    minutes_facturables = max(
        0, duree_en_minutes - _minutes_gratuites(est_electrique)
    )
    return math.ceil(minutes_facturables / MINUTES_PAR_TRANCHE) * TARIF_PAR_TRANCHE


def _plafond(duree_en_minutes):
    journees = max(1, math.ceil(duree_en_minutes / MINUTES_PAR_JOURNEE))
    return journees * PLAFOND_PAR_JOURNEE


def tarif(duree_en_minutes, est_abonne=False, est_electrique=False):
    if duree_en_minutes < 0:
        raise DureeInvalide(f"duree negative : {duree_en_minutes} minutes")
    if duree_en_minutes > DUREE_MAXIMALE_AVANT_FOURRIERE:
        return FORFAIT_DE_FOURRIERE
    montant = min(
        _montant_des_tranches(duree_en_minutes, est_electrique),
        _plafond(duree_en_minutes),
    )
    if est_abonne:
        montant *= PART_PAYEE_PAR_UN_ABONNE
    return round(montant, 2)


def tarif_en_cours(entree, maintenant, est_abonne=False, est_electrique=False):
    minutes = int((maintenant - entree).total_seconds() // 60)
    return tarif(minutes, est_abonne, est_electrique)
