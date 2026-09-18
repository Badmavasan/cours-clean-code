# TP2, corrigé de la mission 1

Le corrigé vit sur la branche **`tp2-corrige`**, qui contient les commits réels.
Le script de ce dossier est ce qui l'a produite.

## Consulter la branche

```bash
git fetch origin
git log --oneline origin/tp2-corrige
git show origin/tp2-corrige:RAPPORT-CONCEPTION.md
git worktree add ../tp2-corrige tp2-corrige
```

## Régénérer

```bash
./rejouer-mission-1.sh /un/dossier/de/travail
```

Le script crée un dépôt neuf, il ne modifie rien sur place.

## Les sept commits

| Message | Étiquette |
|---|---|
| dépôt initialisé et gitignore | `[Mission 0]` |
| code de facturation à auditer | `[Mission 0]` |
| les cinq violations, une par principe | `[Partie 1]` |
| coût de la demande D1, formule decouverte | `[Partie 2] D1` |
| coût de la demande D2, code promo RENTREE | `[Partie 2] D2` |
| coût de la demande D3, palier à deux cents postes | `[Partie 2] D3` |
| graphe des dépendances et candidats à l'inversion | `[Partie 3]` |

Horodatés de 9h05 à 10h18, ce qui correspond aux 20 minutes de mission 0 et aux
40 minutes de mission 1 annoncées dans le sujet.

## Ce que le script vérifie tout seul

Les 25 tests sont verts **avant** que quoi que ce soit ne soit écrit.

À la fin, `git diff depart-tp2 HEAD -- '*.py'` est **vide**. La mission 1 interdit de
toucher au code, et le script s'arrête si un seul fichier Python a bougé.

Les 25 tests sont toujours verts.

## Les quatre points à faire passer en salle

**Trois violations sur cinq se trouvent sans lire un corps de fonction.** `D` se lit dans
l'import ligne 7 de `facture.py`, `I` dans la déclaration ligne 6 de `passerelles.py`,
`L` dans la signature ligne 48 de `abonnements.py`. Le rapport le dit explicitement,
parce que c'est la compétence à transmettre : on diagnostique une conception en lisant
les frontières, pas les algorithmes.

**Le `grep` sur les imports ne trouve que `D`.** Le rapport a une section « ce que le
graphe ne dit pas » : ni le couplage par héritage de `AbonnementAnnuel`, ni celui par
interface de `ClientSMTP` n'apparaissent, puisque parent et enfant sont dans le même
fichier. Un étudiant qui s'arrête à la commande trouve une violation sur cinq. C'est le
moment de dire que l'outil ne remplace pas la lecture.

**La colonne conséquence est ce qui distingue une bonne copie.** « Ce n'est pas
extensible » ne vaut rien. « Ajouter une formule rouvre une fonction couverte par
4 tests » vaut tout. Le corrigé donne pour chaque demande un **détail qui coûte cher**,
et ces trois détails ne se trouvent qu'en lisant vraiment.

**Le piège de D3.** L'ordre des `if` dans `taux_de_remise_volume` porte une règle métier
implicite : les paliers doivent être testés du plus grand au plus petit. Aucun des six
tests actuels ne l'attrape, ils vérifient des valeurs et pas un ordre. C'est exactement
le genre de règle qu'un étudiant casse en mission 4 en refactorisant de bonne foi.
Mieux vaut qu'il l'ait écrit en mission 1.

## Ce que le corrigé ne contient pas

Les missions 2 à 6. La branche s'arrête à la fin du diagnostic, code intact.
