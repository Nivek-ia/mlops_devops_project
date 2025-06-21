# MLOps & DevOps – EPL Match Prediction API

Ce projet combine les pratiques **MLOps** (modélisation, traçabilité, packaging, API FastAPI, MLflow) et **DevOps** (infrastructure as code avec Terraform, déploiement via Ansible, Docker) pour prédire les résultats de matchs de Premier League.

---

## Structure du projet

```
mlops_devops_project/
├── app/                  # Code FastAPI pour exposer l'API de prédiction
├── docker/               # Dockerfile pour l'API
├── epl_model/            # Modèle ML pré-entraîné
├── ml/                   # Scripts de traitement, entraînement et MLflow
├── infrastructure/
│   └── terraform/        # Provisioning AWS EC2 avec Terraform
├── ansible/              # Déploiement de l’API avec Ansible
├── model_registry/       # (Prévu pour usage futur)
├── launch.sh             # Script d'exécution tout-en-un
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

---

## Prérequis

- Python 3.10+
- Git
- Terraform
- Ansible
- Docker (installé sur la VM cible, pas nécessaire localement)
- Un compte AWS avec des credentials AMI valides

---

## Étape 1 — Configuration initiale

### 1.1. Cloner le projet

```bash
git clone https://github.com/ton-utilisateur/mlops_devops_project.git
cd mlops_devops_project
```

Ouvrez Docker

### 1.2. Configurer les credentials AWS

Dans le fichier `~/.aws/credentials` (Linux/macOS) ou `%USERPROFILE%\.aws\credentials` (Windows), ajouter :

```
[awslearnerlab]
aws_access_key_id = VOTRE_ACCESS_KEY
aws_secret_access_key = VOTRE_SECRET_KEY
aws_session_token= #à copier via vos code aws
 
```

---

## Étape 2 — Provisionner une machine EC2

Mettez vous dans la racine du projet, lancez chmod +x launch.sh puis ensuite ./launch.sh 
Faire un yes si demandé

A noter : que le ./launch.sh installe automatiquement les librairies nécessaires via les requirements.txt

IMPORTANT : Notez les IPs publiques générées à la fin 

## Étape 3 — Modifier l’inventaire Ansible

Dans `ansible/inventory.ini` :

```ini
[api_servers]
XX.XX.XX ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem
 
[training_servers]
XX.XXX.XXX ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem
 
#changer les XX par les IP reçu par terraform ou tofu un pour api_servers et l'autre pour le test ML

Remplacez `<XX.XX>` par les IP de votre EC2.

```

## Étape 4 — Script automatisé

Relancer le code dans la racine ./launch.sh

```bash
chmod +x launch.sh
./launch.sh
```

Ce script :

- Lance Terraform
- Met à jour les IP dans `inventory.ini`
- Exécute le déploiement Ansible

---
## Étape 5 — Tester l’API FastAPI déployée

Une fois le déploiement terminé, vous pouvez tester l’API localement sur Swagger UI :

Ouvre http://localhost:8000/docs

Puis envoie la requête suivante sur le endpoint /predict :

```json
{
  "feature1": 5,
  "feature2": 0
}
```
Réponse :

```json
{ "prediction": H }
```

---

## Modèle utilisé

- Algorithme : `RandomForestClassifier`
- Tracking : `MLflow` local
- Métrique principale : `Accuracy`
- Endpoint : `/predict`

---

## Contact

- Nizar Alioua – Kevin Christyras
- Projet réalisé dans le cadre du module MLOps/DevOps

---


