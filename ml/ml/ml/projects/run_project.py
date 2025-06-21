"""
Demonstration MLflow Project - Projet EPL
"""
import subprocess
import sys
import os

print("Démonstration MLflow Project - EPL")

print("\nLancement avec les parametres par défaut...")
# Run 1 avec n_estimators=10, max_depth=3

# lancer le script avec les parametres par défaut
cmd1 = [sys.executable, "ml/projects/train_project.py", "--n_estimators", "10", "--max_depth", "3"]
result1 = subprocess.run(cmd1, capture_output=True, text=True)

if result1.returncode == 0:
    print("Experience 1 terminee avec succes")
else:
    print(f"Erreur dans l'experience 1: {result1.stderr}")

print("\nLancement avec paramètres personnalisés...")
# Run 2 avec n_estimators=30, max_depth=7

print("   Équivalent à: mlflow run . -P n_estimators=30 -P max_depth=7")

# Lancer avec des parametres diff
cmd2 = [sys.executable, "ml/projects/train_project.py", "--n_estimators", "30", "--max_depth", "7"]
result2 = subprocess.run(cmd2, capture_output=True, text=True)

if result2.returncode == 0:
    print("Experience 2 terminee avec succes")
else:
    print(f"Erreur dans l'experience 2: {result2.stderr}")

print("\nTest avec autres parametres...")
# Run 3 avec n_estimators=50, max_depth=12

print("   n_estimators=50, max_depth=12")

cmd3 = [sys.executable, "ml/projects/train_project.py", "--n_estimators", "50", "--max_depth", "12"]
result3 = subprocess.run(cmd3, capture_output=True, text=True)

if result3.returncode == 0:
    print("Experience 3 terminee avec succes")
else:
    print(f"Erreur dans l'experience 3: {result3.stderr}")
