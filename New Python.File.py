#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BUNDLE_NAME="StockMind-AI_full_code_${TIMESTAMP}.zip"
MANIFEST_NAME="StockMind-AI_manifest_${TIMESTAMP}.txt"
CHECKSUM_NAME="StockMind-AI_checksums_${TIMESTAMP}.txt"

# Exclude generated/local artifacts
EXCLUDES=(
  "*/.git/*"
  "*/__pycache__/*"
  "*.pyc"
  "*.pyo"
  "*.pyd"
  "*.db"
  "*.sqlite"
  "*.sqlite3"
  "*.log"
  "*.zip"
  "./.venv/*"
  "./venv/*"
  "./node_modules/*"
  "./.pytest_cache/*"
  "./.mypy_cache/*"
)

ZIP_ARGS=()
for ex in "${EXCLUDES[@]}"; do
  ZIP_ARGS+=("-x" "$ex")
done

zip -r "$BUNDLE_NAME" . "${ZIP_ARGS[@]}" >/dev/null

# Manifest of files included in bundle
unzip -Z1 "$BUNDLE_NAME" | sort > "$MANIFEST_NAME"

# Checksums for traceability
sha256sum "$BUNDLE_NAME" > "$CHECKSUM_NAME"

cat <<EOF
✅ Bundle created: $BUNDLE_NAME
✅ Manifest created: $MANIFEST_NAME
✅ Checksum created: $CHECKSUM_NAME

To verify:
  sha256sum -c $CHECKSUM_NAME
EOF