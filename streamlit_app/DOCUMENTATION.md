# Documentation Pédagogique - Interface Streamlit API Attrition

## Table des Matières

1. [Architecture & Choix Techniques](#architecture--choix-techniques)
2. [Mise en Place Technique](#mise-en-place-technique)
3. [Tests & Qualité](#tests--qualité)
4. [CI/CD](#cicd)
5. [Guide de Développement](#guide-de-développement)
6. [Déploiement](#déploiement)

---

## Architecture & Choix Techniques

### Pourquoi Streamlit ?

**Streamlit** a été choisi pour plusieurs raisons techniques et pratiques :

#### Avantages par rapport aux alternatives

| Critère | Streamlit | Dash (Plotly) | Gradio |
|---------|-----------|---------------|--------|
| **Simplicité** | ✅ Très simple | ⚠️ Complexe | ✅ Simple |
| **Rapidité de développement** | ✅ Rapide | ❌ Lent | ✅ Rapide |
| **Personnalisation UI** | ⚠️ Limitée | ✅ Complète | ❌ Très limitée |
| **Support des graphiques** | ✅ Plotly intégré | ✅ Natif | ⚠️ Basique |
| **Déploiement** | ✅ Facile (HF Spaces) | ⚠️ Moyen | ✅ Facile (HF Spaces) |
| **Communauté** | ✅ Très active | ✅ Active | ⚠️ Moyenne |

**Conclusion** : Streamlit offre le meilleur rapport simplicité/fonctionnalités pour une application de data science.

### Architecture Modulaire

L'application suit une architecture en couches pour faciliter la maintenabilité et l'évolutivité :

```
streamlit_app/
├── config.py              # Configuration centralisée (API URL, couleurs, etc.)
├── utils/                 # Couche utilitaire réutilisable
│   ├── api_client.py      # Client API (pattern Strategy)
│   └── ui_components.py   # Composants UI (pattern Component)
├── app.py                 # Page d'accueil (point d'entrée)
├── pages/                 # Pages multi-pages Streamlit
│   ├── 1_📊_Explorer.py
│   ├── 2_🔍_Recherche.py
│   └── 3_📈_Statistiques.py
└── tests/                 # Tests séparés par type
    ├── unit/
    └── functional/
```

#### Justification de l'architecture

1. **Séparation des préoccupations** :
   - `config.py` : Toutes les constantes au même endroit (principe DRY)
   - `utils/` : Logique réutilisable, indépendante de Streamlit
   - `pages/` : Code spécifique à l'interface, isolé

2. **Testabilité** :
   - `api_client.py` peut être testé sans Streamlit
   - Les `ui_components` sont des fonctions pures facilement testables

3. **Extensibilité** :
   - Ajouter une nouvelle page = créer un fichier dans `pages/`
   - Ajouter un nouveau graphique = utiliser `api_client` existant

### Client API Pattern

Le fichier `utils/api_client.py` implémente le **pattern Repository** :

```python
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, method, endpoint, **kwargs):
        # Logique centralisée pour les requêtes HTTP
        # Gestion des erreurs, timeouts, retry...

    def get_employees(self, skip, limit):
        # Méthode spécifique au domaine
```

**Avantages** :
- **Abstraction** : Les pages ne connaissent pas les détails HTTP
- **Réutilisabilité** : Méthodes partagées entre toutes les pages
- **Testabilité** : Facile à mocker pour les tests
- **Maintenance** : Un seul endroit pour changer la logique API

### Choix de Plotly pour les graphiques

**Plotly** a été choisi pour :

1. **Interactivité native** : Zoom, pan, hover sans code JavaScript
2. **Performance** : Rendu côté client, pas de requêtes serveur
3. **Esthétique** : Graphiques modernes et personnalisables
4. **Compatibilité** : Intégration native avec Streamlit
5. **Thème cohérent** : Personnalisation facile (couleurs bleu nuit + corail)

```python
# Exemple de personnalisation
fig = px.bar(data, color_continuous_scale=["#1A1A2E", "#FF6B6B"])
```

---

## Mise en Place Technique

### Structure du Projet

#### 1. Configuration (config.py)

Ce fichier centralise toutes les constantes de l'application :

```python
# URL API configurable via environnement (pour HF Spaces)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Thème de couleurs (bleu nuit + corail)
COLORS = {
    "primary": "#FF6B6B",      # Corail
    "secondary": "#1A1A2E",    # Bleu nuit
}
```

**Pourquoi ?**
- ✅ Un seul endroit pour changer l'URL API lors du déploiement
- ✅ Cohérence visuelle garantie
- ✅ Facile à tester (mock `os.getenv`)

#### 2. Thème Personnalisé (.streamlit/config.toml)

```toml
[theme]
primaryColor = "#FF6B6B"        # Corail (boutons)
backgroundColor = "#16213E"      # Bleu nuit (fond)
secondaryBackgroundColor = "#1A1A2E"  # Bleu nuit foncé (sidebar)
textColor = "#FFFFFF"            # Blanc
```

**Impact** :
- Thème cohérent sur toute l'application
- Pas de CSS custom nécessaire
- Compatible avec les composants Streamlit natifs

#### 3. Gestion de l'État (st.session_state)

Streamlit recharge le script à chaque interaction. Pour persister les données :

```python
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()
```

**Bonnes pratiques** :
- Initialiser les objets coûteux une seule fois
- Stocker le cache API dans `session_state`
- Éviter les rechargements inutiles avec `@st.cache_data`

#### 4. Gestion des Erreurs

Pattern utilisé dans toutes les pages :

```python
try:
    with st.spinner("Chargement..."):
        data = api_client.get_employees()
except Exception as e:
    show_error(f"Erreur : {str(e)}")
```

**Avantages** :
- UX améliorée (spinner pendant le chargement)
- Erreurs utilisateur-friendly
- Pas de crash de l'application

---

## Tests & Qualité

### Stratégie de Test

L'application utilise une **pyramide de tests** :

```
     /\
    /  \    Tests fonctionnels (peu, lents)
   /----\
  / Unit \  Tests unitaires (nombreux, rapides)
 /________\
```

### Tests Unitaires

**Fichier** : `tests/unit/test_api_client.py`

```python
def test_health_check_success(mock_request, api_client):
    """Test le health check avec succès."""
    mock_request.return_value = mock_response
    result = api_client.health_check()
    assert result == {"status": "healthy"}
```

**Caractéristiques** :
- ✅ Rapides (<10ms chacun)
- ✅ Isolés (pas de réseau)
- ✅ Déterministes (mocks)
- ✅ Coverage > 80%

**Exécution** :
```bash
pytest tests/unit -v --cov=utils
```

### Tests Fonctionnels

**Fichier** : `tests/functional/test_app.py`

```python
def test_api_client_health_check(mock_api_client):
    """Test que le health check fonctionne."""
    result = mock_api_client.health_check()
    assert result["status"] == "healthy"
```

**Objectif** :
- Vérifier l'intégration entre composants
- Tester les scénarios utilisateur complets

**Exécution** :
```bash
pytest tests/functional -v
```

### Coverage

Objectif : **> 80% de couverture de code**

```bash
# Générer le rapport de coverage
pytest tests/ --cov=. --cov-report=html

# Ouvrir le rapport
open htmlcov/index.html
```

---

## CI/CD

### GitHub Actions Workflow

**Fichier** : `.github/workflows/streamlit.yml`

#### Pipeline

```yaml
lint-and-test → build → (deploy)
```

#### Étapes

1. **Linting** (ruff) :
   - Détecte les erreurs de syntaxe
   - Vérifie le style de code PEP8

2. **Format check** (black) :
   - Vérifie le formatage du code

3. **Tests unitaires** :
   - Exécute tous les tests de `tests/unit/`
   - Génère un rapport de coverage

4. **Tests fonctionnels** :
   - Exécute tous les tests de `tests/functional/`

5. **Upload coverage** :
   - Envoie le rapport à Codecov
   - Badge de coverage sur le README

#### Déclenchement

```yaml
on:
  push:
    branches: [main, dev]
    paths:
      - 'streamlit_app/**'
  pull_request:
    branches: [main, dev]
```

**Avantages** :
- Tests automatiques sur chaque commit
- Détection précoce des bugs
- Protection de la branche `main`

---

## Guide de Développement

### Ajouter une Nouvelle Page

1. Créer un fichier dans `pages/` :
   ```python
   # pages/4_🎯_Ma_Nouvelle_Page.py
   import streamlit as st
   from utils.api_client import APIClient

   st.set_page_config(page_title="Ma Page", layout="wide")

   if "api_client" not in st.session_state:
       st.session_state.api_client = APIClient()

   st.title("🎯 Ma Nouvelle Page")
   ```

2. Ajouter la logique métier

3. Ajouter les tests :
   ```python
   # tests/functional/test_ma_page.py
   def test_ma_page_loads():
       # Test que la page se charge
   ```

### Ajouter un Nouveau Graphique

1. Créer la fonction de graphique :
   ```python
   # utils/charts.py (nouveau fichier)
   def create_bar_chart(data):
       fig = px.bar(data, color_discrete_sequence=[COLORS["primary"]])
       return fig
   ```

2. Utiliser dans une page :
   ```python
   from utils.charts import create_bar_chart

   fig = create_bar_chart(data)
   st.plotly_chart(fig, use_container_width=True)
   ```

3. Ajouter les tests :
   ```python
   def test_create_bar_chart():
       data = pd.DataFrame(...)
       fig = create_bar_chart(data)
       assert fig is not None
   ```

### Bonnes Pratiques Streamlit

#### 1. Performance

```python
# ❌ Mauvais : Rechargé à chaque interaction
data = api_client.get_employees()

# ✅ Bon : Caché
@st.cache_data(ttl=3600)
def get_employees_cached():
    return api_client.get_employees()
```

#### 2. Layout

```python
# Utiliser les colonnes pour l'organisation
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Métrique 1", 100)

# Utiliser les onglets pour les vues multiples
tab1, tab2 = st.tabs(["Vue 1", "Vue 2"])
```

#### 3. État

```python
# Initialiser l'état une seule fois
if "counter" not in st.session_state:
    st.session_state.counter = 0

# Utiliser l'état
st.session_state.counter += 1
```

---

## Déploiement

### Hugging Face Spaces

#### Prérequis

1. Compte Hugging Face
2. Repository Git synchronisé

#### Étapes

1. **Créer un nouveau Space** :
   - Aller sur https://huggingface.co/spaces
   - "New Space" → Streamlit SDK
   - Nom : `api-attrition-dashboard`

2. **Configuration** :
   - Créer un fichier `.streamlit/config.toml` (déjà fait)
   - Ajouter `requirements.txt` (déjà fait)

3. **Variables d'environnement** :
   - Dans les settings du Space
   - Ajouter `API_URL` = URL de votre API déployée

4. **Déploiement** :
   ```bash
   git remote add hf https://huggingface.co/spaces/VOTRE_USERNAME/api-attrition-dashboard
   git push hf main
   ```

5. **Vérification** :
   - Le Space build automatiquement
   - URL : `https://VOTRE_USERNAME-api-attrition-dashboard.hf.space`

#### Troubleshooting

**Problème** : Space ne démarre pas
```bash
# Vérifier les logs dans l'onglet "Logs" du Space
# Vérifier que requirements.txt est correct
# Vérifier que API_URL est défini
```

**Problème** : API non accessible
```bash
# Vérifier que l'API est déployée et accessible publiquement
# Vérifier CORS sur l'API FastAPI
# Tester avec curl depuis le terminal du Space
```

---

## Conclusion

Cette application Streamlit démontre :

- ✅ **Architecture modulaire** pour la scalabilité
- ✅ **Tests complets** (unitaires + fonctionnels)
- ✅ **CI/CD automatisé** (GitHub Actions)
- ✅ **Documentation pédagogique** complète
- ✅ **Déploiement facile** (Hugging Face Spaces)

Elle est prête pour :
- Ajout de nouvelles fonctionnalités (prédictions ML)
- Évolution du design
- Déploiement en production
