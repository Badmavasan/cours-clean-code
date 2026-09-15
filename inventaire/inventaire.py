"""Gestion du stock de l entrepot nord."""

import datetime
import json
import math

TAUX_TVA = 0.2
MULTIPLICATEUR_DE_REAPPROVISIONNEMENT = 3
TAUX_DE_REMISE_GROS_VOLUME = 0.1
QUANTITE_MINIMALE_POUR_REMISE = 100
JOURS_DE_LA_PERIODE_DE_VENTE = 30
SEUIL_RUPTURE_IMMINENTE_EN_JOURS = 7
SEUIL_SURVEILLANCE_EN_JOURS = 30
CATEGORIES_CONNUES = ("outil", "consommable", "piece")
CATEGORIE_PAR_DEFAUT = "autre"
JOURNAL = []
DERNIER = 0


def valeur_brute(a):
    return a["q"] * a["pu"]


def val(arts):
    return round(sum(valeur_brute(a) for a in arts if a["q"] > 0), 2)


def alerte(arts):
    return [a["ref"] for a in arts if a["q"] < a["seuil"]]


def mouv(a, q, t="out", j=None, force=False):
    global DERNIER
    if q <= 0:
        return False
    if t == "out":
        a["q"] = a["q"] - q
        if a["q"] < 0 and not force:
            return False
    elif t == "in":
        a["q"] = a["q"] + q
    else:
        return False
    DERNIER = DERNIER + 1
    ecriture = {"id": DERNIER, "ref": a["ref"], "q": q, "t": t}
    if j is not None:
        j.append(ecriture)
    JOURNAL.append(dict(ecriture))
    return True


def quantite_a_commander(a):
    return a["seuil"] * MULTIPLICATEUR_DE_REAPPROVISIONNEMENT - a["q"]


def cout(a):
    if a["q"] >= a["seuil"]:
        return 0
    quantite = quantite_a_commander(a)
    montant = quantite * a["pu"]
    if quantite > QUANTITE_MINIMALE_POUR_REMISE:
        montant -= montant * TAUX_DE_REMISE_GROS_VOLUME
    return round(montant, 2)


def classer(arts):
    return sorted(arts, key=valeur_brute, reverse=True)


def rot(a, v):
    if v == 0:
        return 0
    return math.floor(a["q"] / (v / JOURS_DE_LA_PERIODE_DE_VENTE))


def par_cat(arts):
    totaux = {}
    for a in arts:
        categorie = a["cat"] if a["cat"] in CATEGORIES_CONNUES else CATEGORIE_PAR_DEFAUT
        totaux[categorie] = totaux.get(categorie, 0) + valeur_brute(a)
    return {categorie: round(valeur, 2) for categorie, valeur in totaux.items()}


def rapport(arts, ventes=None, cat=None, seuil_min=None, export=False, verbose=True, d=None):
    if d is None:
        d = datetime.datetime.now()
    res = {}
    res["date"] = str(d)
    tot = 0
    nb = 0
    liste_alerte = []
    for a in arts:
        if cat is not None:
            if a["cat"] != cat:
                continue
        if seuil_min is not None:
            if a["q"] < seuil_min:
                continue
        if a["q"] > 0:
            if a["pu"] > 0:
                tot = tot + a["q"] * a["pu"]
                nb = nb + 1
                if a["q"] < a["seuil"]:
                    liste_alerte.append(a["ref"])
                    if verbose:
                        print("ALERTE " + a["ref"] + " : " + str(a["q"]) + " restants")
                if ventes is not None:
                    if a["ref"] in ventes:
                        if ventes[a["ref"]] > 0:
                            j = math.floor(a["q"] / (ventes[a["ref"]] / JOURS_DE_LA_PERIODE_DE_VENTE))
                            if j < SEUIL_RUPTURE_IMMINENTE_EN_JOURS:
                                if verbose:
                                    print("RUPTURE IMMINENTE " + a["ref"])
                            elif j < SEUIL_SURVEILLANCE_EN_JOURS:
                                if verbose:
                                    print("a surveiller " + a["ref"])
                        else:
                            if verbose:
                                print("aucune vente pour " + a["ref"])
            else:
                if verbose:
                    print("prix invalide " + a["ref"])
        else:
            if verbose:
                print("stock vide " + a["ref"])
    res["valeur"] = round(tot, 2)
    res["nb"] = nb
    res["alertes"] = liste_alerte
    res["ttc"] = round(tot * (1 + TAUX_TVA), 2)
    if export:
        f = open("/tmp/rapport.json", "w")
        f.write(json.dumps(res))
        f.close()
    return res


def export_json(res, chemin="/tmp/inv.json", hist=[]):
    hist.append(res)
    f = open(chemin, "w")
    f.write(json.dumps(hist))
    f.close()
    return hist
