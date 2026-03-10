# MLflow Demo (Local ML Workflow)

A minimal Python project for demonstrating local machine learning experiment tracking with MLflow.

## Project Structure

mlflow-demo/
- train_model.py
- load_model.py
- requirements.txt
- README.md

## What this demo shows

- Training a simple classification model using XGBoost on a small synthetic dataset
- Tracking runs in MLflow
- Logging:
  - parameters (e.g., `test_size`, `model_type`)
  - metrics (e.g., `accuracy`)
  - model artifacts (trained model)
- Loading a logged model later and making predictions

## Run from this folder

cd /Users/pranesh/Devloper/Cloud\ Product/cloudinsight/mlflow-demo

## 1) Install dependencies

pip install -r requirements.txt

## 2) Run training

python train_model.py

This creates an MLflow run and prints:
- run ID
- model metrics
- model URI (for example: `runs:/<run_id>/model`)

It also writes the latest run ID to `latest_run_id.txt` for quick model loading.

## 3) Launch MLflow UI

mlflow ui

## 4) Open MLflow UI

http://127.0.0.1:5000

In the UI, you can inspect:
- experiment runs
- parameters
- accuracy metric
- model artifacts

## Load model for prediction

Run with latest run:

python load_model.py

Run using the saved latest run ID file:

python load_model.py --from-file

Or run with a specific run ID:

python load_model.py <run_id>

The script loads the logged model using `mlflow.xgboost.load_model` and prints a sample prediction.

## Notes for macOS (XGBoost)

If XGBoost fails with `libomp.dylib` error, install OpenMP runtime:

brew install libomp
