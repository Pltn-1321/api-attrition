"""Configuration centralisée pour l'application Streamlit."""

import os

# URL de l'API (configurable via variable d'environnement pour HF Spaces)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configuration de l'application
APP_TITLE = "API Attrition - Dashboard"
APP_ICON = "📊"
APP_LAYOUT = "wide"

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Couleurs du thème (bleu nuit + corail)
COLORS = {
    "primary": "#FF6B6B",  # Corail
    "secondary": "#1A1A2E",  # Bleu nuit foncé
    "background": "#16213E",  # Bleu nuit
    "text": "#FFFFFF",  # Blanc
    "accent": "#0F3460",  # Bleu nuit clair
}

# Configuration des graphiques
CHART_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
}

# Messages
MESSAGES = {
    "api_error": "❌ Erreur de connexion à l'API",
    "no_data": "ℹ️ Aucune donnée disponible",
    "loading": "⏳ Chargement...",
    "success": "✅ Opération réussie",
}
