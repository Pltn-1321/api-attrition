"""Tests unitaires pour le client API."""

import pytest
from unittest.mock import Mock, patch
from utils.api_client import APIClient


@pytest.fixture
def api_client():
    """Fixture pour créer un client API de test."""
    return APIClient(base_url="http://test-api:8000")


@pytest.fixture
def mock_response():
    """Fixture pour simuler une réponse HTTP."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"status": "healthy"}
    mock.raise_for_status = Mock()
    return mock


class TestAPIClient:
    """Tests pour la classe APIClient."""

    def test_init(self, api_client):
        """Test l'initialisation du client."""
        assert api_client.base_url == "http://test-api:8000"
        assert api_client.timeout == 10

    @patch("requests.request")
    def test_health_check_success(self, mock_request, api_client, mock_response):
        """Test le health check avec succès."""
        mock_request.return_value = mock_response
        result = api_client.health_check()

        assert result == {"status": "healthy"}
        mock_request.assert_called_once()

    @patch("requests.request")
    def test_health_check_failure(self, mock_request, api_client):
        """Test le health check avec échec."""
        import requests

        mock_request.side_effect = requests.exceptions.RequestException(
            "Connection error"
        )

        with pytest.raises(Exception) as exc_info:
            api_client.health_check()

        assert "Erreur API : Connection error" in str(exc_info.value)

    @patch("requests.request")
    def test_get_employees(self, mock_request, api_client):
        """Test la récupération des employés."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "total": 294,
            "employees": [{"id": 1, "name": "Test"}],
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        result = api_client.get_employees(skip=0, limit=10)

        assert result["total"] == 294
        assert len(result["employees"]) == 1
        mock_request.assert_called_once()

    @patch("requests.request")
    def test_get_employee(self, mock_request, api_client):
        """Test la récupération d'un employé spécifique."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "Test Employee"}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        result = api_client.get_employee(1)

        assert result["id"] == 1
        assert result["name"] == "Test Employee"

    def test_filter_employees(self, api_client):
        """Test le filtrage des employés."""
        mock_employees = [
            {"id": 1, "departement": "IT", "age": 30},
            {"id": 2, "departement": "HR", "age": 40},
            {"id": 3, "departement": "IT", "age": 25},
        ]

        with patch.object(
            api_client, "get_employees", return_value={"employees": mock_employees}
        ):
            # Filtre par département
            result = api_client.filter_employees(departement="IT")
            assert len(result) == 2

            # Filtre par âge
            result = api_client.filter_employees(age_min=30)
            assert len(result) == 2
