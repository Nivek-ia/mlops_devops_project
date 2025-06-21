import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
 
print("Entraînement et sauvegarde du modèle EPL...")
 
# Charger les données
df = pd.read_csv("ml/data/English_Premier_League.csv")
df = df.dropna(subset=["HomeGoals", "AwayGoals", "Result"])
 
# Features - labels
X = df[["HomeGoals", "AwayGoals"]]
y = df["Result"]
 
# split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
 
# Entrainer le modèle
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)
 
# sauvegarder modèle avec MLflow (
model_path = "epl_model"
mlflow.sklearn.save_model(model, model_path)
import pickle
import os
 
pickle_path = "app/model.pkl"
os.makedirs(os.path.dirname(pickle_path), exist_ok=True)
 
with open(pickle_path, "wb") as f:
    pickle.dump(model, f)
 
print(f"Modele pickle sauvegarde dans: {pickle_path}")
print(f"Modele sauvegarde dans: {model_path}")
 
print("\nChargement et utilisation du modele EPL...")
 
# charger
loaded_model = mlflow.sklearn.load_model(model_path)
 
# tester 
# Exemple : Home 2 but, Away 1 but
new_data = np.array([[2.0, 1.0]])
prediction = loaded_model.predict(new_data)
proba = loaded_model.predict_proba(new_data)
 
print("Modele charge avec succes")
print(f"Prediction: {prediction[0]} (H=domicile, A=exterieur, D=nul)")
print(f"Probabilites: {dict(zip(loaded_model.classes_, proba[0]))}")