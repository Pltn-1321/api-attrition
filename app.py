"""
Page d'accueil de l'application Streamlit.
Application de prédiction d'attrition des employés.
"""

import streamlit as st
from utils.api_client import APIClient
from utils.ui_components import render_metric_card, show_error, render_footer
from config import APP_TITLE, APP_ICON, APP_LAYOUT, API_URL

# Configuration de la page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded",
)

# Initialisation du client API dans session_state
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()
    st.session_state.api_url = API_URL

# Header
st.title(f"{APP_ICON} API Attrition - Dashboard")
st.markdown(
    "### Bienvenue sur le tableau de bord de prédiction d'attrition des employés"
)

st.markdown("---")

# Section Health Check
st.header("🏥 État de l'API")

col1, col2 = st.columns(2)

with st.spinner("🔄 Connexion à l'API..."):
    try:
        health_data = st.session_state.api_client.health_check()

        with col1:
            status = health_data.get("status", "unknown")
            status_icon = "✅" if status == "healthy" else "❌"
            render_metric_card(
                title="API Status",
                value=status.capitalize(),
                icon=status_icon,
            )

        with col2:
            db_status = health_data.get("database", "unknown")
            db_icon = "✅" if "connected" in db_status else "❌"
            render_metric_card(
                title="Database Status",
                value=db_status.capitalize(),
                icon=db_icon,
            )

        # Si l'API est OK, afficher les statistiques générales
        if status == "healthy":
            st.markdown("---")
            st.header("📊 Statistiques Générales")

            try:
                # Récupérer tous les employés pour les stats
                data = st.session_state.api_client.get_employees(skip=0, limit=100)
                total_employees = data.get("total", 0)
                employees = data.get("employees", [])

                # Calculer des statistiques moyennes
                avg_age = (
                    sum(emp.get("age", 0) for emp in employees) / len(employees)
                    if employees
                    else 0
                )
                avg_satisfaction = (
                    sum(emp.get("satisfaction_moyenne", 0) for emp in employees)
                    / len(employees)
                    if employees
                    else 0
                )
                avg_revenue = (
                    sum(emp.get("revenu_mensuel", 0) for emp in employees)
                    / len(employees)
                    if employees
                    else 0
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    render_metric_card(
                        title="Total Employés",
                        value=total_employees,
                        icon="👥",
                    )

                with col2:
                    render_metric_card(
                        title="Âge Moyen",
                        value=f"{avg_age:.0f} ans",
                        icon="📅",
                    )

                with col3:
                    render_metric_card(
                        title="Satisfaction Moyenne",
                        value=f"{avg_satisfaction:.1f}/4",
                        icon="⭐",
                    )

            except Exception as e:
                show_error(
                    f"Erreur lors de la récupération des statistiques : {str(e)}"
                )

    except Exception as e:
        show_error(f"Impossible de se connecter à l'API : {str(e)}")
        st.info(f"URL de l'API : {API_URL}")

# Instructions
st.markdown("---")
st.header("📖 Comment utiliser cette application")

st.markdown(
    """
Utilisez la barre latérale pour naviguer entre les différentes pages :

- **📊 Explorer** : Parcourez et filtrez la liste complète des employés
- **🔍 Recherche** : Recherchez un employé spécifique par son ID
- **📈 Statistiques** : Visualisez les données avec des graphiques interactifs

Toutes les données proviennent de l'API FastAPI qui est connectée à une base PostgreSQL.
"""
)

# Footer
render_footer()
