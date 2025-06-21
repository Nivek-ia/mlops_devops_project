#!/bin/bash
set -e

echo "=== Installation des dépendances Python ==="

# Fonction pour installer requirements si le fichier existe
install_requirements() {
  local req_path=$1
  if [ -f "$req_path" ]; then
    echo "Installation des dépendances depuis $req_path"
    pip install -r "$req_path"
  else
    echo "Pas de requirements trouvé à $req_path"
  fi
}

# Installer requirements dans l'ordre souhaité
install_requirements "requirements.txt"
install_requirements "app/requirements.txt"
install_requirements "epl_model/requirements.txt"

echo ""
echo "=== Création et activation de l'environnement conda (optionnel) ==="
ENV_NAME="mlops_env"

# Vérifie si conda existe
if command -v conda &> /dev/null; then
  if conda env list | grep -q "$ENV_NAME"; then
    echo "Environnement conda $ENV_NAME déjà existant, activation..."
  else
    echo "Création de l'environnement conda $ENV_NAME"
    conda env create -f epl_model/conda.yaml -n "$ENV_NAME"
  fi
  # Activation
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate "$ENV_NAME"
else
  echo "Conda non trouvé, passe à l'étape suivante..."
fi

echo ""
echo "=== Entraînement du modèle et export en .pkl ==="
python ml/projects/save_load_model.py

if [ -f "app/model.pkl" ]; then
  echo " Modèle .pkl généré avec succès dans app/model.pkl"
else
  echo " Erreur : modèle .pkl non trouvé. Vérifiez ml/projects/save_load_model.py"
  exit 1
fi

echo ""
echo "=== Infrastructure avec Terraform ==="
cd infrastructure/terraform

terraform init
terraform apply -auto-approve

cd ../../

echo ""
echo "===  Déploiement avec Ansible ==="
ansible-playbook ansible/playbook_api.yml -i ansible/inventory.ini

echo ""
echo "===  L’API est maintenant déployée ! ==="

# Personnaliser ici selon l'adresse IP retournée par Terraform/Ansible
API_URL="http://localhost:8000"

echo ""
echo "===================== Accès API ML ====================="
echo " Endpoint de l'API       : $API_URL"
echo "Interface Swagger (POST): $API_URL/docs"
echo ""
echo " Tester /predict en cliquant sur 'Try it out', puis envoyer un JSON"
echo "Exemple :"
echo '{
  "feature1": 2,
  "feature2": 4
}'
echo "============================================================"
