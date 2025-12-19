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
  - data-science
  - analytics
  - fastapi
  - streamlit
---

# API Attrition

[![codecov](https://codecov.io/gh/Pltn-1321/api-attrition/branch/main/graph/badge.svg)](https://codecov.io/gh/Pltn-1321/api-attrition)
[![CI/CD](https://github.com/Pltn-1321/api-attrition/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/Pltn-1321/api-attrition/actions)

API FastAPI pour la prédiction d'attrition des employés avec machine learning.

**Stack** : FastAPI · PostgreSQL/SQLite · SQLAlchemy · Streamlit · Scikit-learn · Docker

**Déploiement** : GitHub Actions · Hugging Face Spaces · CI/CD

## Démarrage Rapide

```bash
# 1. Cloner et installer
git clone git@github.com:Pltn-1321/api-attrition.git
cd api-attrition
uv add pandas sqlalchemy psycopg2-binary fastapi uvicorn streamlit

# 2. Démarrer PostgreSQL
docker-compose up -d

# 3. Importer les données (294 employés)
uv run database/import_data.py

# 4. Lancer l'application (API + Interface)
uv run streamlit_launcher.py
```

**URLs** :
- Interface : http://localhost:8501
- API : http://localhost:8000
- Docs API : http://localhost:8000/docs

## 🧪 Tests

### Structure des Tests
```
tests/
├── unit/                    # Tests unitaires (logique isolée)
│   └── test_ml_model.py    # Tests modèle ML et calculs
├── functional/             # Tests fonctionnels (scénarios complets)
│   └── test_prediction_api.py  # Tests endpoint /predict
├── conftest.py            # Fixtures partagées
└── fixtures/              # Données de test
```

### Exécuter les Tests

```bash
# Tous les tests avec couverture
uv run pytest

# Tests unitaires uniquement
uv run pytest tests/unit/ -v

# Tests fonctionnels uniquement
uv run pytest tests/functional/ -v

# Tests ML spécifiques
uv run pytest tests/unit/test_ml_model.py -v --ml

# Tests API
uv run pytest tests/functional/test_prediction_api.py -v --api

# Rapport de couverture HTML
uv run pytest --cov=utils --cov=api --cov-report=html
```

### Types de Tests

#### 🤖 Tests Machine Learning
- **Chargement du modèle** : Vérifie que `attrition_model.joblib` se charge correctement
- **Prédictions** : Teste la cohérence des résultats (0/1, probabilités)
- **Cas limites** : Gestion des valeurs extrêmes et données manquantes
- **Performance** : Temps de réponse < 100ms par prédiction

#### 🔌 Tests API
- **Endpoint `/predict`** : Validation des schémas et réponses
- **Gestion d'erreurs** : Modèle indisponible, données invalides
- **Concurrence** : Requêtes simultanées sans conflit
- **Robustesse** : Caractères spéciaux, types de données

#### 📊 Couverture Cible
- **API endpoints** : 100%
- **Logique métier** : 95%
- **Modèle ML** : 90%
- **Components UI** : 85%

### Fixtures de Test

- `sample_employee_data_low_risk` : Profil employé faible risque
- `sample_employee_data_high_risk` : Profil employé haut risque
- `sample_employee_data_medium_risk` : Profil employé risque moyen
- `ml_model` : Modèle ML chargé pour les tests

### CI/CD Integration

Les tests s'exécutent automatiquement sur :
- **Push** vers `main`/`dev`
- **Pull Requests**
- **Workflow manuel**

Le pipeline génère :
- Rapports de couverture Codecov
- Artefacts HTML de couverture
- Validation qualité (Ruff, Black)

## Commandes

### Lancer l'application

```bash
# Tout en un (recommandé) - Lance API + Interface
uv run streamlit_launcher.py

# Ou avec le script interactif
./start.sh

# Ou séparément
uv run uvicorn main:app --reload --port 8000  # API seulement
uv run streamlit run app.py  # Interface seulement
```

### Arrêter l'application

```bash
# Avec Ctrl+C si lancé avec streamlit_launcher.py
# Ou tuer les processus
lsof -ti:8000,8501 | xargs kill -9
```

### Commandes PostgreSQL

```bash
docker-compose up -d              # Démarrer
docker-compose down               # Arrêter
docker logs attrition_db          # Voir les logs

# Accéder à psql
docker exec -it attrition_db psql -U attrition_user -d attrition_db
```

## API Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Informations de l'API |
| `/health` | GET | Vérification de santé (API + DB) |
| `/employees` | GET | Liste des employés (pagination : `?skip=0&limit=100`) |
| `/employees/{id}` | GET | Détails d'un employé |

**Exemples** :
```bash
curl http://localhost:8000/health
curl http://localhost:8000/employees?limit=10
curl http://localhost:8000/employees/1
```

Documentation interactive : http://localhost:8000/docs

## Architecture Technique

### Infrastructure de Production (Hugging Face Spaces)

L'application utilise une architecture **monolithique conteneurisée** où FastAPI et Streamlit s'exécutent dans un seul conteneur Docker :

```
┌─────────────────────────────────────┐
│  Conteneur Docker (HF Spaces)      │
│                                     │
│  FastAPI (port 8000) ──────┐       │
│       ↑                     │       │
│       │ localhost:8000      │       │
│       │                     ↓       │
│  Streamlit (port 7860) → Internet  │
└─────────────────────────────────────┘
```

**Points importants** :
- ✅ `API_URL=http://localhost:8000` est **correct** pour la production
- ✅ Les deux processus communiquent via localhost interne
- ✅ Seul le port 7860 (Streamlit) est exposé à Internet
- ✅ L'API démarre en premier, Streamlit attend qu'elle soit prête (max 30s)

### Séquence de Démarrage

1. **Lancement du conteneur Docker** (`Dockerfile`)
2. **Démarrage FastAPI** sur port 8000 (interne)
3. **Vérification santé** : Polling de `/health` toutes les 1s (max 30s)
4. **Démarrage Streamlit** sur port 7860 (public)

Cette séquence évite l'erreur 503 "Service Unavailable" en garantissant que l'API est prête avant que Streamlit essaie de s'y connecter.

### Variables d'Environnement

| Variable | Valeur par défaut | Usage |
|----------|-------------------|-------|
| `API_URL` | `http://localhost:8000` | URL de connexion Streamlit→API |
| `DB_TYPE` | `sqlite` | Type de BDD (`sqlite` ou `postgres`) |
| `STREAMLIT_SERVER_PORT` | `8501` (local) / `7860` (HF) | Port d'écoute Streamlit |

**Configuration automatique** :
- Le `Dockerfile` définit `ENV API_URL=http://localhost:8000`
- La CI/CD valide que cette configuration est correcte avant déploiement
- Les tests unitaires vérifient que `config.py` respecte ces valeurs

## Données

**294 employés · 34 colonnes**

Catégories : Démographie · Carrière · Rémunération · Satisfaction · Formation · Indicateurs de risque

<details>
<summary>Voir toutes les colonnes</summary>

**Profil** : `id`, `genre`, `age`, `statut_marital`, `ayant_enfants`, `niveau_education`

**Professionnel** : `poste`, `departement`, `domaine_etude`, `niveau_hierarchique_poste`, `nombre_experiences_precedentes`, `annee_experience_totale`, `annees_dans_l_entreprise`, `annees_dans_le_poste_actuel`, `annees_depuis_la_derniere_promotion`, `annes_sous_responsable_actuel`, `nombre_employee_sous_responsabilite`

**Travail** : `revenu_mensuel`, `heure_supplementaires`, `nombre_heures_travailless`, `distance_domicile_travail`, `distance_categorie`, `frequence_deplacement`

**Satisfaction** : `satisfaction_employee_environnement`, `satisfaction_employee_nature_travail`, `satisfaction_employee_equipe`, `satisfaction_employee_equilibre_pro_perso`, `satisfaction_moyenne`, `note_evaluation_precedente`, `note_evaluation_actuelle`

**Développement** : `nb_formations_suivies`, `nombre_participation_pee`

**Risques** : `parent_burnout`, `sous_paye_niveau_dept`, `augementation_salaire_precedente`
</details>

## Interface Streamlit

Interface web interactive avec 3 pages :
- **Explorer** : Liste des employés avec filtres
- **Recherche** : Détails par ID
- **Statistiques** : Visualisations interactives (Plotly)

Voir [streamlit_app/DOCUMENTATION.md](streamlit_app/DOCUMENTATION.md) pour plus de détails.

## Structure du Projet

```
api-attrition/
├── main.py                     # API FastAPI
├── streamlit_launcher.py       # Launcher API + Interface
├── database/                   # Config DB + modèles SQLAlchemy
├── api/                        # Schémas Pydantic
├── streamlit_app/              # Interface Streamlit
│   ├── app.py                  # Page d'accueil
│   ├── pages/                  # Pages multi-pages
│   └── utils/                  # Client API + composants UI
└── data/                       # Dataset CSV (294 employés)
```

## 🚀 Déploiement sur Hugging Face Spaces

L'application est automatiquement déployée sur HF Spaces via GitHub Actions.

### Configuration (première fois)

1. **Créer un token Hugging Face**
   - Allez sur https://huggingface.co/settings/tokens
   - Créez un token avec permission **Write**
   - Copiez le token (format: `hf_xxxxxxxxxxxxx`)

2. **Ajouter le token dans GitHub Secrets**
   - Allez dans Settings → Secrets and variables → Actions
   - Créez un secret `HF_TOKEN` avec votre token

3. **Pusher sur main**
   ```bash
   git push origin main
   ```

Le déploiement se fait automatiquement ! 🎉

**URL du Space** : https://huggingface.co/spaces/ppluton/api_technova

Voir [.github/DEPLOYMENT.md](.github/DEPLOYMENT.md) pour la documentation complète.

### Base de données : PostgreSQL vs SQLite

L'application supporte deux types de bases de données :

**PostgreSQL** (développement local avec Docker) :
```bash
export DB_TYPE=postgres  # ou ne rien définir avec Docker
docker-compose up -d
uv run database/import_data.py
```

**SQLite** (production HF Spaces / développement simple) :
```bash
export DB_TYPE=sqlite  # par défaut
uv run database/migrate_to_sqlite.py  # Génère database.db
```

La base SQLite (`database.db`) est automatiquement créée et incluse dans le repo pour HF Spaces.

## Roadmap

- [x] ~~Déploiement cloud (Hugging Face Spaces)~~ ✅
- [x] ~~Support SQLite pour déploiement cloud~~ ✅
- [x] ~~CI/CD automatique vers HF Spaces~~ ✅
- [ ] Modèle ML pour prédiction d'attrition
- [ ] Endpoint POST /predict
- [ ] Filtres avancés sur GET /employees
- [ ] Authentification API (JWT)

## Tests & CI/CD

### Lancer les tests

```bash
# Lancer tous les tests (13 tests)
pytest tests/

# Tests unitaires (8 tests)
pytest tests/unit -v

# Tests fonctionnels (5 tests)
pytest tests/functional -v

# Avec coverage (rapport dans le terminal)
pytest tests/ --cov=. --cov-report=term-missing
```

### Rapports de couverture

**Local** :
```bash
# Générer rapport HTML
pytest tests/ --cov=. --cov-report=html

# Ouvrir le rapport
open htmlcov/index.html  # macOS
```

**CI/CD** :
- Badge de couverture visible en haut du README
- Rapport détaillé sur [Codecov](https://codecov.io/gh/Pltn-1321/api-attrition)
- Rapport HTML téléchargeable dans les artifacts GitHub Actions

### Pipeline automatique

Le workflow CI/CD (`ci-cd.yml`) s'exécute automatiquement :
- **Sur push/PR** : Lint + Tests + Coverage
- **Sur push `main`** : + Déploiement vers Hugging Face Spaces

**Documentation complète** : [CI-CD.md](CI-CD.md) - Architecture, stratégie de tests, pipeline GitHub Actions

## FAQ & Troubleshooting

### ❓ Pourquoi l'application utilise `localhost:8000` en production ?

**Réponse** : C'est normal et correct ! Sur Hugging Face Spaces, FastAPI et Streamlit s'exécutent dans le **même conteneur Docker**. Streamlit communique avec FastAPI via `localhost:8000` en interne. Seul le port 7860 (Streamlit) est exposé à Internet.

```
Utilisateur → HF Spaces (port 7860) → Streamlit → localhost:8000 → FastAPI
```

### ⚠️ Erreur 503: Service Unavailable

**Symptôme** : "503 Server Error: Service Unavailable for url: http://localhost:8000/..."

**Causes possibles** :
1. L'API FastAPI n'a pas encore terminé son démarrage
2. L'API a crashé au démarrage
3. Les ports ne sont pas correctement configurés

**Solutions** :

1. **Attendre et réessayer** (le plus courant)
   - L'application attend automatiquement jusqu'à 30 secondes que l'API soit prête
   - Cliquez sur le bouton "🔄 Réessayer la connexion" dans l'interface

2. **Vérifier les logs** (Hugging Face Spaces)
   - Allez dans l'onglet "Logs" de votre Space
   - Vérifiez que les deux messages apparaissent :
     ```
     ✅ API démarrée sur http://localhost:8000
     ✅ API est prête ! (démarrage en Xs)
     ```

3. **Vérifier la configuration locale**
   ```bash
   # Vérifier que les ports sont libres
   lsof -i:8000  # Doit être vide
   lsof -i:8501  # Doit être vide

   # Redémarrer proprement
   lsof -ti:8000,8501 | xargs kill -9
   uv run streamlit_launcher.py
   ```

### 🔧 Tests de diagnostic

```bash
# Vérifier la configuration
pytest tests/unit/test_config.py -v

# Vérifier la disponibilité de l'API
pytest tests/functional/test_api_availability.py -v

# Vérifier Dockerfile
grep "ENV API_URL" Dockerfile
# Devrait afficher: ENV API_URL=http://localhost:8000
```

### 🐛 L'API démarre trop lentement

**Solution** : Le `streamlit_launcher.py` attend désormais jusqu'à **30 secondes** pour que l'API démarre. Si votre machine est lente :

```python
# Dans streamlit_launcher.py (ligne 139)
api_ready = wait_for_api(API_PORT, max_retries=30, retry_interval=1)
# Vous pouvez augmenter max_retries si nécessaire
```

### 📊 Les tests de couverture échouent

**Problème** : `FAIL Required test coverage of 60% not reached`

**Solution** : Assurez-vous d'exécuter TOUS les tests ensemble :
```bash
# ✅ Correct - tous les tests
pytest tests/ --cov=utils.api_client --cov=api --cov=database --cov=main

# ❌ Incorrect - tests partiels
pytest tests/unit/test_ml_model.py --cov=main  # Couverture trop faible
```

### 🔄 Déploiement automatique ne fonctionne pas

**Checklist** :
1. ✅ Le secret `HF_TOKEN` est défini dans GitHub Secrets
2. ✅ Le push est sur la branche `main`
3. ✅ Tous les tests passent (voir GitHub Actions)
4. ✅ Le fichier `Dockerfile` est présent et valide
5. ✅ L'URL du Space est correcte dans `.github/workflows/ci-cd.yml`

### 📚 Plus d'aide

- **Documentation technique** : [CLAUDE.md](CLAUDE.md)
- **CI/CD détaillée** : [CI-CD.md](CI-CD.md)
- **Issues GitHub** : https://github.com/Pltn-1321/api-attrition/issues
