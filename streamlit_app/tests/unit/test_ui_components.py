"""Tests unitaires pour les composants UI."""

import pytest
from utils.ui_components import render_status_badge


class TestUIComponents:
    """Tests pour les composants UI."""

    def test_render_status_badge_active(self):
        """Test le badge pour un employé actif."""
        badge = render_status_badge(0)
        assert "Actif" in badge
        assert "#4ECDC4" in badge

    def test_render_status_badge_left(self):
        """Test le badge pour un employé parti."""
        badge = render_status_badge(1)
        assert "A quitté" in badge
        assert "#FF6B6B" in badge
