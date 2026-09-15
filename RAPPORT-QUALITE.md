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
