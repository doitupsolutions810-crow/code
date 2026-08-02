from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import uuid

def log_attestation(*, artifact: str, verified: bool, provenance: dict | None, agent_id: str, outcome: str, reason: str | None = None, exit_code: int | None = None, stdout: bytes = b"") -> Path:
    directory = Path(os.getenv("SACP_ATTESTATION_DIR", "attestations"))
    directory.mkdir(parents=True, exist_ok=True)
    document = {
        "run_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "artifact": artifact,
        "artifact_signature_verified": verified,
        "provenance_summary": provenance or {},
        "agent_id": agent_id,
        "runner_image": os.getenv("SACP_RUNNER_IMAGE", "unknown"),
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "exit_code": exit_code,
        "outcome": outcome,
        "reason": reason,
        "signed_by_control_plane": None,
    }
    name = f"{document['timestamp'].replace(':', '-')}-{document['run_id']}.json"
    path = directory / name
    path.write_text(json.dumps(document, sort_keys=True, indent=2) + "\n")
    return path
