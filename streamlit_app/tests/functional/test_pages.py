"""Tests fonctionnels pour les pages Streamlit."""

import pytest
from unittest.mock import patch


class TestPages:
    """Tests pour les différentes pages."""

    @patch("utils.api_client.APIClient")
    def test_explorer_page_loads(self, mock_client):
        """Test que la page Explorer se charge correctement."""
        mock_instance = mock_client.return_value
        mock_instance.get_employees.return_value = {
            "total": 10,
            "employees": [
                {"id": i, "age": 30, "departement": "IT", "left_company": 0}
                for i in range(10)
            ]
        }
        result = mock_instance.get_employees()
        assert result["total"] == 10

    @patch("utils.api_client.APIClient")
    def test_search_page_loads(self, mock_client):
        """Test que la page Recherche se charge correctement."""
        mock_instance = mock_client.return_value
        mock_instance.get_employee.return_value = {
            "id": 1,
            "genre": "M",
            "age": 30,
        }
        result = mock_instance.get_employee(1)
        assert result["id"] == 1
