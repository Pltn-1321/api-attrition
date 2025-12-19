"""Page de prédiction d'attrition des employés."""

import streamlit as st
from utils.ui_components import (
    render_metric_card,
    render_employee_card,
    render_prediction_card,
    render_risk_gauge,
    render_employee_search,
    render_loading_prediction,
    show_error,
    show_success,
)
import time


def render_prediction_results(prediction_data: dict, employee_data: dict):
    """
    Affiche les résultats complets de la prédiction avec analyses.

    Args:
        prediction_data: Résultats de la prédiction
        employee_data: Données de l'employé
    """
    # Carte principale de prédiction
    render_prediction_card(prediction_data)

    # Jauge de risque
    render_risk_gauge(
        prediction_data.get("attrition_risk", 0), prediction_data.get("risk_level", "Inconnu")
    )

    # Métriques clés
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card("Âge", f"{employee_data.get('age', 'N/A')} ans", icon="👤")

    with col2:
        render_metric_card(
            "Satisfaction moyenne",
            f"{employee_data.get('satisfaction_moyenne', 'N/A')}/4",
            icon="😊",
        )

    with col3:
        render_metric_card(
            "Années dans l'entreprise",
            f"{employee_data.get('annees_dans_l_entreprise', 'N/A')}",
            icon="🏢",
        )

    with col4:
        render_metric_card(
            "Revenu mensuel", f"{employee_data.get('revenu_mensuel', 'N/A')}€", icon="💰"
        )

    # Facteurs influençant la prédiction
    with st.expander("📊 Analyse des facteurs de risque", expanded=False):
        render_risk_factors_analysis(employee_data, prediction_data)

    # Recommandations
    with st.expander("💡 Recommandations", expanded=False):
        render_recommendations(employee_data, prediction_data)


def get_risk_factors_intelligent(employee_data: dict, prediction_data: dict):
    """
    Analyse intelligente des facteurs de risque avec pondération contextuelle.

    Args:
        employee_data: Données de l'employé
        prediction_data: Résultats de la prédiction

    Returns:
        Liste de facteurs de risque avec poids et contexte
    """
    risk_factors = []

    # Facteurs de satisfaction (poids élevé)
    satisfaction = employee_data.get("satisfaction_moyenne", 4)
    if satisfaction < 2.0:
        risk_factors.append(
            {
                "icon": "🚨",
                "title": "Satisfaction très faible",
                "description": f"Satisfaction critique: {satisfaction}/4",
                "weight": 0.25,
                "category": "satisfaction",
            }
        )
    elif satisfaction < 2.5:
        risk_factors.append(
            {
                "icon": "⚠️",
                "title": "Satisfaction faible",
                "description": f"Satisfaction moyenne: {satisfaction}/4",
                "weight": 0.15,
                "category": "satisfaction",
            }
        )

    # Facteurs de charge de travail
    hours = employee_data.get("nombre_heures_travailless", 40)
    if hours > 50:
        risk_factors.append(
            {
                "icon": "⏰",
                "title": "Surcharge de travail",
                "description": f"{hours}h/semaine (charge excessive)",
                "weight": 0.20,
                "category": "workload",
            }
        )
    elif hours > 45:
        risk_factors.append(
            {
                "icon": "⚖️",
                "title": "Charge de travail élevée",
                "description": f"{hours}h/semaine",
                "weight": 0.10,
                "category": "workload",
            }
        )

    # Facteurs d'ancienneté (contextuels)
    years_company = employee_data.get("annees_dans_l_entreprise", 0)
    age = employee_data.get("age", 30)

    if years_company < 1:
        risk_factors.append(
            {
                "icon": "🆕",
                "title": "Nouvel employé",
                "description": "Moins d'1 an dans l'entreprise (période critique)",
                "weight": 0.18,
                "category": "tenure",
            }
        )
    elif years_company < 2 and age < 30:
        risk_factors.append(
            {
                "icon": "👶",
                "title": "Jeune talent",
                "description": f"{age} ans, {years_company} an(s) d'ancienneté (risque de départ)",
                "weight": 0.12,
                "category": "tenure",
            }
        )

    # Facteurs de carrière
    last_promotion = employee_data.get("annees_depuis_la_derniere_promotion", 0)
    niveau_hierarchique = employee_data.get("niveau_hierarchique_poste", 1)

    if last_promotion > 3 and niveau_hierarchique < 3:
        risk_factors.append(
            {
                "icon": "📈",
                "title": "Stagnation professionnelle",
                "description": f"Dernière promotion il y a {last_promotion} ans, niveau {niveau_hierarchique}",
                "weight": 0.15,
                "category": "career",
            }
        )
    elif last_promotion > 2:
        risk_factors.append(
            {
                "icon": "⏳",
                "title": "Carrière en pause",
                "description": f"Dernière promotion il y a {last_promotion} ans",
                "weight": 0.08,
                "category": "career",
            }
        )

    # Facteurs de rémunération (contextuels)
    revenu = employee_data.get("revenu_mensuel", 0)
    if revenu > 0:
        # Comparaison avec le marché (approximation)
        annees_experience = employee_data.get("annee_experience_totale", 0)
        expected_revenu = 2500 + (annees_experience * 200) + (niveau_hierarchique * 500)

        if revenu < expected_revenu * 0.8:
            risk_factors.append(
                {
                    "icon": "💰",
                    "title": "Rémunération sous le marché",
                    "description": f"{revenu}€ vs {expected_revenu:.0f}€ attendu",
                    "weight": 0.12,
                    "category": "compensation",
                }
            )

    # Facteurs de burnout
    burnout = employee_data.get("parent_burnout", 0)
    if burnout >= 3:
        risk_factors.append(
            {
                "icon": "🔥",
                "title": "Risque de burnout élevé",
                "description": f"Score burnout: {burnout}/4 (niveau critique)",
                "weight": 0.20,
                "category": "wellbeing",
            }
        )
    elif burnout >= 2:
        risk_factors.append(
            {
                "icon": "😰",
                "title": "Stress important",
                "description": f"Score burnout: {burnout}/4",
                "weight": 0.10,
                "category": "wellbeing",
            }
        )

    # Facteurs d'équilibre vie pro/perso
    equilibre = employee_data.get("satisfaction_employee_equilibre_pro_perso", 3)
    having_kids = employee_data.get("ayant_enfants", "Non")

    if equilibre <= 2 and having_kids == "Oui":
        risk_factors.append(
            {
                "icon": "👨‍👩‍👧‍👦",
                "title": "Conflit travail/famille",
                "description": f"Équilibre {equilibre}/4 avec enfants à charge",
                "weight": 0.15,
                "category": "worklife",
            }
        )
    elif equilibre <= 2:
        risk_factors.append(
            {
                "icon": "⚖️",
                "title": "Déséquilibre vie pro/perso",
                "description": f"Équilibre {equilibre}/4",
                "weight": 0.08,
                "category": "worklife",
            }
        )

    return sorted(risk_factors, key=lambda x: x["weight"], reverse=True)


def render_risk_factors_analysis(employee_data: dict, prediction_data: dict):
    """
    Affiche l'analyse intelligente des facteurs de risque.

    Args:
        employee_data: Données de l'employé
        prediction_data: Résultats de la prédiction
    """
    risk_factors = get_risk_factors_intelligent(employee_data, prediction_data)

    if not risk_factors:
        st.success("✅ Excellent profil ! Aucun facteur de risque majeur identifié")
        return

    # Affichage par catégorie avec pondération visuelle
    categories = {}
    for factor in risk_factors:
        cat = factor["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(factor)

    # Couleurs selon l'impact
    for category, factors in categories.items():
        category_titles = {
            "satisfaction": "😊 Satisfaction et Engagement",
            "workload": "⏰ Charge de Travail",
            "tenure": "📅 Ancienneté et Expérience",
            "career": "📈 Développement de Carrière",
            "compensation": "💰 Rémunération",
            "wellbeing": "🧘 Bien-être et Santé",
            "worklife": "👨‍👩‍👧‍👦 Équilibre Vie Pro/Perso",
        }

        st.markdown(f"#### {category_titles.get(category, category.capitalize())}")

        for factor in factors:
            # Couleur selon le poids
            if factor["weight"] >= 0.18:
                bg_color = "#f8d7da"  # rouge
                border_color = "#dc3545"
            elif factor["weight"] >= 0.12:
                bg_color = "#fff3cd"  # jaune
                border_color = "#ffc107"
            else:
                bg_color = "#d1ecf1"  # bleu
                border_color = "#17a2b8"

            # Barre de poids visuel
            weight_percent = factor["weight"] * 100

            html_factor = f"""
            <div style="
                margin: 10px 0;
                padding: 15px;
                background: {bg_color};
                border-radius: 8px;
                border-left: 4px solid {border_color};
                position: relative;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{factor['icon']} {factor['title']}</strong><br>
                        <small style="color: #666;">{factor['description']}</small>
                    </div>
                    <div style="
                        background: {border_color};
                        color: white;
                        padding: 2px 8px;
                        border-radius: 12px;
                        font-size: 11px;
                        font-weight: bold;
                    ">
                        {weight_percent:.0f}%
                    </div>
                </div>
                <div style="
                    margin-top: 8px;
                    height: 4px;
                    background: rgba(0,0,0,0.1);
                    border-radius: 2px;
                ">
                    <div style="
                        width: {weight_percent}%;
                        height: 100%;
                        background: {border_color};
                        border-radius: 2px;
                    "></div>
                </div>
            </div>
            """

            st.markdown(html_factor, unsafe_allow_html=True)


def get_personalized_recommendations(employee_data: dict, prediction_data: dict):
    """
    Génère des recommandations personnalisées basées sur l'analyse complète.

    Args:
        employee_data: Données de l'employé
        prediction_data: Résultats de la prédiction

    Returns:
        Liste de recommandations structurées par priorité
    """
    risk_level = prediction_data.get("risk_level", "Inconnu")
    risk_percentage = prediction_data.get("attrition_risk", 0)
    risk_factors = get_risk_factors_intelligent(employee_data, prediction_data)

    recommendations = {
        "urgent": [],  # Actions immédiates (24-48h)
        "short_term": [],  # Court terme (1-4 semaines)
        "medium_term": [],  # Moyen terme (1-3 mois)
        "preventive": [],  # Préventif (continu)
    }

    # Extraire les facteurs de risque par catégorie
    factor_categories = {}
    for factor in risk_factors:
        cat = factor["category"]
        if cat not in factor_categories:
            factor_categories[cat] = []
        factor_categories[cat].append(factor)

    # Recommandations urgentes (risque très élevé)
    if risk_level == "Très élevé" or risk_percentage > 80:
        recommendations["urgent"].append("🚨 **ALERTE : Risque de départ imminent**")
        recommendations["urgent"].append("🎯 Planifier un entretien individuel sous 48h")
        recommendations["urgent"].append(
            "💬 Évaluer immédiatement les sources d'insatisfaction principales"
        )

    # Recommandations basées sur les facteurs identifiés
    if "satisfaction" in factor_categories:
        satisfaction_issues = factor_categories["satisfaction"]
        high_satisfaction_risk = any(f["weight"] >= 0.18 for f in satisfaction_issues)

        if high_satisfaction_risk:
            recommendations["urgent"].append(
                "🔍 Audit complet de satisfaction avec questionnaire détaillé"
            )
            recommendations["short_term"].append("💰 Évaluer la rémunération par rapport au marché")
            recommendations["short_term"].append(
                "🏡 Discuter des conditions de travail et environnement"
            )

    if "workload" in factor_categories:
        hours = employee_data.get("nombre_heures_travailless", 40)

        if hours > 50:
            recommendations["urgent"].append("⚖️ Réduction immédiate de la charge de travail")
            recommendations["short_term"].append("📋 Révision des priorités et délégation")
        elif hours > 45:
            recommendations["short_term"].append(
                "📊 Analyse et optimisation de la charge de travail"
            )

        recommendations["medium_term"].append("🛠️ Formation sur la gestion du temps et priorisation")

    if "career" in factor_categories:
        last_promotion = employee_data.get("annees_depuis_la_derniere_promotion", 0)
        niveau = employee_data.get("niveau_hierarchique_poste", 1)

        if last_promotion > 3:
            recommendations["short_term"].append("📈 Élaborer un plan de développement de carrière")
            recommendations["medium_term"].append(
                "🎓 Identifier les compétences à développer pour promotion"
            )
            if niveau < 3:
                recommendations["medium_term"].append(
                    "🎯 Préparer un objectif de promotion dans les 6-12 mois"
                )

        recommendations["short_term"].append("👥 Assigner un mentor si pas déjà fait")

    if "compensation" in factor_categories:
        recommendations["short_term"].append("💰 Révision salariale avec benchmark marché")
        recommendations["medium_term"].append(
            "🎁 Envisager avantages complémentaires (flexibilité, formation)"
        )

    if "wellbeing" in factor_categories:
        burnout_issues = factor_categories["wellbeing"]
        high_burnout = any(f["weight"] >= 0.18 for f in burnout_issues)

        if high_burnout:
            recommendations["urgent"].append("🏥 Proposer un accompagnement psychologique")
            recommendations["short_term"].append("🏖️ Encourager une pause/congé si possible")

        recommendations["short_term"].append("🧘 Programme de prévention du stress")
        recommendations["medium_term"].extend(
            ["🏃‍♂️ Promouvoir activités bien-être", "📱 Encourager déconnexion hors travail heures"]
        )

    if "worklife" in factor_categories:
        equilibre = employee_data.get("satisfaction_employee_equilibre_pro_perso", 3)
        having_kids = employee_data.get("ayant_enfants", "Non")

        if having_kids == "Oui" and equilibre <= 2:
            recommendations["short_term"].extend(
                [
                    "👨‍👩‍👧‍👦 Discuter aménagements horaires si possible",
                    "🏠 Évaluer options de télétravail",
                ]
            )

        recommendations["medium_term"].append("⚖️ Politique d'équilibre vie pro/perso personnalisée")

    # Recommandations par niveau de risque global
    if risk_level in ["Moyen"]:
        recommendations["preventive"].extend(
            [
                "👂 Maintenir des points réguliers (mensuels)",
                "📊 Suivi des indicateurs de satisfaction",
                "🎉 Reconnaître et célébrer les contributions",
            ]
        )
    elif risk_level == "Faible":
        recommendations["preventive"].extend(
            [
                "😊 Continuer la valorisation régulière",
                "🌟 Identifier opportunités de développement",
                "👥 Proposer du mentorat inversé",
            ]
        )

    # Recommandations préventives générales
    if risk_level in ["Élevé", "Très élevé"]:
        recommendations["preventive"].extend(
            [
                "📈 Mettre en place un plan de suivi hebdomadaire",
                "🤝 Impliquer l'équipe dans le plan d'action",
                "📝 Documenter les actions et progrès",
            ]
        )

    return recommendations


def render_recommendations(employee_data: dict, prediction_data: dict):
    """
    Affiche des recommandations personnalisées basées sur l'analyse complète.

    Args:
        employee_data: Données de l'employé
        prediction_data: Résultats de la prédiction
    """
    recommendations = get_personalized_recommendations(employee_data, prediction_data)

    # Afficher par ordre de priorité
    priority_order = ["urgent", "short_term", "medium_term", "preventive"]
    priority_info = {
        "urgent": {"icon": "🚨", "title": "Actions Urgentes (24-48h)", "color": "#dc3545"},
        "short_term": {"icon": "⏰", "title": "Court Terme (1-4 semaines)", "color": "#fd7e14"},
        "medium_term": {"icon": "📅", "title": "Moyen Terme (1-3 mois)", "color": "#17a2b8"},
        "preventive": {"icon": "🛡️", "title": "Préventif (Continu)", "color": "#28a745"},
    }

    for priority in priority_order:
        items = recommendations.get(priority, [])
        if not items:
            continue

        info = priority_info[priority]

        # En-tête de section
        st.markdown(
            f"""
        <div style="
            margin: 15px 0;
            padding: 12px;
            background: {info['color']}15;
            border-left: 4px solid {info['color']};
            border-radius: 5px;
        ">
            <h4 style="margin: 0; color: {info['color']};">
                {info['icon']} {info['title']}
            </h4>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Liste des recommandations
        for rec in items:
            # Extraire l'icône si présente au début
            if rec.startswith(
                (
                    "🚨",
                    "🎯",
                    "💬",
                    "⚖️",
                    "🔍",
                    "💰",
                    "🏡",
                    "📋",
                    "🛠️",
                    "📈",
                    "🎓",
                    "🎁",
                    "👥",
                    "🏥",
                    "🏖️",
                    "🧘",
                    "🏃‍♂️",
                    "📱",
                    "👨‍👩‍👧‍👦",
                    "🏠",
                    "⚖️",
                    "👂",
                    "📊",
                    "🎉",
                    "🌟",
                    "😊",
                    "🛡️",
                    "📈",
                    "🤝",
                    "📝",
                )
            ):
                icon = rec[:2]  # Prendre l'emoji
                text = rec[3:]  # Le reste du texte
                if text.startswith("**"):
                    # Titre en gras
                    st.markdown(f"**{icon} {text}**")
                else:
                    st.markdown(f"{icon} {text}")
            else:
                st.markdown(f"- {rec}")

    # Résumé du plan d'action
    total_actions = sum(len(recs) for recs in recommendations.values())
    st.markdown(
        f"""
    <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; text-align: center;">
        <strong>📋 Plan d'action : {total_actions} recommandations identifiées</strong><br>
        <small>Priorisez les actions urgentes pour réduire efficacement le risque d'attrition</small>
    </div>
    """,
        unsafe_allow_html=True,
    )


def main():
    """Fonction principale de la page de prédiction."""
    st.set_page_config(page_title="Prédiction d'Attrition", page_icon="🎯", layout="wide")

    st.title("🎯 Prédiction d'Attrition")
    st.markdown("---")
    st.markdown(
        """
        Utilisez l'intelligence artificielle pour prédire le risque d'attrition des employés.
        Saisissez les informations d'un employé pour obtenir une analyse complète du risque de départ.
        """
    )

    # Initialiser l'API client
    api_client = st.session_state.api_client

    # Interface de recherche
    search_type, search_value = render_employee_search()

    # Stocker les résultats dans la session
    if "selected_employee" not in st.session_state:
        st.session_state.selected_employee = None
    if "prediction_result" not in st.session_state:
        st.session_state.prediction_result = None

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("🔍 Rechercher", type="primary"):
            if search_value:
                try:
                    with st.spinner("Recherche de l'employé..."):
                        if search_type == "ID Employé":
                            employee = api_client.get_employee(search_value)
                            st.session_state.selected_employee = employee
                            show_success(f"Employé trouvé: {employee.get('poste', 'N/A')}")
                        else:
                            employees = api_client.search_employees(str(search_value))
                            if employees:
                                st.session_state.selected_employee = employees[0]
                                show_success(f"{len(employees)} employé(s) trouvé(s)")
                            else:
                                show_error("Aucun employé trouvé pour cette recherche")
                                st.session_state.selected_employee = None

                    st.session_state.prediction_result = None
                    st.rerun()

                except Exception as e:
                    show_error(f"Erreur lors de la recherche: {str(e)}")
            else:
                show_error("Veuillez saisir une valeur pour la recherche")

    with col2:
        if st.session_state.selected_employee:
            if st.button("🎯 Prédire l'attrition", type="secondary"):
                try:
                    render_loading_prediction()
                    time.sleep(1)  # Simulation pour l'effet visuel

                    with st.spinner("Analyse avec le modèle de machine learning..."):
                        prediction_data = api_client.predict_attrition(
                            st.session_state.selected_employee
                        )
                        st.session_state.prediction_result = prediction_data
                        show_success("Prédiction réalisée avec succès!")
                        time.sleep(0.5)
                        st.rerun()

                except Exception as e:
                    show_error(f"Erreur lors de la prédiction: {str(e)}")

    # Afficher les résultats
    if st.session_state.selected_employee:
        st.markdown("### 👤 Employé sélectionné")
        render_employee_card(st.session_state.selected_employee)

        if st.session_state.prediction_result:
            st.markdown("### 🎯 Résultats de la prédiction")
            render_prediction_results(
                st.session_state.prediction_result, st.session_state.selected_employee
            )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 20px;">
            <p>🤖 Prédiction basée sur un modèle de machine learning entraîné sur des données RH historiques</p>
            <p style="font-size: 12px;">Les prédictions sont des estimations et doivent être utilisées comme outil d'aide à la décision</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
