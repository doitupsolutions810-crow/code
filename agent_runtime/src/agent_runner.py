from __future__ import annotations
import subprocess

DEFAULT_FLAGS = [
    "--security-opt", "no-new-privileges",
    "--security-opt", "seccomp=/app/security/seccomp.json",
    "--cap-drop", "ALL",
    "--read-only",
    "--network", "none",
    "--pids-limit", "128",
    "--memory", "512m",
    "--cpus", "1.0",
]

def launch(image: str, command: list[str]) -> subprocess.CompletedProcess[str]:
    if "@sha256:" not in image:
        raise ValueError("runner image must be digest pinned")
    return subprocess.run(["docker", "run", "--rm", *DEFAULT_FLAGS, image, *command], shell=False, text=True, capture_output=True, timeout=900)
