"""Composants UI réutilisables pour l'interface Streamlit."""

import streamlit as st
from typing import Dict, Any, Optional
from config import COLORS


def render_metric_card(title: str, value: Any, delta: Optional[str] = None, icon: str = "📊"):
    """
    Affiche une carte de métrique stylisée.

    Args:
        title: Titre de la métrique
        value: Valeur de la métrique
        delta: Variation (optionnel)
        icon: Icône emoji
    """
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['accent']} 0%, {COLORS['secondary']} 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid {COLORS['primary']};
            margin: 10px 0;
        ">
            <p style="color: {COLORS['text']}; font-size: 14px; margin: 0;">
                {icon} {title}
            </p>
            <p style="color: {COLORS['primary']}; font-size: 32px; font-weight: bold; margin: 5px 0;">
                {value}
            </p>
            {f'<p style="color: {COLORS["text"]}; font-size: 12px; margin: 0;">{delta}</p>' if delta else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_employee_card(employee: Dict[str, Any]):
    """
    Affiche une carte détaillée pour un employé.

    Args:
        employee: Dictionnaire contenant les données de l'employé
    """
    st.markdown(
        f"""
        <div style="
            background: {COLORS['secondary']};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid {COLORS['accent']};
            margin: 10px 0;
        ">
            <h3 style="color: {COLORS['text']}; margin: 0;">
                ID #{employee.get('id', 'N/A')} - {employee.get('poste', 'N/A')}
            </h3>
            <hr style="border-color: {COLORS['accent']};">
            <div style="color: {COLORS['text']};">
                <p><strong>Département:</strong> {employee.get('departement', 'N/A')}</p>
                <p><strong>Âge:</strong> {employee.get('age', 'N/A')} ans</p>
                <p><strong>Genre:</strong> {employee.get('genre', 'N/A')}</p>
                <p><strong>Revenu mensuel:</strong> {employee.get('revenu_mensuel', 'N/A')} €</p>
                <p><strong>Satisfaction moyenne:</strong> {employee.get('satisfaction_moyenne', 'N/A')}/4</p>
                <p><strong>Années dans l'entreprise:</strong> {employee.get('annees_dans_l_entreprise', 'N/A')}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_error(message: str):
    """
    Affiche un message d'erreur stylisé.

    Args:
        message: Message d'erreur
    """
    st.error(f"❌ {message}")


def show_success(message: str):
    """
    Affiche un message de succès stylisé.

    Args:
        message: Message de succès
    """
    st.success(f"✅ {message}")


def show_info(message: str):
    """
    Affiche un message d'information stylisé.

    Args:
        message: Message d'information
    """
    st.info(f"ℹ️ {message}")


def render_footer():
    """Affiche le footer de l'application."""
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align: center; color: {COLORS['text']}; padding: 20px;">
            <p>API Attrition Dashboard - Développé avec ❤️ et Streamlit</p>
            <p style="font-size: 12px;">URL API: {st.session_state.get('api_url', 'Non configurée')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_card(prediction_data: Dict[str, Any]):
    """
    Affiche le résultat de prédiction de manière simple avec composants Streamlit natifs.

    Args:
        prediction_data: Résultats de la prédiction contenant attrition_risk,
                        attrition_probability, prediction, risk_level
    """
    risk_level = prediction_data.get("risk_level", "Inconnu")
    risk_percentage = prediction_data.get("attrition_risk", 0)
    probability = prediction_data.get("attrition_probability", 0)
    prediction = prediction_data.get("prediction", 0)

    # Icône selon le niveau de risque
    risk_icons = {"Faible": "😊", "Moyen": "😐", "Élevé": "😟", "Très élevé": "😱", "Inconnu": "❓"}
    icon = risk_icons.get(risk_level, "❓")

    prediction_text = "Risque élevé de départ" if prediction == 1 else "Risque faible de départ"

    # Affichage simple avec composants natifs Streamlit
    st.subheader(f"{icon} Résultat de la prédiction d'attrition")

    # Métriques principales
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Risque d'attrition", f"{risk_percentage}%")
    with col2:
        st.metric("Niveau de risque", risk_level)

    # Informations détaillées
    st.write(f"**Prédiction:** {prediction_text}")
    st.write(f"**Probabilité:** {probability:.4f}")


def render_risk_gauge(risk_percentage: float, risk_level: str):
    """
    Affiche une barre de progression simple pour le risque.

    Args:
        risk_percentage: Pourcentage de risque (0-100)
        risk_level: Niveau de risque textuel
    """
    st.write("**Indicateur de risque**")
    # Convertir le pourcentage en valeur 0-1 pour st.progress
    progress_value = max(0.0, min(1.0, risk_percentage / 100.0))
    st.progress(progress_value)
    st.caption(f"{risk_percentage}% - {risk_level}")


def render_employee_search():
    """
    Affiche une interface de recherche d'employé avec options ID et nom.

    Returns:
        tuple: (search_type, search_value)
    """
    col1, col2 = st.columns([1, 2])

    with col1:
        search_type = st.selectbox(
            "Type de recherche", ["ID Employé", "Nom/Poste/Département"], key="search_type"
        )

    with col2:
        if search_type == "ID Employé":
            search_value = st.number_input(
                "ID de l'employé", min_value=1, step=1, key="employee_id_search"
            )
        else:
            search_value = st.text_input(
                "Rechercher par nom, poste ou département",
                placeholder="Ex: Tech Lead, Consulting, Homme...",
                key="employee_name_search",
            )

    return search_type, search_value


def render_loading_prediction():
    """Affiche un indicateur de chargement stylisé pour la prédiction."""
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            margin: 20px 0;
        ">
            <div style="font-size: 24px; margin-bottom: 10px;">🤖</div>
            <h3>Prédiction en cours...</h3>
            <p>Analyse des données de l'employé avec le modèle de machine learning</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
