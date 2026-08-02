# SACP Mitigations

1. **Supply chain:** digest pinning, Cosign verification, in-toto provenance, SBOM requirement, and Trivy CI.
2. **Runtime isolation:** immutable image, non-root UID, seccomp allowlist, capability removal, read-only root, PID/memory/CPU bounds, and default-deny networking.
3. **Control plane:** OpenAPI request/response validation, bounded input sizes, explicit agent IDs, and fail-closed scheduling.
4. **Audit:** every rejection and execution produces a content-hash-bearing attestation.
5. **Model plane:** CONTROL12 approvals, dataset lineage, leases, cancellation, GPU runtime discovery, Ray/KubeRay controllers, and Supabase RLS.
6. **Human gates:** production trust roots, registry, object lock, admission enforcement, and branch protection are never auto-selected.

## Remaining gaps

- GitHub Actions cannot currently allocate jobs in this private bootstrap repository; tracked in issue #3.
- The final `sacp-platform` repository is not visible to the connector; tracked in issue #1.
- The full CONTROL12 v0.2.0 source archive remains in the validated external bundle until the final repository is available.
- Production Sigstore identity/issuer, OCI registry, object-lock target, and admission enforcement require human decisions.
