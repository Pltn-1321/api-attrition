# 🚀 Guide de déploiement sur Hugging Face Spaces

Ce guide explique comment configurer le déploiement automatique de l'application sur Hugging Face Spaces via GitHub Actions.

## ⚙️ Configuration initiale

### 1. Obtenir un token Hugging Face

1. Connectez-vous à [Hugging Face](https://huggingface.co/)
2. Allez dans **Settings** → **Access Tokens**
3. Cliquez sur **New token**
4. Donnez un nom au token (ex: `github-actions-deploy`)
5. Sélectionnez le scope **Write** (nécessaire pour pousser du code)
6. Copiez le token généré (format: `hf_xxxxxxxxxxxxx`)

⚠️ **IMPORTANT**: Ne partagez JAMAIS ce token publiquement et ne le commitez JAMAIS dans le code !

### 2. Ajouter le token dans GitHub Secrets

1. Allez dans votre repository GitHub
2. Cliquez sur **Settings** → **Secrets and variables** → **Actions**
3. Cliquez sur **New repository secret**
4. Nom du secret: `HF_TOKEN`
5. Valeur: Collez votre token Hugging Face
6. Cliquez sur **Add secret**

### 3. Créer le Space sur Hugging Face (optionnel)

Le workflow peut créer automatiquement le Space s'il n'existe pas, mais vous pouvez aussi le créer manuellement :

1. Allez sur [Hugging Face](https://huggingface.co/)
2. Cliquez sur votre profil → **New Space**
3. Nom du Space: `api_technova`
4. License: MIT
5. SDK: **Streamlit**
6. Visibilité: **Public**
7. Cliquez sur **Create Space**

## 🔄 Workflow de déploiement

### Automatique (recommandé)

Le déploiement se fait automatiquement à chaque push sur la branche `main` :

```bash
# Sur votre branche dev
git add .
git commit -m "Nouvelle fonctionnalité"
git push origin dev

# Fusionner vers main (après review)
git checkout main
git merge dev
git push origin main
```

Dès que le push sur `main` est effectué :
1. ✅ Les tests s'exécutent automatiquement
2. ✅ Si les tests passent, le déploiement démarre
3. ✅ L'application est déployée sur HF Spaces
4. ✅ Le Space redémarre automatiquement

### Manuel

Vous pouvez aussi déclencher le déploiement manuellement :

1. Allez dans **Actions** sur GitHub
2. Sélectionnez le workflow **Deploy to Hugging Face Spaces**
3. Cliquez sur **Run workflow**
4. Sélectionnez la branche `main`
5. Cliquez sur **Run workflow**

## 📋 Vérification du déploiement

### Pendant le déploiement

1. Allez dans l'onglet **Actions** de votre repo GitHub
2. Cliquez sur le dernier workflow en cours
3. Suivez les logs en temps réel

### Après le déploiement

1. Vérifiez que le workflow s'est terminé avec succès (✅)
2. Accédez à votre Space: https://huggingface.co/spaces/ppluton/api_technova
3. Attendez que le Space démarre (peut prendre 1-2 minutes)
4. Testez l'application

## 🐛 Résolution de problèmes

### Erreur: "Invalid credentials"

- Vérifiez que le secret `HF_TOKEN` est bien configuré dans GitHub
- Vérifiez que le token HF a les permissions `write`
- Régénérez un nouveau token si nécessaire

### Erreur: "Space not found"

- Le workflow créera automatiquement le Space lors du premier déploiement
- Vérifiez que le nom du Space est correct dans le workflow (`api_technova`)

### Erreur: "Tests failed"

- Le déploiement ne se lancera pas si les tests échouent
- Vérifiez les logs du job `test` pour identifier le problème
- Corrigez les erreurs et re-pushez

### Erreur: "Git LFS"

- Assurez-vous que Git LFS est activé sur votre repo
- Installez Git LFS localement: `git lfs install`
- Trackez les fichiers: `git lfs track "*.db"`

### Le Space affiche "Building" indéfiniment

- Vérifiez les logs du Space sur HF
- Vérifiez que tous les fichiers nécessaires sont présents
- Vérifiez que `requirements.txt` est correct
- Redémarrez le Space manuellement si nécessaire

## 📊 Fichiers déployés

Les fichiers suivants sont automatiquement déployés sur HF Spaces :

✅ **Déployés**:
- `app.py` (point d'entrée)
- `main.py` (API FastAPI)
- `streamlit_app/` (interface)
- `database/` (config DB)
- `database.db` (données SQLite)
- `data/` (datasets)
- `api/` (schémas)
- `requirements.txt`
- `packages.txt`
- `.streamlit/config.toml`
- `.gitattributes`
- `README.md` (généré depuis README_HF.md)

❌ **Exclus** (non nécessaires sur HF):
- `.git/`
- `.github/` (workflows)
- `docker-compose.yml`
- `start.sh`
- `streamlit_launcher.py`
- `__pycache__/`
- `.pytest_cache/`

## 🔐 Sécurité

- ✅ Le token HF est stocké de manière sécurisée dans GitHub Secrets
- ✅ Le token n'apparaît jamais dans les logs
- ✅ Les credentials ne sont jamais committés dans le code
- ✅ Les secrets sont automatiquement masqués dans les logs GitHub Actions

## 📝 Maintenance

### Mettre à jour le Space

Le Space se met à jour automatiquement à chaque push sur `main`.

Pour forcer une mise à jour :
```bash
git commit --allow-empty -m "Force redeploy"
git push origin main
```

### Redémarrer le Space

1. Allez sur https://huggingface.co/spaces/ppluton/api_technova
2. Cliquez sur **Settings**
3. Cliquez sur **Factory reboot**

### Supprimer le Space

⚠️ **Attention**: Cette action est irréversible !

1. Allez sur https://huggingface.co/spaces/ppluton/api_technova
2. Cliquez sur **Settings**
3. Scroll vers le bas
4. Cliquez sur **Delete this Space**

## 📚 Ressources

- [Documentation Hugging Face Spaces](https://huggingface.co/docs/hub/spaces)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Documentation Git LFS](https://git-lfs.github.com/)
