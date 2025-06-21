"""
Classification des résultats de football PL 

"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
from datetime import datetime
import os

print("Entraînement classique - English Premier League")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Paramètres
n_estimators = 15
max_depth = 3
test_size = 0.30
random_seed = 42

# 1. charger les données
data_path = "ml/data/English_Premier_League.csv"
df = pd.read_csv(data_path)

# 2. nettoyage minimal
df = df.dropna(subset=["HomeGoals", "AwayGoals", "Result"])

# 3. features - labels
X = df[["HomeGoals", "AwayGoals"]]
y = df["Result"]  # Valeurs: H, D, A

print(f"Nombre de matchs: {len(df)}")
print(f"Exemples de features :\n{X.head()}")
print(f"Classes: {y.unique()}")

# 4. split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=random_seed
)

# 5. entrainement
model = RandomForestClassifier(
    n_estimators=n_estimators, 
    max_depth=max_depth,
    random_state=random_seed
)
model.fit(X_train, y_train)

# 6. evaluation
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Precision: {accuracy:.2%}")

# 7. sauvegarde 
os.makedirs("models", exist_ok=True)
model_filename = f"models/epl_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
with open(model_filename, 'wb') as f:
    pickle.dump(model, f)

print(f"Modele saved : {model_filename}")
