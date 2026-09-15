#!/usr/bin/env bash
# Rejoue la demo 4 du jour 1 : un cycle TDD complet sur FizzBuzz,
# avec un commit par phase rouge, verte et bleue.
#
# Usage : ./rejouer-demo.sh [dossier_de_sortie]
# Par defaut le dossier de sortie est ./fizzbuzz-demo
#
# A la fin, "git log --oneline" dans ce dossier montre l'historique
# exactement tel qu'il doit ressembler chez les etudiants au TP1.

set -euo pipefail

SORTIE="${1:-fizzbuzz-demo}"
rm -rf "$SORTIE"
mkdir -p "$SORTIE"
cd "$SORTIE"

git init -q
git config user.name "Demo TDD"
git config user.email "demo@example.org"

# pas de fichiers parasites dans l'historique
export PYTHONDONTWRITEBYTECODE=1
printf '__pycache__/\n.pytest_cache/\n.venv/\n' > .gitignore

rouge() {
  echo ""
  echo ">>> ROUGE : $1"
  set +e
  python3 -m pytest -q 2>&1 | tail -3
  set -e
  git add -A && git commit -q -m "red: $1"
}

vert() {
  echo ">>> VERT : $1"
  python3 -m pytest -q 2>&1 | tail -2
  git add -A && git commit -q -m "green: $1"
}

bleu() {
  echo ">>> REFACTOR : $1"
  python3 -m pytest -q 2>&1 | tail -2
  git add -A && git commit -q -m "refactor: $1"
}

# --- Tour 1 : le plus petit comportement possible -------------------------
cat > test_fizzbuzz.py <<'EOF'
from fizzbuzz import fizzbuzz


def test_1_renvoie_1():
    assert fizzbuzz(1) == "1"
EOF
rouge "1 renvoie 1"

cat > fizzbuzz.py <<'EOF'
def fizzbuzz(nombre):
    return "1"
EOF
vert "1 renvoie 1"

# --- Tour 2 : triangulation, la constante ne tient plus -------------------
cat >> test_fizzbuzz.py <<'EOF'


def test_2_renvoie_2():
    assert fizzbuzz(2) == "2"
EOF
rouge "2 renvoie 2"

cat > fizzbuzz.py <<'EOF'
def fizzbuzz(nombre):
    return str(nombre)
EOF
vert "2 renvoie 2"

# --- Tour 3 : premiere regle metier, encore en dur ------------------------
cat >> test_fizzbuzz.py <<'EOF'


def test_3_renvoie_fizz():
    assert fizzbuzz(3) == "Fizz"
EOF
rouge "3 renvoie Fizz"

cat > fizzbuzz.py <<'EOF'
def fizzbuzz(nombre):
    if nombre == 3:
        return "Fizz"
    return str(nombre)
EOF
vert "3 renvoie Fizz"

# --- Tour 4 : on force la generalisation ---------------------------------
cat >> test_fizzbuzz.py <<'EOF'


def test_6_renvoie_fizz():
    assert fizzbuzz(6) == "Fizz"
EOF
rouge "6 renvoie Fizz"

cat > fizzbuzz.py <<'EOF'
def fizzbuzz(nombre):
    if nombre % 3 == 0:
        return "Fizz"
    return str(nombre)
EOF
vert "les multiples de 3 renvoient Fizz"

# --- Tour 5 : Buzz -------------------------------------------------------
cat >> test_fizzbuzz.py <<'EOF'


def test_5_renvoie_buzz():
    assert fizzbuzz(5) == "Buzz"


def test_10_renvoie_buzz():
    assert fizzbuzz(10) == "Buzz"
EOF
rouge "les multiples de 5 renvoient Buzz"

cat > fizzbuzz.py <<'EOF'
def fizzbuzz(nombre):
    if nombre % 3 == 0:
        return "Fizz"
    if nombre % 5 == 0:
        return "Buzz"
    return str(nombre)
EOF
vert "les multiples de 5 renvoient Buzz"

# --- Tour 6 : le cas combine --------------------------------------------
cat >> test_fizzbuzz.py <<'EOF'


def test_15_renvoie_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"
EOF
rouge "15 renvoie FizzBuzz"

cat > fizzbuzz.py <<'EOF'
def fizzbuzz(nombre):
    if nombre % 15 == 0:
        return "FizzBuzz"
    if nombre % 3 == 0:
        return "Fizz"
    if nombre % 5 == 0:
        return "Buzz"
    return str(nombre)
EOF
vert "15 renvoie FizzBuzz"

# --- Phase bleue : on ne touche pas aux tests -----------------------------
cat > fizzbuzz.py <<'EOF'
DIVISEURS = ((3, "Fizz"), (5, "Buzz"))


def fizzbuzz(nombre):
    """Renvoie Fizz, Buzz, FizzBuzz ou le nombre lui-meme, en texte."""
    resultat = "".join(
        mot for diviseur, mot in DIVISEURS if nombre % diviseur == 0
    )
    return resultat or str(nombre)
EOF
bleu "table de diviseurs a la place des branches"

echo ""
echo "=============================================="
echo "Historique produit :"
git log --oneline
echo ""
echo "Nombre de commits : $(git rev-list --count HEAD)"
echo "=============================================="
