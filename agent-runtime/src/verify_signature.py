from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import subprocess

class SignatureVerificationError(RuntimeError):
    pass

@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    signer_identity: str | None
    raw: str

def _run(args: list[str]) -> VerificationResult:
    process = subprocess.run(args, check=False, text=True, capture_output=True, shell=False, timeout=120)
    raw = (process.stdout + "\n" + process.stderr).strip()
    if process.returncode:
        raise SignatureVerificationError(raw or f"cosign exited {process.returncode}")
    identity = None
    for line in process.stdout.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        identity = item.get("critical", {}).get("identity", {}).get("docker-reference") or item.get("optional", {}).get("Subject")
        if identity:
            break
    return VerificationResult(True, identity, raw)

def verify_artifact_signature(artifact_ref: str, signature_path: str | None = None, certificate_identity: str | None = None, certificate_oidc_issuer: str | None = None) -> VerificationResult:
    if not artifact_ref:
        raise ValueError("artifact_ref is required")
    artifact_path = Path(artifact_ref)
    if artifact_path.exists():
        signature = Path(signature_path) if signature_path else Path(str(artifact_path) + ".sig")
        if not signature.is_file():
            raise SignatureVerificationError(f"missing signature: {signature}")
        args = ["cosign", "verify-blob", "--signature", str(signature)]
        if certificate_identity:
            args += ["--certificate-identity", certificate_identity]
        if certificate_oidc_issuer:
            args += ["--certificate-oidc-issuer", certificate_oidc_issuer]
        args += [str(artifact_path)]
        return _run(args)
    if "@sha256:" not in artifact_ref:
        raise SignatureVerificationError("OCI references must be digest pinned")
    args = ["cosign", "verify", "--output", "json"]
    if certificate_identity:
        args += ["--certificate-identity", certificate_identity]
    if certificate_oidc_issuer:
        args += ["--certificate-oidc-issuer", certificate_oidc_issuer]
    args += [artifact_ref]
    return _run(args)
