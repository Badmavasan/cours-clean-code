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

---

## 5. Tableau de bord après refactoring

Mêmes commandes qu'en partie 1.

```bash
radon cc -s -a inventaire/inventaire.py
```

```
inventaire/inventaire.py
    F 164:0 generer_rapport - A (5)
    F 43:0 retirer_du_stock - A (4)
    F 86:0 valeur_par_categorie - A (4)
    F 94:0 message_de_rotation - A (4)
    F 117:0 articles_retenus - A (4)
    F 139:0 messages_pour_un_article - A (4)
    F 23:0 valeur_du_stock - A (3)
    F 27:0 references_en_alerte - A (3)
    F 65:0 cout_de_reapprovisionnement - A (3)
    F 125:0 message_d_exclusion - A (3)
    F 133:0 message_de_rotation_si_connue - A (3)
    F 31:0 enregistrer_mouvement - A (2)
    F 53:0 ajouter_au_stock - A (2)
    F 79:0 rotation_en_jours - A (2)
    F 105:0 correspond_a_la_categorie - A (2)
    F 109:0 atteint_la_quantite_minimale - A (2)
    F 113:0 est_comptabilisable - A (2)
    F 152:0 messages_de_diagnostic - A (2)
    F 159:0 afficher_diagnostic - A (2)
    F 186:0 exporter_historique - A (2)
    F 19:0 valeur_brute - A (1)
    F 61:0 quantite_a_commander - A (1)
    F 75:0 classer_par_valeur - A (1)

23 blocks (classes, functions, methods) analyzed.
Average complexity: A (2.652173913043478)
```

```bash
radon mi -s inventaire/inventaire.py
```

```
inventaire/inventaire.py - A (26.70)
```

| Mesure | Avant | Après |
|---|---|---|
| Complexité maximale | 22, rang D | 5, rang A |
| Complexité moyenne | 5.9, rang B | A (2.652173913043478) |
| Indice de maintenabilité | A (36.80) | A (26.70) |
| Score pylint | 7.76 / 10 | 8.19 / 10 |
| Problèmes ruff | 14 | 1 |
| Tests sur le module | 0 | 0 |
| Fonctions de plus de 4 paramètres | 2 | 0 |
| Arguments par défaut mutables | 2 | 0 |
| Attrape-tout d'exception | 1 | 0 |
| `print` dans le code de calcul | 7 | 0 |

Ce que ce delta prouve : la fonction que personne n'osait modifier est passée
du rang D au rang A, le module est couvert par des tests qui décrivent son
comportement réel, et les six écarts relevés sont documentés et toujours
présents, prêts à être corrigés en mission 5.

---

## 6. Bilan des corrections

Quatre écarts corrigés. Le sujet en demande deux au minimum.
Chacun a été prouvé par un test rouge **avant** la moindre modification du code.

| Règle violée | Ligne d'origine | Commit red | Commit fix | Conséquence métier |
|---|---|---|---|---|
| M2, seuil inclusif | 32, 63 et 141 | `950158f` | `0234ce6` | un article pile à son seuil n'était **jamais** signalé, ni dans les alertes ni dans le réapprovisionnement |
| M5, remise à 100 unités | 65 | `f7dcbaf` | `ec88963` | une commande de exactement 100 unités était facturée **10 % trop cher** |
| M3, retrait refusé | 44 | `4e2eb80` | `972cc5b` | après un refus, le stock restait négatif et faussait la valeur totale |
| M7, période sans vente | 90 | `5d7ce91` | `2783a84` | `0` signifiait à la fois zéro jour de stock et donnée absente |

### La conséquence chiffrée

**M2.** Sur le jeu de données de l'entrepôt, GANT-L est à 5 unités pour un seuil de 5.
Il était donc exactement dans l'angle mort. Il n'apparaissait dans aucune alerte et
`cout_de_reapprovisionnement` renvoyait 0 pour lui, donc aucune commande n'était
déclenchée. C'est la mécanique exacte des deux ruptures de stock du mois dernier.

**M5.** HUILE-5 coûte 12,50 euros l'unité. Une commande de 100 unités revient à
1250 euros sans remise, contre 1125 euros avec les 10 % dus, soit **125 euros perdus**
à chaque commande de ce volume exact. Le bug ne se déclenche que sur la valeur pile,
ce qui explique qu'il soit passé inaperçu pendant sept ans.

### Le geste qui compte

Pour chaque écart, l'ordre est le même et il n'est pas négociable :

1. un test qui exprime la règle officielle, et qui **échoue**
2. la correction, minimale, une ligne dans trois cas sur quatre
3. la mise à jour du filet, dont le test figeait l'ancien comportement

Le troisième commit est le seul moment du TP où l'on a le droit de modifier un test
existant, et c'est parce que le comportement attendu a officiellement changé.

Pour M2, une préparation a précédé le cycle : la comparaison était écrite à quatre
endroits. Un `refactor:` l'a d'abord réunie dans `est_en_alerte`, ce qui a réduit
la correction à **un seul caractère**. Préparer avant de corriger vaut mieux que
corriger quatre fois.
