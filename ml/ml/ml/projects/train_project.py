"""
Entraînement modèle EPL - compatible MLflow Projects
Utilisable avec MLflow run
"""
import argparse
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def load_epl_data(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["HomeGoals", "AwayGoals", "Result"])
    X = df[["HomeGoals", "AwayGoals"]]
    y = df["Result"]
    return X, y

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=15)
    parser.add_argument("--max_depth", type=int, default=3)
    parser.add_argument("--test_size", type=float, default=0.3)
    parser.add_argument("--random_seed", type=int, default=42)
    args = parser.parse_args()

    mlflow.set_experiment("epl-classification")

    with mlflow.start_run():
        mlflow.log_params(vars(args))

        # Chargement des données
        X, y = load_epl_data("ml/data/English_Premier_League.csv")
        mlflow.log_param("dataset_size", len(X))

        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=args.random_seed
        )

        model = RandomForestClassifier(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=args.random_seed
        )
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        mlflow.log_metric("accuracy", accuracy)

        # Enregistrement model
        mlflow.sklearn.log_model(model, "model")

        print(f"Precision: {accuracy:.2%}")
        print("Modèle et paramètres enregistrés dans MLflow")
