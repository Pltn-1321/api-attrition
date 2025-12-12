"""
Script de migration des données CSV vers SQLite.
Utilise SQLAlchemy pour créer la base de données et les tables.
"""
import os
import sys
import pandas as pd
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Employee

# Chemins
BASE_DIR = Path(__file__).parent.parent
CSV_FILE = BASE_DIR / "data" / "export-api" / "test_employees.csv"
SQLITE_DB = BASE_DIR / "database.db"


def migrate_to_sqlite():
    """
    Migre les données du CSV vers une base de données SQLite.
    """
    print("🚀 Début de la migration vers SQLite...")

    # 1. Vérifier que le CSV existe
    if not CSV_FILE.exists():
        print(f"❌ Erreur: Fichier CSV introuvable: {CSV_FILE}")
        return False

    print(f"✓ Fichier CSV trouvé: {CSV_FILE}")

    # 2. Lire le CSV
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✓ CSV chargé: {len(df)} employés trouvés")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du CSV: {e}")
        return False

    # 3. Créer la base SQLite
    sqlite_url = f"sqlite:///{SQLITE_DB}"
    print(f"✓ Création de la base SQLite: {SQLITE_DB}")

    try:
        engine = create_engine(sqlite_url, echo=False)

        # Supprimer les tables existantes si présentes
        Base.metadata.drop_all(bind=engine)

        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        print("✓ Tables créées avec succès")

    except Exception as e:
        print(f"❌ Erreur lors de la création de la base: {e}")
        return False

    # 4. Insérer les données
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Ajouter un ID auto-incrémenté si non présent
        if 'id' not in df.columns:
            df.insert(0, 'id', range(1, len(df) + 1))

        # Convertir le DataFrame en objets Employee
        employees = []
        for _, row in df.iterrows():
            employee = Employee(
                id=row.get('id'),
                genre=row.get('genre'),
                age=row.get('age'),
                statut_marital=row.get('statut_marital'),
                ayant_enfants=row.get('ayant_enfants'),
                distance_domicile_travail=row.get('distance_domicile_travail'),
                niveau_education=row.get('niveau_education'),
                poste=row.get('poste'),
                domaine_etude=row.get('domaine_etude'),
                departement=row.get('departement'),
                niveau_hierarchique_poste=row.get('niveau_hierarchique_poste'),
                nombre_experiences_precedentes=row.get('nombre_experiences_precedentes'),
                annee_experience_totale=row.get('annee_experience_totale'),
                annees_dans_l_entreprise=row.get('annees_dans_l_entreprise'),
                annees_dans_le_poste_actuel=row.get('annees_dans_le_poste_actuel'),
                annees_depuis_la_derniere_promotion=row.get('annees_depuis_la_derniere_promotion'),
                annes_sous_responsable_actuel=row.get('annes_sous_responsable_actuel'),
                nombre_employee_sous_responsabilite=row.get('nombre_employee_sous_responsabilite'),
                revenu_mensuel=row.get('revenu_mensuel'),
                heure_supplementaires=row.get('heure_supplementaires'),
                nombre_heures_travailless=row.get('nombre_heures_travailless'),
                distance_categorie=row.get('distance_categorie'),
                frequence_deplacement=row.get('frequence_deplacement'),
                satisfaction_employee_environnement=row.get('satisfaction_employee_environnement'),
                satisfaction_employee_nature_travail=row.get('satisfaction_employee_nature_travail'),
                satisfaction_employee_equipe=row.get('satisfaction_employee_equipe'),
                satisfaction_employee_equilibre_pro_perso=row.get('satisfaction_employee_equilibre_pro_perso'),
                satisfaction_moyenne=row.get('satisfaction_moyenne'),
                note_evaluation_precedente=row.get('note_evaluation_precedente'),
                note_evaluation_actuelle=row.get('note_evaluation_actuelle'),
                nb_formations_suivies=row.get('nb_formations_suivies'),
                nombre_participation_pee=row.get('nombre_participation_pee'),
                parent_burnout=row.get('parent_burnout'),
                sous_paye_niveau_dept=row.get('sous_paye_niveau_dept'),
                augementation_salaire_precedente=row.get('augementation_salaire_precedente')
            )
            employees.append(employee)

        # Insertion en batch
        db.bulk_save_objects(employees)
        db.commit()

        print(f"✓ {len(employees)} employés insérés avec succès")

        # Vérification
        count = db.query(Employee).count()
        print(f"✓ Vérification: {count} employés dans la base")

        db.close()

    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données: {e}")
        import traceback
        traceback.print_exc()
        return False

    print(f"\n✅ Migration terminée avec succès!")
    print(f"📁 Base de données créée: {SQLITE_DB}")
    print(f"📊 Taille du fichier: {SQLITE_DB.stat().st_size / 1024:.2f} KB")

    return True


if __name__ == "__main__":
    success = migrate_to_sqlite()
    sys.exit(0 if success else 1)
