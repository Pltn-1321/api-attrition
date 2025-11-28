# ML Attrition Deployment

Projet de machine learning pour la prédiction d'attrition client avec API FastAPI et déploiement.

## Structure du Projet

```
ml-attrition-deploy/
├── api/                    # Code FastAPI
├── models/                 # Modèle ML pré-entraîné
├── database/              # Scripts PostgreSQL
├── tests/                 # Tests Pytest
├── .github/
│   └── workflows/         # CI/CD (GitHub Actions)
├── requirements.txt
├── README.md
├── .gitignore
└── main.py
```

## Lancement de l'API

```bash
uvicorn main:app --reload
```

L'API sera disponible sur http://localhost:8000

## Tests

```bash
pytest
```
