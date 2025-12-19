"""Tests fonctionnels pour l'application Streamlit."""

import pytest
from unittest.mock import patch, Mock


@pytest.fixture
def mock_api_client():
    """Mock du client API pour les tests."""
    with patch("utils.api_client.APIClient") as mock:
        instance = mock.return_value
        instance.health_check.return_value = {
            "status": "healthy",
            "database": "connected",
        }
        instance.get_employees.return_value = {
            "total": 294,
            "employees": [{"id": 1, "departement": "IT", "age": 30, "left_company": 0}],
        }
        instance.get_employee.return_value = {
            "id": 1,
            "genre": "M",
            "age": 30,
            "poste": "Developer",
            "departement": "IT",
            "left_company": 0,
        }
        yield instance


class TestStreamlitApp:
    """Tests fonctionnels pour l'application."""

    def test_api_client_health_check(self, mock_api_client):
        """Test que le health check fonctionne."""
        result = mock_api_client.health_check()
        assert result["status"] == "healthy"
        assert result["database"] == "connected"

    def test_get_employees(self, mock_api_client):
        """Test la récupération des employés."""
        result = mock_api_client.get_employees(skip=0, limit=10)
        assert result["total"] == 294
        assert len(result["employees"]) == 1

    def test_get_employee_by_id(self, mock_api_client):
        """Test la récupération d'un employé par ID."""
        result = mock_api_client.get_employee(1)
        assert result["id"] == 1
        assert result["departement"] == "IT"
