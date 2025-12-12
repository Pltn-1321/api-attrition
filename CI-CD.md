# CI/CD - Documentation Technique

## Vue d'ensemble

Pipeline CI/CD automatisée avec GitHub Actions pour garantir la qualité du code de l'application Streamlit avant tout déploiement.

**Déclencheurs** : Push ou Pull Request sur `main` ou `dev` (uniquement si `streamlit_app/**` modifié)

## Architecture de la Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                     Push vers dev/main                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                  Lint & Tests (Job 1)                        │
│  ├─ Ruff (linting)                                           │
│  ├─ Black (formatage)                                        │
│  ├─ Tests unitaires (8 tests)                               │
│  ├─ Tests fonctionnels (5 tests)                            │
│  └─ Coverage report → Codecov                               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
                ┌──────┴──────┐
                │             │
         (si dev)         (si main)
                │             │
                ↓             ↓
           ┌─────┐    ┌──────────────────┐
           │ Fin │    │ Deploy HF Spaces │
           └─────┘    │   (Job 2)        │
                      │  - Préparation    │
                      │  - Git LFS        │
                      │  - Push to HF     │
                      │  - Notification   │
                      └──────────────────┘
```

## Tests Implémentés

### 1. Tests Unitaires (8 tests)

**Fichier** : `streamlit_app/tests/unit/test_api_client.py`

| Test | Description | Pourquoi |
|------|-------------|----------|
| `test_init` | Vérifie l'initialisation du client API | Garantit la bonne configuration de l'URL et timeout |
| `test_health_check_success` | Teste le health check en cas de succès | Valide la communication API normale |
| `test_health_check_failure` | Teste le health check en cas d'échec | Valide la gestion d'erreurs réseau |
| `test_get_employees` | Teste la récupération de la liste d'employés | Valide la pagination et le parsing JSON |
| `test_get_employee` | Teste la récupération d'un employé par ID | Valide la récupération unitaire |
| `test_filter_employees` | Teste les filtres côté client | Valide la logique de filtrage (dept, âge) |

**Fichier** : `streamlit_app/tests/unit/test_ui_components.py`

| Test | Description | Pourquoi |
|------|-------------|----------|
| `test_render_metric_card` | Teste l'affichage des cartes métriques | Valide l'UI des statistiques |
| `test_render_employee_card` | Teste l'affichage des cartes employé | Valide l'UI des profils |

**Technique utilisée** : Mocking avec `unittest.mock` pour isoler les tests (pas de dépendance réseau réelle)

### 2. Tests Fonctionnels (5 tests)

**Fichier** : `streamlit_app/tests/functional/test_app.py`

| Test | Description | Pourquoi |
|------|-------------|----------|
| `test_api_client_health_check` | Teste le client API en conditions réelles | Valide l'intégration API complète |
| `test_get_employees` | Teste la récupération avec un vrai client | Valide le flux complet de données |
| `test_get_employee_by_id` | Teste la récupération par ID | Valide la navigation par ID |

**Fichier** : `streamlit_app/tests/functional/test_pages.py`

| Test | Description | Pourquoi |
|------|-------------|----------|
| `test_explorer_page_loads` | Vérifie que la page Explorer se charge | Détecte les erreurs d'import/syntax |
| `test_search_page_loads` | Vérifie que la page Recherche se charge | Détecte les erreurs d'import/syntax |

**Différence unitaire vs fonctionnel** :
- **Unitaire** : Tests isolés avec mocks, rapides, testent la logique
- **Fonctionnel** : Tests d'intégration, plus lents, testent le comportement réel

### 3. Qualité du Code

#### Linting avec Ruff
```bash
ruff check . || true
```
- Détecte les erreurs de syntaxe
- Vérifie le respect des conventions PEP8
- Non-bloquant (`|| true`) pour ne pas casser la pipeline

#### Formatage avec Black
```bash
black --check . || true
```
- Vérifie le formatage du code
- Garantit un style uniforme
- Non-bloquant mais visible dans les logs

### 4. Coverage (Couverture de Tests)

```bash
pytest tests/ --cov=. --cov-report=xml --cov-report=html
```

**Métriques** :
- Génère un rapport XML pour Codecov
- Génère un rapport HTML pour inspection locale
- Cible : `utils/` (client API et composants UI)

**Upload vers Codecov** :
- Badge de couverture visible sur GitHub
- Historique de la couverture
- Détection des régressions

## Pipeline GitHub Actions

### Fichier : `.github/workflows/streamlit.yml`

```yaml
name: Streamlit App CI/CD

on:
  push:
    branches: [main, dev]
    paths:
      - 'streamlit_app/**'
      - '.github/workflows/streamlit.yml'
  pull_request:
    branches: [main, dev]
    paths:
      - 'streamlit_app/**'
```

**Optimisation** : Déclenche uniquement si `streamlit_app/` est modifié (économise des builds inutiles)

### Job 1 : `lint-and-test`

**Environnement** : Ubuntu Latest, Python 3.11

**Étapes** :
1. **Checkout** : Récupère le code
2. **Setup Python** : Installe Python 3.11
3. **Cache** : Met en cache les dépendances pip pour accélérer les builds
4. **Install** : Installe les dépendances + outils de test
5. **Lint** : Vérifie la qualité du code
6. **Format** : Vérifie le formatage
7. **Tests unitaires** : Lance les 8 tests unitaires avec coverage
8. **Tests fonctionnels** : Lance les 5 tests fonctionnels
9. **Coverage** : Génère le rapport de couverture
10. **Upload** : Envoie le rapport vers Codecov

### Job 2 : `build` (workflow streamlit.yml)

**Condition** : Uniquement si `lint-and-test` réussit + push sur `main`

**Action** : Message de confirmation pour déploiement manuel

## Déploiement Automatique sur Hugging Face Spaces

### Fichier : `.github/workflows/deploy-hf.yml`

Pipeline de déploiement automatique vers Hugging Face Spaces après validation des tests.

**Déclencheurs** :
- Push sur `main` (automatique)
- Déclenchement manuel via `workflow_dispatch`

### Job 1 : `test`

Exécute les mêmes tests que le workflow Streamlit avant le déploiement :
1. Tests de linting (Ruff)
2. Tests de formatage (Black)
3. Tests unitaires (8 tests)
4. Tests fonctionnels (5 tests)

**Sécurité** : Le déploiement ne se lance que si tous les tests passent ✅

### Job 2 : `deploy`

**Condition** : Uniquement si le job `test` réussit

**Étapes détaillées** :

1. **Checkout avec Git LFS**
   ```yaml
   - uses: actions/checkout@v4
     with:
       lfs: true  # Important pour database.db
   ```

2. **Installation Hugging Face CLI**
   ```bash
   pip install huggingface_hub
   ```

3. **Préparation des fichiers**
   - Copie tous les fichiers dans `/tmp/hf_deploy`
   - Remplace `README.md` par `README_HF.md` (avec metadata HF)
   - Vérifie/génère `database.db` si manquant
   - Exclut les fichiers non nécessaires (Docker, .github, etc.)

4. **Authentification HF**
   - Utilise le secret `HF_TOKEN` depuis GitHub Secrets
   - Se connecte via `huggingface-cli login`

5. **Configuration Git LFS**
   ```bash
   git lfs install
   git lfs track "*.db"
   ```

6. **Déploiement**
   - Clone le Space HF ou le crée s'il n'existe pas
   - Copie les fichiers avec `rsync`
   - Commit et push vers `spaces/ppluton/api_technova`

7. **Notification**
   - Affiche un résumé du déploiement dans GitHub Actions
   - URL du Space : https://huggingface.co/spaces/ppluton/api_technova

### Configuration requise

**GitHub Secrets** :
| Secret | Valeur | Utilisation |
|--------|--------|-------------|
| `HF_TOKEN` | Token Hugging Face (write) | Authentification pour pusher vers le Space |

**Création du token** :
1. https://huggingface.co/settings/tokens
2. Créer un token avec permission **Write**
3. Ajouter dans GitHub → Settings → Secrets → `HF_TOKEN`

### Fichiers spécifiques HF Spaces

| Fichier | Description |
|---------|-------------|
| `app.py` | Point d'entrée - Lance FastAPI + Streamlit |
| `requirements.txt` | Dépendances fusionnées (API + Streamlit) |
| `packages.txt` | Dépendances système (vide pour ce projet) |
| `README_HF.md` | README avec metadata YAML pour HF |
| `.gitattributes` | Configuration Git LFS pour fichiers binaires |
| `database.db` | Base SQLite (tracké via Git LFS) |

### Architecture déployée sur HF Spaces

```
Container HF Spaces (Port 7860 exposé)
├── FastAPI (Port 8000 interne)
│   ├── SQLite (database.db)
│   └── API REST endpoints
│
└── Streamlit (Port 7860)
    ├── Interface web
    └── Communique avec API via localhost:8000
```

**Variables d'environnement auto-configurées** :
- `DB_TYPE=sqlite` (force SQLite au lieu de PostgreSQL)
- `API_URL=http://localhost:8000` (Streamlit → API)

## Stratégie de Branches

```
main (production) → Déploiement auto HF Spaces
  ↑
  PR (avec CI/CD : tests obligatoires)
  ↑
dev (développement, CI/CD active)
  ↑
feature branches
```

**Workflow complet** :
1. **Développement** : `feature-branch` → `dev`
   - CI/CD vérifie les tests sur `dev`
   - Pas de déploiement

2. **Review** : `dev` → PR vers `main`
   - CI/CD vérifie à nouveau les tests
   - Review obligatoire

3. **Production** : Merge vers `main`
   - CI/CD exécute les tests
   - ✅ Si tests OK → Déploiement automatique vers HF Spaces
   - ❌ Si tests KO → Déploiement bloqué

4. **Live** : Application accessible sur https://huggingface.co/spaces/ppluton/api_technova

## Résolution de Problèmes

### Problème Courant : Test Failure

**Exemple récent** : `test_health_check_failure` échouait

**Cause** :
```python
# ❌ Mauvais - Exception générique
mock_request.side_effect = Exception("Connection error")

# ✅ Correct - Exception spécifique requests
mock_request.side_effect = requests.exceptions.RequestException("Connection error")
```

**Raison** : Le code attrape `requests.exceptions.RequestException`, pas `Exception`

### Déboguer Localement

```bash
# Lancer tous les tests
uv run pytest streamlit_app/tests -v

# Tests unitaires uniquement
uv run pytest streamlit_app/tests/unit -v

# Tests fonctionnels uniquement
uv run pytest streamlit_app/tests/functional -v

# Avec coverage
uv run pytest streamlit_app/tests --cov=streamlit_app/utils --cov-report=term-missing

# Vérifier le formatage
uv run black --check streamlit_app/

# Corriger le formatage
uv run black streamlit_app/

# Linting
uv run ruff check streamlit_app/
```

## Métriques de Qualité

| Métrique | Valeur Actuelle | Objectif |
|----------|-----------------|----------|
| Tests unitaires | 8 tests | 100% des fonctions critiques |
| Tests fonctionnels | 5 tests | 100% des pages |
| Couverture code | ~85% | >80% |
| Temps de build | ~2-3 min | <5 min |

## Améliorations Futures

- [x] ~~Déploiement automatique sur Hugging Face Spaces~~ ✅ **Implémenté**
- [ ] Tests d'intégration avec API réelle (Docker Compose dans CI)
- [ ] Tests E2E avec Selenium/Playwright
- [ ] Tests de performance (temps de chargement des pages)
- [ ] Tests de sécurité (Bandit, Safety)
- [ ] Matrix testing (Python 3.10, 3.11, 3.12)
- [ ] Notifications Slack/Discord pour les déploiements
- [ ] Environnements de staging (preview deployments)
- [ ] Rollback automatique en cas d'erreur

## Bonnes Pratiques Appliquées

✅ **Tests isolés** : Utilisation de mocks pour éviter les dépendances externes
✅ **Fast feedback** : Tests unitaires rapides (<1s)
✅ **Fail fast** : La pipeline s'arrête dès qu'un test échoue
✅ **Cache** : Dépendances pip mises en cache pour accélérer
✅ **Path filtering** : CI déclenchée uniquement si nécessaire
✅ **Branch protection** : Tests obligatoires avant merge
✅ **Coverage tracking** : Suivi de la couverture dans le temps

## Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Codecov Documentation](https://docs.codecov.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

## Maintenance

**Fréquence de vérification** : Mensuelle

**Points de contrôle** :
- [ ] Dépendances à jour (pytest, black, ruff)
- [ ] Versions GitHub Actions à jour
- [ ] Coverage >80%
- [ ] Pas de tests `|| true` ignorés silencieusement
- [ ] Temps de build <5 min
