"""Tests unitaires pour le modèle ML et la logique de prédiction."""

import pytest
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from main import get_risk_level


@pytest.mark.ml
class TestMLModel:
    """Tests pour le modèle de machine learning."""

    def test_model_loading(self, ml_model):
        """Test que le modèle se charge correctement."""
        assert ml_model is not None
        assert hasattr(ml_model, "predict")
        assert hasattr(ml_model, "predict_proba")
        assert hasattr(ml_model, "feature_names_in_")

    def test_model_prediction_structure(self, ml_model, sample_employee_data_low_risk):
        """Test que la prédiction retourne la bonne structure."""
        # Convertir en DataFrame
        df = pd.DataFrame([sample_employee_data_low_risk])

        # S'assurer que toutes les colonnes requises sont présentes
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

        # Réorganiser les colonnes
        df = df[required_columns]

        # Tester la prédiction
        prediction = ml_model.predict(df)
        prediction_proba = ml_model.predict_proba(df)

        assert len(prediction) == 1
        assert prediction[0] in [0, 1]  # Classification binaire
        assert prediction_proba.shape == (1, 2)  # Probabilités pour 2 classes
        assert np.isclose(np.sum(prediction_proba[0]), 1.0)  # Probabilités somment à 1

    def test_low_risk_prediction(self, ml_model, sample_employee_data_low_risk):
        """Test prédiction pour un profil à faible risque."""
        df = pd.DataFrame([sample_employee_data_low_risk])

        # Ajouter colonnes manquantes
        required_columns = ml_model.feature_names_in_.tolist()
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

        df = df[required_columns]

        prediction = ml_model.predict(df)[0]
        prediction_proba = ml_model.predict_proba(df)[0, 1]

        # Pour un profil à faible risque, on s'attend à une prédiction de 0
        assert prediction == 0
        assert prediction_proba < 0.5

    def test_high_risk_prediction(self, ml_model, sample_employee_data_high_risk):
        """Test prédiction pour un profil à haut risque."""
        df = pd.DataFrame([sample_employee_data_high_risk])

        # Ajouter colonnes manquantes
        required_columns = ml_model.feature_names_in_.tolist()
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

        df = df[required_columns]

        prediction_proba = ml_model.predict_proba(df)[0, 1]

        # Pour un profil à haut risque, on s'attend à une probabilité élevée
        # Note: ce test peut échouer selon le modèle réel, c'est pour illustrer
        assert prediction_proba > 0.5

    def test_edge_cases(self, ml_model, edge_case_employee_data):
        """Test avec des cas limites."""
        df = pd.DataFrame([edge_case_employee_data])

        # Ajouter colonnes manquantes
        required_columns = ml_model.feature_names_in_.tolist()
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

        df = df[required_columns]

        # Le modèle devrait gérer les valeurs extrêmes sans erreur
        prediction = ml_model.predict(df)
        prediction_proba = ml_model.predict_proba(df)

        assert len(prediction) == 1
        assert prediction[0] in [0, 1]
        assert np.isclose(np.sum(prediction_proba[0]), 1.0)

    def test_multiple_predictions(
        self, ml_model, sample_employee_data_low_risk, sample_employee_data_high_risk
    ):
        """Test avec plusieurs prédictions en même temps."""
        employees_data = [sample_employee_data_low_risk, sample_employee_data_high_risk]
        df = pd.DataFrame(employees_data)

        # Ajouter colonnes manquantes
        required_columns = ml_model.feature_names_in_.tolist()
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

        df = df[required_columns]

        predictions = ml_model.predict(df)
        prediction_probas = ml_model.predict_proba(df)

        assert len(predictions) == 2
        assert all(pred in [0, 1] for pred in predictions)
        assert prediction_probas.shape == (2, 2)


@pytest.mark.unit
class TestRiskLevelCalculation:
    """Tests pour la fonction de calcul de niveau de risque."""

    @pytest.mark.parametrize(
        "probability,expected_level",
        [
            (0.1, "Faible"),
            (0.2, "Faible"),
            (0.29, "Faible"),
            (0.3, "Moyen"),
            (0.5, "Moyen"),
            (0.59, "Moyen"),
            (0.6, "Élevé"),
            (0.7, "Élevé"),
            (0.79, "Élevé"),
            (0.8, "Très élevé"),
            (0.9, "Très élevé"),
            (1.0, "Très élevé"),
            (0.0, "Faible"),
        ],
    )
    def test_get_risk_level_boundaries(self, probability, expected_level):
        """Test les niveaux de risque aux limites."""
        assert get_risk_level(probability) == expected_level

    def test_get_risk_level_invalid_input(self):
        """Test avec des entrées invalides."""
        # Test avec None
        with pytest.raises(TypeError):
            get_risk_level(None)

        # Test avec chaîne de caractères
        with pytest.raises(TypeError):
            get_risk_level("0.5")

        # Test avec nombres négatifs
        with pytest.raises(ValueError):
            get_risk_level(-0.1)

        # Test avec nombres > 1
        with pytest.raises(ValueError):
            get_risk_level(1.1)


@pytest.mark.unit
class TestModelIntegration:
    """Tests d'intégration pour le modèle."""

    def test_prediction_consistency(self, ml_model, sample_employee_data_medium_risk):
        """Test que les prédictions sont cohérentes."""
        df = pd.DataFrame([sample_employee_data_medium_risk])

        # Ajouter colonnes manquantes
        required_columns = ml_model.feature_names_in_.tolist()
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

        df = df[required_columns]

        # Faire plusieurs prédictions identiques
        prediction1 = ml_model.predict(df)[0]
        prediction2 = ml_model.predict(df)[0]

        # Les prédictions devraient être identiques
        assert prediction1 == prediction2

        # Les probabilités devraient être très proches
        proba1 = ml_model.predict_proba(df)[0, 1]
        proba2 = ml_model.predict_proba(df)[0, 1]
        assert abs(proba1 - proba2) < 1e-10
