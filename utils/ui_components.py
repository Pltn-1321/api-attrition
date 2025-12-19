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
    Affiche une carte de résultat de prédiction avec indicateur de risque visuel.

    Args:
        prediction_data: Résultats de la prédiction contenant attrition_risk,
                        attrition_probability, prediction, risk_level
    """
    risk_level = prediction_data.get("risk_level", "Inconnu")
    risk_percentage = prediction_data.get("attrition_risk", 0)
    probability = prediction_data.get("attrition_probability", 0)
    prediction = prediction_data.get("prediction", 0)

    # Couleurs selon le niveau de risque
    risk_colors = {
        "Faible": {"bg": "#d4edda", "border": "#28a745", "text": "#155724"},
        "Moyen": {"bg": "#fff3cd", "border": "#ffc107", "text": "#856404"},
        "Élevé": {"bg": "#f8d7da", "border": "#dc3545", "text": "#721c24"},
        "Très élevé": {"bg": "#f5c6cb", "border": "#bd2130", "text": "#721c24"},
        "Inconnu": {"bg": "#e2e3e5", "border": "#6c757d", "text": "#383d41"},
    }

    colors = risk_colors.get(risk_level, risk_colors["Inconnu"])

    # Icône selon le niveau de risque
    risk_icons = {"Faible": "😊", "Moyen": "😐", "Élevé": "😟", "Très élevé": "😱", "Inconnu": "❓"}

    icon = risk_icons.get(risk_level, "❓")

    prediction_text = "Risque élevé de départ" if prediction == 1 else "Risque faible de départ"

    html_content = f"""
    <div style="
        background: {colors['bg']};
        padding: 25px;
        border-radius: 15px;
        border: 3px solid {colors['border']};
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: {colors['text']}; margin: 0;">
                {icon} Résultat de la prédiction d'attrition
            </h2>
        </div>

        <div style="display: flex; justify-content: space-around; align-items: center; margin: 20px 0;">
            <div style="text-align: center;">
                <div style="font-size: 48px; font-weight: bold; color: {colors['border']};">
                    {risk_percentage}%
                </div>
                <div style="font-size: 16px; color: {colors['text']}; margin-top: 5px;">
                    Risque d'attrition
                </div>
            </div>

            <div style="text-align: center;">
                <div style="
                    background: {colors['border']};
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 18px;
                    display: inline-block;
                ">
                    {risk_level}
                </div>
            </div>
        </div>

        <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.5); border-radius: 8px;">
            <p style="color: {colors['text']}; margin: 5px 0;">
                <strong>Probabilité:</strong> {probability:.4f}
            </p>
            <p style="color: {colors['text']}; margin: 5px 0;">
                <strong>Prédiction:</strong> {prediction_text}
            </p>
        </div>
    </div>
    """

    st.markdown(html_content, unsafe_allow_html=True)


def render_risk_gauge(risk_percentage: float, risk_level: str):
    """
    Affiche une jauge de risque visuelle.

    Args:
        risk_percentage: Pourcentage de risque (0-100)
        risk_level: Niveau de risque textuel
    """
    # Déterminer la couleur et la position selon le risque
    if risk_percentage < 30:
        color = "#28a745"  # vert
        position = risk_percentage
    elif risk_percentage < 60:
        color = "#ffc107"  # jaune
        position = risk_percentage
    elif risk_percentage < 80:
        color = "#fd7e14"  # orange
        position = risk_percentage
    else:
        color = "#dc3545"  # rouge
        position = risk_percentage

    # S'assurer que la position est dans les bornes 0-100%
    position = max(0, min(100, float(risk_percentage)))

    html_gauge = f"""
    <div style="margin: 20px 0; text-align: center;">
        <h4 style="margin-bottom: 15px;">Indicateur de risque</h4>
        <div style="
            width: 100%;
            height: 30px;
            background: linear-gradient(to right, #28a745, #ffc107, #fd7e14, #dc3545);
            border-radius: 15px;
            position: relative;
            margin: 10px 0;
        ">
            <div style="
                position: absolute;
                top: -5px;
                left: {position}%;
                transform: translateX(-50%);
                width: 40px;
                height: 40px;
                background: {color};
                border: 3px solid white;
                border-radius: 50%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            "></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 5px;">
            <span style="font-size: 12px; color: {COLORS['text']};">0%</span>
            <span style="font-size: 12px; color: {COLORS['text']};">25%</span>
            <span style="font-size: 12px; color: {COLORS['text']};">50%</span>
            <span style="font-size: 12px; color: {COLORS['text']};">75%</span>
            <span style="font-size: 12px; color: {COLORS['text']};">100%</span>
        </div>
    </div>
    """

    st.markdown(html_gauge, unsafe_allow_html=True)


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
