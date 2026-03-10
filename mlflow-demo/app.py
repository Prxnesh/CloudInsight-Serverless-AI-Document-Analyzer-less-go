from pathlib import Path

import gradio as gr
import mlflow
import mlflow.xgboost
import pandas as pd

# Point to the local mlruns directory beside this file
MLRUNS_DIR = Path(__file__).resolve().parent / "mlruns"
mlflow.set_tracking_uri(MLRUNS_DIR.resolve().as_uri())

# Load best run from the mlflow-demo experiment
client = mlflow.MlflowClient()
# Search both possible experiment names (mlflow-demo from demo script,
# local-xgboost-classification from train_model.py)
experiment = (
    client.get_experiment_by_name("mlflow-demo")
    or client.get_experiment_by_name("local-xgboost-classification")
)
if experiment is None:
    raise RuntimeError(
        "No MLflow experiment found. Run mlflow_demo.py or train_model.py first."
    )
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.accuracy DESC"],
    max_results=1,
)
best_run = runs[0]
model_uri = f"runs:/{best_run.info.run_id}/model"
model = mlflow.xgboost.load_model(model_uri)

# Determine which feature column names the model was trained with
_sample_input = best_run.data.params
_uses_underscore = "feature_1" in str(best_run.inputs)
FEATURE_COLS = ["feature_1", "feature_2"] if experiment.name == "local-xgboost-classification" else ["feature1", "feature2"]
print(f"Loaded model from experiment '{experiment.name}' run {best_run.info.run_id}")
print(f"Accuracy: {best_run.data.metrics.get('accuracy', 'n/a')}  |  Features: {FEATURE_COLS}")


def predict(feature1: float, feature2: float) -> str:
    df = pd.DataFrame([[feature1, feature2]], columns=FEATURE_COLS)
    pred = model.predict(df)
    return f"Predicted class: {int(pred[0])}"


interface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="Feature 1"),
        gr.Number(label="Feature 2"),
    ],
    outputs="text",
    title="MLflow Model Demo",
    description="Simple MLflow tracked model prediction",
)

interface.launch()