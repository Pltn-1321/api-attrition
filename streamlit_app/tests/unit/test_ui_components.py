"""Tests unitaires pour les composants UI."""

import pytest
from utils.ui_components import render_metric_card, render_employee_card


class TestUIComponents:
    """Tests pour les composants UI."""

    def test_render_metric_card(self):
        """Test la création d'une carte de métrique."""
        # Test basique - vérifie que la fonction ne plante pas
        render_metric_card("Test", "100", icon="📊")
        assert True

    def test_render_employee_card(self):
        """Test la création d'une carte employé."""
        employee = {
            "id": 1,
            "poste": "Data Scientist",
            "departement": "Data Science",
            "age": 30,
            "genre": "M",
            "revenu_mensuel": 5000,
            "satisfaction_moyenne": 3.5,
            "annees_dans_l_entreprise": 3,
        }
        # Test basique - vérifie que la fonction ne plante pas
        render_employee_card(employee)
        assert True
