"""Tests fonctionnels pour la disponibilité de l'API."""

import pytest
import requests
import time
from fastapi.testclient import TestClient
from main import app


@pytest.mark.functional
class TestAPIAvailability:
    """Tests de disponibilité de l'API."""

    def setup_method(self):
        """Configuration pour chaque test."""
        self.client = TestClient(app)

    def test_health_endpoint_exists(self):
        """Test que l'endpoint /health existe."""
        response = self.client.get("/health")
        assert response.status_code == 200

    def test_health_response_structure(self):
        """Test la structure de la réponse du health check."""
        response = self.client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "database" in data
        assert data["status"] in ["healthy", "unhealthy"]

    def test_health_check_is_fast(self):
        """Test que le health check répond rapidement."""
        start_time = time.time()
        response = self.client.get("/health")
        end_time = time.time()

        assert response.status_code == 200
        assert (
            end_time - start_time
        ) < 1.0, "Le health check devrait répondre en moins d'1 seconde"

    def test_api_responds_after_startup(self):
        """Test que l'API répond après un démarrage simulé."""
        # Simuler un délai de démarrage
        time.sleep(0.5)

        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.functional
class TestStreamlitAPIConnection:
    """Tests de connexion entre Streamlit et l'API."""

    def setup_method(self):
        """Configuration pour chaque test."""
        from utils.api_client import APIClient

        self.api_client = APIClient()

    def test_api_client_can_reach_health(self):
        """Test que le client API peut atteindre le endpoint /health."""
        # Vérifier d'abord si l'API est disponible
        try:
            requests.get("http://localhost:8000/health", timeout=1)
            api_running = True
        except Exception:
            api_running = False

        if not api_running:
            pytest.skip("API n'est pas en cours d'exécution (test nécessite serveur actif)")

        # Si l'API tourne, tester la connexion
        health = self.api_client.health_check()
        assert isinstance(health, dict)
        assert "status" in health

    def test_api_client_handles_connection_error(self):
        """Test que le client API gère correctement les erreurs de connexion."""
        from utils.api_client import APIClient

        # Créer un client avec une mauvaise URL
        bad_client = APIClient(base_url="http://localhost:9999")

        # Le client devrait lever une exception lors d'une erreur de connexion
        with pytest.raises((Exception, ConnectionError, requests.exceptions.RequestException)):
            bad_client.health_check()


@pytest.mark.functional
@pytest.mark.slow
class TestDockerConfiguration:
    """Tests de configuration Docker."""

    def test_dockerfile_sets_api_url(self):
        """Test que le Dockerfile configure correctement API_URL."""
        import subprocess

        result = subprocess.run(
            ["grep", "ENV API_URL", "Dockerfile"], capture_output=True, text=True
        )

        # Le Dockerfile devrait contenir ENV API_URL=http://localhost:8000
        assert result.returncode == 0, "Dockerfile devrait contenir ENV API_URL"
        assert (
            "http://localhost:8000" in result.stdout
        ), "API_URL devrait pointer vers localhost:8000"

    def test_dockerfile_sets_db_type(self):
        """Test que le Dockerfile configure correctement DB_TYPE."""
        import subprocess

        result = subprocess.run(
            ["grep", "ENV DB_TYPE", "Dockerfile"], capture_output=True, text=True
        )

        # Le Dockerfile devrait configurer DB_TYPE
        assert result.returncode == 0, "Dockerfile devrait contenir ENV DB_TYPE"
        assert "sqlite" in result.stdout, "DB_TYPE devrait être configuré pour SQLite"
