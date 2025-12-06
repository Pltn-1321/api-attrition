#!/bin/bash

# Détection du répertoire du script et positionnement
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Démarrage de l'application API Attrition..."
echo "📂 Répertoire du projet: $SCRIPT_DIR"
echo ""

# Vérifier que Docker est démarré
if ! docker ps &> /dev/null; then
    echo "❌ Docker n'est pas démarré. Lancez Docker Desktop puis relancez ce script."
    exit 1
fi

# Démarrer PostgreSQL si pas déjà lancé
if ! docker ps | grep attrition_db &> /dev/null; then
    echo "📦 Démarrage de PostgreSQL..."
    docker-compose up -d
    echo "⏳ Attente de PostgreSQL (5s)..."
    sleep 5
fi

echo "✅ PostgreSQL est démarré"
echo ""
echo "🔧 Choisissez ce que vous voulez lancer:"
echo "1) API seulement (FastAPI)"
echo "2) Interface seulement (Streamlit)"
echo "3) Les deux"
echo ""
read -p "Votre choix (1-3): " choice

case $choice in
    1)
        echo "🚀 Lancement de l'API FastAPI..."
        uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ;;
    2)
        echo "🚀 Lancement de Streamlit..."
        cd streamlit_app && uv run streamlit run app.py
        ;;
    3)
        echo "🚀 Lancement de l'API en arrière-plan..."
        uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
        API_PID=$!
        echo "✅ API lancée (PID: $API_PID)"
        sleep 2
        echo "🚀 Lancement de Streamlit..."
        cd streamlit_app && uv run streamlit run app.py
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac
