from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Déterminer le type de base de données (SQLite par défaut pour HF Spaces)
DB_TYPE = os.getenv("DB_TYPE", "sqlite")

# Configuration selon le type de base de données
if DB_TYPE == "sqlite":
    # SQLite - pour Hugging Face Spaces et développement local
    BASE_DIR = Path(__file__).parent.parent
    SQLITE_DB = BASE_DIR / "database.db"
    DATABASE_URL = f"sqlite:///{SQLITE_DB}"
    # SQLite nécessite check_same_thread=False pour FastAPI
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
    )
else:
    # PostgreSQL - pour environnement Docker local
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://attrition_user:attrition_pass@localhost:5432/attrition_db"
    )
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
