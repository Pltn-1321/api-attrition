---
title: API Technova - Gestion RH & Attrition
emoji: 👥
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.30.0"
app_file: app.py
pinned: false
license: mit
tags:
  - rh
  - data-science
  - analytics
  - fastapi
  - streamlit
---

# 👥 API Technova - Plateforme de Gestion RH

Application complète de gestion et d'analyse des données RH avec :
- **API REST** (FastAPI) pour l'accès programmatique aux données
- **Interface web interactive** (Streamlit) pour la visualisation et l'exploration
- **Base de données** SQLite avec 294 employés

## 🚀 Fonctionnalités

### 📊 Explorer
- Liste complète des employés avec pagination
- Filtres par département et tranche d'âge
- Export CSV des données filtrées
- Statistiques en temps réel

### 🔍 Recherche
- Recherche détaillée par ID employé
- Affichage du profil complet
- Métriques de satisfaction

### 📈 Statistiques
- Visualisations interactives (Plotly)
- Analyses démographiques
- Indicateurs de satisfaction

### 🔌 API REST
- `/health` - Vérification de l'état du système
- `/employees` - Liste des employés (avec pagination)
- `/employees/{id}` - Détails d'un employé
- Documentation Swagger disponible sur `/docs`

## 💡 Utilisation

L'application démarre automatiquement avec :
- **API FastAPI** sur le port 8000 (backend)
- **Interface Streamlit** sur le port 7860 (frontend)

Accédez simplement à l'interface Streamlit pour commencer à explorer les données !

## 🛠️ Technologies

- **Backend**: FastAPI, SQLAlchemy, Uvicorn
- **Frontend**: Streamlit, Plotly, Pandas
- **Database**: SQLite
- **ML**: Scikit-learn (modèle de prédiction inclus)

## 📊 Données

- **294 employés** dans la base de données
- **34 champs** par employé (démographie, carrière, satisfaction, etc.)
- Données anonymisées et générées pour démonstration

## 📝 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

---

Développé avec ❤️ pour la gestion moderne des ressources humaines
