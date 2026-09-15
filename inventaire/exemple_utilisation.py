"""Voici comment l equipe logistique appelle le module aujourd hui."""

from inventaire import (
    afficher_diagnostic,
    classer_par_valeur,
    cout_de_reapprovisionnement,
    generer_rapport,
    references_en_alerte,
    valeur_du_stock,
    valeur_par_categorie,
)

ARTICLES = [
    {"ref": "VIS-M6", "lib": "Vis M6 acier", "q": 2, "pu": 0.15, "seuil": 20, "cat": "piece"},
    {"ref": "PERC-18", "lib": "Perceuse 18V", "q": 12, "pu": 89.90, "seuil": 3, "cat": "outil"},
    {"ref": "GANT-L", "lib": "Gants L", "q": 5, "pu": 4.20, "seuil": 5, "cat": "consommable"},
    {"ref": "HUILE-5", "lib": "Huile 5L", "q": 40, "pu": 12.50, "seuil": 10, "cat": "consommable"},
    {"ref": "CAB-3G", "lib": "Cable 3G2.5", "q": 0, "pu": 1.80, "seuil": 50, "cat": "autre"},
]

VENTES_30_JOURS = {"VIS-M6": 300, "PERC-18": 4, "GANT-L": 60, "HUILE-5": 15, "CAB-3G": 0}

if __name__ == "__main__":
    print("valeur du stock :", valeur_du_stock(ARTICLES))
    print("articles en alerte :", references_en_alerte(ARTICLES))
    print("cout de reappro des gants :", cout_de_reapprovisionnement(ARTICLES[2]))
    print("valeur par categorie :", valeur_par_categorie(ARTICLES))
    print("classement :", [a["ref"] for a in classer_par_valeur(ARTICLES)])
    print("---")
    afficher_diagnostic(ARTICLES, VENTES_30_JOURS)
    print(generer_rapport(ARTICLES))
