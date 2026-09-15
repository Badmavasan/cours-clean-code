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


def valeur_brute(a):
    return a["q"] * a["pu"]


def valeur_du_stock(articles):
    return round(sum(valeur_brute(a) for a in articles if a["q"] > 0), 2)


def est_en_alerte(article):
    return article["q"] <= article["seuil"]


def references_en_alerte(articles):
    return [a["ref"] for a in articles if est_en_alerte(a)]


def enregistrer_mouvement(article, quantite, sens, journal):
    ecriture = {
        "id": len(JOURNAL) + 1,
        "ref": article["ref"],
        "q": quantite,
        "t": sens,
    }
    if journal is not None:
        journal.append(ecriture)
    JOURNAL.append(dict(ecriture))


def retirer_du_stock(article, quantite, journal=None, force=False):
    if quantite <= 0:
        return False
    article["q"] = article["q"] - quantite
    if article["q"] < 0 and not force:
        return False
    enregistrer_mouvement(article, quantite, "out", journal)
    return True


def ajouter_au_stock(article, quantite, journal=None):
    if quantite <= 0:
        return False
    article["q"] = article["q"] + quantite
    enregistrer_mouvement(article, quantite, "in", journal)
    return True


def quantite_a_commander(a):
    return a["seuil"] * MULTIPLICATEUR_DE_REAPPROVISIONNEMENT - a["q"]


def cout_de_reapprovisionnement(article):
    if not est_en_alerte(article):
        return 0
    quantite = quantite_a_commander(article)
    montant = quantite * article["pu"]
    if quantite >= QUANTITE_MINIMALE_POUR_REMISE:
        montant -= montant * TAUX_DE_REMISE_GROS_VOLUME
    return round(montant, 2)


def classer_par_valeur(articles):
    return sorted(articles, key=valeur_brute, reverse=True)


def rotation_en_jours(article, ventes_sur_la_periode):
    if ventes_sur_la_periode == 0:
        return 0
    ventes_par_jour = ventes_sur_la_periode / JOURS_DE_LA_PERIODE_DE_VENTE
    return math.floor(article["q"] / ventes_par_jour)


def valeur_par_categorie(articles):
    totaux = {}
    for a in articles:
        categorie = a["cat"] if a["cat"] in CATEGORIES_CONNUES else CATEGORIE_PAR_DEFAUT
        totaux[categorie] = totaux.get(categorie, 0) + valeur_brute(a)
    return {categorie: round(valeur, 2) for categorie, valeur in totaux.items()}


def message_de_rotation(a, ventes_sur_la_periode):
    if ventes_sur_la_periode <= 0:
        return "aucune vente pour " + a["ref"]
    jours = math.floor(a["q"] / (ventes_sur_la_periode / JOURS_DE_LA_PERIODE_DE_VENTE))
    if jours < SEUIL_RUPTURE_IMMINENTE_EN_JOURS:
        return "RUPTURE IMMINENTE " + a["ref"]
    if jours < SEUIL_SURVEILLANCE_EN_JOURS:
        return "a surveiller " + a["ref"]
    return None


def correspond_a_la_categorie(a, cat):
    return cat is None or a["cat"] == cat


def atteint_la_quantite_minimale(a, seuil_min):
    return seuil_min is None or a["q"] >= seuil_min


def est_comptabilisable(a):
    return a["q"] > 0 and a["pu"] > 0


def articles_retenus(arts, cat=None, seuil_min=None):
    return (
        a
        for a in arts
        if correspond_a_la_categorie(a, cat) and atteint_la_quantite_minimale(a, seuil_min)
    )


def message_d_exclusion(a):
    if a["q"] <= 0:
        return "stock vide " + a["ref"]
    if a["pu"] <= 0:
        return "prix invalide " + a["ref"]
    return None


def message_de_rotation_si_connue(a, ventes):
    if ventes is None or a["ref"] not in ventes:
        return None
    return message_de_rotation(a, ventes[a["ref"]])


def messages_pour_un_article(a, ventes=None):
    exclusion = message_d_exclusion(a)
    if exclusion is not None:
        return [exclusion]
    messages = []
    if est_en_alerte(a):
        messages.append("ALERTE " + a["ref"] + " : " + str(a["q"]) + " restants")
    rotation = message_de_rotation_si_connue(a, ventes)
    if rotation is not None:
        messages.append(rotation)
    return messages


def messages_de_diagnostic(arts, ventes=None, cat=None, seuil_min=None):
    messages = []
    for a in articles_retenus(arts, cat, seuil_min):
        messages.extend(messages_pour_un_article(a, ventes))
    return messages


def afficher_diagnostic(arts, ventes=None, cat=None, seuil_min=None):
    for message in messages_de_diagnostic(arts, ventes, cat, seuil_min):
        print(message)


def generer_rapport(articles, categorie=None, quantite_minimale=None, date_du_rapport=None):
    if date_du_rapport is None:
        date_du_rapport = datetime.datetime.now()
    total = 0
    nombre_d_articles = 0
    alertes = []
    for article in articles_retenus(articles, categorie, quantite_minimale):
        if not est_comptabilisable(article):
            continue
        total = total + valeur_brute(article)
        nombre_d_articles = nombre_d_articles + 1
        if est_en_alerte(article):
            alertes.append(article["ref"])
    return {
        "date": str(date_du_rapport),
        "valeur": round(total, 2),
        "nb": nombre_d_articles,
        "alertes": alertes,
        "ttc": round(total * (1 + TAUX_TVA), 2),
    }


def exporter_historique(rapport, chemin="/tmp/inv.json", historique=None):
    entrees = [] if historique is None else historique
    entrees.append(rapport)
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(json.dumps(entrees))
    return entrees
