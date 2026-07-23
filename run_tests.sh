#!/bin/bash
# vitalXAI Test Runner
# Usage: ./run_tests.sh [--coverage|--lint|--fix]

set -e

FLAGS="-q --tb=short -W ignore"
COV="--cov=services --cov=routers --cov=database --cov-report=term-missing"

case "${1:-all}" in
  --coverage|-c)
    PYTHONWARNINGS=ignore python -m pytest tests/unit/ $COV $FLAGS
    ;;
  --lint|-l)
    ruff check . -q --ignore E501
    ;;
  --fix|-f)
    ruff check . --fix -q
    ;;
  all|-a|"")
    PYTHONWARNINGS=ignore python -m pytest tests/unit/ $COV $FLAGS
    echo ""
    ruff check . -q --ignore E501
    echo ""
    echo "[OK] All checks passed"
    ;;
  *)
    echo "Usage: ./run_tests.sh [--coverage|--lint|--fix]"
    exit 1
    ;;
esac
