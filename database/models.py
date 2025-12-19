from sqlalchemy import Column, Integer, String, Float, BigInteger
from database.config import Base


class Employee(Base):
    """
    Modèle SQLAlchemy pour la table employees.
    Représente un employé avec toutes ses caractéristiques.
    """

    __tablename__ = "employees"

    # Identifiant
    id = Column(BigInteger, primary_key=True, index=True)

    # Informations personnelles
    genre = Column(String)
    age = Column(BigInteger)
    statut_marital = Column(String)
    ayant_enfants = Column(String)
    distance_domicile_travail = Column(BigInteger)
    niveau_education = Column(BigInteger)

    # Informations professionnelles
    poste = Column(String)
    domaine_etude = Column(String)
    departement = Column(String)
    niveau_hierarchique_poste = Column(BigInteger)

    # Carrière et expérience
    nombre_experiences_precedentes = Column(BigInteger)
    annee_experience_totale = Column(BigInteger)
    annees_dans_l_entreprise = Column(BigInteger)
    annees_dans_le_poste_actuel = Column(BigInteger)
    annees_depuis_la_derniere_promotion = Column(BigInteger)
    annes_sous_responsable_actuel = Column(BigInteger)
    nombre_employee_sous_responsabilite = Column(BigInteger)

    # Conditions de travail
    revenu_mensuel = Column(BigInteger)
    heure_supplementaires = Column(String)
    nombre_heures_travailless = Column(BigInteger)
    distance_categorie = Column(String)
    frequence_deplacement = Column(String)

    # Satisfaction et évaluation
    satisfaction_employee_environnement = Column(BigInteger)
    satisfaction_employee_nature_travail = Column(BigInteger)
    satisfaction_employee_equipe = Column(BigInteger)
    satisfaction_employee_equilibre_pro_perso = Column(BigInteger)
    satisfaction_moyenne = Column(Float)
    note_evaluation_precedente = Column(BigInteger)
    note_evaluation_actuelle = Column(BigInteger)

    # Formation et développement
    nb_formations_suivies = Column(BigInteger)
    nombre_participation_pee = Column(BigInteger)

    # Indicateurs de risque
    parent_burnout = Column(BigInteger)
    sous_paye_niveau_dept = Column(BigInteger)
    augementation_salaire_precedente = Column(BigInteger)

    def __repr__(self):
        return f"<Employee(id={self.id}, nom={self.poste}, departement={self.departement})>"
