#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m compileall -q agent-runtime/src agent_runtime
python3 -m pytest -q agent-runtime/tests
node --check control-plane/src/server.js
node --check control-plane/tests/contracts.test.js

python3 - <<'PY'
import json
from pathlib import Path
import yaml

for path in Path('.').rglob('*.json'):
    if '.git' not in path.parts:
        json.loads(path.read_text())
for path in Path('.').rglob('*.y*ml'):
    if '.git' not in path.parts:
        list(yaml.safe_load_all(path.read_text()))
print('structured documents: PASS')
PY

if command -v helm >/dev/null 2>&1; then
  if helm template sacp infra/helm-chart --set image.repository=ghcr.io/example/sacp --set image.digest=sha256:$(printf 'a%.0s' {1..64}) >/dev/null; then
    echo 'helm template: PASS'
  else
    echo 'helm template: FAIL' >&2
    exit 1
  fi
else
  echo 'helm: SKIPPED (not installed)'
fi

if command -v trivy >/dev/null 2>&1; then
  trivy fs --exit-code 1 --severity CRITICAL --ignore-unfixed .
else
  echo 'trivy: SKIPPED (not installed)'
fi

echo 'SACP_LOCAL_VALIDATION_PASS'
