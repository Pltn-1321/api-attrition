from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from database.config import get_db, engine
from database.models import Employee
from api.schemas import EmployeeResponse, EmployeeListResponse, HealthResponse

app = FastAPI(
    title="ML Attrition API",
    description="API pour la prédiction d'attrition des employés avec Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

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
            "employee_by_id": "/employees/{id}"
        }
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

    return {
        "status": "healthy",
        "database": db_status
    }

@app.get("/employees", response_model=EmployeeListResponse)
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
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

    return {
        "total": total,
        "employees": employees
    }

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un employé spécifique par son ID.

    - **employee_id**: L'identifiant unique de l'employé
    """
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail=f"Employé avec l'ID {employee_id} non trouvé"
        )

    return employee

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)