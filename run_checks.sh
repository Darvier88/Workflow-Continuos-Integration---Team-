#!/usr/bin/env bash
#
# run_checks.sh
# Replica localmente lo que hace el CI (.github/workflows/python-app.yml)
# para verificar que todo este en verde ANTES de abrir un PR.
#
# Uso:
#   ./run_checks.sh
#
# Que hace:
#   1. Crea/usa un entorno virtual aislado (.venv) -> no toca tu Python global.
#   2. Instala flake8 y pytest (las mismas herramientas del CI).
#   3. Corre el lint estricto que SI rompe el build en el CI.
#   4. Corre el lint completo (informativo, no rompe).
#   5. Corre pytest.
# Si algo falla, el script termina con codigo != 0 y un mensaje claro.

set -euo pipefail

# Carpeta donde vive este script (raiz del proyecto)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

VENV_DIR=".venv"
EXCLUDES=".venv,.git,__pycache__"

echo "==> Proyecto: $ROOT_DIR"

# 1. Entorno virtual
if [ ! -x "$VENV_DIR/bin/python" ]; then
  echo "==> Creando entorno virtual en $VENV_DIR ..."
  python3 -m venv "$VENV_DIR"
fi

# Usamos los binarios del venv directamente (no hace falta 'activate')
PY="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

# 2. Dependencias (mismas que el CI)
echo "==> Instalando flake8 y pytest ..."
"$PIP" install --quiet --upgrade pip
"$PIP" install --quiet flake8 pytest
if [ -f requirements.txt ]; then
  "$PIP" install --quiet -r requirements.txt
fi

# 3. Lint estricto: errores de sintaxis o nombres indefinidos (ESTE rompe el CI)
echo ""
echo "==> [1/3] flake8 estricto (E9,F63,F7,F82) ..."
"$PY" -m flake8 . --count --select=E9,F63,F7,F82 --show-source \
  --statistics --exclude="$EXCLUDES"

# 4. Lint completo: informativo, no rompe el build
echo ""
echo "==> [2/3] flake8 completo (informativo) ..."
"$PY" -m flake8 . --count --exit-zero --max-complexity=10 \
  --max-line-length=127 --statistics --exclude="$EXCLUDES"

# 5. Tests
echo ""
echo "==> [3/3] pytest ..."
"$PY" -m pytest -q

echo ""
echo "======================================"
echo " TODO EN VERDE. Listo para abrir el PR."
echo "======================================"
