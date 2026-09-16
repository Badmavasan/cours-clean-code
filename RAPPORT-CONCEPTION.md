# Rapport de conception

Nom : corrigé de référence
Date : jour 2
Empreinte du commit `depart-tp2` : voir `git rev-parse --short depart-tp2`

---

## 1. Les cinq violations

Une par principe. Le symptôme est un fait vérifiable, la conséquence décrit ce qui
arrive à quelqu'un.

| Principe | Fichier et ligne | Le symptôme observable | La conséquence concrète |
|---|---|---|---|
| **S** | `facturation/facture.py:33` | `emettre` calcule les montants (l. 44 et 45), assemble le corps du courriel (l. 48 à 57), puis déclenche l'envoi (l. 58) | trois acteurs peuvent demander de la modifier ; vérifier un montant oblige à capturer la sortie standard, comme le montrent les trois tests d'émission |
| **O** | `facturation/tarifs.py:21`, `:31` et `:39` | les **trois** fonctions de tarification enchaînent des `if` : sur la formule, sur le palier de volume, sur le code promo | chacune des trois demandes de lundi rouvre une de ces fonctions, couverte par 4, 6 et 4 tests |
| **L** | `facturation/abonnements.py:48` | `AbonnementAnnuel.resilier` lève `ResiliationImpossible` alors que le contrat écrit lignes 19 à 30 promet de renvoyer la date de fin et n'autorise que `ValueError` | tout code qui parcourt une liste d'abonnements pour résilier ceux arrivés à terme plante dès qu'un abonnement annuel s'y trouve |
| **I** | `facturation/passerelles.py:6` | `PasserelleDeCommunication` déclare 6 méthodes abstraites ; `ClientSMTP` en lève `NotImplementedError` sur 2 (l. 40 et 43) ; la facturation n'en appelle qu'une seule | un double de test doit implémenter 6 méthodes pour un besoin d'une ; et l'implémentation ment, ce qui viole aussi L |
| **D** | `facturation/facture.py:7` et `:40` | le module métier importe la classe concrète `ClientSMTP`, et appelle `datetime.now()` au milieu du calcul | impossible d'écrire un test sur le numéro de facture d'une année donnée, ni sur le destinataire sans capturer la sortie standard |

### Trois formes de la même violation

Les trois fonctions violent OCP, mais pas de la même façon, et la forme décide de la
technique d'ouverture.

| Fonction | Ce qui varie | Forme | Comment on l'ouvre |
|---|---|---|---|
| `prix_par_poste` | un catalogue de **valeurs** indépendantes | aiguillage sur une clé | un dictionnaire |
| `appliquer_code_promo` | un catalogue de **comportements** | aiguillage sur une clé, chaque cas a sa logique | un registre de fonctions |
| `taux_de_remise_volume` | une **échelle ordonnée** de seuils | cascade dont l'ordre est la règle | une table triée |

La différence tient en une phrase. Dans les deux premières, les cas sont **indépendants** :
ajouter `decouverte` ne change rien à `pro`. Dans la troisième, les cas forment une
**échelle** : l'ordre des `if` encode la règle « on teste du palier le plus haut vers le
plus bas », et cette règle n'est écrite nulle part.

### Ce que la lecture des imports suffisait à trouver

Trois des cinq se voient sans ouvrir un seul corps de fonction.

**D** se lit dans l'import de `facture.py` ligne 7 : un module métier qui importe un
module nommé `passerelles`, c'est une dépendance qui descend au lieu de monter.

**I** se lit dans la déclaration de `passerelles.py` ligne 6 : six méthodes abstraites
dans une seule interface.

**L** se lit dans la signature de `abonnements.py` ligne 48 : une méthode redéfinie dont
le corps ne fait que lever une exception.

Les deux autres demandent de lire un corps de fonction, mais un seul coup d'oeil suffit :
un enchaînement de `if` pour **O**, une méthode qui fait trois choses pour **S**.

---

## 2. Le coût des trois demandes, avant

Aucune ligne de code écrite pour remplir cette partie. On ouvre, on lit, on compte.

### D1, la formule `decouverte` à 4 euros par poste

| | |
|---|---|
| Fichiers à rouvrir | **2** : `abonnements.py` pour la constante, `tarifs.py` pour le prix |
| Fonctions à modifier | **1** : `prix_par_poste`, plus un bloc de constantes |
| Tests couvrant directement la fonction | **4** : `test_chaque_formule_a_son_prix_par_poste` compte pour 3 cas, plus `test_une_formule_inconnue_est_refusee` |
| Tests rejoués en pratique | **25**, parce que personne ne rejoue un sous-ensemble |

Le détail qui coûte cher : la constante `FORMULE_DECOUVERTE` doit vivre dans
`abonnements.py`, à côté des trois autres, alors que le prix vit dans `tarifs.py`. Une
seule notion métier, deux fichiers à garder en phase. Le jour où quelqu'un ajoute la
constante sans le prix, `prix_par_poste` lève `FormuleInconnue` sur une formule qui
existe pourtant au catalogue.
