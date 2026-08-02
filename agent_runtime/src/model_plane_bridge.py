from pathlib import Path

MODEL_PLANE_ROOT = Path(__file__).resolve().parents[2] / "systems" / "control12-model-plane"

def capabilities() -> dict:
    return {
        "control12_model_plane": str(MODEL_PLANE_ROOT),
        "features": [
            "gpu",
            "ray",
            "kuberay",
            "supabase",
            "dataset-lineage",
            "leases",
            "cancellation",
            "model-lab-dashboard",
        ],
    }
