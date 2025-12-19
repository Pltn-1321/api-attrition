"""
Page de diagnostic pour l'application API Attrition.
Permet de débuguer les problèmes sur HF Spaces.
"""

import streamlit as st
import requests
import json
import time
from utils.api_client import APIClient
from config import API_URL

# Configuration de la page
st.set_page_config(
    page_title="Diagnostic API",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Titre
st.title("🔧 Page de Diagnostic")
st.markdown("---")

st.header("🏥 État de l'API et Diagnostic")

# Initialiser le client API si nécessaire
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()
    st.session_state.api_url = API_URL

col1, col2, col3 = st.columns(3)

# Test 1: Health Check
with col1:
    st.subheader("📡 API Health")
    try:
        health_response = requests.get(f"{API_URL}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ API disponible")
            st.json(health_data)
        else:
            st.error(f"❌ Erreur {health_response.status_code}")
            st.text(health_response.text)
    except Exception as e:
        st.error(f"❌ Connexion impossible")
        st.code(str(e))

# Test 2: Model Status
with col2:
    st.subheader("🤖 Modèle ML")
    try:
        model_response = requests.get(f"{API_URL}/model-status", timeout=10)
        if model_response.status_code == 200:
            model_data = model_response.json()
            if model_data.get("model_loaded"):
                st.success("✅ Modèle chargé")
            else:
                st.error("❌ Modèle non chargé")

            st.json(model_data)
        else:
            st.error(f"❌ Erreur {model_response.status_code}")
            st.text(model_response.text)
    except Exception as e:
        st.error(f"❌ Impossible de vérifier le modèle")
        st.code(str(e))

# Test 3: Test de prédiction
with col3:
    st.subheader("🔮 Test Prédiction")

    test_data = {
        "genre": "Homme",
        "age": 30,
        "revenu_mensuel": 5000,
        "poste": "Technicien",
        "departement": "Informatique"
    }

    try:
        pred_response = requests.post(f"{API_URL}/predict",
                                    json=test_data,
                                    timeout=15)
        if pred_response.status_code == 200:
            pred_data = pred_response.json()
            st.success("✅ Prédiction fonctionnelle")
            st.json(pred_data)
        else:
            st.error(f"❌ Erreur {pred_response.status_code}")
            st.text(pred_response.text)
    except Exception as e:
        st.error(f"❌ Prédiction impossible")
        st.code(str(e))

st.markdown("---")

# Section d'informations système
st.header("🖥️ Informations Système")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("📡 Configuration API")
    st.code(f"URL API: {API_URL}")
    st.code(f"Timeout: {st.session_state.api_client.timeout}s")

    # Test de connectivité
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}/", timeout=5)
        latency = (time.time() - start_time) * 1000
        st.success(f"✅ Latence: {latency:.0f}ms")
    except:
        st.error("❌ Pas de connectivité")

with col_info2:
    st.subheader("🔍 Logs de debug")

    # Bouton pour rafraîchir
    if st.button("🔄 Rafraîchir tout"):
        st.rerun()

    # Afficher l'URL de l'API
    st.info(f"URL configurée: `{API_URL}`")
    st.info("Si vous voyez des erreurs, vérifiez les logs du conteneur HF Spaces")

st.markdown("---")

# Actions de diagnostic
st.header("🛠️ Actions de Diagnostic")

col_action1, col_action2, col_action3 = st.columns(3)

with col_action1:
    if st.button("🏥 Vérifier Health", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/health", timeout=10)
            st.json(response.json())
        except Exception as e:
            st.error(f"Erreur: {e}")

with col_action2:
    if st.button("🤖 Vérifier Modèle", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/model-status", timeout=10)
            st.json(response.json())
        except Exception as e:
            st.error(f"Erreur: {e}")

with col_action3:
    if st.button("🧪 Test Endpoint Racine", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/", timeout=10)
            st.json(response.json())
        except Exception as e:
            st.error(f"Erreur: {e}")

st.markdown("---")

# Guide de dépannage
st.header("📚 Guide de Dépannage")

with st.expander("🔍 Comment utiliser cette page de diagnostic"):
    st.markdown("""
    ### Étapes de diagnostic:

    1. **Vérifier API Health**: L'API doit répondre au `/health`
    2. **Vérifier Modèle ML**: Le modèle doit être chargé (`model_loaded: true`)
    3. **Test de prédiction**: La prédiction doit fonctionner avec des données test

    ### Si problème de modèle:
    - Erreur 503 = modèle non chargé
    - Vérifiez que `data/export-api/attrition_model.joblib` existe
    - Vérifiez la version scikit-learn (doit être 1.7.1)

    ### Si problème de connectivité:
    - Erreur timeout = API pas démarrée
    - Attendez 30-60s après déploiement
    - Vérifiez les logs du conteneur HF Spaces
    """)

with st.expander("📋 Logs HF Spaces"):
    st.markdown("""
    ### Pour voir les logs sur Hugging Face Spaces:

    1. Allez sur votre espace HF Spaces
    2. Cliquez sur l'onglet "Files"
    3. Cliquez sur "Settings" → "Logs"
    4. Cherchez ces messages:
       - `🚀 INITIALISATION API FASTAPI`
       - `🔍 DIAGNOSTIC MODÈLE ML`
       - `✅ Modèle chargé avec succès!`

    ### Erreurs communes dans les logs:
    - `ModuleNotFoundError`: dépendance manquante
    - `FileNotFoundError`: fichier modèle manquant
    - `Version incompatible`: sklearn version incorrecte
    """)

# Footer
st.markdown("---")
st.markdown("🔧 Page de diagnostic - utilisez cette page pour identifier les problèmes sur HF Spaces")