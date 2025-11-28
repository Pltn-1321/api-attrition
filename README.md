# API Attrition

API FastAPI pour la prédiction d'attrition des employés avec machine learning.

## Structure du Projet

```
api-attrition/
|-- api
├── data/                   # Données d'entraînement et de test
│   └── dataset_employe.csv # Dataset des employés
|--models
|--scripts
|--test
├── main.py                 # Application FastAPI principale
├── requirements.txt        # Dépendances Python
└── README.md              # Documentation du projet
```

## Branches Git

- `main` (production)
- `dev` (développement - branche de base)

## Technologies

- **FastAPI**: Framework API Python
- **SQLAlchemy**: ORM pour base de données
- **PostgreSQL**: Base de données
- **Scikit-learn**: Machine Learning
- **Pydantic**: Validation des données
- **Uvicorn**: Serveur ASGI

## Installation

```bash
# Cloner le dépôt
git clone git@github.com:Pltn-1321/api-attrition.git
cd api-attrition

# Installer les dépendances
pip install -r requirements.txt
```

## Lancement de l'API

```bash
# Développement (avec rechargement automatique)
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Endpoints

## Tests

```bash
pytest
```
