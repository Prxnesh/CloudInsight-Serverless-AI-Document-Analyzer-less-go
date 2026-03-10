from pathlib import Path

import mlflow
import mlflow.xgboost
import xgboost as xgb
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Pin tracking to the mlruns folder next to this script
MLRUNS_DIR = Path(__file__).resolve().parent / "mlruns"
mlflow.set_tracking_uri(MLRUNS_DIR.resolve().as_uri())

print("SCRIPT STARTED")
print("Tracking URI:", mlflow.get_tracking_uri())

# Sample dataset
data = {
    "feature1": list(range(1, 11)),
    "feature2": list(range(11, 21)),
    "target": [0,0,0,0,1,1,1,1,1,1]
}

df = pd.DataFrame(data)

X = df[["feature1","feature2"]]
y = df["target"]

# train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mlflow.set_experiment("mlflow-demo")

for depth in [2, 3, 4, 5]:

    with mlflow.start_run(run_name=f"xgb_depth_{depth}"):

        model = xgb.XGBClassifier(
            max_depth=depth,
            eval_metric="logloss"
        )

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)

        mlflow.log_param("max_depth", depth)
        mlflow.log_metric("accuracy", acc)

        mlflow.xgboost.log_model(model, "model")

        print("Depth:", depth, "Accuracy:", acc)