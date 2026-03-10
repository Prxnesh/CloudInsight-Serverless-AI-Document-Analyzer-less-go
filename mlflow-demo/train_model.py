from pathlib import Path

import mlflow
import mlflow.xgboost
import pandas as pd
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


EXPERIMENT_NAME = "local-xgboost-classification"
MLRUNS_DIR = Path(__file__).resolve().parent / "mlruns"


def create_dataset() -> tuple[pd.DataFrame, pd.Series]:
    """Create a tiny synthetic binary classification dataset using pandas."""
    features, target = make_classification(
        n_samples=200,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        n_classes=2,
        random_state=42,
    )

    X = pd.DataFrame(features, columns=["feature_1", "feature_2"])
    y = pd.Series(target, name="target")
    return X, y


def ensure_experiment_exists(experiment_name: str) -> str:
    """Create the MLflow experiment if missing and return experiment id."""
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        return mlflow.create_experiment(experiment_name)
    return experiment.experiment_id


def main() -> None:
    MLRUNS_DIR.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(MLRUNS_DIR.resolve().as_uri())

    experiment_id = ensure_experiment_exists(EXPERIMENT_NAME)
    X, y = create_dataset()

    # Multiple run configs make side-by-side comparison easy in MLflow UI.
    run_configs = [
        {"run_name": "xgb_test20", "test_size": 0.20, "max_depth": 3},
        {"run_name": "xgb_test30", "test_size": 0.30, "max_depth": 4},
        {"run_name": "xgb_test40", "test_size": 0.40, "max_depth": 5},
    ]

    for config in run_configs:
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=config["test_size"],
            random_state=42,
            stratify=y,
        )

        model = xgb.XGBClassifier(
            n_estimators=80,
            max_depth=config["max_depth"],
            learning_rate=0.1,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=42,
        )

        with mlflow.start_run(experiment_id=experiment_id, run_name=config["run_name"]) as run:
            # Required parameter logging
            mlflow.log_param("model_type", "xgboost.XGBClassifier")
            mlflow.log_param("test_size", config["test_size"])

            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)

            # Required metric logging
            mlflow.log_metric("accuracy", float(accuracy))

            # Required model artifact logging
            try:
                mlflow.xgboost.log_model(model, name="model")
            except TypeError:
                mlflow.xgboost.log_model(model, artifact_path="model")

            print(
                f"Run: {run.info.run_id} | test_size={config['test_size']} "
                f"| accuracy={accuracy:.4f}"
            )

    print("\nTracking URI:", mlflow.get_tracking_uri())
    print("Experiment:", EXPERIMENT_NAME)
    print("Start UI with: mlflow ui --port 5001")
    print("Open in browser: http://127.0.0.1:5001")


if __name__ == "__main__":
    main()
