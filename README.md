# Crafting Code, 4 jours

Support de cours et travaux pratiques.

## Jour 1, clean code et TDD

```
jour1/
  cours-jour1.md      support Marp, 118 slides, environ 3 h
  cours-jour1.pdf     le même, exporté
  img/                les 6 schémas SVG utilisés dans les slides
  demos/              les 4 démonstrations faites en direct
tp1/
  README.md           l'énoncé des 5 missions, environ 5 h
  legacy/             le module à auditer et à refactoriser
  modeles/            le squelette du rapport qualité à rendre
  outils/             le script qui vérifie que le TDD a vraiment été fait
```

## Projeter les slides

Le support est un fichier Marp. Deux façons de l'utiliser.

Dans VS Code, avec l'extension **Marp for VS Code**, ouvrir `jour1/cours-jour1.md`
et lancer l'aperçu.

En ligne de commande, pour produire le PDF ou le HTML :

```bash
cd jour1
npx @marp-team/marp-cli cours-jour1.md --pdf --allow-local-files
npx @marp-team/marp-cli cours-jour1.md --html --allow-local-files
```

L'option `--allow-local-files` est obligatoire, les schémas SVG sont des fichiers locaux.

## Préparer les démonstrations

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov ruff pylint radon xenon vulture mypy pre-commit
```

Le détail de chaque démo est dans `jour1/demos/README.md`.

Répéter la démo TDD avant le cours :

```bash
cd jour1/demos/demo-tdd && ./rejouer-demo.sh && cd fizzbuzz-demo && git log --oneline
```

## Corriger le TP1

```bash
cd tp1
./outils/verifier-historique.sh /chemin/vers/le/depot/de/l/etudiant 3
```

Le script contrôle la convention de commits, l'alternance rouge puis vert, l'absence de
code de production dans les commits `red:`, et rejoue des commits `red:` tirés au hasard
pour vérifier qu'ils sont réellement rouges.

## Jours 2 à 4

À produire : SOLID et patrons de conception, code legacy et odeurs, stratégie de tests
complète avec CI/CD, débogage structuré et éco-conception.
