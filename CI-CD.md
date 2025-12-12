# CI/CD - Documentation Technique

## Vue d'ensemble

Pipeline CI/CD automatisée avec GitHub Actions pour garantir la qualité du code de l'application Streamlit avant tout déploiement.

**Déclencheurs** : Push ou Pull Request sur `main` ou `dev` (uniquement si `streamlit_app/**` modifié)

## Architecture de la Pipeline

```
Push/PR → Lint & Tests → Build → Déploiement (manuel)
          │
          ├─ Ruff (linting)
          ├─ Black (formatage)
          ├─ Tests unitaires (8 tests)
          ├─ Tests fonctionnels (5 tests)
          └─ Coverage report
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

### Job 2 : `build`

**Condition** : Uniquement si `lint-and-test` réussit + push sur `main`

**Action** : Message de confirmation pour déploiement manuel

## Stratégie de Branches

```
main (production)
  ↑
  PR (avec CI/CD)
  ↑
dev (développement, CI/CD active)
  ↑
feature branches
```

**Workflow** :
1. Développement sur `dev` → CI/CD vérifie les tests
2. PR vers `main` → CI/CD vérifie à nouveau
3. Merge → Job `build` se déclenche
4. Déploiement manuel vers Hugging Face Spaces

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

- [ ] Tests d'intégration avec API réelle (Docker Compose dans CI)
- [ ] Tests E2E avec Selenium/Playwright
- [ ] Déploiement automatique sur Hugging Face Spaces (via webhook)
- [ ] Tests de performance (temps de chargement des pages)
- [ ] Tests de sécurité (Bandit, Safety)
- [ ] Matrix testing (Python 3.10, 3.11, 3.12)

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
