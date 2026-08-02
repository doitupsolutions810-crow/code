from unittest.mock import patch
from agent_runtime.src.orchestrator import execute

class Verification:
    verified = True

class Process:
    returncode = 0
    stdout = "ok"
    stderr = ""

def test_ordered_security_gates(tmp_path, monkeypatch):
    monkeypatch.setenv("SACP_ATTESTATION_DIR", str(tmp_path / "attestations"))
    with patch("agent_runtime.src.orchestrator.verify_artifact_signature", return_value=Verification()) as verify, patch("agent_runtime.src.orchestrator.validate_provenance", return_value={"validated": True}) as provenance, patch("agent_runtime.src.orchestrator.launch", return_value=Process()) as launch:
        result = execute(
            artifact_ref="artifact",
            signature_path="artifact.sig",
            provenance_path="artifact.intoto.json",
            agent_id="agent",
            image="runner@sha256:" + "a" * 64,
            command=["true"],
        )
    assert result["outcome"] == "succeeded"
    verify.assert_called_once()
    provenance.assert_called_once()
    launch.assert_called_once()
