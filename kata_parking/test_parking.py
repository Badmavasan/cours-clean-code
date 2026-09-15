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
