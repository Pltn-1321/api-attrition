# 🚀 Guide rapide de déploiement Hugging Face Spaces

Ce guide vous explique comment déployer votre application sur Hugging Face Spaces en **3 étapes simples**.

## ✅ Changements apportés

### Nouvelle architecture de déploiement
- ✨ **Script Python** (`deploy_to_hf.py`) : Remplace les commandes CLI bash pour plus de fiabilité
- 🔧 **Workflow simplifié** : Plus besoin de `huggingface-cli`, tout se fait via l'API Python
- 📝 **Configuration centralisée** : Tous les paramètres dans un seul fichier Python

### Configuration actuelle
- **Username HF** : `Pedro1321`
- **Nom du Space** : `Api-Technova`
- **URL du Space** : https://huggingface.co/spaces/Pedro1321/Api-Technova
- **SDK** : Streamlit

---

## 🎯 Déploiement en 3 étapes

### Étape 1️⃣ : Configurer le token Hugging Face

1. **Créer un token sur Hugging Face** (si pas déjà fait)
   - Allez sur : https://huggingface.co/settings/tokens
   - Cliquez sur "New token"
   - Nom : `github-actions-deploy`
   - Type : **Write** (IMPORTANT !)
   - Copiez le token (format: `hf_xxxxxxxxxxxxx`)

2. **Ajouter le token dans GitHub Secrets**
   - Allez sur : https://github.com/Pltn-1321/api-attrition/settings/secrets/actions
   - Cliquez sur "New repository secret"
   - **Name** : `HF_TOKEN`
   - **Value** : Collez votre token HF
   - Cliquez sur "Add secret"

### Étape 2️⃣ : Commiter et pousser les changements

```bash
# Ajouter tous les fichiers modifiés
git add .

# Commiter les changements
git commit -m "feat: Add Python-based HF Spaces deployment script

- Replace CLI commands with Python API (huggingface_hub)
- Simplify GitHub Actions workflow
- Configure for Pedro1321/Api-Technova Space
- Update documentation with new approach"

# Pousser vers dev pour tester
git push origin dev
```

### Étape 3️⃣ : Déployer vers main

Une fois que les tests passent sur `dev` :

```bash
# Merger vers main
git checkout main
git merge dev
git push origin main
```

Le workflow GitHub Actions se déclenchera automatiquement et déploiera vers HF Spaces ! 🎉

---

## 📊 Suivi du déploiement

### Voir les logs en temps réel

1. Allez sur : https://github.com/Pltn-1321/api-attrition/actions
2. Cliquez sur le dernier workflow "Deploy to Hugging Face Spaces"
3. Suivez les étapes :
   - ✅ Tests (unitaires + fonctionnels)
   - ✅ Installation des dépendances
   - ✅ Déploiement vers HF Spaces

### Accéder à votre Space

Une fois le déploiement terminé (2-3 minutes) :
- **URL** : https://huggingface.co/spaces/Pedro1321/Api-Technova
- Le Space peut prendre 1-2 minutes supplémentaires pour démarrer

---

## 🔧 Modifier la configuration

### Changer le nom du Space ou le username

Éditez le fichier `deploy_to_hf.py` :

```python
# Lignes 11-13
HF_USERNAME = "Pedro1321"     # ← Remplacez par votre username
SPACE_NAME = "Api-Technova"   # ← Remplacez par le nom souhaité
```

Puis recommitez et pushez.

### Changer le SDK (Streamlit → Gradio, etc.)

Éditez le fichier `deploy_to_hf.py` :

```python
# Ligne 14
SPACE_SDK = "streamlit"  # Options: streamlit, gradio, docker, static
```

---

## 🐛 Résolution de problèmes

### Le workflow échoue avec "HF_TOKEN not found"

**Cause** : Le secret GitHub n'est pas configuré

**Solution** :
1. Vérifiez sur https://github.com/Pltn-1321/api-attrition/settings/secrets/actions
2. Le secret `HF_TOKEN` doit être présent
3. Si absent, ajoutez-le (voir Étape 1)

### Le workflow échoue avec "Invalid credentials"

**Cause** : Le token HF est invalide ou n'a pas la permission Write

**Solutions** :
1. Vérifiez que le token a la permission **Write**
2. Régénérez un nouveau token sur HF
3. Mettez à jour le secret GitHub avec le nouveau token

### Le workflow échoue avec "database.db not found"

**Cause** : La base de données SQLite n'a pas été générée

**Solution** :
```bash
# Générer la base de données localement
uv run python database/migrate_to_sqlite.py

# Vérifier qu'elle existe
ls -lh database.db

# Commiter et pousser
git add database.db
git commit -m "Add SQLite database"
git push
```

### Le Space ne démarre pas sur HF

**Causes possibles** :
1. Erreur dans `app.py` (point d'entrée)
2. Dépendances manquantes dans `requirements.txt`
3. Port incorrect (doit être 7860 sur HF Spaces)

**Solutions** :
1. Vérifiez les logs du Space sur HF
2. Testez localement : `python app.py`
3. Vérifiez que `app.py` configure le port 7860 pour Streamlit

---

## 🧪 Tester localement avant de déployer

### Test complet du déploiement

```bash
# Définir le token HF
export HF_TOKEN="votre_token_ici"

# Installer les dépendances
pip install huggingface_hub

# Lancer le script de déploiement
python deploy_to_hf.py
```

Le script affichera toutes les étapes et créera/mettra à jour votre Space.

### Test de l'application localement

```bash
# Avec SQLite (comme sur HF Spaces)
export DB_TYPE=sqlite
python app.py
```

Accédez à http://localhost:7860 pour tester.

---

## 📚 Documentation complète

- **Configuration détaillée** : [.github/HF_CONFIG.md](.github/HF_CONFIG.md)
- **Guide de déploiement** : [.github/DEPLOYMENT.md](.github/DEPLOYMENT.md)
- **CI/CD** : [../CI-CD.md](../CI-CD.md)

---

## 🎉 Workflow final

```
┌─────────────────────────────────────────────────────────┐
│  1. Développement sur feature branch ou dev             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  2. Push vers dev → Tests GitHub Actions                │
└────────────────────┬────────────────────────────────────┘
                     │ (si ✅)
                     ↓
┌─────────────────────────────────────────────────────────┐
│  3. Merge dev → main                                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  4. Push main → Tests + Déploiement auto HF Spaces      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  5. Application live sur HF Spaces ! 🎉                  │
│     https://huggingface.co/spaces/Pedro1321/Api-Technova│
└─────────────────────────────────────────────────────────┘
```

---

**Besoin d'aide ?** Consultez [HF_CONFIG.md](HF_CONFIG.md) ou ouvrez une issue sur GitHub.
