from parking import tarif


def test_un_stationnement_de_trente_minutes_est_gratuit():
    assert tarif(30) == 0.00
