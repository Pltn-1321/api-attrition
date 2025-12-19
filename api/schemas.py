from pydantic import BaseModel, ConfigDict
from typing import Optional

class EmployeeBase(BaseModel):
    """Schéma de base pour un employé."""
    genre: Optional[str] = None
    age: Optional[int] = None
    statut_marital: Optional[str] = None
    ayant_enfants: Optional[str] = None
    distance_domicile_travail: Optional[int] = None
    niveau_education: Optional[int] = None
    poste: Optional[str] = None
    domaine_etude: Optional[str] = None
    departement: Optional[str] = None
    niveau_hierarchique_poste: Optional[int] = None
    nombre_experiences_precedentes: Optional[int] = None
    annee_experience_totale: Optional[int] = None
    annees_dans_l_entreprise: Optional[int] = None
    annees_dans_le_poste_actuel: Optional[int] = None
    annees_depuis_la_derniere_promotion: Optional[int] = None
    annes_sous_responsable_actuel: Optional[int] = None
    nombre_employee_sous_responsabilite: Optional[int] = None
    revenu_mensuel: Optional[int] = None
    heure_supplementaires: Optional[str] = None
    nombre_heures_travailless: Optional[int] = None
    distance_categorie: Optional[str] = None
    frequence_deplacement: Optional[str] = None
    satisfaction_employee_environnement: Optional[int] = None
    satisfaction_employee_nature_travail: Optional[int] = None
    satisfaction_employee_equipe: Optional[int] = None
    satisfaction_employee_equilibre_pro_perso: Optional[int] = None
    satisfaction_moyenne: Optional[float] = None
    note_evaluation_precedente: Optional[int] = None
    note_evaluation_actuelle: Optional[int] = None
    nb_formations_suivies: Optional[int] = None
    nombre_participation_pee: Optional[int] = None
    parent_burnout: Optional[int] = None
    sous_paye_niveau_dept: Optional[int] = None
    augementation_salaire_precedente: Optional[int] = None

class EmployeeResponse(EmployeeBase):
    """Schéma de réponse pour un employé (inclut l'ID)."""
    id: int

    model_config = ConfigDict(from_attributes=True)

class EmployeeListResponse(BaseModel):
    """Schéma de réponse pour une liste d'employés."""
    total: int
    employees: list[EmployeeResponse]

class PredictionRequest(BaseModel):
    """Schéma pour les données de prédiction d'attrition."""
    genre: Optional[str] = None
    age: Optional[int] = None
    statut_marital: Optional[str] = None
    ayant_enfants: Optional[str] = None
    distance_domicile_travail: Optional[int] = None
    niveau_education: Optional[int] = None
    poste: Optional[str] = None
    domaine_etude: Optional[str] = None
    departement: Optional[str] = None
    niveau_hierarchique_poste: Optional[int] = None
    nombre_experiences_precedentes: Optional[int] = None
    annee_experience_totale: Optional[int] = None
    annees_dans_l_entreprise: Optional[int] = None
    annees_dans_le_poste_actuel: Optional[int] = None
    annees_depuis_la_derniere_promotion: Optional[int] = None
    annes_sous_responsable_actuel: Optional[int] = None
    nombre_employee_sous_responsabilite: Optional[int] = None
    revenu_mensuel: Optional[int] = None
    heure_supplementaires: Optional[str] = None
    nombre_heures_travailless: Optional[int] = None
    distance_categorie: Optional[str] = None
    frequence_deplacement: Optional[str] = None
    satisfaction_employee_environnement: Optional[int] = None
    satisfaction_employee_nature_travail: Optional[int] = None
    satisfaction_employee_equipe: Optional[int] = None
    satisfaction_employee_equilibre_pro_perso: Optional[int] = None
    satisfaction_moyenne: Optional[float] = None
    note_evaluation_precedente: Optional[int] = None
    note_evaluation_actuelle: Optional[int] = None
    nb_formations_suivies: Optional[int] = None
    nombre_participation_pee: Optional[int] = None
    parent_burnout: Optional[int] = None
    sous_paye_niveau_dept: Optional[int] = None
    augementation_salaire_precedente: Optional[int] = None

class PredictionResponse(BaseModel):
    """Schéma de réponse pour la prédiction d'attrition."""
    attrition_risk: float
    attrition_probability: float
    prediction: int
    risk_level: str

class HealthResponse(BaseModel):
    """Schéma de réponse pour le health check."""
    status: str
    database: str
