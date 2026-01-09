"""Page Statistiques - Visualisations et analyses des données."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.api_client import APIClient
from utils.ui_components import show_error
from config import APP_TITLE, APP_ICON, APP_LAYOUT, COLORS

st.set_page_config(
    page_title=f"{APP_TITLE} - Statistiques",
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
)

# Initialisation
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

st.title("📈 Statistiques et Visualisations")
st.markdown("Analysez les données des employés avec des graphiques interactifs.")

st.markdown("---")

# Récupération des données
try:
    with st.spinner("Chargement des données..."):
        data = st.session_state.api_client.get_employees(skip=0, limit=1000)
        total_employees = data.get("total", 0)
        employees = data.get("employees", [])

        if not employees:
            st.info("Aucune donnée disponible.")
            st.stop()

        df = pd.DataFrame(employees)

        # 1. Métriques générales
        st.subheader("📊 Vue d'Ensemble")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Employés", total_employees)

        with col2:
            avg_age = df["age"].mean()
            st.metric("Âge Moyen", f"{avg_age:.0f} ans")

        with col3:
            avg_satisfaction = df["satisfaction_moyenne"].mean()
            st.metric("Satisfaction Moyenne", f"{avg_satisfaction:.1f}/4")

        with col4:
            avg_revenue = df["revenu_mensuel"].mean()
            st.metric("Revenu Moyen", f"{avg_revenue:,.0f} €".replace(",", " "))

        st.markdown("---")

        # 2. Graphiques
        tab1, tab2, tab3, tab4 = st.tabs(
            ["📊 Départements", "👥 Démographie", "💰 Rémunération", "😊 Satisfaction"]
        )

        with tab1:
            st.subheader("Répartition par Département")

            # Graphique en barres : Employés par département
            dept_counts = df["departement"].value_counts().reset_index()
            dept_counts.columns = ["departement", "count"]

            fig1 = px.bar(
                dept_counts,
                x="departement",
                y="count",
                title="Nombre d'Employés par Département",
                labels={"departement": "Département", "count": "Nombre d'employés"},
                color="count",
                color_continuous_scale=["#1A1A2E", "#FF6B6B"],
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)

            # Revenu moyen par département
            dept_salary = df.groupby("departement")["revenu_mensuel"].mean().reset_index()

            fig2 = px.bar(
                dept_salary,
                x="departement",
                y="revenu_mensuel",
                title="Revenu Moyen par Département (€)",
                labels={
                    "departement": "Département",
                    "revenu_mensuel": "Revenu moyen (€)",
                },
                color="revenu_mensuel",
                color_continuous_scale=["#1A1A2E", "#FF6B6B"],
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            st.subheader("Analyse Démographique")

            col1, col2 = st.columns(2)

            with col1:
                # Distribution par âge
                fig3 = px.histogram(
                    df,
                    x="age",
                    nbins=20,
                    title="Distribution par Âge",
                    labels={"age": "Âge", "count": "Nombre d'employés"},
                    color_discrete_sequence=[COLORS["primary"]],
                )
                st.plotly_chart(fig3, use_container_width=True)

            with col2:
                # Distribution par genre
                genre_counts = df["genre"].value_counts().reset_index()
                genre_counts.columns = ["genre", "count"]

                fig4 = px.pie(
                    genre_counts,
                    names="genre",
                    values="count",
                    title="Répartition par Genre",
                    color_discrete_sequence=[COLORS["primary"], COLORS["accent"]],
                )
                st.plotly_chart(fig4, use_container_width=True)

        with tab3:
            st.subheader("Analyse de Rémunération")

            col1, col2 = st.columns(2)

            with col1:
                # Distribution des revenus
                fig6 = px.box(
                    df,
                    y="revenu_mensuel",
                    title="Distribution des Revenus Mensuels",
                    labels={"revenu_mensuel": "Revenu mensuel (€)"},
                    color_discrete_sequence=[COLORS["primary"]],
                )
                st.plotly_chart(fig6, use_container_width=True)

            with col2:
                # Revenu moyen par département
                dept_salary = df.groupby("departement")["revenu_mensuel"].mean().reset_index()

                fig7 = px.bar(
                    dept_salary,
                    x="departement",
                    y="revenu_mensuel",
                    title="Revenu Moyen par Département",
                    labels={
                        "departement": "Département",
                        "revenu_mensuel": "Revenu moyen (€)",
                    },
                    color="revenu_mensuel",
                    color_continuous_scale=["#1A1A2E", "#FF6B6B"],
                )
                st.plotly_chart(fig7, use_container_width=True)

            # Scatter : Revenu vs Années d'expérience
            fig8 = px.scatter(
                df,
                x="annee_experience_totale",
                y="revenu_mensuel",
                color="departement",
                title="Revenu vs Expérience par Département",
                labels={
                    "annee_experience_totale": "Années d'expérience",
                    "revenu_mensuel": "Revenu mensuel (€)",
                    "departement": "Département",
                },
            )
            st.plotly_chart(fig8, use_container_width=True)

        with tab4:
            st.subheader("Analyse de Satisfaction")

            # Satisfaction moyenne par département
            dept_satisfaction = (
                df.groupby("departement")["satisfaction_moyenne"].mean().reset_index()
            )

            fig9 = px.bar(
                dept_satisfaction,
                x="departement",
                y="satisfaction_moyenne",
                title="Satisfaction Moyenne par Département",
                labels={
                    "departement": "Département",
                    "satisfaction_moyenne": "Satisfaction moyenne",
                },
                color="satisfaction_moyenne",
                color_continuous_scale=["#FF6B6B", "#4ECDC4"],
            )
            fig9.add_hline(y=2.5, line_dash="dash", line_color="white", annotation_text="Moyenne")
            st.plotly_chart(fig9, use_container_width=True)

            # Répartition de la satisfaction
            satisfaction_distribution = (
                df["satisfaction_moyenne"].value_counts().sort_index().reset_index()
            )
            satisfaction_distribution.columns = ["satisfaction", "count"]

            fig10 = px.bar(
                satisfaction_distribution,
                x="satisfaction",
                y="count",
                title="Distribution de la Satisfaction",
                labels={
                    "satisfaction": "Niveau de satisfaction",
                    "count": "Nombre d'employés",
                },
                color="satisfaction",
                color_continuous_scale=["#FF6B6B", "#4ECDC4"],
            )
            st.plotly_chart(fig10, use_container_width=True)

except Exception as e:
    show_error(f"Erreur lors du chargement des statistiques : {str(e)}")
