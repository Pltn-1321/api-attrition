# 🔧 Configuration Hugging Face Spaces

Ce fichier explique où et comment modifier les paramètres de déploiement.

> ℹ️ **Nouvelle approche** : Le déploiement utilise maintenant un script Python (`deploy_to_hf.py`) au lieu des commandes CLI bash, pour plus de fiabilité et de simplicité !

## 📍 Où modifier les paramètres

### 1️⃣ Nom du Space Hugging Face

**Fichier** : `deploy_to_hf.py`

**Lignes 11-13** :
```python
HF_USERNAME = "Pedro1321"
SPACE_NAME = "Api-Technova"
SPACE_REPO_ID = f"{HF_USERNAME}/{SPACE_NAME}"
```

**Valeurs actuelles** :
- Username: `Pedro1321`
- Space: `Api-Technova`
- URL complète: `https://huggingface.co/spaces/Pedro1321/Api-Technova`

**Pour modifier** :
1. Ouvrir `deploy_to_hf.py`
2. Remplacer `Pedro1321` par votre nom d'utilisateur HF
3. Remplacer `Api-Technova` par le nom de votre Space
4. Le `SPACE_REPO_ID` sera automatiquement généré

**Exemple** :
```python
HF_USERNAME = "VOTRE_USERNAME"
SPACE_NAME = "VOTRE_SPACE_NAME"
```

---

### 2️⃣ Token Hugging Face (HF_TOKEN)

Le token HF ne doit **JAMAIS** être dans le code. Il doit être configuré dans GitHub Secrets.

#### Option A : Via l'interface GitHub (RECOMMANDÉ)

1. **Aller sur votre repository GitHub**
   - https://github.com/Pltn-1321/api-attrition

2. **Cliquer sur "Settings"** (⚙️ en haut à droite)

3. **Dans le menu de gauche** :
   - Secrets and variables → Actions

4. **Cliquer sur "New repository secret"** (bouton vert)

5. **Remplir** :
   - **Name** : `HF_TOKEN` (EXACTEMENT ce nom, en majuscules)
   - **Value** : Votre token HF (format: `hf_xxxxxxxxxxxxx`)

6. **Cliquer sur "Add secret"**

#### Option B : Via GitHub CLI (terminal)

```bash
# Installer GitHub CLI si nécessaire
brew install gh

# Se connecter
gh auth login

# Ajouter le secret
gh secret set HF_TOKEN --body "VOTRE_TOKEN_ICI"
```

#### Obtenir un token Hugging Face

1. Aller sur : https://huggingface.co/settings/tokens
2. Cliquer sur "New token"
3. Nom : `github-actions-deploy` (ou autre)
4. Type : **Write** (très important !)
5. Copier le token généré (commence par `hf_`)

⚠️ **ATTENTION** : Ne partagez JAMAIS ce token publiquement !

---

### 3️⃣ SDK du Space (optionnel)

**Fichier** : `deploy_to_hf.py`

**Ligne 14** :
```python
SPACE_SDK = "streamlit"
```

**Options disponibles** :
- `streamlit` (actuel, recommandé pour ce projet)
- `gradio`
- `docker`
- `static`

**Pour modifier** :
```python
SPACE_SDK = "VOTRE_SDK"
```

---

### 4️⃣ URL du Space dans la documentation (optionnel)

**Fichiers à modifier si vous voulez mettre à jour la documentation** :

1. **README.md** (ligne 151)
2. **CI-CD.md** (plusieurs lignes)
3. **.github/DEPLOYMENT.md**
4. **.github/workflows/deploy-hf.yml** (ligne 95)

**Valeurs actuelles** :
- Username: `Pedro1321`
- Space: `Api-Technova`
- URL: `https://huggingface.co/spaces/Pedro1321/Api-Technova`

**Pour modifier** : Utiliser la fonction rechercher/remplacer dans votre éditeur :
- Rechercher : `ppluton/api_technova` ou `Pedro1321/Api-Technova`
- Remplacer par : `VOTRE_USERNAME/VOTRE_SPACE_NAME`

---

### 5️⃣ README Hugging Face

**Fichier** : `README_HF.md`

**Lignes 2-3** :
```yaml
title: API Technova - Gestion RH & Attrition
emoji: 👥
```

**Pour modifier** :
- `title` : Le titre affiché sur HF
- `emoji` : L'emoji du Space (peut être n'importe quel emoji)
- `colorFrom` et `colorTo` : Couleurs du gradient

---

## 📝 Checklist de configuration

Avant de déployer, vérifiez que vous avez :

- [ ] Créé un compte Hugging Face
- [ ] Généré un token HF avec permission **Write**
- [ ] Ajouté le token dans GitHub Secrets (`HF_TOKEN`)
- [ ] Configuré le username et le nom du Space dans `deploy_to_hf.py` (lignes 11-13)
- [ ] Généré le fichier `database.db` (via `uv run python database/migrate_to_sqlite.py`)
- [ ] (Optionnel) Mis à jour les URLs dans la documentation

**Configuration actuelle** :
- ✅ Username: `Pedro1321`
- ✅ Space: `Api-Technova`
- ✅ SDK: `streamlit`
- ✅ Script de déploiement: `deploy_to_hf.py`

---

## 🔍 Vérifier la configuration

### Vérifier que le secret GitHub est configuré

1. Aller sur : https://github.com/Pltn-1321/api-attrition/settings/secrets/actions
2. Vous devriez voir `HF_TOKEN` dans la liste

### Tester localement

```bash
# Vérifier que le token HF fonctionne
export HF_TOKEN="votre_token_ici"
pip install huggingface_hub
python deploy_to_hf.py
```

Le script affichera toutes les étapes du déploiement.

**Test rapide sans déploiement** :
```bash
# Tester l'authentification
export HF_TOKEN="votre_token_ici"
python -c "from huggingface_hub import login; login(token='$HF_TOKEN'); print('✅ Authentification réussie!')"
```

---

## 🚨 Erreurs courantes

### Erreur : "ModuleNotFoundError: No module named 'huggingface_hub'"
**Solution** :
```bash
pip install huggingface_hub
```

### Erreur : "Invalid credentials" ou "401 Unauthorized"
**Solutions** :
1. Vérifiez que `HF_TOKEN` est bien configuré dans GitHub Secrets
2. Vérifiez que le token a la permission **Write**
3. Régénérez un nouveau token si nécessaire
4. Testez localement: `export HF_TOKEN="..." && python deploy_to_hf.py`

### Erreur : "Space not found" ou "Repository not found"
**Solutions** :
1. Vérifiez le nom du Space dans `deploy_to_hf.py` (lignes 11-13)
2. Le script créera automatiquement le Space s'il n'existe pas
3. Vérifiez que votre username HF est correct

### Erreur : "Permission denied" lors du push Git
**Solutions** :
1. Vérifiez que le token a la permission **Write**
2. Vérifiez que le token n'a pas expiré
3. Testez l'authentification: `python -c "from huggingface_hub import login; login('votre_token')"`

### Erreur : "database.db not found"
**Solution** :
```bash
# Générer la base de données
uv run python database/migrate_to_sqlite.py
```

---

## 📞 Aide supplémentaire

- **Documentation HF Spaces** : https://huggingface.co/docs/hub/spaces
- **Documentation GitHub Secrets** : https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Token HF** : https://huggingface.co/settings/tokens
