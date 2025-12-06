"""Composants UI réutilisables pour l'interface Streamlit."""

import streamlit as st
from typing import Dict, Any, Optional
from config import COLORS


def render_metric_card(
    title: str, value: Any, delta: Optional[str] = None, icon: str = "📊"
):
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
