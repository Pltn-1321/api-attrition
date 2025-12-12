# API Attrition

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

## Commandes

### Lancer l'application

```bash
# Tout en un (recommandé) - Lance API + Interface
uv run streamlit_launcher.py

# Ou avec le script interactif
./start.sh

# Ou séparément
uv run uvicorn main:app --reload --port 8000  # API seulement
cd streamlit_app && uv run streamlit run app.py  # Interface seulement
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

```bash
# Lancer tous les tests
pytest

# Tests unitaires (8 tests)
pytest streamlit_app/tests/unit -v

# Tests fonctionnels (5 tests)
pytest streamlit_app/tests/functional -v

# Avec coverage
pytest streamlit_app/tests --cov=streamlit_app/utils
```

**Documentation complète** : [CI-CD.md](CI-CD.md) - Architecture, stratégie de tests, pipeline GitHub Actions
