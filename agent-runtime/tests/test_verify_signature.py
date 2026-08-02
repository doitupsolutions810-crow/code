from pathlib import Path
import pytest
from agent_runtime.src.verify_signature import verify_artifact_signature, SignatureVerificationError

def test_blob_requires_signature(tmp_path):
    artifact = tmp_path / "a.bin"
    artifact.write_bytes(b"x")
    with pytest.raises(SignatureVerificationError):
        verify_artifact_signature(str(artifact))

def test_oci_must_be_digest_pinned():
    with pytest.raises(SignatureVerificationError):
        verify_artifact_signature("ghcr.io/acme/a:latest")
