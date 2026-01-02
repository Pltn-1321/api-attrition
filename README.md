---
title: API Technova - Gestion RH & Attrition
emoji: 👥
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
tags:
  - rh
  - ai-engineer
  - machine-learning
  - analytics
  - fastapi
  - streamlit
---

# Projet 5 - API Attrition Technova | Parcours AI Engineer OpenClassroom

[![CI/CD](https://github.com/Pltn-1321/api-attrition/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/Pltn-1321/api-attrition/actions)
[![codecov](https://codecov.io/gh/Pltn-1321/api-attrition/branch/main/graph/badge.svg)](https://codecov.io/gh/Pltn-1321/api-attrition)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.123+-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-FF4B4B.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

> **Déploiement en production d'un modèle ML de prédiction d'attrition RH**
> Transformation d'un modèle de machine learning en API REST production-ready avec interface web interactive

**🔗 Liens Rapides:**
- [🚀 Demo Live](https://huggingface.co/spaces/Pedro1321/Api-Technova) - Application déployée sur Hugging Face Spaces
- [📊 Repository GitHub](https://github.com/Pltn-1321/api-attrition) - Code source complet
- [📈 Coverage Report](https://codecov.io/gh/Pltn-1321/api-attrition) - Rapports de couverture des tests
- [🔄 CI/CD Pipeline](https://github.com/Pltn-1321/api-attrition/actions) - Workflows d'intégration continue

---

## Table des Matières

1. [Synopsis du Projet](#synopsis-du-projet)
2. [Objectifs Pédagogiques et Compétences](#objectifs-pédagogiques-et-compétences)
3. [Architecture Technique](#architecture-technique)
4. [Modèle de Données](#modèle-de-données)
5. [Installation et Développement Local](#installation-et-développement-local)
6. [Tests et Assurance Qualité](#tests-et-assurance-qualité)
7. [Pipeline CI/CD](#pipeline-cicd)
8. [Déploiement Production](#déploiement-production)
9. [Troubleshooting & FAQ](#troubleshooting--faq)
10. [Réflexions et Perspectives](#réflexions-et-perspectives)
11. [Références et Ressources](#références-et-ressources)
12. [License et Crédits](#license-et-crédits)

---

## Synopsis du Projet

### Contexte Pédagogique

Ce projet s'inscrit dans le cadre du **parcours AI Engineer d'OpenClassroom** et constitue le **Projet 5**, consacré au déploiement en production d'applications de machine learning.

#### Projet 4 - Développement du Modèle ML

Le projet précédent (P4) a permis de développer un modèle de classification pour prédire le risque d'attrition des employés de l'entreprise Technova :

- **Analyse exploratoire** du dataset complet (1,470 employés)
- **Feature engineering** sur 34 variables (démographie, carrière, satisfaction, rémunération)
- **Entraînement d'un modèle** de classification avec scikit-learn 1.7.1
- **Validation** par cross-validation et analyse des métriques de performance
- **Export du modèle** : `attrition_model.joblib` + `original_features.joblib`

#### Projet 5 - Déploiement en Production

Le présent projet (P5) transforme ce modèle ML en une **application web production-ready** déployée sur le cloud :

**Objectifs principaux :**
- Concevoir une **architecture API REST** robuste et scalable
- Développer un **backend FastAPI** avec documentation OpenAPI automatique
- Créer une **interface web Streamlit** multi-pages interactive
- Implémenter un **système dual-database** (PostgreSQL dev / SQLite prod)
- Mettre en place des **tests automatisés** (unit + functional)
- Déployer un **pipeline CI/CD** complet avec GitHub Actions
- **Conteneuriser** l'application avec Docker
- Déployer sur **Hugging Face Spaces** avec monitoring
- Assurer le **troubleshooting** et la maintenance en production

**Compétences évaluées :**
- ✅ Développement full-stack (Backend + Frontend)
- ✅ DevOps et automatisation (CI/CD, Docker)
- ✅ Déploiement cloud et gestion d'environnements
- ✅ Tests logiciels et qualité de code
- ✅ Architecture distribuée et patterns de conception

### Cas d'Affaires - Technova

**Problématique RH :**
Technova, entreprise fictive du secteur technologique, fait face à un taux d'attrition préoccupant. Les départs d'employés qualifiés impactent la productivité, augmentent les coûts de recrutement et affectent la culture d'entreprise.

**Solution proposée :**
Une plateforme web permettant aux équipes RH de :
- **Explorer** la base de données des employés avec filtres dynamiques
- **Rechercher** et analyser le profil détaillé de chaque collaborateur
- **Visualiser** des statistiques agrégées (départements, rémunération, satisfaction)
- **Prédire** le risque de départ à l'aide du modèle ML
- **Diagnostiquer** l'état de santé du système en production

**Dataset :**
- **1,470 employés** au total (dataset complet d'entraînement)
- **294 employés de test** utilisés en production (données non vues pendant le training)
- **34 features** par employé réparties en 6 catégories :
  - Profil démographique (âge, genre, statut marital, enfants, éducation)
  - Carrière professionnelle (poste, département, domaine, expérience)
  - Conditions de travail (salaire, heures supplémentaires, distance domicile-travail)
  - Satisfaction (environnement, nature du travail, équipe, équilibre vie pro/perso)
  - Développement (formations suivies, participation PEE)
  - Indicateurs de risque (burnout parental, sous-rémunération)

### Réalisations Clés

Ce projet démontre la maîtrise de l'ensemble de la chaîne de valeur du déploiement ML :

✅ **API REST Production-Ready**
- 6 endpoints FastAPI avec validation Pydantic
- Documentation OpenAPI interactive à `/docs`
- Gestion d'erreurs robuste et logging
- Health checks pour monitoring

✅ **Interface Web Interactive**
- 5 pages Streamlit avec navigation fluide
- Visualisations Plotly interactives
- Filtres et recherche temps réel
- Design responsive et UX optimisée

✅ **Architecture Dual-Database**
- PostgreSQL pour le développement local (Docker Compose)
- SQLite pour la production cloud (embedded)
- Basculement automatique via variable d'environnement
- Migrations gérées avec SQLAlchemy ORM

✅ **Pipeline CI/CD Automatisé**
- 13 tests automatisés (8 unit + 5 functional)
- Coverage à 60%+ sur les modules core
- Linting et formatage (Ruff, Black)
- Déploiement automatique sur Hugging Face Spaces

✅ **Déploiement Production Dockerisé**
- Conteneur unique avec 2 processus (FastAPI + Streamlit)
- Startup intelligent avec health check retry (30s)
- Configuration environment-based
- Monitoring et troubleshooting intégrés

✅ **Qualité Logicielle**
- Tests unitaires et fonctionnels
- Couverture de code mesurée et rapportée
- Validation automatique en CI
- Documentation technique complète (CLAUDE.md)

---

## Objectifs Pédagogiques et Compétences

### Progression Projet 4 → Projet 5

Le tableau ci-dessous illustre l'évolution des compétences entre les deux projets :

| Aspect | Projet 4 (ML Development) | Projet 5 (Production Deployment) |
|--------|---------------------------|-----------------------------------|
| **Focus** | Modélisation statistique | Ingénierie logicielle |
| **Livrables** | Modèle .joblib + notebook | Application web + API + CI/CD |
| **Technologies** | scikit-learn, pandas, matplotlib | + FastAPI, Streamlit, Docker, GitHub Actions |
| **Environnement** | Jupyter Notebook local | Multi-env (dev/prod), cloud deployment |
| **Tests** | Validation manuelle du modèle | Tests automatisés (13 tests), coverage 60%+ |
| **Déploiement** | Fichier .joblib sauvegardé | API REST déployée sur HF Spaces |
| **Monitoring** | Métriques offline (precision, recall) | Health checks, logs, diagnostic page |
| **Base de données** | Fichiers CSV | PostgreSQL + SQLite avec ORM |

**Projet 4 - Compétences Développées :**
- Analyse exploratoire de données (EDA)
- Feature engineering et sélection de variables
- Entraînement et optimisation de modèles (GridSearch, cross-validation)
- Évaluation des performances (matrices de confusion, courbes ROC)
- Export et versioning de modèles ML

**Projet 5 - Nouvelles Compétences Acquises :**
- Conception d'architecture API REST
- Développement backend asynchrone (FastAPI + Uvicorn)
- Développement frontend interactif (Streamlit multi-pages)
- Gestion de bases de données relationnelles (SQLAlchemy)
- Écriture de tests automatisés (pytest, mocking, fixtures)
- Configuration CI/CD (GitHub Actions, workflows)
- Conteneurisation d'applications (Docker, Dockerfile)
- Déploiement cloud (Hugging Face Spaces)
- Monitoring et troubleshooting production
- Documentation technique et opérationnelle

### Compétences Techniques Acquises

| Domaine | Technologies | Niveau Maîtrisé | Preuve |
|---------|-------------|-----------------|--------|
| **Backend API** | FastAPI, Uvicorn, Pydantic | Production-ready | 6 endpoints, OpenAPI docs, error handling |
| **Frontend Web** | Streamlit 1.30.0, Plotly 5.18.0 | Multi-page apps | 5 pages interactives, visualisations dynamiques |
| **Base de Données** | SQLAlchemy, PostgreSQL, SQLite | Dual-backend pattern | Environment-based config, migrations |
| **Machine Learning** | scikit-learn 1.7.1, joblib | Model deployment | Intégration API, prédictions temps réel |
| **Testing** | pytest, pytest-cov, pytest-mock | 60%+ coverage | 13 tests (unit + functional), fixtures |
| **DevOps** | GitHub Actions, Docker | Full CI/CD pipeline | 2-job workflow, automated deployment |
| **Cloud** | Hugging Face Spaces | Containerized deployment | Live production app, monitoring |
| **Code Quality** | Ruff, Black | Automated linting | Pre-commit hooks, CI validation |
| **Data Processing** | pandas 2.3.3, NumPy | DataFrame operations | Data loading, transformation, validation |
| **HTTP Client** | httpx, requests | API communication | Streamlit↔FastAPI integration |

**Soft Skills Développées :**
- Gestion de projet technique complexe
- Documentation technique et utilisateur
- Résolution de problèmes en production (503 errors, compatibility issues)
- Compréhension des besoins métier (RH analytics)
- Communication technique (README académique, CLAUDE.md)

---

## Architecture Technique

### Vue d'Ensemble

L'application adopte une **architecture two-tier** séparant clairement le backend (API) et le frontend (interface web), déployée dans un conteneur Docker unique sur Hugging Face Spaces.

```
┌─────────────────────────────────────────────────┐
│   Conteneur Docker (Hugging Face Spaces)       │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Process 1: FastAPI (port 8000)          │  │
│  │ • Modèle ML (attrition_model.joblib)    │  │
│  │ • Base SQLite (database.db)             │  │
│  │ • 6 endpoints REST + OpenAPI            │  │
│  │ • Validation Pydantic                   │  │
│  │ • NON exposé à Internet                 │  │
│  └──────────────────────────────────────────┘  │
│                    ↑                            │
│                    │ localhost:8000             │
│                    │ (communication interne)    │
│                    │                            │
│  ┌──────────────────────────────────────────┐  │
│  │ Process 2: Streamlit (port 7860)        │  │
│  │ • 5 pages interactives                  │  │
│  │ • Visualisations Plotly                 │  │
│  │ • API Client (httpx)                    │  │
│  │ • Session state management              │  │
│  │ • EXPOSÉ à Internet                     │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  Port 7860 → Internet                          │
│  (Seul point d'accès utilisateur)              │
└─────────────────────────────────────────────────┘
```

**Principes architecturaux :**

1. **Séparation backend/frontend** : Pas de couplage direct, communication via HTTP REST
2. **API-first design** : Le frontend ne peut pas accéder directement à la base de données
3. **Stateless API** : Chaque requête est indépendante, facilite le scaling horizontal
4. **Singleton pattern** : API Client unique en session state Streamlit
5. **Environment-based config** : Adaptation automatique dev/prod via variables d'environnement

**Avantages de cette architecture :**
- ✅ Scalabilité indépendante des composants
- ✅ Testabilité (mocking des API calls facile)
- ✅ Sécurité (API non exposée directement)
- ✅ Simplicité de déploiement (un seul container)
- ✅ Performance (communication localhost, pas de latence réseau)

### Stack Technologique

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| **API Framework** | FastAPI | ≥0.123.10 | Framework async moderne, génération OpenAPI automatique, validation Pydantic intégrée |
| **ASGI Server** | Uvicorn | ≥0.38.0 | Serveur ASGI haute performance pour FastAPI, support WebSockets |
| **Frontend Framework** | Streamlit | 1.30.0 | Prototypage rapide, Python-native, multi-page apps out-of-the-box |
| **Data Visualization** | Plotly | 5.18.0 | Graphiques interactifs (zoom, hover, export), rendu HTML5 |
| **ORM** | SQLAlchemy | ≥2.0.44 | Abstraction base de données, migrations, type safety |
| **DB Development** | PostgreSQL | 15 | Base robuste pour dev, support transactions, contraintes |
| **DB Production** | SQLite | 3 | Embedded, zero-config, parfait pour read-heavy workloads |
| **ML Framework** | scikit-learn | 1.7.1 | **Version critique** : compatibilité avec modèle P4 |
| **ML Serialization** | joblib | ≥1.5.3 | Format optimisé pour objets NumPy, compression |
| **Data Processing** | pandas | 2.3.3 | DataFrames, manipulation de données tabulaires |
| **HTTP Client** | httpx | ≥0.28.1 | Client async/sync, support timeout, modern API |
| **Testing Framework** | pytest | 7.4.3 | Standard Python testing, fixtures, parametrize |
| **Test Coverage** | pytest-cov | 4.1.0 | Mesure de couverture, rapports HTML/XML |
| **Test Mocking** | pytest-mock | ≥3.15.1 | Mocking simplifié pour tests unitaires |
| **Linter** | Ruff | ≥0.14.10 | Linter ultra-rapide (Rust), remplace flake8+isort |
| **Formatter** | Black | ≥25.12.0 | Code formatter opinionated, PEP 8 compliant |
| **Containerization** | Docker | - | Standardisation environnements, portabilité |
| **CI/CD** | GitHub Actions | - | Intégration native GitHub, runners gratuits |
| **Cloud Platform** | Hugging Face Spaces | - | Plateforme ML-focused, Docker SDK, déploiement git-based |

**Dépendances complètes :** Voir [pyproject.toml](pyproject.toml) et [requirements.txt](requirements.txt)

### Base de Données - Dual Backend Pattern

L'application supporte deux backends de base de données avec basculement automatique via variable d'environnement.

**Configuration dynamique ([database/config.py](database/config.py:5-15)) :**

```python
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # Default: sqlite

if DB_TYPE == "postgres":
    # PostgreSQL pour développement local
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
else:
    # SQLite pour production HF Spaces
    DATABASE_URL = "sqlite:///./database.db"
    connect_args = {"check_same_thread": False}  # FastAPI compatibility
```

#### PostgreSQL (Développement Local)

**Avantages :**
- Transactions ACID complètes
- Contraintes d'intégrité référentielle
- Support de migrations complexes
- Proche de l'environnement production typique

**Configuration Docker Compose :**

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    container_name: attrition_db
    environment:
      POSTGRES_USER: attrition_user
      POSTGRES_PASSWORD: attrition_password
      POSTGRES_DB: attrition_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**Import des données :**

```bash
docker-compose up -d
uv run database/import_data.py  # Charge test_employees.csv → PostgreSQL
```

#### SQLite (Production HF Spaces)

**Avantages :**
- Zero configuration (fichier unique)
- Pas de service externe à maintenir
- Parfait pour workloads read-heavy
- Réduction des coûts (pas de DB cloud)
- Fichier committé dans le repo → déploiement simplifié

**Migration depuis PostgreSQL :**

```bash
export DB_TYPE=sqlite
uv run database/migrate_to_sqlite.py  # Copie PostgreSQL → database.db
```

**Fichier généré :** [database.db](database.db) (43 KB, 294 rows)

**Modèle ORM SQLAlchemy ([database/models.py](database/models.py)) :**

```python
class Employee(Base):
    __tablename__ = "employees"

    id = Column(BigInteger, primary_key=True)
    age = Column(Integer)
    genre = Column(String)
    # ... 31 autres colonnes (34 features total)
```

### API REST - Endpoints

L'API FastAPI expose 6 endpoints documentés automatiquement via OpenAPI.

| Endpoint | Méthode | Description | Pagination | Auth |
|----------|---------|-------------|------------|------|
| `/` | GET | Informations générales de l'API | - | - |
| `/health` | GET | Health check (API + DB + Modèle) | - | - |
| `/model-status` | GET | Diagnostic modèle ML (version, features, path) | - | - |
| `/employees` | GET | Liste paginée des employés | `?skip=0&limit=100` | - |
| `/employees/{id}` | GET | Détails d'un employé par ID | - | - |
| `/predict` | POST | Prédiction risque d'attrition ML | - | - |

**Schémas Pydantic ([api/schemas.py](api/schemas.py)) :**

```python
class EmployeeBase(BaseModel):
    """34 champs : age, genre, poste, departement, satisfaction_moyenne, etc."""
    age: Optional[int]
    genre: Optional[str]
    # ... 32 autres champs

class EmployeeResponse(EmployeeBase):
    id: int
    class Config:
        from_attributes = True

class EmployeeListResponse(BaseModel):
    total: int
    employees: List[EmployeeResponse]

class PredictionRequest(BaseModel):
    """Données employé pour prédiction (34 features requises)"""
    # ... 34 champs

class PredictionResponse(BaseModel):
    attrition_risk: float  # Pourcentage 0-100
    probability: float     # Probabilité 0-1
    prediction: int        # Classe binaire 0/1
    risk_level: str        # "Faible" | "Moyen" | "Élevé" | "Très élevé"
```

**Documentation interactive :** http://localhost:8000/docs (Swagger UI)

**Exemple de requête :**

```bash
# Health check
curl http://localhost:8000/health
# Réponse: {"status": "healthy", "database": "connected", "model": "loaded"}

# Liste employés (10 premiers)
curl "http://localhost:8000/employees?limit=10"
# Réponse: {"total": 294, "employees": [...]}

# Détail employé
curl http://localhost:8000/employees/42
# Réponse: {"id": 42, "age": 35, "genre": "F", "poste": "Tech Lead", ...}
```

### Frontend Streamlit - Multi-Page App

Streamlit utilise le pattern de découverte automatique des pages via le dossier `pages/`.

#### Structure des Pages

**1. [app.py](app.py) - Dashboard d'Accueil**

Page principale affichant :
- Health check API + Database en temps réel
- Statistiques générales (total employés, âge moyen, satisfaction moyenne)
- Guide de navigation vers les autres pages
- Gestion gracieuse des erreurs de connexion (bouton retry)

**2. [pages/1_📊_Explorer.py](pages/1_📊_Explorer.py) - Liste et Filtres**

Fonctionnalités :
- Filtres interactifs dans la sidebar :
  - Multi-select département (Commercial, Consulting, Data Science, RH, IT)
  - Slider âge (18-70 ans)
  - Bouton reset filtres
- Tableau paginé (100 employés affichés)
- Statistiques filtrées (nombre, âge moyen, satisfaction, ancienneté)
- Export CSV des résultats filtrés

**3. [pages/2_🔍_Recherche.py](pages/2_🔍_Recherche.py) - Recherche Individuelle**

Fonctionnalités :
- Recherche par ID employé (input numérique)
- Carte employé avec résumé (poste, département, âge, salaire, satisfaction)
- 4 onglets d'informations détaillées :
  - **👤 Profil** : Genre, âge, statut marital, enfants, distance domicile-travail, éducation
  - **💼 Professionnel** : Poste, département, domaine, salaire, heures supplémentaires, niveau hiérarchique
  - **📈 Carrière** : Expérience totale, ancienneté entreprise/poste, formations, promotions
  - **😊 Satisfaction** : 4 dimensions (environnement, nature travail, équipe, équilibre) + moyenne
- Indicateurs de risque (burnout parental, sous-rémunération)

**4. [pages/3_📈_Statistiques.py](pages/3_📈_Statistiques.py) - Visualisations**

4 onglets avec graphiques Plotly interactifs :
- **📊 Départements** : Distribution effectifs + salaire moyen par département
- **👥 Démographie** : Histogramme âges + pie chart genre
- **💰 Rémunération** : Box plot salaires + salaire moyen par département + scatter expérience vs salaire
- **😊 Satisfaction** : Satisfaction moyenne par département + distribution des scores

**5. [pages/4_🎯_Prediction.py](pages/4_🎯_Prediction.py) - Prédiction ML**

Workflow complet :
1. **Recherche employé** (ID ou filtres)
2. **Appel API POST /predict** avec données employé
3. **Affichage résultats** :
   - Card de prédiction avec emoji (😊 faible → 😱 très élevé)
   - Métriques clés (âge, satisfaction, ancienneté, salaire)
   - Gauge de risque (barre de progression 0-100%)
4. **Analyse avancée des risques** (7 catégories pondérées) :
   - 🚨 Satisfaction & Engagement
   - ⏰ Workload (charge de travail)
   - 🆕 Tenure & Experience
   - 📈 Career Development
   - 💰 Compensation
   - 🔥 Well-being & Health
   - ⚖️ Work-Life Balance
5. **Recommandations personnalisées** (4 niveaux de priorité) :
   - 🚨 Actions urgentes (24-48h)
   - ⏰ Actions court terme (1-4 semaines)
   - 📅 Actions moyen terme (1-3 mois)
   - 🛡️ Actions préventives (continues)

**6. [pages/9_🔧_Diagnostic.py](pages/9_🔧_Diagnostic.py) - System Health**

Outils de troubleshooting :
- Quick status checks (API Health, ML Model, Prediction Test)
- Informations système (API URL, timeout, latency)
- Boutons d'actions diagnostiques
- Guide de résolution d'erreurs communes (503, model missing, version conflicts)

#### Composants Partagés

**[utils/api_client.py](utils/api_client.py) - HTTP Client**

Classe singleton pour communication avec l'API :

```python
class APIClient:
    def health_check() -> dict
    def get_employees(skip: int = 0, limit: int = 100) -> dict
    def get_employee(employee_id: int) -> dict
    def predict_attrition(employee_data: dict) -> dict
    def filter_employees(employees: list, filters: dict) -> list
    def search_employees(employees: list, query: str) -> list
```

**[utils/ui_components.py](utils/ui_components.py) - UI Components**

Fonctions de rendu réutilisables :
- `render_metric_card()` : Cartes métriques avec gradients
- `render_employee_card()` : Profil employé détaillé
- `render_prediction_card()` : Résultats prédiction
- `render_risk_gauge()` : Barre de progression risque
- `show_error/success/info()` : Messages stylisés

**[config.py](config.py) - Configuration Frontend**

```python
API_URL = os.getenv("API_URL", "http://localhost:8000")
APP_TITLE = "API Attrition - Dashboard"
DEFAULT_PAGE_SIZE = 20
COLORS = {
    "primary": "#FF6B6B",    # Coral
    "secondary": "#1A1A2E",  # Dark Blue
    "accent": "#0F3460",     # Blue
    # ...
}
CHART_CONFIG = {"displayModeBar": False, "responsive": True}
```

---

## Modèle de Données

### Dataset - Statistiques

- **Dataset complet** : 1,470 employés (utilisé pour entraînement en Projet 4)
- **Dataset test** : 294 employés ([data/export-api/test_employees.csv](data/export-api/test_employees.csv))
- **Features** : 34 colonnes organisées en 6 catégories
- **Format** : CSV avec header, délimiteur virgule
- **Taille** : 43 KB (dataset test), 196 KB (dataset complet)

### Catégories de Variables

<details>
<summary><b>Profil Démographique (6 features)</b></summary>

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `id` | int | Identifiant unique | 1-294 |
| `genre` | str | Genre | F, M |
| `age` | int | Âge | 18-70 ans |
| `statut_marital` | str | Statut marital | Marié(e), Célibataire, Divorcé(e) |
| `ayant_enfants` | str | A des enfants | Oui, Non, Y, N |
| `niveau_education` | int | Niveau d'études | 1-5 |

</details>

<details>
<summary><b>Professionnel (11 features)</b></summary>

| Variable | Type | Description |
|----------|------|-------------|
| `poste` | str | Intitulé du poste (Tech Lead, Senior Manager, etc.) |
| `departement` | str | Département (Commercial, Consulting, Data Science, RH, IT) |
| `domaine_etude` | str | Domaine (Infra & Cloud, Transformation Digitale, etc.) |
| `niveau_hierarchique_poste` | int | Niveau hiérarchique (1-5) |
| `nombre_experiences_precedentes` | int | Nombre d'emplois précédents |
| `annee_experience_totale` | int | Années d'expérience totale |
| `annees_dans_l_entreprise` | int | Ancienneté dans l'entreprise |
| `annees_dans_le_poste_actuel` | int | Ancienneté dans le poste |
| `annees_depuis_la_derniere_promotion` | int | Années depuis dernière promotion |
| `annes_sous_responsable_actuel` | int | Années sous le manager actuel |
| `nombre_employee_sous_responsabilite` | int | Nombre de personnes managées |

</details>

<details>
<summary><b>Travail (6 features)</b></summary>

| Variable | Type | Description |
|----------|------|-------------|
| `revenu_mensuel` | int | Salaire mensuel en € |
| `heure_supplementaires` | str | Heures supplémentaires (Oui/Non) |
| `nombre_heures_travailless` | int | Heures travaillées par semaine |
| `distance_domicile_travail` | int | Distance domicile-travail en km |
| `distance_categorie` | str | Catégorie distance (< 10 km, 10-20 km, etc.) |
| `frequence_deplacement` | str | Fréquence déplacements (Aucun, Occasionnel, Fréquent) |

</details>

<details>
<summary><b>Satisfaction (7 features)</b></summary>

Toutes les variables de satisfaction sont sur une échelle de 1 à 4 :

| Variable | Description |
|----------|-------------|
| `satisfaction_employee_environnement` | Satisfaction environnement de travail |
| `satisfaction_employee_nature_travail` | Satisfaction nature du travail |
| `satisfaction_employee_equipe` | Satisfaction travail en équipe |
| `satisfaction_employee_equilibre_pro_perso` | Satisfaction équilibre vie pro/perso |
| `satisfaction_moyenne` | Moyenne des 4 dimensions (float) |
| `note_evaluation_precedente` | Note évaluation précédente |
| `note_evaluation_actuelle` | Note évaluation actuelle |

</details>

<details>
<summary><b>Développement (2 features)</b></summary>

| Variable | Type | Description |
|----------|------|-------------|
| `nb_formations_suivies` | int | Nombre de formations suivies |
| `nombre_participation_pee` | int | Nombre de participations PEE (Plan Épargne Entreprise) |

</details>

<details>
<summary><b>Indicateurs de Risque (3 features)</b></summary>

| Variable | Type | Description |
|----------|------|-------------|
| `parent_burnout` | int | Score burnout parental (0-4) |
| `sous_paye_niveau_dept` | int | Indicateur sous-rémunération vs département |
| `augementation_salaire_precedente` | int | Augmentation salaire en mois |

</details>

### Intégration Modèle ML

#### Fichiers Modèle

- **[data/export-api/attrition_model.joblib](data/export-api/attrition_model.joblib)** (9 KB)
  - Modèle scikit-learn 1.7.1 entraîné en Projet 4
  - Format joblib (compression optimisée pour NumPy)
  - Type : Estimator avec `predict()` et `predict_proba()`

- **[data/export-api/original_features.joblib](data/export-api/original_features.joblib)** (872 bytes)
  - Liste des features originales du modèle
  - Ordre et noms exacts pour validation

#### Prédiction via API ([main.py:228-364](main.py:228))

**Workflow endpoint POST /predict :**

1. **Réception** : `PredictionRequest` avec 34 features
2. **Conversion** : Dictionnaire → pandas DataFrame
3. **Validation** : Vérification colonnes requises, ajout valeurs par défaut si manquantes
4. **Prédiction probabilité** : `model.predict_proba(df)[:, 1]` → float [0-1]
5. **Prédiction classe** : `model.predict(df)[0]` → int {0, 1}
6. **Mapping niveau de risque** :
   ```python
   if probability < 0.3:
       risk_level = "Faible"
   elif probability < 0.6:
       risk_level = "Moyen"
   elif probability < 0.8:
       risk_level = "Élevé"
   else:
       risk_level = "Très élevé"
   ```
7. **Réponse** : `PredictionResponse` avec `attrition_risk` (%), `probability`, `prediction`, `risk_level`

**Gestion des erreurs :**
- Modèle non chargé → HTTP 503 Service Unavailable
- Données invalides → HTTP 422 Unprocessable Entity
- Erreur prédiction → HTTP 500 Internal Server Error

---

## Installation et Développement Local

### Prérequis

- **Python 3.11** ([télécharger](https://www.python.org/downloads/))
- **Docker** + **Docker Compose** ([installer](https://docs.docker.com/get-docker/))
- **Git** + **Git LFS** ([installer](https://git-lfs.github.com/))
- **uv** package manager ([installer](https://github.com/astral-sh/uv))

### Démarrage Rapide

```bash
# 1. Cloner le repository
git clone git@github.com:Pltn-1321/api-attrition.git
cd api-attrition

# 2. Installer les dépendances
uv sync

# 3. Démarrer PostgreSQL (développement)
docker-compose up -d

# 4. Importer les données
uv run database/import_data.py

# 5. Lancer l'application complète (API + Streamlit)
uv run streamlit_launcher.py
```

**Points d'accès :**
- 🌐 **Interface Streamlit** : http://localhost:8501
- 🔌 **API FastAPI** : http://localhost:8000
- 📚 **Documentation API** : http://localhost:8000/docs (Swagger UI)

### Commandes de Développement

#### Gestion Application

```bash
# Full stack (recommandé) - Lance API + Streamlit avec health check
uv run streamlit_launcher.py

# API seule (pour debug)
uv run uvicorn main:app --reload --port 8000

# Streamlit seul (nécessite API démarrée)
uv run streamlit run app.py

# Arrêter l'application proprement
lsof -ti:8000,8501 | xargs kill -9
```

#### Gestion Base de Données

```bash
# PostgreSQL (Docker Compose)
docker-compose up -d              # Démarrer le container
docker-compose down               # Arrêter et supprimer
docker-compose logs -f db         # Voir les logs en temps réel
docker logs attrition_db          # Logs complets

# Accès direct psql
docker exec -it attrition_db psql -U attrition_user -d attrition_db

# Commandes SQL utiles
\dt                               # Lister tables
\d employees                      # Décrire table employees
SELECT COUNT(*) FROM employees;   # Compter les lignes

# Migration vers SQLite (pour production)
export DB_TYPE=sqlite
uv run database/migrate_to_sqlite.py
# Génère database.db avec les 294 employés
```

#### Qualité de Code

```bash
# Linting avec Ruff
ruff check .                      # Vérifier violations
ruff check . --fix                # Auto-fix violations

# Formatage avec Black
black . --line-length=100         # Formater tous les fichiers
black --check . --line-length=100 # Vérifier format (CI mode)
black app.py main.py              # Formater fichiers spécifiques

# Vérification complète (comme en CI)
ruff check . && black --check . --line-length=100
```

### Structure du Projet

```
api-attrition/
├── main.py                     # 🔹 FastAPI application (endpoints, model loading)
├── app.py                      # 🔹 Streamlit home page (dashboard)
├── streamlit_launcher.py       # 🔹 Dual-process launcher (orchestration)
├── config.py                   # Frontend configuration (API_URL, colors)
├── requirements.txt            # Production dependencies
├── pyproject.toml              # uv project config + dev dependencies
├── pytest.ini                  # pytest configuration
├── Dockerfile                  # Production container definition
├── docker-compose.yml          # Local PostgreSQL setup
│
├── api/
│   └── schemas.py              # Pydantic models (API request/response contracts)
│
├── database/
│   ├── config.py               # 🔹 DB connection (dual-backend switching)
│   ├── models.py               # SQLAlchemy ORM models (Employee class)
│   ├── import_data.py          # Script: CSV → PostgreSQL
│   └── migrate_to_sqlite.py   # Script: PostgreSQL → SQLite
│
├── utils/
│   ├── api_client.py           # 🔹 HTTP client for API communication
│   └── ui_components.py        # Reusable Streamlit UI components
│
├── pages/                      # Streamlit multi-page app (auto-discovery)
│   ├── 1_📊_Explorer.py        # Employee list with filters
│   ├── 2_🔍_Recherche.py       # Individual search by ID
│   ├── 3_📈_Statistiques.py    # Interactive visualizations
│   ├── 4_🎯_Prediction.py      # ML prediction interface
│   └── 9_🔧_Diagnostic.py      # System health diagnostics
│
├── data/
│   ├── dataset_employe.csv     # Full dataset (1,470 employees, training data)
│   └── export-api/
│       ├── test_employees.csv  # Test dataset (294 employees, production)
│       ├── attrition_model.joblib       # 🔹 Trained ML model (9 KB)
│       └── original_features.joblib     # Feature metadata (872 bytes)
│
├── tests/
│   ├── unit/                   # 8 unit tests (mocked dependencies)
│   │   ├── test_config.py      # Configuration validation
│   │   ├── test_api_client.py  # API client logic
│   │   ├── test_ml_model.py    # Model loading & predictions
│   │   └── test_ui_components.py
│   ├── functional/             # 5 functional tests (integration scenarios)
│   │   ├── test_prediction_api.py     # End-to-end prediction
│   │   ├── test_api_availability.py   # Health checks
│   │   └── test_app.py         # Streamlit app rendering
│   ├── conftest.py             # Shared fixtures (sample_employee_data_*)
│   └── fixtures/               # Test data files
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # 🔹 CI/CD pipeline (test + deploy jobs)
│
├── database.db                 # SQLite database (production, 43 KB)
├── CLAUDE.md                   # 🔹 Technical documentation for AI assistants
└── README.md                   # This file (academic project report)
```

**Légende :**
🔹 = Fichiers critiques pour comprendre l'architecture

---

## Tests et Assurance Qualité

### Stratégie de Tests

**Philosophie adoptée :**
- **Tests unitaires** : Logique isolée avec mocking des dépendances externes
- **Tests fonctionnels** : Scénarios d'intégration end-to-end (API + DB + Modèle)
- **Séparation des préoccupations** : Unit tests rapides (< 1s), functional tests plus lents (< 5s)
- **Coverage ciblé** : Modules core à 60%+, exclusion des UI pages et scripts

**Statistiques :**
- **Total** : 13 tests
- **Unit tests** : 8 (tests/unit/)
- **Functional tests** : 5 (tests/functional/)
- **Coverage** : 60%+ sur modules core
- **Modules couverts** : `utils.api_client`, `api.schemas`, `database.models`, `database.config`, `main`
- **Exclusions** : `pages/`, `app.py`, scripts de migration, `streamlit_launcher.py`

### Suites de Tests

#### Tests Unitaires (8 tests) - [tests/unit/](tests/unit/)

**1. [test_config.py](tests/unit/test_config.py) (3 tests)**
- ✅ Configuration par défaut (`API_URL`, `DB_TYPE`)
- ✅ Override via variables d'environnement
- ✅ Validation Dockerfile environment variables

**2. [test_api_client.py](tests/unit/test_api_client.py) (2 tests)**
- ✅ `APIClient.health_check()` avec mocking httpx
- ✅ `APIClient.get_employees()` avec pagination

**3. [test_ml_model.py](tests/unit/test_ml_model.py) (2 tests)**
- ✅ Chargement `attrition_model.joblib` sans erreur
- ✅ Prédictions cohérentes (probability [0-1], risk_level mapping)
- ✅ Performance latency < 100ms par prédiction

**4. [test_ui_components.py](tests/unit/test_ui_components.py) (1 test)**
- ✅ `render_metric_card()` génère HTML valide
- ✅ `render_employee_card()` affiche toutes les données

#### Tests Fonctionnels (5 tests) - [tests/functional/](tests/functional/)

**1. [test_prediction_api.py](tests/functional/test_prediction_api.py) (2 tests)**
- ✅ Endpoint `POST /predict` retourne `PredictionResponse` valide
- ✅ Gestion erreurs : modèle manquant → 503, données invalides → 422

**2. [test_api_availability.py](tests/functional/test_api_availability.py) (2 tests)**
- ✅ `GET /health` répond en < 2 secondes
- ✅ Dockerfile configure `API_URL=http://localhost:8000`
- ✅ Startup sequence timing (API ready in < 30s)

**3. [test_app.py](tests/functional/test_app.py) (1 test)**
- ✅ Page Streamlit se rend sans erreur
- ✅ API client initialisé en session_state

#### Fixtures de Test - [tests/conftest.py](tests/conftest.py)

```python
@pytest.fixture
def sample_employee_data_low_risk():
    """Profil faible risque : satisfaction élevée, ancienneté longue"""
    return {
        "age": 45,
        "satisfaction_moyenne": 3.5,
        "annees_dans_l_entreprise": 10,
        "revenu_mensuel": 5500,
        # ... 30 autres champs
    }

@pytest.fixture
def sample_employee_data_high_risk():
    """Profil haut risque : satisfaction faible, burnout, sous-payé"""
    return {
        "age": 28,
        "satisfaction_moyenne": 1.2,
        "parent_burnout": 4,
        "sous_paye_niveau_dept": 1,
        # ... 30 autres champs
    }

@pytest.fixture
def ml_model():
    """Modèle ML chargé pour tests unitaires"""
    return joblib.load("data/export-api/attrition_model.joblib")
```

### Exécution des Tests

```bash
# Tous les tests avec coverage (13 tests)
pytest

# Tests unitaires seulement (rapide, 8 tests)
pytest tests/unit -v

# Tests fonctionnels seulement (integration, 5 tests)
pytest tests/functional -v

# Tests spécifiques par marker
pytest -m ml -v                   # Tests modèle ML
pytest -m api -v                  # Tests API
pytest -m unit -v                 # Tous les tests unitaires
pytest -m functional -v           # Tous les tests fonctionnels

# Coverage report complet (HTML + terminal)
pytest --cov=utils.api_client --cov=api --cov=database --cov=main \
       --cov-report=html --cov-report=term-missing --cov-fail-under=60

# Ouvrir rapport HTML dans navigateur
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Tests avec output verbeux
pytest -vv --tb=short

# Tests en parallèle (nécessite pytest-xdist)
pytest -n auto
```

### Qualité de Code

**Outils utilisés :**

| Outil | Version | Rôle | Configuration |
|-------|---------|------|---------------|
| **Ruff** | ≥0.14.10 | Linter ultra-rapide (Rust) | Remplace flake8, isort, pylint |
| **Black** | ≥25.12.0 | Code formatter opinionated | `--line-length=100` |
| **pytest-cov** | 4.1.0 | Mesure de couverture | Rapports XML, HTML, terminal |
| **pytest-mock** | ≥3.15.1 | Mocking simplifié | Wrapper de unittest.mock |

**Automatisation en CI :**
- ✅ Ruff check à chaque commit (job `test`)
- ✅ Black format validation (pas de code mal formatté autorisé)
- ✅ Tests + coverage comme quality gate (échec si < 60%)
- ✅ Rapports uploadés sur Codecov + GitHub Artifacts

**Commandes CI reproduites localement :**

```bash
# Validation complète (comme en CI)
uv run ruff check . --output-format=github && \
uv run black --check . --line-length=100 && \
uv run pytest tests/ \
  --cov=utils.api_client --cov=api --cov=database --cov=main \
  --cov-report=xml --cov-report=html --cov-report=term-missing \
  --cov-fail-under=60
```

---

## Pipeline CI/CD

### Vue d'Ensemble

**Workflow :** [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)

**Déclencheurs :**
- ✅ Push sur branches `main` ou `dev`
- ✅ Pull requests vers `main` ou `dev`
- ✅ Manual dispatch (GitHub Actions UI)
- ✅ Filtres de paths (ignore docs, README.md, etc.)

**Architecture 2 Jobs :**

```
┌─────────────────────┐
│   Job 1: test       │  (Toujours exécuté)
│   Ubuntu Latest     │  • Lint (Ruff, Black)
│   Python 3.11       │  • 13 tests
│                     │  • Coverage ≥60%
└──────────┬──────────┘
           │ success required
           ↓
┌─────────────────────┐
│   Job 2: deploy     │  (Si main + push seulement)
│   Ubuntu Latest     │  • Git push → HF Spaces
│                     │  • Deploy summary
└─────────────────────┘
```

### Job 1: Tests & Quality (18 étapes)

**Environnement :**
- **OS** : Ubuntu Latest
- **Python** : 3.11
- **Package manager** : uv
- **Cache** : uv dependencies (~/.cache/uv)

**Étapes principales :**

1-5. **Setup**
   - Checkout code (actions/checkout@v4)
   - Setup Python 3.11 (actions/setup-python@v5)
   - Cache uv dependencies (actions/cache@v4)
   - Install uv (astral-sh/setup-uv@v3)
   - Install dependencies (`uv sync` + dev deps)

6-7. **Code Quality**
   ```bash
   # Lint with Ruff
   uv run ruff check . --output-format=github

   # Check formatting with Black
   uv run black --check . --line-length=100
   ```

8. **Validate Configuration**
   - Vérifier `ENV API_URL=http://localhost:8000` dans Dockerfile
   - Vérifier `ENV DB_TYPE=sqlite` dans Dockerfile
   - Exit 1 si configuration manquante ou incorrecte

9-14. **Tests Séquentiels** (sans coverage pour rapidité)
   ```bash
   # Configuration tests
   uv run pytest tests/unit/test_config.py -v --tb=short --no-cov

   # ML Model tests
   uv run pytest tests/unit/test_ml_model.py -v --tb=short -m ml --no-cov

   # ML Model compatibility check
   python -c "import joblib, sklearn; ..."

   # API tests
   uv run pytest tests/functional/test_prediction_api.py -v -m api --no-cov

   # All unit tests
   uv run pytest tests/unit/ -v -m unit --no-cov

   # All functional tests
   uv run pytest tests/functional/ -v -m functional --no-cov
   ```

15. **Generate Comprehensive Coverage Report**
   ```bash
   pytest tests/ \
     --cov=utils.api_client \
     --cov=api \
     --cov=database.models \
     --cov=database.config \
     --cov=main \
     --cov-report=xml \
     --cov-report=html \
     --cov-report=term-missing \
     --cov-fail-under=60
   ```

16-18. **Upload Artifacts**
   - Upload coverage to Codecov (codecov/codecov-action@v4)
   - Upload HTML coverage report (retention: 30 days)
   - Upload test results (retention: 7 days)

**Quality Gates (échec du job si) :**
- ❌ Ruff trouve des violations de style
- ❌ Code mal formatté (Black)
- ❌ Configuration Dockerfile invalide
- ❌ Un seul test échoue (sur 13)
- ❌ Coverage < 60%

### Job 2: Deploy to Hugging Face Spaces

**Conditions d'exécution :**
- `needs: test` (succès requis)
- `if: github.ref == 'refs/heads/main' && github.event_name == 'push'`

**Étapes :**

1. **Checkout code**
   - Avec `lfs: true` (Git Large File Storage)
   - Avec `fetch-depth: 0` (historique complet)

2. **Configure Git**
   ```bash
   git config --global user.email "github-actions[bot]@users.noreply.github.com"
   git config --global user.name "GitHub Actions"
   ```

3. **Push to Hugging Face Spaces**
   ```bash
   git remote add hf https://huggingface.co/spaces/Pedro1321/Api-Technova || true
   git push -f https://oauth2:${HF_TOKEN}@huggingface.co/spaces/Pedro1321/Api-Technova HEAD:main
   ```
   - Secret : `HF_TOKEN` (stocké dans GitHub Secrets)
   - Force push : `-f` (overwrite HF Spaces branch)

4-5. **Deployment Summary**
   - Success : Message avec URL + timestamp dans GitHub Step Summary
   - Failure : Message d'erreur dans Step Summary

### Monitoring et Artifacts

**Artifacts générés :**
| Artifact | Retention | Taille | Usage |
|----------|-----------|--------|-------|
| HTML coverage report | 30 jours | ~500 KB | Téléchargeable depuis GitHub Actions |
| Test results cache | 7 jours | ~50 KB | Cache pytest |

**Intégrations externes :**
- **Codecov** : Coverage tracking + badge + PR comments
- **GitHub Actions badge** : Status CI/CD dans README
- **HF Spaces** : Auto-rebuild après push

**URLs Monitoring :**
- 🔄 **Pipeline** : https://github.com/Pltn-1321/api-attrition/actions
- 📊 **Codecov** : https://codecov.io/gh/Pltn-1321/api-attrition
- 🚀 **HF Spaces** : https://huggingface.co/spaces/Pedro1321/Api-Technova

---

## Déploiement Production

### Architecture de Production - Hugging Face Spaces

L'application est déployée sur Hugging Face Spaces dans un **conteneur Docker unique** hébergeant deux processus qui communiquent via localhost.

```
┌─────────────────────────────────────────────────┐
│   Docker Container (HF Spaces)                  │
│   Image: python:3.11-slim                       │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Process 1: FastAPI (port 8000)          │  │
│  │ └─ Uvicorn main:app --host 0.0.0.0     │  │
│  │                                          │  │
│  │ • API REST (6 endpoints)                │  │
│  │ • Modèle ML chargé au démarrage         │  │
│  │ • Base SQLite (database.db)             │  │
│  │ • Logging structuré                     │  │
│  │ • NON exposé à Internet                 │  │
│  └──────────────────────────────────────────┘  │
│                    ↑                            │
│                    │ localhost:8000             │
│                    │ (communication interne)    │
│                    │                            │
│  ┌──────────────────────────────────────────┐  │
│  │ Process 2: Streamlit (port 7860)        │  │
│  │ └─ streamlit run app.py                 │  │
│  │                                          │  │
│  │ • 5 pages interactives                  │  │
│  │ • Visualisations Plotly                 │  │
│  │ • API Client → localhost:8000           │  │
│  │ • Session state management              │  │
│  │ • EXPOSÉ à Internet                     │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  Port 7860 → Internet (users)                  │
│  (Seul point d'accès public)                   │
└─────────────────────────────────────────────────┘
```

**Rationale Architecture :**
- ✅ **Simplicité** : Un seul container à gérer, pas d'orchestration complexe
- ✅ **Coût** : Pas de service BDD externe, pas de load balancer
- ✅ **Performance** : Communication localhost (latence < 1ms), pas de réseau
- ✅ **Sécurité** : API non exposée directement, reverse proxy implicite
- ✅ **Déploiement** : Git push → rebuild automatique, zero-downtime

### Séquence de Démarrage

**Orchestration par [streamlit_launcher.py](streamlit_launcher.py) :**

```
1. Container starts
   └─ CMD ["python", "streamlit_launcher.py"]

2. Check port 8000 availability
   └─ Kill existing process if occupied

3. Start FastAPI subprocess
   └─ subprocess.Popen(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])
   └─ Output: "✅ API démarrée sur http://localhost:8000"

4. Health check loop (max 30 retries × 1s interval)
   ├─ GET http://localhost:8000/health
   ├─ If fail: retry (log progress every 5s)
   └─ If success: break
   └─ Output: "✅ API est prête ! (démarrage en Xs)"

5. Check port 7860/8501 availability
   └─ Kill existing process if occupied

6. Start Streamlit subprocess
   └─ subprocess.Popen(["streamlit", "run", "app.py", "--server.port", PORT])
   └─ Output: "✅ Streamlit démarré sur http://localhost:7860"

7. Wait for both subprocesses
   └─ Handle Ctrl+C for graceful shutdown

8. Application Ready!
   └─ Users can access https://huggingface.co/spaces/Pedro1321/Api-Technova
```

**Gestion des erreurs :**
- **Timeout API (30s)** : Warning + continue → Streamlit affichera bouton retry
- **Port occupé** : Kill process existant → restart
- **Ctrl+C** : Terminate subprocesses → cleanup
- **Model load failure** : API démarre mais retourne 503 sur /predict

### Configuration Environnement

**Dockerfile Environment Variables ([Dockerfile:22-26](Dockerfile:22)) :**

```dockerfile
ENV STREAMLIT_SERVER_PORT=7860          # ⚠️ HF Spaces requirement (not 8501)
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0    # Bind all interfaces
ENV STREAMLIT_SERVER_HEADLESS=true      # No browser auto-open
ENV API_URL=http://localhost:8000       # ⚠️ CRITICAL: same container communication
ENV DB_TYPE=sqlite                       # Lightweight embedded database
```

**Justifications techniques :**
- `STREAMLIT_SERVER_PORT=7860` : Port standard HF Spaces (configurable dans Space settings)
- `API_URL=localhost:8000` : Les deux processus sont **dans le même container**, donc localhost est correct
- `DB_TYPE=sqlite` : Pas besoin de PostgreSQL cloud, database.db est committé dans le repo
- `HEADLESS=true` : Pas d'environnement graphique en production

**Variables d'environnement dynamiques :**
- Développement local : `API_URL=http://localhost:8000` (par défaut)
- Production HF Spaces : `API_URL=http://localhost:8000` (même container)
- Déploiements séparés : `API_URL=https://api.example.com` (override)

### Processus de Déploiement

#### Configuration Initiale (One-Time Setup)

**1. Créer compte Hugging Face**
   - Aller sur https://huggingface.co/join
   - Compléter le profil

**2. Générer Access Token**
   - Settings → [Access Tokens](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Name: `github-actions-deploy`
   - Permission: **Write** (required for git push)
   - Copier le token : `hf_xxxxxxxxxxxxxxxxxxxxx`

**3. Ajouter Secret GitHub**
   - Repository → Settings → [Secrets and variables](../../settings/secrets/actions) → Actions
   - Click "New repository secret"
   - Name: `HF_TOKEN`
   - Value: (coller le token HF)
   - Click "Add secret"

**4. Créer Space sur Hugging Face**
   - Aller sur https://huggingface.co/new-space
   - Owner: `Pedro1321`
   - Space name: `Api-Technova`
   - License: MIT
   - SDK: **Docker**
   - Visibility: Public
   - Click "Create Space"

#### Déploiement Automatique

**Chaque push sur `main` déclenche :**

```bash
# Développeur local
git add .
git commit -m "feat: nouvelle fonctionnalité prédiction"
git push origin main

# → GitHub Actions workflow triggered
#   1. Checkout code
#   2. Run Ruff linting ✓
#   3. Run Black formatting check ✓
#   4. Validate Dockerfile configuration ✓
#   5. Run 13 tests ✓
#   6. Generate coverage report (60%+) ✓
#   7. Upload to Codecov ✓
#   8. Deploy job starts (if all above passed)
#   9. Git push to HF Spaces
#  10. HF Spaces rebuilds Docker image
#  11. Container restarts with new code
#  12. Application available in ~2-3 minutes
```

**Vérification déploiement :**
- GitHub Actions : Check job "deploy" status (vert = succès)
- HF Spaces : Onglet "Logs" pour voir rebuild + startup
- Application : Refresh https://huggingface.co/spaces/Pedro1321/Api-Technova

#### Déploiement Manuel

**Via GitHub Actions UI :**
1. Repository → Actions → "CI/CD Pipeline"
2. Click "Run workflow"
3. Select branch `main`
4. Click "Run workflow"

**Force redeploy (sans changement de code) :**

```bash
git commit --allow-empty -m "chore: force redeploy"
git push origin main
```

### URLs de Production

| Ressource | URL | Description |
|-----------|-----|-------------|
| **Application Live** | https://huggingface.co/spaces/Pedro1321/Api-Technova | Interface Streamlit publique |
| **Repository Source** | https://github.com/Pltn-1321/api-attrition | Code source complet |
| **CI/CD Pipeline** | https://github.com/Pltn-1321/api-attrition/actions | Workflows GitHub Actions |
| **Coverage Report** | https://codecov.io/gh/Pltn-1321/api-attrition | Rapports de couverture |
| **HF Spaces Settings** | https://huggingface.co/spaces/Pedro1321/Api-Technova/settings | Configuration Space |

---

## Troubleshooting & FAQ

### Erreur 503: Service Unavailable

**Symptôme :**
```
503 Server Error: Service Unavailable for url: http://localhost:8000/...
streamlit.errors.StreamlitAPIException: ...
```

**Cause racine :**
FastAPI n'a pas encore terminé son démarrage quand Streamlit tente de se connecter. Le modèle ML peut prendre 5-10 secondes à charger sur des machines lentes.

**Solutions :**

1. **Attendre et réessayer** (le plus courant)
   - L'application implémente un **retry automatique** (30 secondes)
   - Cliquer sur le bouton **"🔄 Réessayer la connexion"** dans l'interface Streamlit
   - Attendre que le message "✅ API est prête !" apparaisse

2. **Vérifier les logs Hugging Face Spaces**
   - Aller sur https://huggingface.co/spaces/Pedro1321/Api-Technova
   - Cliquer sur l'onglet **"Logs"**
   - Chercher les messages :
     ```
     ✅ API démarrée sur http://localhost:8000
     ✅ API est prête ! (démarrage en Xs)
     ```
   - Si absent : erreur de démarrage du modèle (voir logs d'erreur)

3. **Vérifier configuration locale**
   ```bash
   # Ports libres?
   lsof -i:8000  # Doit être vide ou montrer "Python main.py"
   lsof -i:8501  # Doit être vide ou montrer "streamlit"

   # Si occupés par autre chose
   lsof -ti:8000,8501 | xargs kill -9

   # Redémarrage propre
   uv run streamlit_launcher.py
   ```

**Prévention :**
Le `streamlit_launcher.py` inclut désormais un health check avec **30 retries × 1s**. Si votre machine est lente, augmenter `max_retries` :

```python
# streamlit_launcher.py:139
api_ready = wait_for_api(API_PORT, max_retries=30, retry_interval=1)
# Augmenter à 60 pour machines lentes
api_ready = wait_for_api(API_PORT, max_retries=60, retry_interval=1)
```

### Erreur: Configuration API_URL Incorrecte

**Symptôme :**
```
Connection timeout
httpx.ConnectError: [Errno 61] Connection refused
```

**Root cause :**
Variable d'environnement `API_URL` pointe vers une URL invalide ou inaccessible.

**Configuration correcte :**

| Environnement | API_URL | Raison |
|---------------|---------|--------|
| **Local dev** | `http://localhost:8000` | Default, API et Streamlit sur même machine |
| **HF Spaces** | `http://localhost:8000` | **Critique** : même container, communication localhost |
| **Déploiements séparés** | `https://api.example.com` | API et Streamlit sur serveurs différents |

**Vérification :**

```bash
# Test configuration
pytest tests/unit/test_config.py -v

# Vérifier Dockerfile
grep "ENV API_URL" Dockerfile
# Expected output: ENV API_URL=http://localhost:8000

# Vérifier variable d'environnement locale
echo $API_URL
# Expected: http://localhost:8000 ou vide (utilise default)
```

### Tests de Coverage Échouent en CI

**Problème :**
```
FAIL Required test coverage of 60% not reached. Total coverage: 42.31%
```

**Root cause :**
Coverage calculé sur fichiers individuels au lieu de l'ensemble du projet.

**Solution :**
Toujours exécuter **TOUS** les tests ensemble pour coverage complet :

```bash
# ✅ Correct - coverage complète
pytest tests/ \
  --cov=utils.api_client \
  --cov=api \
  --cov=database \
  --cov=main

# ❌ Incorrect - coverage partielle
pytest tests/unit/test_ml_model.py --cov=main
# Résultat: Seulement les lignes de main.py touchées par ce test
```

**Reproduction locale du CI :**

```bash
# Commande exacte du CI
uv run pytest tests/ \
  --cov=utils.api_client \
  --cov=api \
  --cov=database.models \
  --cov=database.config \
  --cov=main \
  --cov-report=xml \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=60
```

### Déploiement Automatique N'est Pas Déclenché

**Checklist de diagnostic :**

- [ ] **Secret HF_TOKEN configuré dans GitHub Secrets ?**
  - Repository → Settings → Secrets and variables → Actions
  - Doit exister un secret nommé exactement `HF_TOKEN`

- [ ] **Push sur branche `main` (pas `dev`) ?**
  - Vérifier : `git branch --show-current`
  - Le job `deploy` ne s'exécute QUE sur `main`

- [ ] **Tous les tests passent dans job `test` ?**
  - Check GitHub Actions : job "test" doit être vert
  - Si rouge : corriger erreurs avant que deploy ne puisse s'exécuter

- [ ] **Dockerfile est valide ?**
  - Test local : `docker build -t test .`
  - Doit builder sans erreur

- [ ] **URL HF Spaces correcte dans [ci-cd.yml](.github/workflows/ci-cd.yml:182) ?**
  - Vérifier ligne 182 : `git push -f https://oauth2:${HF_TOKEN}@huggingface.co/spaces/Pedro1321/Api-Technova HEAD:main`
  - Remplacer `Pedro1321/Api-Technova` par votre espace

### Outils de Diagnostic

#### Tests de Configuration

```bash
# Valider configuration complète
pytest tests/unit/test_config.py -v

# Valider API availability
pytest tests/functional/test_api_availability.py -v

# Tester Dockerfile environment variables
docker run --rm api-attrition env | grep -E "(API_URL|DB_TYPE|STREAMLIT)"
```

#### Page Diagnostic Streamlit

1. Naviguer vers **"🔧 Diagnostic"** dans la sidebar
2. Quick Status Checks :
   - ✅ API Health → Check `/health` endpoint
   - ✅ ML Model Status → Verify model loaded
   - ✅ Prediction Test → End-to-end test
3. System Information :
   - API URL configuré
   - Timeout settings
   - Latency measurement
4. Guide de troubleshooting intégré

#### Logs Hugging Face Spaces

- **Accès** : https://huggingface.co/spaces/Pedro1321/Api-Technova → Onglet "Logs"
- **Temps réel** : Les logs s'affichent en temps réel pendant rebuild
- **Output complet** : Voir stdout/stderr des deux processus

**Messages clés à chercher :**
```
✅ API démarrée sur http://localhost:8000
✅ API est prête ! (démarrage en Xs)
✅ Streamlit démarré sur http://localhost:7860
```

---

## Réflexions et Perspectives

### Défis Surmontés

#### Challenge 1: Dual Database Support

**Problème :**
Nécessité de développer localement avec PostgreSQL (pour apprendre une vraie base relationnelle) mais déployer sur HF Spaces avec SQLite (pour simplicité et coût zéro).

**Solution implémentée :**
Pattern environment-based configuration avec variable `DB_TYPE` :

```python
# database/config.py
DB_TYPE = os.getenv("DB_TYPE", "sqlite")

if DB_TYPE == "postgres":
    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(DATABASE_URL)
else:
    DATABASE_URL = "sqlite:///./database.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

**Apprentissage :**
Les couches d'abstraction (ORM SQLAlchemy) permettent de switcher de backend sans changer le code métier. Importance de tester dans l'environnement de production (SQLite) avant déploiement.

#### Challenge 2: Erreur 503 sur Hugging Face Spaces

**Problème :**
Streamlit se connectait à l'API **avant** que FastAPI ait fini de charger le modèle ML (9 KB mais désérialisation lente). Résultat : 503 Service Unavailable au premier chargement.

**Solution implémentée :**
Health check retry logic dans `streamlit_launcher.py` :

```python
def wait_for_api(port, max_retries=30, retry_interval=1):
    for i in range(max_retries):
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                return True
        except:
            time.sleep(retry_interval)
    return False

api_ready = wait_for_api(8000)
if not api_ready:
    print("⚠️ Warning: API not ready, but continuing...")
```

**Apprentissage :**
Les systèmes distribués nécessitent une gestion **graceful** du startup. Principe : "Expect failures, design for resilience". Ajout de timeouts, retries, et fallbacks.

#### Challenge 3: Compatibilité Modèle ML

**Problème :**
Modèle entraîné avec scikit-learn 1.3.2 (Projet 4) ne se chargeait pas avec scikit-learn 1.5.0 (CI/CD auto-install). Erreur : `AttributeError: 'RandomForestClassifier' object has no attribute 'n_features_in_'`.

**Solution implémentée :**
- Pin exact version dans `requirements.txt` : `scikit-learn==1.7.1`
- Validation en CI : étape dédiée qui charge le modèle et vérifie compatibilité
- Logging amélioré au démarrage de l'API avec version scikit-learn

**Apprentissage :**
La reproductibilité ML exige un **versioning strict** de TOUTES les dépendances. Utiliser des outils comme Poetry, pipenv ou uv pour lock versions. Tester le chargement du modèle en CI avant déploiement.

#### Challenge 4: Coverage Variable entre Local et CI

**Problème :**
Coverage à 72% en local mais 45% en CI. Cause : pytest-cov calculait différemment selon l'ordre d'exécution des tests.

**Solution implémentée :**
Séparation exécution tests (sans coverage) et rapport final (avec coverage) :

```yaml
# CI - Run tests WITHOUT coverage (fast)
- name: Run Unit Tests
  run: pytest tests/unit/ -v --no-cov

- name: Run Functional Tests
  run: pytest tests/functional/ -v --no-cov

# CI - Generate comprehensive coverage report (once)
- name: Generate comprehensive coverage report
  run: pytest tests/ --cov=utils --cov=api --cov=database --cov=main
```

**Apprentissage :**
Les pipelines CI doivent être **déterministes**. Éviter les side effects, utiliser des seeds, tester localement avec `--no-cache-dir`.

### Compétences Renforcées

**Avant Projet 5 (acquis en Projet 4) :**
- Analyse exploratoire de données (pandas, seaborn)
- Feature engineering et sélection de variables
- Entraînement de modèles ML (RandomForest, GridSearchCV)
- Validation et métriques (accuracy, precision, recall, F1)

**Après Projet 5 (nouvelles compétences maîtrisées) :**

| Catégorie | Compétences | Preuve de Maîtrise |
|-----------|-------------|-------------------|
| **Backend Development** | Conception API REST, async/await, validation Pydantic | 6 endpoints, OpenAPI docs, error handling |
| **Frontend Development** | Multi-page apps, state management, visualisations | 5 pages Streamlit, Plotly charts |
| **Database Engineering** | ORM SQLAlchemy, migrations, dual-backend pattern | PostgreSQL ↔ SQLite switching |
| **DevOps** | CI/CD GitHub Actions, Docker multi-stage builds | 2-job workflow, automated deploy |
| **Cloud Deployment** | Containerization, environment-based config, monitoring | HF Spaces, health checks, logs |
| **Software Testing** | Unit tests, functional tests, mocking, fixtures | 13 tests, 60%+ coverage, pytest |
| **Code Quality** | Linting, formatting, pre-commit hooks | Ruff, Black, automated validation |
| **Documentation** | Technical writing, README, inline docs | README académique, CLAUDE.md |
| **Troubleshooting** | Debugging production issues, log analysis | 503 error resolution, diagnostic page |

### Améliorations Futures

#### Roadmap Technique

**Fonctionnalités API :**
- [ ] **Filtres avancés** sur `GET /employees` (par département, poste, âge, satisfaction)
- [ ] **Authentification JWT** avec roles (admin, RH, manager)
- [ ] **Rate limiting** pour éviter abus (ex: max 100 req/min par IP)
- [ ] **Versioning API** (`/v1/employees`, `/v2/employees`)
- [ ] **Webhooks** pour notifications temps réel (employé à haut risque)
- [ ] **Export bulk** (CSV, Excel, JSON) via endpoint `/employees/export`

**Machine Learning :**
- [ ] **Versioning modèle** (A/B testing entre `model_v1.joblib` et `model_v2.joblib`)
- [ ] **Monitoring prédictions** (dashboard métriques : latency, accuracy, drift)
- [ ] **Retraining automatique** (trigger si drift détecté ou nouvelle data)
- [ ] **Explainability** (SHAP values pour expliquer prédictions)
- [ ] **Feature importance** (afficher top 10 features dans UI)

**Frontend :**
- [ ] **Dashboard RH avancé** (tendances attrition, départements à risque)
- [ ] **Notifications push** (alertes pour nouveaux employés haut risque)
- [ ] **Export rapports PDF** (profil employé + prédiction)
- [ ] **Mode dark** (toggle dans sidebar)
- [ ] **Multilingue** (FR/EN avec i18n)

#### Architecture Evolution

**Scalabilité :**
- Séparer containers API et Streamlit (déploiement indépendant)
- Load balancer (NGINX) devant plusieurs instances API
- Cache Redis pour requêtes fréquentes (`GET /employees`)
- PostgreSQL production (AWS RDS ou GCP Cloud SQL)
- Horizontal scaling avec Kubernetes

**Observabilité :**
- Logs centralisés (ELK stack ou Datadog)
- Métriques applicatives (Prometheus + Grafana)
- Distributed tracing (OpenTelemetry)
- Alertes (PagerDuty si API down > 5min)

**Sécurité :**
- HTTPS obligatoire (certificats Let's Encrypt)
- Secrets management (HashiCorp Vault)
- OWASP Top 10 compliance
- Audit logs (qui a accédé à quel employé quand)

#### Testing Enhancements

**Coverage :**
- Augmenter à **80%+** (inclure pages Streamlit)
- Tests d'intégration avec vraies bases de données (testcontainers)
- Tests de propriétés (Hypothesis)

**Performance :**
- Load testing (Locust, JMeter) : 100 req/s sans dégradation
- Latency tests : p95 < 200ms, p99 < 500ms
- Memory leak detection (profiling avec memory_profiler)

**End-to-End :**
- Tests browser avec Selenium ou Playwright
- Screenshots automatiques de chaque page
- Visual regression testing

---

## Références et Ressources

### Documentation Officielle

**Technologies Utilisées :**

| Technology | Documentation | Utilisation Projet |
|------------|---------------|-------------------|
| **FastAPI** | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) | Framework API, endpoints, validation Pydantic |
| **Streamlit** | [docs.streamlit.io](https://docs.streamlit.io/) | Multi-page app, visualisations, session state |
| **SQLAlchemy** | [docs.sqlalchemy.org](https://docs.sqlalchemy.org/) | ORM, modèles, migrations, dual-backend |
| **Hugging Face Spaces** | [hf.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces) | Déploiement Docker, configuration, logs |
| **GitHub Actions** | [docs.github.com/actions](https://docs.github.com/en/actions) | CI/CD workflow, jobs, secrets |
| **Docker** | [docs.docker.com](https://docs.docker.com/) | Containerization, Dockerfile, multi-stage builds |
| **pytest** | [docs.pytest.org](https://docs.pytest.org/) | Testing framework, fixtures, parametrize |
| **scikit-learn** | [scikit-learn.org](https://scikit-learn.org/) | ML model, predict(), predict_proba() |
| **Plotly** | [plotly.com/python](https://plotly.com/python/) | Graphiques interactifs, charts, visualisations |
| **Pydantic** | [docs.pydantic.dev](https://docs.pydantic.dev/) | Validation schémas, BaseModel, type hints |

### Documentation Interne Projet

- **[CLAUDE.md](CLAUDE.md)** - Guide technique complet pour assistants IA
  - Architecture détaillée (two-tier, dual-database)
  - Troubleshooting production (503 errors, startup sequence)
  - Configuration environnements (API_URL, DB_TYPE)
  - Patterns de conception (singleton, factory, dependency injection)

- **[.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)** - Pipeline CI/CD complet
  - Job test : 18 étapes (lint, tests, coverage)
  - Job deploy : Git push vers HF Spaces
  - Quality gates et artifacts

- **[Dockerfile](Dockerfile)** - Définition container production
  - Python 3.11-slim base image
  - Multi-process (FastAPI + Streamlit)
  - Environment variables

- **[pyproject.toml](pyproject.toml)** - Configuration uv + dépendances
  - Production dependencies
  - Dev dependencies (ruff, black, pytest)

### Ressources Pédagogiques

**OpenClassroom :**
- [Parcours AI Engineer](https://openclassrooms.com/fr/paths/ai-engineer)
- Projet 4 : "Développez un modèle de scoring" (ML model development)
- Projet 5 : "Déployez un modèle dans le cloud" (production deployment)

**Python & Frameworks :**
- [Python 3.11 Documentation](https://docs.python.org/3.11/)
- [Real Python - FastAPI Tutorials](https://realpython.com/fastapi-python-web-apis/)
- [Streamlit Gallery](https://streamlit.io/gallery) - Exemples d'applications

**Bases de Données :**
- [PostgreSQL 15 Documentation](https://www.postgresql.org/docs/15/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLAlchemy Tutorials](https://docs.sqlalchemy.org/en/20/tutorial/)

**DevOps & Cloud :**
- [GitHub Actions - CI/CD Best Practices](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [The Twelve-Factor App](https://12factor.net/) - Méthodologie app cloud-native

---

## License et Crédits

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour détails.

```
Copyright (c) 2025 ppluton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
...
```

### Auteur

**Projet Académique OpenClassroom**

- **Étudiant** : ppluton
- **Parcours** : [AI Engineer](https://openclassrooms.com/fr/paths/ai-engineer)
- **Projet** : P5 - Déploiement Production API Attrition
- **Période** : Décembre 2025
- **Mentor** : OpenClassroom
- **GitHub** : [@Pltn-1321](https://github.com/Pltn-1321)

### Remerciements

**Formation et Encadrement :**
- [OpenClassroom](https://openclassrooms.com/) pour le framework pédagogique et l'accompagnement
- Mentors et évaluateurs pour les retours constructifs

**Cas d'Affaires :**
- Technova (entreprise fictive) pour le dataset et la problématique RH

**Communautés Open-Source :**
- [FastAPI](https://github.com/tiangolo/fastapi) - Sebastián Ramírez (tiangolo) pour le framework API moderne
- [Streamlit](https://github.com/streamlit/streamlit) - Streamlit Inc. pour le framework frontend Python-native
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) - Mike Bayer pour l'ORM puissant
- [pytest](https://github.com/pytest-dev/pytest) - Holger Krekel et contributeurs pour le framework de tests
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) - Communauté scikit-learn pour les outils ML

**Plateformes :**
- [Hugging Face](https://huggingface.co/) pour Spaces (hébergement gratuit ML apps)
- [GitHub](https://github.com/) pour le versioning et GitHub Actions
- [Codecov](https://codecov.io/) pour le tracking de coverage

**Inspiration et Ressources :**
- Documentation officielle de chaque technologie
- Stack Overflow et communautés techniques
- Blogs techniques et tutoriels open-source

---

<p align="center">
  <strong>📊 Projet réalisé dans le cadre du parcours AI Engineer OpenClassroom</strong><br>
  <em>Démonstration de compétences full-stack : ML → API → Frontend → CI/CD → Production</em>
</p>

<p align="center">
  <a href="https://huggingface.co/spaces/Pedro1321/Api-Technova">🚀 Demo Live</a> •
  <a href="https://github.com/Pltn-1321/api-attrition">💻 Code Source</a> •
  <a href="https://codecov.io/gh/Pltn-1321/api-attrition">📈 Coverage</a> •
  <a href="CLAUDE.md">📚 Documentation Technique</a>
</p>
