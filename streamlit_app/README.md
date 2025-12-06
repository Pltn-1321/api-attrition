# Interface Streamlit - API Attrition Dashboard

Interface web interactive pour visualiser et explorer les données de l'API Attrition.

## Fonctionnalités

- 📊 **Explorer** : Parcourez la liste des employés avec filtres avancés
- 🔍 **Recherche** : Trouvez un employé par son ID
- 📈 **Statistiques** : Visualisez les données avec des graphiques interactifs
- 🎨 **Thème personnalisé** : Design moderne bleu nuit + corail
- ⚡ **Performance** : Cache et optimisations pour une expérience fluide

## Quick Start

### Installation Locale

```bash
# Depuis la racine du projet
cd streamlit_app

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

L'application sera disponible sur http://localhost:8501

### Configuration

Par défaut, l'app se connecte à `http://localhost:8000`. Pour changer l'URL de l'API :

```bash
# Définir une variable d'environnement
export API_URL=https://votre-api.com

# Lancer l'app
streamlit run app.py
```

## Déploiement sur Hugging Face Spaces

### 1. Créer un nouveau Space

1. Aller sur https://huggingface.co/spaces
2. Cliquer sur "New Space"
3. Choisir "Streamlit" comme SDK
4. Nommer le Space : `api-attrition-dashboard`

### 2. Pousser le code

```bash
# Ajouter le remote Hugging Face
git remote add hf https://huggingface.co/spaces/VOTRE_USERNAME/api-attrition-dashboard

# Pousser le code (seulement le dossier streamlit_app)
git subtree push --prefix streamlit_app hf main
```

### 3. Configurer les variables d'environnement

Dans les settings du Space :
- `API_URL` : URL de votre API déployée (ex: `https://api-attrition.onrender.com`)

### 4. Vérifier le déploiement

Le Space build automatiquement et sera disponible sur :
`https://VOTRE_USERNAME-api-attrition-dashboard.hf.space`

## Structure

```
streamlit_app/
├── app.py                    # Page d'accueil
├── pages/                    # Pages multi-pages
│   ├── 1_📊_Explorer.py
│   ├── 2_🔍_Recherche.py
│   └── 3_📈_Statistiques.py
├── utils/                    # Utilitaires réutilisables
│   ├── api_client.py        # Client API
│   └── ui_components.py     # Composants UI
├── config.py                 # Configuration centralisée
├── tests/                    # Tests unitaires et fonctionnels
├── .streamlit/              # Configuration Streamlit
│   └── config.toml          # Thème personnalisé
└── requirements.txt         # Dépendances Python
```

## Tests

```bash
# Tests unitaires
pytest tests/unit -v

# Tests fonctionnels
pytest tests/functional -v

# Tous les tests avec coverage
pytest tests/ --cov=. --cov-report=html
```

## Documentation

- [DOCUMENTATION.md](DOCUMENTATION.md) : Documentation pédagogique complète
- Architecture & choix techniques
- Guide de développement
- Tests & CI/CD

## Technologies

- **Streamlit** : Framework web pour data science
- **Plotly** : Graphiques interactifs
- **Pandas** : Manipulation de données
- **Requests** : Client HTTP

## Licence

Voir le fichier [LICENSE](../LICENSE) à la racine du projet.
