import os
from pathlib import Path

import joblib
import numpy as np
from huggingface_hub import hf_hub_download


class HeuristicFraudModel:
    def predict_proba(self, features):
        rows = np.asarray(features, dtype=float)
        scores = (
            (rows[:, 0] > 1000) * 0.30
            + ((rows[:, 1] < 6) | (rows[:, 1] > 22)) * 0.20
            + (rows[:, 2] > 20) * 0.20
            + (rows[:, 3] > 3) * 0.20
            + (rows[:, 4] == 1) * 0.10
        )
        fraud_probability = np.clip(scores, 0.05, 0.95)
        return np.column_stack([1 - fraud_probability, fraud_probability])

    def predict(self, features):
        return (self.predict_proba(features)[:, 1] >= 0.5).astype(int)


def load_model(repo_id: str):
    token = os.getenv("HF_TOKEN") or None
    filename = os.getenv("HF_MODEL_FILENAME", "model.joblib")

    try:
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            token=token,
            cache_dir=Path.home() / ".cache" / "huggingface",
        )
        return joblib.load(model_path)
    except Exception:
        return HeuristicFraudModel()
