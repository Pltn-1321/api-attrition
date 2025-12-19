"""Tests unitaires pour la configuration de l'application."""

import pytest
import os
import sys
from unittest.mock import patch


@pytest.mark.unit
class TestConfiguration:
    """Tests pour la configuration de l'application."""

    def test_api_url_default(self):
        """Test que API_URL a la valeur par défaut correcte."""
        # Sauvegarder la valeur actuelle
        original_value = os.environ.get("API_URL")

        try:
            # Nettoyer la variable d'environnement
            if "API_URL" in os.environ:
                del os.environ["API_URL"]

            # Retirer config du cache si déjà importé
            if "config" in sys.modules:
                del sys.modules["config"]

            # Importer après avoir nettoyé
            import config

            # Vérifier la valeur par défaut
            assert config.API_URL == "http://localhost:8000"

        finally:
            # Restaurer la valeur originale
            if original_value is not None:
                os.environ["API_URL"] = original_value
            elif "API_URL" in os.environ:
                del os.environ["API_URL"]

            # Nettoyer le cache
            if "config" in sys.modules:
                del sys.modules["config"]

    def test_api_url_from_env(self):
        """Test que API_URL respecte la variable d'environnement."""
        # Sauvegarder la valeur actuelle
        original_value = os.environ.get("API_URL")

        try:
            # Définir une valeur personnalisée
            os.environ["API_URL"] = "https://test-api.com"

            # Retirer config du cache
            if "config" in sys.modules:
                del sys.modules["config"]

            # Importer avec la nouvelle valeur
            import config

            # Vérifier que la variable d'environnement est utilisée
            assert config.API_URL == "https://test-api.com"

        finally:
            # Restaurer la valeur originale
            if original_value is not None:
                os.environ["API_URL"] = original_value
            else:
                del os.environ["API_URL"]

            # Nettoyer le cache
            if "config" in sys.modules:
                del sys.modules["config"]

    def test_api_url_localhost_format(self):
        """Test que l'URL par défaut utilise le bon format localhost."""
        # Sauvegarder
        original_value = os.environ.get("API_URL")

        try:
            if "API_URL" in os.environ:
                del os.environ["API_URL"]

            if "config" in sys.modules:
                del sys.modules["config"]

            import config

            # Vérifier le format
            assert config.API_URL.startswith("http://")
            assert "localhost" in config.API_URL or "127.0.0.1" in config.API_URL
            assert ":8000" in config.API_URL

        finally:
            if original_value is not None:
                os.environ["API_URL"] = original_value
            elif "API_URL" in os.environ:
                del os.environ["API_URL"]

            if "config" in sys.modules:
                del sys.modules["config"]


@pytest.mark.unit
class TestDatabaseConfiguration:
    """Tests pour la configuration de la base de données."""

    def test_db_type_default(self):
        """Test que DB_TYPE a la valeur par défaut correcte."""
        original_value = os.environ.get("DB_TYPE")

        try:
            if "DB_TYPE" in os.environ:
                del os.environ["DB_TYPE"]

            if "database.config" in sys.modules:
                del sys.modules["database.config"]

            from database import config as db_config

            # Par défaut, devrait être sqlite
            assert db_config.DB_TYPE == "sqlite"

        finally:
            if original_value is not None:
                os.environ["DB_TYPE"] = original_value
            elif "DB_TYPE" in os.environ:
                del os.environ["DB_TYPE"]

            if "database.config" in sys.modules:
                del sys.modules["database.config"]

    def test_db_type_postgres(self):
        """Test que DB_TYPE peut être configuré pour PostgreSQL."""
        original_value = os.environ.get("DB_TYPE")

        try:
            os.environ["DB_TYPE"] = "postgres"

            # Nettoyer tous les modules database
            modules_to_delete = [key for key in sys.modules.keys() if key.startswith("database")]
            for module in modules_to_delete:
                del sys.modules[module]

            # Ré-importer avec la nouvelle valeur
            import importlib
            from database import config as db_config

            importlib.reload(db_config)

            assert db_config.DB_TYPE == "postgres"

        finally:
            if original_value is not None:
                os.environ["DB_TYPE"] = original_value
            elif "DB_TYPE" in os.environ:
                del os.environ["DB_TYPE"]

            # Nettoyer le cache
            modules_to_delete = [key for key in sys.modules.keys() if key.startswith("database")]
            for module in modules_to_delete:
                del sys.modules[module]
