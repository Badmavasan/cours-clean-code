# Les quatre démonstrations du jour 1

À projeter et à reproduire en direct. Chaque dossier est autonome.

## Préparer la machine, une fois

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov ruff pylint radon xenon vulture mypy pre-commit
```

## Démo 1, le nommage

Pas de fichier. Les cinq déclarations sont sur la slide, on les réécrit à l'oral au tableau.
Objectif de la discussion : faire disparaître le commentaire en réparant le nom.

## Démo 2, les outils sur un cas réel

Dossier `demo-outils`. Deux fichiers au comportement métier identique.

```bash
cd demo-outils
radon cc -s -a avant.py
radon mi -s avant.py
pylint avant.py
ruff check avant.py
vulture avant.py
xenon --max-absolute B --max-modules A --max-average A avant.py ; echo "code retour : $?"
```

Puis les mêmes commandes sur `apres.py`, et on remplit le tableau de la slide.

Les chiffres de la slide ont été relevés avec ces commandes exactes. Ils peuvent varier
de quelques dixièmes selon la version de pylint installée.

Le moment pédagogique important est la double surprise : pylint donne 8.04 sur 10 à
`avant.py`, et l'indice de maintenabilité reste A des deux côtés. Un score global ne
diagnostique rien.

## Démo 3, le commit refusé

Dossier `demo-garde-fou`. Copier `.pre-commit-config.yaml`, `pyproject.toml` et
`verifier.sh` dans un dépôt de travail, puis :

```bash
pre-commit install
# casser volontairement une ligne de code de production
git add -A && git commit -m "je casse tout"
```

Le commit est refusé, rien n'est enregistré.

## Démo 4, le cycle TDD complet

Dossier `demo-tdd`. À faire en direct au clavier, sans regarder le script.

Le script `rejouer-demo.sh` sert à répéter avant le cours, ou à rattraper si la démo
en direct dérape. Il produit exactement l'historique git montré sur la slide.

```bash
cd demo-tdd
./rejouer-demo.sh
cd fizzbuzz-demo && git log --oneline
```

13 commits pour FizzBuzz. C'est le rythme attendu au TP1.
