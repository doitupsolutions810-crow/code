from .verify_signature import verify_artifact_signature, SignatureVerificationError
from .provenance import validate_provenance, ProvenanceError
from .attestation import log_attestation
from .agent_runner import launch

def execute(*, artifact_ref: str, signature_path: str | None, provenance_path: str, agent_id: str, image: str, command: list[str]):
    try:
        verification = verify_artifact_signature(artifact_ref, signature_path)
        provenance = validate_provenance(artifact_ref, provenance_path)
    except (SignatureVerificationError, ProvenanceError, ValueError) as exc:
        log_attestation(
            artifact=artifact_ref,
            verified=False,
            provenance=None,
            agent_id=agent_id,
            outcome="rejected",
            reason=str(exc),
        )
        raise
    result = launch(image, command)
    outcome = "succeeded" if result.returncode == 0 else "failed"
    attestation = log_attestation(
        artifact=artifact_ref,
        verified=verification.verified,
        provenance=provenance,
        agent_id=agent_id,
        outcome=outcome,
        exit_code=result.returncode,
        stdout=result.stdout.encode(),
    )
    return {
        "outcome": outcome,
        "attestation": str(attestation),
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
    }
