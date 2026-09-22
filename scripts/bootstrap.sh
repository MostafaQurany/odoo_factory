#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Odoo Factory Platform — Idempotent Bootstrap & Profile Installer
# ==============================================================================

PROFILE="core"
DEMO=false
MODULES=""
DB_NAME=""
UPDATE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --demo)
      DEMO=true
      shift
      ;;
    --modules)
      MODULES="$2"
      shift 2
      ;;
    --db)
      DB_NAME="$2"
      shift 2
      ;;
    --update)
      UPDATE=true
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$DB_NAME" ]]; then
  if [[ -f .env ]]; then
    DB_NAME=$(grep -E '^ODOO_DB=' .env | cut -d '=' -f 2 | tr -d ' \r\n' || echo "")
  fi
  if [[ -z "$DB_NAME" ]]; then
    DB_NAME="odoo"
  fi
fi

TARGET_MODULES=""
if [[ -n "$MODULES" ]]; then
  TARGET_MODULES="$MODULES"
else
  case "${PROFILE,,}" in
    core) TARGET_MODULES="factory_profile_core" ;;
    operations) TARGET_MODULES="factory_profile_operations" ;;
    advanced) TARGET_MODULES="factory_profile_advanced" ;;
    full) TARGET_MODULES="factory_profile_full" ;;
    legacy) TARGET_MODULES="odoo_factory_all" ;;
    *) echo "Invalid profile: $PROFILE. Valid: core, operations, advanced, full, legacy" >&2; exit 1 ;;
  esac
fi

if [[ "$DEMO" = true ]]; then
  TARGET_MODULES="${TARGET_MODULES},factory_demo"
fi

FLAG="-i"
if [[ "$UPDATE" = true ]]; then
  FLAG="-u"
fi

echo "=========================================================="
echo " ODOO FACTORY PLATFORM — BOOTSTRAP RUNNER"
echo " Database : $DB_NAME"
echo " Action   : $FLAG"
echo " Modules  : $TARGET_MODULES"
echo "=========================================================="

docker compose run --rm web odoo -d "$DB_NAME" "$FLAG" "$TARGET_MODULES" --stop-after-init
echo "[SUCCESS] Bootstrap operation completed."
