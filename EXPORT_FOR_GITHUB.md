# Export Full Code Package for GitHub

If you want to download **all source files** from this tool and upload to your GitHub repo, use the script below.

## 1) Create a full-code bundle

\\\ash
bash scripts/create_full_repo_bundle.sh
\\\

This generates:
- \StockMind-AI_full_code_<timestamp>.zip\ -> full project bundle
- \StockMind-AI_manifest_<timestamp>.txt\ -> file list in bundle
- \StockMind-AI_checksums_<timestamp>.txt\ -> SHA256 checksum

## 2) Verify the package

\\\ash
sha256sum -c StockMind-AI_checksums_<timestamp>.txt
\\\
