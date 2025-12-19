"""Configuration pytest avec fixtures partagées pour les tests."""

import pytest
import joblib
import pandas as pd
import os
from typing import Dict, Any, List


@pytest.fixture
def sample_employee_data_low_risk() -> Dict[str, Any]:
    """Données d'employé avec faible risque d'attrition."""
    return {
        "genre": "F",
        "age": 35,
        "statut_marital": "Marié(e)",
        "ayant_enfants": "Oui",
        "distance_domicile_travail": 5,
        "niveau_education": 3,
        "poste": "Tech Lead",
        "domaine_etude": "Infra & Cloud",
        "departement": "Consulting",
        "niveau_hierarchique_poste": 3,
        "nombre_experiences_precedentes": 2,
        "annee_experience_totale": 10,
        "annees_dans_l_entreprise": 5,
        "annees_dans_le_poste_actuel": 2,
        "annees_depuis_la_derniere_promotion": 1,
        "annes_sous_responsable_actuel": 1,
        "nombre_employee_sous_responsabilite": 4,
        "revenu_mensuel": 5500,
        "heure_supplementaires": "Non",
        "nombre_heures_travailless": 40,
        "distance_categorie": "< 10 km",
        "frequence_deplacement": "Aucun",
        "satisfaction_employee_environnement": 4,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 4,
        "satisfaction_moyenne": 4.0,
        "note_evaluation_precedente": 4,
        "note_evaluation_actuelle": 4,
        "nb_formations_suivies": 5,
        "nombre_participation_pee": 3,
        "parent_burnout": 0,
        "sous_paye_niveau_dept": 0,
        "augementation_salaire_precedente": 15,
    }


@pytest.fixture
def sample_employee_data_high_risk() -> Dict[str, Any]:
    """Données d'employé avec haut risque d'attrition."""
    return {
        "genre": "M",
        "age": 28,
        "statut_marital": "Célibataire",
        "ayant_enfants": "Non",
        "distance_domicile_travail": 30,
        "niveau_education": 2,
        "poste": "Consultant",
        "domaine_etude": "Marketing",
        "departement": "Commercial",
        "niveau_hierarchique_poste": 1,
        "nombre_experiences_precedentes": 0,
        "annee_experience_totale": 2,
        "annees_dans_l_entreprise": 0,
        "annees_dans_le_poste_actuel": 0,
        "annees_depuis_la_derniere_promotion": 0,
        "annes_sous_responsable_actuel": 0,
        "nombre_employee_sous_responsabilite": 0,
        "revenu_mensuel": 2200,
        "heure_supplementaires": "Oui",
        "nombre_heures_travailless": 55,
        "distance_categorie": "20-30 km",
        "frequence_deplacement": "Frequent",
        "satisfaction_employee_environnement": 1,
        "satisfaction_employee_nature_travail": 1,
        "satisfaction_employee_equipe": 2,
        "satisfaction_employee_equilibre_pro_perso": 1,
        "satisfaction_moyenne": 1.25,
        "note_evaluation_precedente": 2,
        "note_evaluation_actuelle": 2,
        "nb_formations_suivies": 0,
        "nombre_participation_pee": 0,
        "parent_burnout": 4,
        "sous_paye_niveau_dept": 1,
        "augementation_salaire_precedente": 3,
    }


@pytest.fixture
def sample_employee_data_medium_risk() -> Dict[str, Any]:
    """Données d'employé avec risque moyen d'attrition."""
    return {
        "genre": "F",
        "age": 32,
        "statut_marital": "Marié(e)",
        "ayant_enfants": "Oui",
        "distance_domicile_travail": 15,
        "niveau_education": 3,
        "poste": "Senior Manager",
        "domaine_etude": "Transformation Digitale",
        "departement": "Consulting",
        "niveau_hierarchique_poste": 2,
        "nombre_experiences_precedentes": 1,
        "annee_experience_totale": 8,
        "annees_dans_l_entreprise": 3,
        "annees_dans_le_poste_actuel": 1,
        "annees_depuis_la_derniere_promotion": 2,
        "annes_sous_responsable_actuel": 2,
        "nombre_employee_sous_responsabilite": 2,
        "revenu_mensuel": 3800,
        "heure_supplementaires": "Non",
        "nombre_heures_travailless": 42,
        "distance_categorie": "10-20 km",
        "frequence_deplacement": "Occasionnel",
        "satisfaction_employee_environnement": 3,
        "satisfaction_employee_nature_travail": 3,
        "satisfaction_employee_equipe": 3,
        "satisfaction_employee_equilibre_pro_perso": 2,
        "satisfaction_moyenne": 2.75,
        "note_evaluation_precedente": 3,
        "note_evaluation_actuelle": 3,
        "nb_formations_suivies": 2,
        "nombre_participation_pee": 1,
        "parent_burnout": 2,
        "sous_paye_niveau_dept": 1,
        "augementation_salaire_precedente": 8,
    }


@pytest.fixture
def prediction_response_low_risk() -> Dict[str, Any]:
    """Réponse de prédiction pour faible risque."""
    return {
        "attrition_risk": 11.48,
        "attrition_probability": 0.1148,
        "prediction": 0,
        "risk_level": "Faible",
    }


@pytest.fixture
def prediction_response_high_risk() -> Dict[str, Any]:
    """Réponse de prédiction pour haut risque."""
    return {
        "attrition_risk": 89.73,
        "attrition_probability": 0.8973,
        "prediction": 1,
        "risk_level": "Très élevé",
    }


@pytest.fixture
def ml_model():
    """Charge le modèle ML pour les tests."""
    model_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "export-api", "attrition_model.joblib"
    )

    # Si le modèle n'existe pas, créer un mock
    if not os.path.exists(model_path):
        pytest.skip("Modèle ML non trouvé - tests ignorés")

    model = joblib.load(model_path)
    return model


@pytest.fixture
def mock_api_client():
    """Mock du client API pour les tests."""
    from unittest.mock import MagicMock

    mock_client = MagicMock()

    # Configurer les réponses par défaut
    mock_client.health_check.return_value = {"status": "healthy", "database": "connected"}
    mock_client.get_employee.return_value = {"id": 1, "poste": "Test Employee"}

    return mock_client


@pytest.fixture
def invalid_prediction_data():
    """Données invalides pour tester la gestion d'erreurs."""
    return {
        # Manque des champs requis
        "age": 25,
        # Autres champs manquants...
    }


@pytest.fixture
def edge_case_employee_data():
    """Données d'employé avec cas limites."""
    return {
        "genre": None,  # Valeur nulle
        "age": 0,  # Âge limite
        "revenu_mensuel": 0,  # Salaire nul
        "satisfaction_moyenne": 5.0,  # Au-delà de l'échelle
        "parent_burnout": 10,  # Valeur extrême
    }


@pytest.fixture
def list_employees_data():
    """Liste d'employés pour les tests de recherche."""
    return [
        {
            "id": 1,
            "poste": "Tech Lead",
            "departement": "Consulting",
            "domaine_etude": "Infra & Cloud",
            "age": 35,
        },
        {
            "id": 2,
            "poste": "Consultant",
            "departement": "Commercial",
            "domaine_etude": "Marketing",
            "age": 28,
        },
        {
            "id": 3,
            "poste": "Senior Manager",
            "departement": "Consulting",
            "domaine_etude": "Transformation Digitale",
            "age": 32,
        },
    ]


@pytest.fixture
def temp_directory(tmp_path):
    """Fixture pour les tests avec fichiers temporaires."""
    return tmp_path


@pytest.fixture
def mock_streamlit():
    """Mock des fonctions Streamlit pour les tests."""
    from unittest.mock import patch

    with (
        patch("streamlit.markdown") as mock_markdown,
        patch("streamlit.success") as mock_success,
        patch("streamlit.error") as mock_error,
        patch("streamlit.info") as mock_info,
    ):

        yield {
            "markdown": mock_markdown,
            "success": mock_success,
            "error": mock_error,
            "info": mock_info,
        }
