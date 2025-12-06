# API Attrition

API FastAPI pour la prédiction d'attrition des employés avec machine learning.

## Structure du Projet

```
api-attrition/
├── api/                        # Schémas et modèles de l'API
│   └── schemas.py              # Schémas Pydantic pour validation
├── data/                       # Données d'entraînement et de test
│   └── export-api/
│       └── test_employees.csv  # Dataset des employés (294 lignes)
├── database/                   # Configuration base de données
│   ├── config.py               # Configuration SQLAlchemy
│   ├── models.py               # Modèles ORM
│   └── import_data.py          # Script d'import CSV vers PostgreSQL
├── streamlit_app/              # Interface web Streamlit
│   ├── app.py                  # Page d'accueil
│   ├── pages/                  # Pages multi-pages
│   ├── utils/                  # Client API et composants UI
│   ├── tests/                  # Tests unitaires et fonctionnels
│   ├── .streamlit/             # Configuration et thème
│   ├── DOCUMENTATION.md        # Documentation pédagogique complète
│   └── requirements.txt        # Dépendances Python
├── models/                     # Modèles ML (à venir)
├── scripts/                    # Scripts utilitaires
├── tests/                      # Tests unitaires API
├── .github/workflows/          # CI/CD GitHub Actions
├── main.py                     # Application FastAPI principale
├── docker-compose.yml          # Configuration Docker (PostgreSQL)
├── pyproject.toml              # Configuration uv et dépendances
└── README.md                   # Documentation du projet
```

## Branches Git

- `main` (production)
- `dev` (développement - branche de base)

## Technologies

- **FastAPI**: Framework API Python
- **SQLAlchemy**: ORM pour base de données
- **PostgreSQL**: Base de données
- **Scikit-learn**: Machine Learning
- **Pydantic**: Validation des données
- **Uvicorn**: Serveur ASGI

## Prérequis

- **Docker** et **Docker Compose** installés ([Télécharger Docker Desktop](https://www.docker.com/products/docker-desktop))
- **Python 3.11+**
- **uv** - Gestionnaire de paquets Python moderne ([Installation uv](https://docs.astral.sh/uv/))

## Installation

```bash
# Cloner le dépôt
git clone git@github.com:Pltn-1321/api-attrition.git
cd api-attrition

# Initialiser le projet avec uv
uv init --no-readme

# Installer les dépendances
uv add pandas sqlalchemy psycopg2-binary fastapi uvicorn
```

## Installation de la Base de Données

### Étape 1 : Démarrer PostgreSQL avec Docker

Le projet utilise Docker Compose pour gérer PostgreSQL. La configuration se trouve dans `docker-compose.yml`.

```bash
# Démarrer PostgreSQL
docker-compose up -d

# Vérifier que le container tourne
docker ps
```

Vous devriez voir le container `attrition_db` (PostgreSQL sur le port 5432).

### Étape 2 : Importer les données dans PostgreSQL

Le script `database/import_data.py` charge automatiquement le fichier CSV dans PostgreSQL :

```bash
# Importer les données
uv run database/import_data.py
```

Résultat attendu :
```
✅ 294 employés importés dans PostgreSQL
```

### Étape 3 : Vérifier l'import

```bash
# Compter le nombre d'employés
docker exec attrition_db psql -U attrition_user -d attrition_db -c "SELECT COUNT(*) FROM employees;"

# Afficher quelques lignes
docker exec attrition_db psql -U attrition_user -d attrition_db -c "SELECT * FROM employees LIMIT 5;"
```

## Accéder à la Base de Données (optionnel)

### Ligne de commande

```bash
# Accès direct au terminal PostgreSQL
docker exec attrition_db psql -U attrition_user -d attrition_db

# Lister les tables
docker exec attrition_db psql -U attrition_user -d attrition_db -c "\dt"

# Exécuter une requête SQL
docker exec attrition_db psql -U attrition_user -d attrition_db -c "SELECT * FROM employees WHERE age > 30 LIMIT 10;"
```

### Clients Desktop (optionnel)

Vous pouvez utiliser des clients PostgreSQL comme :
- **TablePlus** (Mac/Windows) : https://tableplus.com
- **DBeaver** (Gratuit, multi-plateforme) : https://dbeaver.io

**Paramètres de connexion** :
- Host : `localhost`
- Port : `5432`
- Database : `attrition_db`
- Username : `attrition_user`
- Password : `attrition_pass`

## Commandes Docker Utiles

```bash
# Arrêter PostgreSQL
docker-compose down

# Redémarrer PostgreSQL
docker-compose up -d

# Voir les logs
docker logs attrition_db

# Réinitialiser la base de données (⚠️ supprime toutes les données)
docker-compose down -v
docker-compose up -d
uv run database/import_data.py
```

## Lancement de l'Application

### Option 1 : Script automatique (recommandé)

```bash
# Lancer le script interactif
./start.sh
```

Le script vous permet de choisir :
1. API seulement (FastAPI)
2. Interface seulement (Streamlit)
3. Les deux

### Option 2 : Lancement manuel

```bash
# Terminal 1 - API (avec rechargement automatique)
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Interface Streamlit
cd streamlit_app
uv run streamlit run app.py
```

L'application sera accessible sur :
- **API** : http://localhost:8000
- **Interface Streamlit** : http://localhost:8501
- **Documentation interactive (Swagger)** : http://localhost:8000/docs
- **Documentation alternative (ReDoc)** : http://localhost:8000/redoc

## Arrêter l'Application

### Méthode rapide

```bash
# Arrêter tous les processus uvicorn et streamlit
pkill -9 -f "uvicorn main:app"; pkill -9 -f "streamlit run"
```

### Méthode par port

```bash
# Tuer tous les processus sur les ports 8000 et 8501
lsof -ti:8000,8501 | xargs kill -9
```

### Vérifier l'état

```bash
# Voir les processus actifs
ps aux | grep -E "(uvicorn|streamlit)" | grep -v grep

# Vérifier les ports utilisés
lsof -ti:8000,8501
```

## Utilisation de l'API

### Endpoints disponibles

#### 1. Page d'accueil - `GET /`

```bash
curl http://localhost:8000/
```

Retourne les informations de l'API et la liste des endpoints disponibles.

#### 2. Health Check - `GET /health`

```bash
curl http://localhost:8000/health
```

Vérifie l'état de l'API et de la connexion à la base de données.

**Réponse** :
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### 3. Liste des employés - `GET /employees`

Récupère la liste de tous les employés avec pagination.

```bash
# Récupérer les 10 premiers employés
curl "http://localhost:8000/employees?limit=10"

# Récupérer les employés 20 à 30
curl "http://localhost:8000/employees?skip=20&limit=10"

# Récupérer tous les employés (max 100 par défaut)
curl http://localhost:8000/employees
```

**Paramètres** :
- `skip` (optionnel) : Nombre d'employés à ignorer (défaut: 0)
- `limit` (optionnel) : Nombre maximum d'employés à retourner (défaut: 100, max: 100)

**Réponse** :
```json
{
  "total": 294,
  "employees": [
    {
      "id": 1,
      "genre": "F",
      "age": 24,
      "poste": "Représentant Commercial",
      "departement": "Commercial",
      "revenu_mensuel": 2033,
      "satisfaction_moyenne": 3.0,
      ...
    }
  ]
}
```

#### 4. Employé par ID - `GET /employees/{employee_id}`

Récupère un employé spécifique par son identifiant.

```bash
# Récupérer l'employé avec l'ID 1
curl http://localhost:8000/employees/1

# Récupérer l'employé avec l'ID 42
curl http://localhost:8000/employees/42
```

**Réponse (succès)** :
```json
{
  "id": 1,
  "genre": "F",
  "age": 24,
  "statut_marital": "Marié(e)",
  "ayant_enfants": "Y",
  "poste": "Représentant Commercial",
  "domaine_etude": "Infra & Cloud",
  "departement": "Commercial",
  "revenu_mensuel": 2033,
  "satisfaction_moyenne": 3.0,
  "parent_burnout": 0,
  ...
}
```

**Réponse (erreur - ID inexistant)** :
```json
{
  "detail": "Employé avec l'ID 999 non trouvé"
}
```

### Exemples d'utilisation avec Python

```python
import requests

# Récupérer tous les employés
response = requests.get("http://localhost:8000/employees")
data = response.json()
print(f"Total d'employés : {data['total']}")

# Récupérer un employé spécifique
employee = requests.get("http://localhost:8000/employees/1").json()
print(f"Employé : {employee['poste']} - {employee['departement']}")

# Calculer la satisfaction moyenne
employees = requests.get("http://localhost:8000/employees?limit=100").json()
avg_satisfaction = sum(e['satisfaction_moyenne'] for e in employees['employees']) / len(employees['employees'])
print(f"Satisfaction moyenne : {avg_satisfaction:.1f}/4")
```

### Exemples d'utilisation avec JavaScript

```javascript
// Récupérer tous les employés
fetch('http://localhost:8000/employees')
  .then(response => response.json())
  .then(data => console.log(`Total: ${data.total}`));

// Récupérer un employé spécifique
fetch('http://localhost:8000/employees/1')
  .then(response => response.json())
  .then(employee => console.log(employee.poste));
```

## Structure de la Base de Données

La table `employees` contient **294 employés** avec **34 colonnes** :

### Informations personnelles
- `id` - Identifiant unique
- `genre` - Genre (M/F)
- `age` - Âge de l'employé
- `statut_marital` - Statut marital
- `ayant_enfants` - A des enfants (Y/N)
- `niveau_education` - Niveau d'éducation (1-5)

### Informations professionnelles
- `poste` - Intitulé du poste
- `domaine_etude` - Domaine d'études
- `departement` - Département (Commercial, Consulting, etc.)
- `niveau_hierarchique_poste` - Niveau hiérarchique (1-5)

### Carrière et expérience
- `nombre_experiences_precedentes` - Nombre d'emplois précédents
- `annee_experience_totale` - Années d'expérience totale
- `annees_dans_l_entreprise` - Années dans l'entreprise actuelle
- `annees_dans_le_poste_actuel` - Années dans le poste actuel
- `annees_depuis_la_derniere_promotion` - Années depuis la dernière promotion
- `annes_sous_responsable_actuel` - Années sous le responsable actuel
- `nombre_employee_sous_responsabilite` - Nombre d'employés sous responsabilité

### Conditions de travail
- `revenu_mensuel` - Revenu mensuel
- `heure_supplementaires` - Fait des heures supplémentaires (Oui/Non)
- `nombre_heures_travailless` - Nombre d'heures travaillées par semaine
- `distance_domicile_travail` - Distance domicile-travail (km)
- `distance_categorie` - Catégorie de distance
- `frequence_deplacement` - Fréquence des déplacements

### Satisfaction et évaluation
- `satisfaction_employee_environnement` - Satisfaction environnement (1-4)
- `satisfaction_employee_nature_travail` - Satisfaction nature du travail (1-4)
- `satisfaction_employee_equipe` - Satisfaction équipe (1-4)
- `satisfaction_employee_equilibre_pro_perso` - Satisfaction équilibre vie pro/perso (1-4)
- `satisfaction_moyenne` - Moyenne des satisfactions
- `note_evaluation_precedente` - Note évaluation précédente (1-4)
- `note_evaluation_actuelle` - Note évaluation actuelle (1-4)

### Formation et développement
- `nb_formations_suivies` - Nombre de formations suivies
- `nombre_participation_pee` - Nombre de participations au PEE

### Indicateurs de risque
- `parent_burnout` - Indicateur burnout parental (0/1)
- `sous_paye_niveau_dept` - Sous-payé par rapport au département (0/1)
- `augementation_salaire_precedente` - Pourcentage d'augmentation précédente

## Interface Streamlit

Une interface web interactive est disponible pour visualiser et explorer les données de l'API.

### Fonctionnalités

- **📊 Explorer** : Parcourir la liste des employés avec filtres avancés (département, âge)
- **🔍 Recherche** : Rechercher un employé par son ID avec affichage détaillé
- **📈 Statistiques** : Visualiser les données avec des graphiques Plotly interactifs (démographie, rémunération, satisfaction)
- **🎨 Design moderne** : Thème personnalisé bleu nuit + corail
- **⚡ Performance** : Cache et optimisations pour une expérience fluide

### Lancement Local

```bash
# Depuis la racine du projet
cd streamlit_app

# Installer les dépendances (avec uv)
uv add streamlit pandas plotly requests pytest pytest-cov

# Ou avec pip
pip install -r requirements.txt

# Lancer l'application
uv run streamlit run app.py
# Ou avec streamlit directement
streamlit run app.py
```

L'interface sera accessible sur http://localhost:8501

### Déploiement sur Hugging Face Spaces

```bash
# Depuis streamlit_app/
git remote add hf https://huggingface.co/spaces/VOTRE_USERNAME/api-attrition-dashboard
git subtree push --prefix streamlit_app hf main
```

Configuration requise :
- Variable d'environnement `API_URL` dans les settings du Space

### Documentation

- [streamlit_app/README.md](streamlit_app/README.md) : Guide de démarrage rapide
- [streamlit_app/DOCUMENTATION.md](streamlit_app/DOCUMENTATION.md) : Documentation pédagogique complète
  - Architecture & choix techniques
  - Mise en place technique
  - Tests & qualité
  - CI/CD
  - Guide de développement

## Prochaines étapes

- [ ] Ajouter un endpoint POST pour les prédictions ML
- [ ] Entraîner et intégrer un modèle de Machine Learning (prédiction d'attrition)
- [ ] Ajouter des filtres avancés sur l'endpoint GET /employees (département, satisfaction, etc.)
- [ ] Ajouter des endpoints d'analytics et statistiques
- [ ] Déploiement sur cloud (Render, Railway, ou Hugging Face Spaces)

## Tests

```bash
pytest
```
