from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
import joblib
import sklearn
import os

from database.config import get_db
from database.models import Employee
from api.schemas import (
    EmployeeResponse,
    EmployeeListResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
)

app = FastAPI(
    title="ML Attrition API",
    description="API pour la prédiction d'attrition des employés avec Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Charger le modèle de machine learning
MODEL_PATH = os.path.join(os.path.dirname(__file__), "data", "export-api", "attrition_model.joblib")

# Version attendue du modèle
EXPECTED_SKLEARN_VERSION = "1.7.1"

model = None
model_error = None

print(f"🔍 Tentative de chargement du modèle ML...")
print(f"   📦 Scikit-learn version: {sklearn.__version__}")

# Vérifier la compatibilité de version avant de charger
if sklearn.__version__ != EXPECTED_SKLEARN_VERSION:
    model_error = f"Version de scikit-learn incompatible. Attendue: {EXPECTED_SKLEARN_VERSION}, installée: {sklearn.__version__}"
    print(f"   ❌ {model_error}")
else:
    print(f"   ✅ Version sklearn compatible: {sklearn.__version__}")
    print(f"   📂 Chemin: {MODEL_PATH}")
    print(f"   📍 Chemin absolu: {os.path.abspath(MODEL_PATH)}")
    print(
        f"   {'✅' if os.path.exists(MODEL_PATH) else '❌'} Fichier existe: {os.path.exists(MODEL_PATH)}"
    )

    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print(f"   ✅ Modèle chargé avec succès")
        except Exception as e:
            model_error = str(e)
            print(f"   ❌ Erreur lors du chargement: {e}")
            print(f"   Type d'erreur: {type(e).__name__}")
    else:
        model_error = f"Fichier non trouvé: {MODEL_PATH}"
        print(f"   ❌ {model_error}")
        print(f"   📁 Contenu du répertoire data/:")
        try:
            data_dir = os.path.join(os.path.dirname(__file__), "data")
            if os.path.exists(data_dir):
                for item in os.listdir(data_dir):
                    print(f"      - {item}")
        except Exception as e:
            print(f"      Erreur listage: {e}")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Page d'accueil de l'API."""
    return {
        "message": "API de prédiction d'attrition des employés",
        "version": "1.0.0",
        "endpoints": {
            "documentation": "/docs",
            "health": "/health",
            "employees": "/employees",
            "employee_by_id": "/employees/{id}",
            "predict_attrition": "/predict",
        },
    }


@app.get("/model-status")
async def model_status():
    """
    Retourne l'état du modèle ML pour diagnostic.
    """
    return {
        "model_loaded": model is not None,
        "model_path": MODEL_PATH,
        "model_path_absolute": os.path.abspath(MODEL_PATH),
        "model_file_exists": os.path.exists(MODEL_PATH),
        "model_error": model_error,
        "model_size_bytes": os.path.getsize(MODEL_PATH) if os.path.exists(MODEL_PATH) else None,
    }


@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Vérifier l'état de l'API et de la connexion à la base de données."""
    try:
        # Tester la connexion à la base de données
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {"status": "healthy", "database": db_status}


@app.get("/employees", response_model=EmployeeListResponse)
async def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer la liste de tous les employés avec pagination.

    - **skip**: Nombre d'employés à ignorer (pour la pagination)
    - **limit**: Nombre maximum d'employés à retourner (max 100)
    """
    if limit > 100:
        limit = 100

    # Compter le total d'employés
    total = db.query(Employee).count()

    # Récupérer les employés avec pagination
    employees = db.query(Employee).offset(skip).limit(limit).all()

    return {"total": total, "employees": employees}


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un employé spécifique par son ID.

    - **employee_id**: L'identifiant unique de l'employé
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if employee is None:
        raise HTTPException(status_code=404, detail=f"Employé avec l'ID {employee_id} non trouvé")

    return employee


def get_risk_level(probability: float) -> str:
    """Déterminer le niveau de risque en fonction de la probabilité."""
    if not isinstance(probability, (int, float)):
        raise TypeError("La probabilité doit être un nombre")
    if probability < 0 or probability > 1:
        raise ValueError("La probabilité doit être entre 0 et 1")

    if probability < 0.3:
        return "Faible"
    elif probability < 0.6:
        return "Moyen"
    elif probability < 0.8:
        return "Élevé"
    else:
        return "Très élevé"


@app.post("/predict", response_model=PredictionResponse)
async def predict_attrition(request: PredictionRequest):
    """
    Prédire le risque d'attrition pour un employé.

    Cette endpoint utilise un modèle de machine learning pour prédire
    la probabilité qu'un employé quitte l'entreprise.
    """
    if model is None:
        detail_message = "Modèle de prédiction non disponible"
        if model_error:
            detail_message += f". Erreur de chargement: {model_error}"
        raise HTTPException(status_code=503, detail=detail_message)

    try:
        # Convertir les données de la requête en DataFrame pandas
        data_dict = request.model_dump(exclude_none=True)

        # Créer un DataFrame avec une seule ligne
        df = pd.DataFrame([data_dict])

        # S'assurer que toutes les colonnes requises par le modèle sont présentes
        required_columns = [
            "genre",
            "statut_marital",
            "heure_supplementaires",
            "ayant_enfants",
            "poste",
            "domaine_etude",
            "distance_categorie",
            "frequence_deplacement",
            "departement",
            "age",
            "revenu_mensuel",
            "nombre_experiences_precedentes",
            "nombre_heures_travailless",
            "annee_experience_totale",
            "annees_dans_l_entreprise",
            "annees_dans_le_poste_actuel",
            "satisfaction_employee_environnement",
            "note_evaluation_precedente",
            "niveau_hierarchique_poste",
            "satisfaction_employee_nature_travail",
            "satisfaction_employee_equipe",
            "satisfaction_employee_equilibre_pro_perso",
            "note_evaluation_actuelle",
            "nombre_participation_pee",
            "nb_formations_suivies",
            "nombre_employee_sous_responsabilite",
            "distance_domicile_travail",
            "niveau_education",
            "annees_depuis_la_derniere_promotion",
            "annes_sous_responsable_actuel",
            "satisfaction_moyenne",
            "parent_burnout",
            "sous_paye_niveau_dept",
            "augementation_salaire_precedente",
        ]

        # Ajouter les colonnes manquantes avec des valeurs par défaut
        for col in required_columns:
            if col not in df.columns:
                df[col] = (
                    0
                    if col
                    in [
                        "age",
                        "revenu_mensuel",
                        "distance_domicile_travail",
                        "niveau_education",
                        "niveau_hierarchique_poste",
                        "nombre_experiences_precedentes",
                        "annee_experience_totale",
                        "annees_dans_l_entreprise",
                        "annees_dans_le_poste_actuel",
                        "annees_depuis_la_derniere_promotion",
                        "annes_sous_responsable_actuel",
                        "nombre_employee_sous_responsabilite",
                        "nombre_heures_travailless",
                        "satisfaction_employee_environnement",
                        "note_evaluation_precedente",
                        "satisfaction_employee_nature_travail",
                        "satisfaction_employee_equipe",
                        "satisfaction_employee_equilibre_pro_perso",
                        "note_evaluation_actuelle",
                        "nombre_participation_pee",
                        "nb_formations_suivies",
                        "parent_burnout",
                        "sous_paye_niveau_dept",
                        "augementation_salaire_precedente",
                    ]
                    else "Inconnu"
                )

        # Réorganiser les colonnes dans le bon ordre
        df = df[required_columns]

        # Faire la prédiction
        prediction_proba = model.predict_proba(df)[:, 1]  # Probabilité de la classe positive
        prediction = model.predict(df)[0]  # Classe prédite (0 ou 1)
        probability = float(prediction_proba[0])

        # Calculer le risque d'attrition (probabilité en pourcentage)
        attrition_risk = probability * 100

        # Déterminer le niveau de risque
        risk_level = get_risk_level(probability)

        return PredictionResponse(
            attrition_risk=round(attrition_risk, 2),
            attrition_probability=round(probability, 4),
            prediction=int(prediction),
            risk_level=risk_level,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
