# Sovereign AI Control Plane (SACP)

Security-gated monorepo integrating CONTROL12 Model Plane, Cleanroom agents, the Living Intermediate Control Plane, CycleKernel attestation concepts, and an artifact registry surface.

## Invariants

1. No artifact executes before signature and provenance verification.
2. No private key or long-lived credential is committed.
3. Sandboxes run non-root, read-only, capability-free, network-denied by default.
4. Every accepted or rejected run emits an attestation.
5. Production signing, registry, object-lock, admission, and branch-protection decisions require human approval.

## Temporary publication status

This repository is a reversible bootstrap host because `doitupsolutions810-crow/sacp-platform` is not yet visible to the installed GitHub connector. The final repository name remains `sacp-platform`.
