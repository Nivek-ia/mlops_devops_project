"""
Classification des résultats de football - Avec MLflow Tracking

"""

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from datetime import datetime

print("Entraînement avec MLflow Tracking - Football")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Parametres
n_estimators = 15
max_depth = 3
test_size = 0.30
random_seed = 42

# Créer expérience MLflow
mlflow.set_experiment("epl-match-result-classification")

with mlflow.start_run():
    print("Nouvelle run MLflow")

    # Logger params
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("test_size", test_size)
    mlflow.log_param("random_seed", random_seed)
    mlflow.log_param("model_type", "RandomForest")

    # Données
    df = pd.read_csv("ml/data/English_Premier_League.csv")
    df = df.dropna(subset=["HomeGoals", "AwayGoals", "Result"])
    X = df[["HomeGoals", "AwayGoals"]]
    y = df["Result"]

    mlflow.log_param("dataset", "English_Premier_League.csv")
    mlflow.log_param("n_samples", len(df))
    mlflow.log_param("n_features", X.shape[1])
    mlflow.log_param("n_classes", len(y.unique()))

    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed
    )

    # Entrainement
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_seed
    )
    model.fit(X_train, y_train)

    # evaluation
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("train_samples", len(X_train))
    mlflow.log_metric("test_samples", len(X_test))

    # Sauvegarde
    mlflow.sklearn.log_model(model, "model")

    print(f"Precision: {accuracy:.2%}")
    print(f"Modèle enregistré dans MLflow")
