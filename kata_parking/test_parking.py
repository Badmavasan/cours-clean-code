from datetime import datetime

import pytest
from parking import DureeInvalide, tarif, tarif_en_cours


def test_un_stationnement_de_trente_minutes_est_gratuit():
    assert tarif(30) == 0.00


@pytest.mark.parametrize("minutes", [0, 1, 15, 29, 30])
def test_toute_duree_jusqu_a_trente_minutes_est_gratuite(minutes):
    assert tarif(minutes) == 0.00


def test_la_trente_et_unieme_minute_coute_un_euro_cinquante():
    assert tarif(31) == 1.50


def test_la_soixante_et_unieme_minute_coute_trois_euros():
    assert tarif(61) == 3.00


@pytest.mark.parametrize("minutes, attendu", [(60, 1.50), (90, 3.00), (120, 4.50)])
def test_chaque_demi_heure_commencee_ajoute_un_euro_cinquante(minutes, attendu):
    assert tarif(minutes) == attendu


def test_au_dela_de_six_heures_trente_le_montant_est_plafonne():
    assert tarif(8 * 60) == 18.00


def test_le_plafond_est_atteint_a_exactement_six_heures_trente():
    assert tarif(390) == 18.00


def test_la_vingt_cinquieme_heure_ouvre_une_deuxieme_journee():
    assert tarif(25 * 60) == 36.00


def test_une_journee_commencee_compte_pour_une_journee_entiere():
    assert tarif(24 * 60 + 1) == 36.00


def test_un_abonne_paie_soixante_pour_cent_du_montant():
    assert tarif(31, est_abonne=True) == 0.90


def test_la_remise_abonne_s_applique_aussi_sur_le_plafond():
    assert tarif(8 * 60, est_abonne=True) == 10.80


def test_un_vehicule_electrique_est_gratuit_jusqu_a_une_heure():
    assert tarif(60, est_electrique=True) == 0.00


def test_la_soixante_et_unieme_minute_est_payante_pour_un_electrique():
    assert tarif(61, est_electrique=True) == 1.50


def test_l_avantage_electrique_se_cumule_avec_l_abonnement():
    assert tarif(61, est_abonne=True, est_electrique=True) == 0.90


def test_une_duree_negative_est_refusee():
    with pytest.raises(DureeInvalide, match="negative"):
        tarif(-1)


def test_une_minute_de_plus_que_soixante_douze_heures_declenche_la_fourriere():
    assert tarif(72 * 60 + 1) == 250.00


def test_soixante_douze_heures_pile_restent_au_tarif_normal():
    assert tarif(72 * 60) == 54.00


def test_la_fourriere_ignore_l_abonnement_et_l_electrique():
    assert tarif(100 * 60, est_abonne=True, est_electrique=True) == 250.00


def test_le_montant_du_a_l_instant_present_se_calcule_sur_une_heure_fournie():
    entree = datetime(2026, 9, 15, 8, 0)
    maintenant = datetime(2026, 9, 15, 10, 0)
    assert tarif_en_cours(entree, maintenant) == 4.50


def test_une_sortie_anterieure_a_l_entree_est_refusee():
    entree = datetime(2026, 9, 15, 10, 0)
    with pytest.raises(DureeInvalide, match="anterieure"):
        tarif_en_cours(entree, datetime(2026, 9, 15, 9, 0))


def test_le_montant_en_cours_ne_depend_pas_de_la_date_reelle():
    en_2026 = tarif_en_cours(datetime(2026, 1, 1, 0, 0), datetime(2026, 1, 1, 2, 0))
    en_2036 = tarif_en_cours(datetime(2036, 6, 30, 0, 0), datetime(2036, 6, 30, 2, 0))
    assert en_2026 == en_2036 == 4.50
