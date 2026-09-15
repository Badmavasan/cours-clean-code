# Rapport qualité, module inventaire

Nom : corrigé de référence
Date : jour 1
Empreinte du commit de départ : voir `git log --oneline | tail -1`

---

## 1. Tableau de bord initial

Mesures relevées avant toute modification, sur `inventaire/inventaire.py`.

### Complexité par fonction

```bash
radon cc -s -a inventaire/inventaire.py
```

```
inventaire.py
    F 122:0 rapport - D (22)
    F 94:0 par_cat - B (10)
    F 37:0 mouv - B (9)
    F 74:0 classer - A (5)
    F 19:0 val - A (3)
    F 29:0 alerte - A (3)
    F 62:0 cout - A (3)
    F 87:0 rot - A (2)
    F 175:0 maj_prix - A (1)
    F 185:0 export_json - A (1)

10 blocks (classes, functions, methods) analyzed.
Average complexity: B (5.9)
```

| Fonction | Ligne | Complexité cyclomatique | Rang |
|---|---|---|---|
| `rapport` | 122 | 22 | D |
| `par_cat` | 94 | 10 | B |
| `mouv` | 37 | 9 | B |
| `classer` | 74 | 5 | A |
| `val` | 19 | 3 | A |
| `alerte` | 29 | 3 | A |
| `cout` | 62 | 3 | A |
| `rot` | 87 | 2 | A |
| `maj_prix` | 175 | 1 | A |
| `export_json` | 185 | 1 | A |

`rapport` demande à elle seule **22 tests** pour couvrir toutes ses branches.
Il y en a zéro aujourd'hui.

### Synthèse du fichier

| Mesure | Valeur | Commande |
|---|---|---|
| Lignes de code réelles | 159 | `radon raw inventaire/inventaire.py` |
| Lignes logiques | 161 | `radon raw inventaire/inventaire.py` |
| Complexité maximale | 22, rang D | `radon cc -s inventaire/inventaire.py` |
| Complexité moyenne | 5.9, rang B | `radon cc -a inventaire/inventaire.py` |
| Indice de maintenabilité | A (36.80) | `radon mi -s inventaire/inventaire.py` |
| Score pylint | 7.76 / 10 | `pylint inventaire/inventaire.py` |
| Problèmes ruff | 14 | `ruff check inventaire/inventaire.py` |
| Entrées vulture | 14 | `vulture inventaire/inventaire.py` |
| Couverture de branches | 0 % | `pytest --cov=inventaire --cov-branch` |
| Barrière xenon | échec, code retour 1 | `xenon --max-absolute B --max-modules A --max-average A inventaire/` |

### Les sorties brutes

```bash
radon raw inventaire/inventaire.py
```

```
inventaire.py
    LOC: 190
    LLOC: 161
    SLOC: 159
    Comments: 10
    Blank: 21
    - Comment Stats
        (C % L): 5%
```

```bash
radon mi -s inventaire/inventaire.py
```

```
inventaire.py - A (36.80)
```

```bash
xenon --max-absolute B --max-modules A --max-average A inventaire/ ; echo $?
```

```
ERROR:xenon:block "inventaire.py:122 rapport" has a rank of D
ERROR:xenon:average complexity is ranked B
ERROR:xenon:module 'inventaire.py' has a rank of B
1
```

```bash
pylint inventaire/inventaire.py
```

```
inventaire.py:37:0: W0102: Dangerous default value [] as argument
inventaire.py:37:0: R0913: Too many arguments (6/5)
inventaire.py:38:4: W0603: Using the global statement
inventaire.py:46:15: C0121: Comparison 'force == False' should be 'not force'
inventaire.py:78:8: W0612: Unused variable 'i'
inventaire.py:90:4: W0702: No exception type(s) specified (bare-except)
inventaire.py:94:0: R0912: Too many branches (13/12)
inventaire.py:122:0: R0913: Too many arguments (7/5)
inventaire.py:122:0: R0912: Too many branches (21/12)
inventaire.py:130:4: R1702: Too many nested blocks (8/5)
inventaire.py:169:12: W1514: Using open without explicitly specifying an encoding
inventaire.py:175:13: W0613: Unused argument 'ref'
inventaire.py:185:0: W0102: Dangerous default value [] as argument

Your code has been rated at 7.76/10
```

```bash
ruff check inventaire/inventaire.py
```

```
inventaire.py:37:27: B006 Do not use mutable data structures for argument defaults
inventaire.py:45:9: SIM102 Use a single `if` statement instead of nested `if` statements
inventaire.py:77:9: PERF402 Use `list` or `list.copy` to create a copy of a list
inventaire.py:90:5: E722 Do not use bare `except`
inventaire.py:124:13: DTZ005 `datetime.datetime.now()` called without a `tz` argument
inventaire.py:169:13: SIM115 Use a context manager for opening files
inventaire.py:185:51: B006 Do not use mutable data structures for argument defaults
Found 14 errors.
```

```bash
vulture inventaire/inventaire.py
```

```
inventaire.py:15: unused variable 'STOCK' (60% confidence)
inventaire.py:78: unused variable 'i' (60% confidence)
inventaire.py:175: unused function 'maj_prix' (60% confidence)
inventaire.py:175: unused variable 'p' (100% confidence)
inventaire.py:175: unused variable 'ref' (100% confidence)
```

Les entrées à 60 % qui désignent les fonctions publiques du module ne sont pas
des faux positifs de l'outil, ce sont des fonctions appelées depuis l'extérieur.
Seules `maj_prix`, `STOCK`, `i`, `ref` et `p` sont réellement mortes.

---

## 2. Catalogue des odeurs

Quatorze entrées. La colonne « détecté par » dit quel outil l'a vue. Les lignes
marquées **aucun** sont celles qu'aucun outil ne signale, et ce sont les plus chères.

| # | Ligne | Odeur ou défaut | Détecté par | Conséquence concrète |
|---|---|---|---|---|
| 1 | 4 | commentaire « NE PAS TOUCHER A mouv() SANS PREVENIR » | **aucun** | la peur est documentée au lieu d'être traitée, personne n'ose entrer dans la fonction |
| 2 | 10 à 13 | constantes `TVA`, `S`, `R`, `Q` | **aucun** | `S` et `Q` ne se cherchent pas dans le projet, il faut lire le corps pour savoir ce qu'ils valent |
| 3 | 14 à 16 | état global mutable `JOURNAL`, `STOCK`, `DERNIER` | vulture, partiellement | deux appels successifs ne donnent pas le même résultat, les tests devront s'exécuter dans un ordre précis |
| 4 | 25 | branche morte `else: t = t + 0` | **aucun** | cache une décision métier jamais écrite nulle part sur les quantités négatives |
| 5 | 30 | variable nommée `l` | ruff E741 en mode étendu | se confond avec le chiffre 1 à la lecture |
| 6 | 37 | `mouv(a, q, t="out", j=[], force=False, log=True)` | pylint R0913, W0102 | six paramètres dont trois drapeaux, et un argument par défaut mutable partagé entre tous les appels |
| 7 | 37 | l'argument `t` choisit entre entrée et sortie de stock | **aucun** | ce sont deux fonctions différentes déguisées en une seule, aucun appelant ne lit `mouv(a, 5)` correctement |
| 8 | 44 | la fonction modifie son argument avant de valider | **aucun** | le sujet demande qu'un refus laisse le stock intact, la structure du code rend cette garantie impossible à tenir |
| 9 | 74 à 84 | tri à bulles réimplémenté à la main | **aucun** | `sorted` existe, fait le même travail en une ligne et ne se trompe pas sur les indices |
| 10 | 90 | `except:` nu | pylint W0702, ruff E722 | attrape aussi le Ctrl+C et les fautes de frappe, le bug devient invisible |
| 11 | 91 | renvoie `0` pour dire « je ne sais pas calculer » | **aucun** | zéro jour de stock et absence de données deviennent indistinguables pour l'appelant |
| 12 | 94 à 119 | quatre blocs identiques, catégories écrites en dur | pylint R0912 | ajouter une catégorie oblige à copier un cinquième bloc, et à ne pas en oublier un |
| 13 | 122 | `rapport` calcule, affiche et écrit un fichier | pylint R0913, R0912, R1702 | trois acteurs différents peuvent demander de la modifier, et elle demande 22 tests |
| 14 | 175 à 182 | `maj_prix` morte, avec son ancien corps en commentaire | vulture 60 %, W0613 | lue par chaque nouvel arrivant, maintenue par erreur, et prête à se réveiller |

Sept de ces quatorze entrées ne sont vues par aucun outil.

---

## 3. Faut-il tout réécrire

Non, et les chiffres le disent.

Le problème n'est pas réparti sur les 159 lignes du module. Il est concentré :
**une seule fonction sur dix** est au rang D, et deux autres au rang B. Les sept
autres sont déjà au rang A. Réécrire l'ensemble reviendrait à jeter sept fonctions
correctes, testées par sept ans de production, pour régler un problème qui tient
dans trente lignes.

C'est exactement ce qu'a fait Netscape en 1998. Le moteur de rendu était jugé
irrécupérable, la réécriture a pris trois ans, et pendant ces trois ans Internet
Explorer est passé de 20 % à plus de 80 % du marché. Ce qui manquait à Netscape,
ce n'était pas du courage, c'était un moyen de vérifier qu'une modification ne
cassait rien.

C'est ce qui manque ici aussi : la couverture est de **0 %**. Tant qu'elle reste
à zéro, toute intervention est un pari, y compris une réécriture.

**Ordre d'intervention proposé.**

D'abord écrire des tests sur `val`, `alerte`, `cout`, `classer` et `rot`. Ce sont
les fonctions les plus simples, elles se testent en une heure, et elles portent
les règles métier que la direction lit tous les 5 du mois.

Ensuite seulement attaquer `rapport`, parce que c'est la seule fonction que
personne ne peut modifier aujourd'hui sans risque, et qu'il faut un filet avant
d'y entrer.

Supprimer `maj_prix` et l'état global en dernier : c'est peu risqué, mais ça ne
débloque rien tant que le reste n'est pas couvert.

Budget estimé : une journée. À comparer aux trois semaines d'une réécriture qui
recommencerait par redécouvrir les règles métier qui ne sont écrites nulle part
ailleurs que dans ce fichier.

---

## 4. Écarts constatés entre le code et les règles métier

Relevés pendant la mission 3, en écrivant le filet. **Aucun n'est corrigé ici.**
Chacun est figé par un test dont le nom cite la règle violée, et sera traité en
mission 5 par un test rouge puis une correction.

| Règle | Ligne | Ce que le code fait | Ce que la règle dit |
|---|---|---|---|
| M2 | 32 | `a["q"] < a["seuil"]`, un article pile au seuil n'est pas signalé | au seuil, l'article est en alerte |
| M2 | 63 | `cout` utilise la même comparaison, donc ne commande rien pour un article au seuil | un article au seuil doit être réapprovisionné |
| M2 | 141 | le rapport mensuel reproduit le même écart dans sa liste d'alertes | idem |
| M3 | 44 | le stock est décrémenté **avant** la vérification, et reste négatif après un refus | un retrait refusé laisse le stock inchangé |
| M5 | 65 | `n > Q`, la remise commence à 101 unités | remise à partir de 100 unités incluses |
| M7 | 90 | un `except` nu renvoie `0` quand il n'y a aucune vente | une erreur explicite doit être levée |

### Ce que le filet ne protège pas

Trois comportements actuels ne sont **pas** couverts par le filet, et c'est un choix
assumé plutôt qu'un oubli.

**Les `print`.** Le module affiche des lignes de diagnostic pendant le calcul. La
mission 3 impose de les sortir du code de calcul. Aucun test ne les fige, sinon le
refactoring imposé deviendrait impossible. Les chaînes sont reprises telles quelles
dans les fonctions extraites, et couvertes par un test à ce moment-là.

**L'argument par défaut mutable de `mouv` et de `export_json`.** C'est un défaut
technique, pas un écart métier : aucune règle de M1 à M8 ne décrit ce que doit
contenir un journal par défaut. On le supprime en mission 3 sans passer par la
case mission 5.

**L'attrape-tout de `rot`.** Il absorbait aussi des erreurs que personne n'a jamais
rencontrées, une clé absente par exemple. Le filet ne documente que le cas d'une
période sans vente. Le refactoring ne conserve donc que celui-là, et c'est
exactement la limite d'un filet de caractérisation : il protège ce qu'il couvre,
rien de plus.
