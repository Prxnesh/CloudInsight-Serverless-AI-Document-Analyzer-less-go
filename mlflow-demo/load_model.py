import sys
from pathlib import Path

import mlflow
import mlflow.xgboost
import pandas as pd
from sklearn.datasets import make_classification


EXPERIMENT_NAME = "mlflow-demo-classification"


def get_latest_run_id(experiment_name: str = EXPERIMENT_NAME) -> str:
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise ValueError(
            f"Experiment '{experiment_name}' not found. Run train_model.py first."
        )

    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=1,
    )

    if runs.empty:
        raise ValueError("No runs found. Run train_model.py first.")

    return str(runs.iloc[0]["run_id"])


def get_run_id_from_file(file_path: str = "latest_run_id.txt") -> str:
    p = Path(file_path)
    if not p.exists():
        raise ValueError(
            f"{file_path} not found. Run train_model.py first or pass a run ID."
        )
    return p.read_text(encoding="utf-8").strip()


def main() -> None:
    # CLI usage:
    #   python load_model.py                -> latest from MLflow search
    #   python load_model.py --from-file    -> latest_run_id.txt
    #   python load_model.py <run_id>       -> explicit run
    run_id = None

    if len(sys.argv) > 1 and sys.argv[1] == "--from-file":
        run_id = get_run_id_from_file()
    elif len(sys.argv) > 1:
        run_id = sys.argv[1]
    else:
        run_id = get_latest_run_id()

    model_uri = f"runs:/{run_id}/model"

    # Load model
    model = mlflow.xgboost.load_model(model_uri)

    # Sample input for prediction (same synthetic feature shape used in training)
    X_np, _ = make_classification(
        n_samples=5,
        n_features=8,
        n_informative=5,
        n_redundant=1,
        n_classes=2,
        random_state=42,
    )
    feature_names = [f"feature_{i}" for i in range(X_np.shape[1])]
    X: pd.DataFrame = pd.DataFrame(X_np, columns=feature_names)
    sample = X.iloc[[0]]

    # Predict
    pred = model.predict(sample)
    pred_prob = model.predict_proba(sample)

    print(f"Loaded model from: {model_uri}")
    print(f"Sample prediction: {int(pred[0])}")
    print(f"Class probabilities: {[round(float(x), 4) for x in pred_prob[0]]}")


if __name__ == "__main__":
    main()
