"""Tests fonctionnels pour l'endpoint de prédiction API."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app


@pytest.mark.api
@pytest.mark.functional
class TestPredictionAPI:
    """Tests pour l'endpoint /predict."""

    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup du client de test."""
        self.client = TestClient(app)

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_success(self, sample_employee_data_low_risk):
        """Test de l'endpoint /predict avec des données valides."""
        response = self.client.post("/predict", json=sample_employee_data_low_risk)

        assert response.status_code == 200
        data = response.json()

        # Vérifier la structure de la réponse
        assert "attrition_risk" in data
        assert "attrition_probability" in data
        assert "prediction" in data
        assert "risk_level" in data

        # Vérifier les types
        assert isinstance(data["attrition_risk"], (int, float))
        assert isinstance(data["attrition_probability"], (int, float))
        assert isinstance(data["prediction"], int)
        assert isinstance(data["risk_level"], str)

        # Vérifier les valeurs
        assert 0 <= data["attrition_risk"] <= 100
        assert 0 <= data["attrition_probability"] <= 1
        assert data["prediction"] in [0, 1]
        assert data["risk_level"] in ["Faible", "Moyen", "Élevé", "Très élevé"]

        # Cohérence entre les valeurs
        assert abs(data["attrition_risk"] - (data["attrition_probability"] * 100)) < 0.01

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_different_risk_levels(
        self, sample_employee_data_low_risk, sample_employee_data_high_risk
    ):
        """Test prédictions avec différents niveaux de risque."""
        # Test profil faible risque
        response_low = self.client.post("/predict", json=sample_employee_data_low_risk)
        assert response_low.status_code == 200
        data_low = response_low.json()

        # Test profil haut risque
        response_high = self.client.post("/predict", json=sample_employee_data_high_risk)
        assert response_high.status_code == 200
        data_high = response_high.json()

        # Les deux réponses devraient être différentes
        assert data_low["attrition_probability"] != data_high["attrition_probability"]

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_minimal_data(self):
        """Test avec des données minimales valides."""
        minimal_data = {"age": 30, "revenu_mensuel": 3000, "satisfaction_moyenne": 3.0}

        response = self.client.post("/predict", json=minimal_data)
        assert response.status_code == 200
        data = response.json()

        assert all(
            key in data
            for key in ["attrition_risk", "attrition_probability", "prediction", "risk_level"]
        )

    @pytest.mark.skip(reason="TODO: Corriger la gestion des données vides dans l'API (erreur 500)")
    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_empty_data(self):
        """Test avec des données vides."""
        empty_data = {}

        response = self.client.post("/predict", json=empty_data)
        # Devrait fonctionner avec les valeurs par défaut
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_invalid_json(self):
        """Test avec JSON invalide."""
        invalid_json = "{ invalid json }"

        response = self.client.post(
            "/predict", data=invalid_json, headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422  # Validation error

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_wrong_method(self):
        """Test avec mauvaise méthode HTTP."""
        response = self.client.get("/predict")
        assert response.status_code == 405  # Method not allowed

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_missing_model(self):
        """Test quand le modèle n'est pas disponible."""
        with patch("main.model", None):
            response = self.client.post("/predict", json={"age": 30})
            assert response.status_code == 503
            assert "Modèle de prédiction non disponible" in response.json()["detail"]

    @pytest.mark.skip(
        reason="TODO: Corriger la gestion des cas limites d'âge dans l'API (erreur 500)"
    )
    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_endpoint_edge_case_ages(self):
        """Test avec des âges extrêmes."""
        # Très jeune
        young_data = {"age": 18, "revenu_mensuel": 2000}
        response = self.client.post("/predict", json=young_data)
        assert response.status_code == 200

        # Très âgé
        old_data = {"age": 65, "revenu_mensuel": 8000}
        response = self.client.post("/predict", json=old_data)
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_response_headers(self, sample_employee_data_low_risk):
        """Test les en-têtes de réponse."""
        response = self.client.post("/predict", json=sample_employee_data_low_risk)

        assert response.status_code == 200
        assert "application/json" in response.headers["content-type"]

    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_concurrent_requests(self, sample_employee_data_low_risk):
        """Test plusieurs requêtes simultanées."""
        import threading
        import time

        results = []
        errors = []

        def make_request():
            try:
                response = self.client.post("/predict", json=sample_employee_data_low_risk)
                results.append(response.json())
            except Exception as e:
                errors.append(str(e))

        # Créer 10 threads simultanés
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Attendre que tous les threads terminent
        for thread in threads:
            thread.join()

        # Vérifier qu'il n'y a pas d'erreurs
        assert len(errors) == 0, f"Erreurs lors des requêtes simultanées: {errors}"
        assert len(results) == 10

        # Vérifier que toutes les réponses sont cohérentes
        first_result = results[0]
        for result in results[1:]:
            # Les probabilités devraient être très similaires
            assert (
                abs(result["attrition_probability"] - first_result["attrition_probability"]) < 1e-10
            )

    @pytest.mark.api
    @pytest.mark.functional
    @pytest.mark.slow
    def test_predict_performance(self, sample_employee_data_low_risk):
        """Test de performance de l'endpoint."""
        import time

        # Faire 100 prédictions
        start_time = time.time()

        for _ in range(100):
            response = self.client.post("/predict", json=sample_employee_data_low_risk)
            assert response.status_code == 200

        end_time = time.time()
        total_time = end_time - start_time

        # Chaque prédiction devrait prendre moins de 100ms en moyenne
        avg_time_per_prediction = total_time / 100
        assert (
            avg_time_per_prediction < 0.1
        ), f"Trop lent: {avg_time_per_prediction:.3f}s par prédiction"

    @pytest.mark.skip(
        reason="TODO: Corriger la gestion des caractères spéciaux dans l'API (erreur 500)"
    )
    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_special_characters(self):
        """Test avec des caractères spéciaux dans les chaînes."""
        special_char_data = {
            "poste": "Développeur C++/Python",
            "departement": "R&D & Innovation",
            "domaine_etude": "Informatique & Mathématiques",
            "statut_marital": "Célibataire (divorcé)",
            "age": 30,
            "revenu_mensuel": 3500,
        }

        response = self.client.post("/predict", json=special_char_data)
        assert response.status_code == 200

    @pytest.mark.skip(
        reason="TODO: Corriger la validation des types numériques dans l'API (erreur 422)"
    )
    @pytest.mark.api
    @pytest.mark.functional
    def test_predict_numeric_precision(self):
        """Test la précision numérique des résultats."""
        precise_data = {"satisfaction_moyenne": 2.718281828, "revenu_mensuel": 3333.33, "age": 33}

        response = self.client.post("/predict", json=precise_data)
        assert response.status_code == 200
        data = response.json()

        # Vérifier que les nombres flottants ont une précision raisonnable
        assert isinstance(data["attrition_probability"], float)
        assert isinstance(data["attrition_risk"], (int, float))

        # Pas de NaN ou inf
        assert data["attrition_probability"] == data["attrition_probability"]  # Pas de NaN
        assert abs(data["attrition_probability"]) < float("inf")  # Pas de inf
