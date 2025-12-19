"""Page Recherche - Recherche d'un employé par ID."""

import streamlit as st
from utils.api_client import APIClient
from utils.ui_components import render_employee_card, show_error, show_info
from config import APP_TITLE, APP_ICON, APP_LAYOUT

st.set_page_config(
    page_title=f"{APP_TITLE} - Recherche",
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
)

# Initialisation
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

st.title("🔍 Recherche d'Employé")
st.markdown("Recherchez un employé spécifique par son identifiant unique.")

st.markdown("---")

# Input pour l'ID
col1, col2 = st.columns([3, 1])

with col1:
    employee_id = st.number_input(
        "ID de l'employé",
        min_value=1,
        max_value=1000,
        value=1,
        step=1,
        help="Entrez l'ID de l'employé à rechercher",
    )

with col2:
    search_button = st.button("🔎 Rechercher", use_container_width=True, type="primary")

# Recherche
if search_button or employee_id:
    try:
        with st.spinner("Recherche en cours..."):
            employee = st.session_state.api_client.get_employee(employee_id)

            if employee:
                st.success(f"✅ Employé #{employee_id} trouvé !")

                # Affichage de la carte employé
                render_employee_card(employee)

                # Détails supplémentaires
                st.markdown("---")
                st.subheader("📋 Informations Détaillées")

                # Onglets pour organiser les informations
                tab1, tab2, tab3, tab4 = st.tabs(
                    [
                        "👤 Personnel",
                        "💼 Professionnel",
                        "📈 Carrière",
                        "😊 Satisfaction",
                    ]
                )

                with tab1:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Genre", employee.get("genre", "N/A"))
                        st.metric("Âge", employee.get("age", "N/A"))
                        st.metric("Statut Marital", employee.get("statut_marital", "N/A"))
                    with col2:
                        st.metric("Enfants", employee.get("ayant_enfants", "N/A"))
                        st.metric(
                            "Distance Domicile",
                            f"{employee.get('distance_domicile_travail', 'N/A')} km",
                        )
                        st.metric("Niveau Éducation", employee.get("niveau_education", "N/A"))

                with tab2:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Poste", employee.get("poste", "N/A"))
                        st.metric("Département", employee.get("departement", "N/A"))
                        st.metric("Domaine d'étude", employee.get("domaine_etude", "N/A"))
                    with col2:
                        st.metric(
                            "Revenu Mensuel",
                            f"{employee.get('revenu_mensuel', 0):,.0f} €",
                        )
                        st.metric(
                            "Heures Supplémentaires",
                            employee.get("heure_supplementaires", "N/A"),
                        )
                        st.metric(
                            "Niveau Hiérarchique",
                            employee.get("niveau_hierarchique_poste", "N/A"),
                        )

                with tab3:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Années d'Expérience",
                            employee.get("annee_experience_totale", "N/A"),
                        )
                        st.metric(
                            "Années dans l'Entreprise",
                            employee.get("annees_dans_l_entreprise", "N/A"),
                        )
                        st.metric(
                            "Années au Poste Actuel",
                            employee.get("annees_dans_le_poste_actuel", "N/A"),
                        )
                    with col2:
                        st.metric(
                            "Expériences Précédentes",
                            employee.get("nombre_experiences_precedentes", "N/A"),
                        )
                        st.metric(
                            "Formations Suivies",
                            employee.get("nb_formations_suivies", "N/A"),
                        )
                        st.metric(
                            "Dernière Promotion",
                            f"{employee.get('annees_depuis_la_derniere_promotion', 'N/A')} ans",
                        )

                with tab4:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Satisfaction Environnement",
                            f"{employee.get('satisfaction_employee_environnement', 'N/A')}/4",
                        )
                        st.metric(
                            "Satisfaction Travail",
                            f"{employee.get('satisfaction_employee_nature_travail', 'N/A')}/4",
                        )
                    with col2:
                        st.metric(
                            "Satisfaction Équipe",
                            f"{employee.get('satisfaction_employee_equipe', 'N/A')}/4",
                        )
                        st.metric(
                            "Équilibre Vie Pro/Perso",
                            f"{employee.get('satisfaction_employee_equilibre_pro_perso', 'N/A')}/4",
                        )

                    st.markdown("---")
                    satisfaction_moy = employee.get("satisfaction_moyenne", 0)
                    st.metric(
                        "Satisfaction Moyenne",
                        f"{satisfaction_moy:.2f}/4",
                        delta=(
                            f"{((satisfaction_moy - 2.5) / 2.5 * 100):.0f}% vs moyenne"
                            if satisfaction_moy
                            else None
                        ),
                    )

                # Indicateur de risque
                st.markdown("---")
                st.subheader("⚠️ Indicateurs de Risque")

                risk_col1, risk_col2 = st.columns(2)

                with risk_col1:
                    burnout = employee.get("parent_burnout", 0)
                    if burnout == 1:
                        st.error("🔴 Burnout Parental Détecté")
                    else:
                        st.success("🟢 Pas de Burnout Parental")

                with risk_col2:
                    sous_paye = employee.get("sous_paye_niveau_dept", 0)
                    if sous_paye == 1:
                        st.warning("🟠 Sous-payé par rapport au département")
                    else:
                        st.success("🟢 Salaire aligné")

            else:
                show_info(f"Aucun employé trouvé avec l'ID {employee_id}")

    except Exception as e:
        if "404" in str(e) or "non trouvé" in str(e):
            show_error(f"Employé #{employee_id} non trouvé.")
        else:
            show_error(f"Erreur lors de la recherche : {str(e)}")
