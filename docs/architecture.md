# SACP Architecture

```text
Publisher -> Artifact API -> Signature Gate -> Provenance Gate -> Scheduler
                                                        |          |
                                                        v          v
                                                Rejection Attest   Hardened Runner
                                                                   |
                                                  +----------------+----------------+
                                                  |                                 |
                                      CONTROL12 Model Plane                  Cleanroom Agents
                                      GPU/Ray/KubeRay/Supabase               tools/memory/tasks
                                                  |                                 |
                                                  +--------------+------------------+
                                                                 v
                                                     Signed run attestation
                                                                 |
                                                append-only/object-lock store
```

## Acceptance criteria

| Control | Acceptance |
|---|---|
| Signature | `cosign verify` or `verify-blob` succeeds and identity matches policy |
| Provenance | in-toto subject digest matches the artifact |
| Image | digest pinned; mutable tags rejected |
| Sandbox | non-root, no-new-privileges, all capabilities dropped, read-only root, network denied |
| Attestation | accepted and rejected runs create schema-valid records |
| Secrets | no private keys or long-lived credentials in Git |

## Publication note

The current private `code` repository is a reversible bootstrap host. The canonical destination remains `doitupsolutions810-crow/sacp-platform` once that repository is created and exposed to the GitHub connector.
