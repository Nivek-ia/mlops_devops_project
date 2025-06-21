from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import os
import pickle

app = FastAPI(title="API Prédiction EPL")

MODEL_PATH = "/app/model.pkl"  

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Modèle non trouvé à {MODEL_PATH}")

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

class InputData(BaseModel):
    feature1: float
    feature2: float

@app.get("/")
def read_root():
    return {"message": "API Prédiction EPL est en ligne"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: InputData):
    try:
        input_array = np.array([[data.feature1, data.feature2]]) 
        prediction = model.predict(input_array)
        return {"raw_prediction": prediction[0], "prediction": str(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prédiction: {str(e)}")