#!/usr/bin/env bash
# La commande unique avant de pousser. Elle doit renvoyer 0.
set -e

echo "--- formatage ---"
ruff format --check .

echo "--- lint ---"
ruff check .

echo "--- complexite ---"
radon cc -s -a inventaire kata_parking
xenon --max-absolute B --max-modules A --max-average A inventaire kata_parking

echo "--- tests et couverture ---"
pytest --cov=inventaire --cov=kata_parking --cov-branch --cov-report=term-missing

echo ""
echo "Tout est vert."
