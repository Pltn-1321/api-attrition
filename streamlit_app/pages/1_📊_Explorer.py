"""Page Explorer - Liste et filtre des employés."""

import streamlit as st
import pandas as pd
from utils.api_client import APIClient
from utils.ui_components import show_error, show_info
from config import APP_TITLE, APP_ICON, APP_LAYOUT, DEFAULT_PAGE_SIZE

st.set_page_config(
    page_title=f"{APP_TITLE} - Explorer",
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
)

# Initialisation
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

st.title("📊 Explorer les Employés")
st.markdown("Parcourez et filtrez la liste complète des employés de l'entreprise.")

st.markdown("---")

# Sidebar avec filtres
st.sidebar.header("🔧 Filtres")

with st.sidebar:
    # Filtre par département
    departements = st.multiselect(
        "Département",
        options=["Commercial", "Consulting", "Data Science", "RH", "IT"],
        help="Filtrer par département",
    )

    # Filtre par âge
    st.markdown("**Âge**")
    age_min, age_max = st.slider(
        "Plage d'âge",
        min_value=18,
        max_value=70,
        value=(18, 70),
        label_visibility="collapsed",
    )

    # Bouton reset
    if st.button("🔄 Réinitialiser les filtres"):
        st.rerun()

# Récupération des données
try:
    with st.spinner("Chargement des données..."):
        data = st.session_state.api_client.get_employees(skip=0, limit=100)
        employees = data.get("employees", [])

        if not employees:
            show_info("Aucun employé trouvé.")
            st.stop()

        # Conversion en DataFrame
        df = pd.DataFrame(employees)

        # Application des filtres
        filtered_df = df.copy()

        # Filtre département
        if departements:
            filtered_df = filtered_df[filtered_df["departement"].isin(departements)]

        # Filtre âge
        filtered_df = filtered_df[
            (filtered_df["age"] >= age_min) & (filtered_df["age"] <= age_max)
        ]

        # Affichage des résultats
        st.subheader(f"📋 Résultats ({len(filtered_df)} employés)")

        if filtered_df.empty:
            show_info("Aucun employé ne correspond aux filtres sélectionnés.")
        else:
            # Sélection des colonnes à afficher
            display_columns = [
                "id",
                "genre",
                "age",
                "poste",
                "departement",
                "revenu_mensuel",
                "satisfaction_moyenne",
                "annees_dans_l_entreprise",
            ]

            # Préparation du DataFrame pour l'affichage
            display_df = filtered_df[display_columns].copy()

            # Formatage des colonnes
            display_df["revenu_mensuel"] = display_df["revenu_mensuel"].apply(
                lambda x: f"{x:,.0f} €".replace(",", " ")
            )
            display_df["satisfaction_moyenne"] = display_df[
                "satisfaction_moyenne"
            ].apply(lambda x: f"{x:.1f}/4" if pd.notna(x) else "N/A")

            # Renommer les colonnes pour l'affichage
            display_df = display_df.rename(
                columns={
                    "id": "ID",
                    "genre": "Genre",
                    "age": "Âge",
                    "poste": "Poste",
                    "departement": "Département",
                    "revenu_mensuel": "Revenu Mensuel",
                    "satisfaction_moyenne": "Satisfaction",
                    "annees_dans_l_entreprise": "Ancienneté",
                }
            )

            # Affichage du tableau
            st.dataframe(
                display_df,
                use_container_width=True,
                height=500,
            )

            # Statistiques rapides
            st.markdown("---")
            st.subheader("📊 Statistiques sur la sélection")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total", len(filtered_df))

            with col2:
                avg_age = filtered_df["age"].mean()
                st.metric("Âge moyen", f"{avg_age:.0f} ans")

            with col3:
                avg_satisfaction = filtered_df["satisfaction_moyenne"].mean()
                st.metric("Satisfaction moyenne", f"{avg_satisfaction:.1f}/4")

            with col4:
                avg_anciennete = filtered_df["annees_dans_l_entreprise"].mean()
                st.metric("Ancienneté moyenne", f"{avg_anciennete:.1f} ans")

            # Export CSV
            st.markdown("---")
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger les résultats (CSV)",
                data=csv,
                file_name="employees_filtered.csv",
                mime="text/csv",
            )

except Exception as e:
    show_error(f"Erreur lors du chargement des données : {str(e)}")
