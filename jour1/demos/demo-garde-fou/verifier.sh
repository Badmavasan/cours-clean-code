#!/usr/bin/env bash
# La commande unique que toute l'equipe lance avant de pousser.
# Elle doit renvoyer 0. Si elle renvoie autre chose, on ne pousse pas.
set -e

echo "--- format et lint ---"
ruff format --check .
ruff check .

echo "--- complexite ---"
radon cc -s -a --total-average .
xenon --max-absolute B --max-modules A --max-average A .

echo "--- code mort ---"
vulture . --min-confidence 80

echo "--- tests et couverture ---"
pytest --cov=. --cov-branch --cov-report=term-missing

echo ""
echo "Tout est vert."
