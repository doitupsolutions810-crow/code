# CI continuity plan

GitHub-hosted workflow runs currently terminate with `startup_failure` before a job is allocated. Until repository/account Actions policy is corrected, use `make validate` from a trusted operator workstation or ephemeral runner.

## Local validation

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r agent-runtime/requirements.txt pytest pyyaml
cd control-plane && npm install && cd ..
make validate
```

The command fails closed on Python compilation, Python tests, Node syntax, JSON/YAML parsing, Helm rendering when Helm is installed, and CRITICAL Trivy findings when Trivy is installed.

## Self-hosted runner fallback

A self-hosted runner is an optional continuity path, not an authorization bypass.

1. Use a dedicated ephemeral VM or isolated Kubernetes workload.
2. Create a short-lived repository runner registration token through GitHub's UI/API.
3. Never commit the token or runner credentials.
4. Assign labels such as `self-hosted`, `linux`, `x64`, and `sacp-ephemeral`.
5. Run jobs in a disposable workspace and destroy the runner after each job.
6. Do not mount production Docker sockets, kubeconfigs, cloud credentials, or signing keys into general PR jobs.
7. Require human approval before enabling workflows that access production environments.

The fallback remains blocked until an operator explicitly provisions the runner and confirms repository Actions are enabled. GitHub-hosted CI should remain the default after the account-level startup problem is fixed.
