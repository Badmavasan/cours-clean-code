import pytest
from parking import tarif


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
