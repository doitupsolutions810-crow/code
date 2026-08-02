from pathlib import Path
import json
import hashlib

class ProvenanceError(RuntimeError):
    pass

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def validate_provenance(artifact_ref: str, provenance_path: str | None = None) -> dict:
    if provenance_path is None:
        raise ProvenanceError("provenance document is required")
    path = Path(provenance_path)
    if not path.is_file():
        raise ProvenanceError(f"missing provenance: {path}")
    data = json.loads(path.read_text())
    if data.get("_type") not in ("https://in-toto.io/Statement/v1", "https://in-toto.io/Statement/v0.1"):
        raise ProvenanceError("unsupported in-toto statement")
    subjects = data.get("subject") or []
    if not subjects:
        raise ProvenanceError("provenance has no subject")
    artifact_path = Path(artifact_ref)
    if artifact_path.is_file():
        digest = sha256_file(artifact_path)
        if not any(subject.get("digest", {}).get("sha256") == digest for subject in subjects):
            raise ProvenanceError("artifact digest absent from provenance")
    return {"validated": True, "predicateType": data.get("predicateType"), "subjects": subjects}
