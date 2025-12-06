from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de connexion PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://attrition_user:attrition_pass@localhost:5432/attrition_db"
)

# Créer le moteur SQLAlchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session locale
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Fonction de dépendance pour obtenir la session de base de données
def get_db():
    """
    Générateur de session de base de données pour FastAPI.
    Utilisation : db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
