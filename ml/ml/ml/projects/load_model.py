"""
Chargement et utilisation de notre modèle EPL 
"""
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np

print("Chargement et utilisation modèle EPL...")

# charger le modèle deja sauvegardé
model_path = "epl_model"
loaded_model = mlflow.sklearn.load_model(model_path)

# exemple de match : 
new_data = pd.DataFrame([[3.0, 1.0]], columns=["HomeGoals", "AwayGoals"])
prediction = loaded_model.predict(new_data)
proba = loaded_model.predict_proba(new_data)

print("Modele charge avec succes")
print(f"Prediction: {prediction[0]} (H=domicile, A=exterieur, D=nul)")
print(f"Probabilites: {dict(zip(loaded_model.classes_, proba[0]))}")
