#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Odoo Factory Platform — Automated Test Runner (Disposable Databases)
# ==============================================================================

MODULE=""
SCENARIO=""
KEEP_DB=false
DB_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --module)
      MODULE="$2"
      shift 2
      ;;
    --scenario)
      SCENARIO="$2"
      shift 2
      ;;
    --keep-db)
      KEEP_DB=true
      shift
      ;;
    --db)
      DB_NAME="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$DB_NAME" ]]; then
  RUN_ID=$(date +%s)
  DB_NAME="odoo_test_${RUN_ID}"
fi

echo "=========================================================="
echo " ODOO FACTORY PLATFORM — TEST RUNNER"
echo " Test Database : $DB_NAME"
echo " Target Module : ${MODULE:-All installed}"
echo " Scenario Code : ${SCENARIO:-N/A}"
echo "=========================================================="

TEST_ARGS=("-d" "$DB_NAME" "--test-enable" "--stop-after-init")
if [[ -n "$MODULE" ]]; then
  TEST_ARGS+=("-u" "$MODULE")
fi

cleanup() {
  if [[ "$KEEP_DB" = false ]]; then
    echo "Cleaning up disposable database: $DB_NAME..."
    docker compose exec -T db dropdb -U odoo --if-exists "$DB_NAME" 2>/dev/null || true
  fi
}
trap cleanup EXIT

docker compose run --rm web odoo "${TEST_ARGS[@]}"
echo "[TEST PASS] All tests passed."
