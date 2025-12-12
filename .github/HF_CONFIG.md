# 🔧 Configuration Hugging Face Spaces

Ce fichier explique où et comment modifier les paramètres de déploiement.

## 📍 Où modifier les paramètres

### 1️⃣ Nom du Space Hugging Face

**Fichier** : `.github/workflows/deploy-hf.yml`

**Ligne 114** :
```yaml
SPACE_REPO="spaces/ppluton/api_technova"
```

**Pour modifier** :
- Remplacez `ppluton` par votre nom d'utilisateur HF
- Remplacez `api_technova` par le nom de votre Space

**Exemple** :
```yaml
SPACE_REPO="spaces/VOTRE_USERNAME/VOTRE_SPACE_NAME"
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

### 3️⃣ Nom d'utilisateur HF dans le push

**Fichier** : `.github/workflows/deploy-hf.yml`

**Ligne 152** :
```yaml
git push https://ppluton:$HF_TOKEN@huggingface.co/$SPACE_REPO main
```

**Pour modifier** :
- Remplacez `ppluton` par votre nom d'utilisateur HF

**Exemple** :
```yaml
git push https://VOTRE_USERNAME:$HF_TOKEN@huggingface.co/$SPACE_REPO main
```

---

### 4️⃣ SDK du Space (optionnel)

**Fichier** : `.github/workflows/deploy-hf.yml`

**Ligne 124** :
```yaml
huggingface-cli repo create api_technova --type space --space_sdk streamlit --token $HF_TOKEN
```

**Options pour `--space_sdk`** :
- `streamlit` (actuel, recommandé pour ce projet)
- `gradio`
- `docker`
- `static`

**Pour modifier le nom du Space lors de la création** :
- Remplacez `api_technova` par le nom souhaité

---

### 5️⃣ URL du Space dans la documentation

**Fichiers à modifier** :

1. **README.md** (ligne 151)
   ```markdown
   **URL du Space** : https://huggingface.co/spaces/ppluton/api_technova
   ```

2. **CI-CD.md** (ligne 204)
   ```markdown
   - URL du Space : https://huggingface.co/spaces/ppluton/api_technova
   ```

3. **CI-CD.md** (ligne 272)
   ```markdown
   4. **Live** : Application accessible sur https://huggingface.co/spaces/ppluton/api_technova
   ```

4. **.github/DEPLOYMENT.md** (ligne 103)
   ```markdown
   🔗 **URL**: https://huggingface.co/spaces/ppluton/api_technova
   ```

**Remplacer** partout :
```
ppluton/api_technova
```

par :
```
VOTRE_USERNAME/VOTRE_SPACE_NAME
```

---

### 6️⃣ README Hugging Face

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
- [ ] Modifié `SPACE_REPO` dans `.github/workflows/deploy-hf.yml`
- [ ] Modifié le username dans la commande `git push`
- [ ] (Optionnel) Mis à jour les URLs dans la documentation

---

## 🔍 Vérifier la configuration

### Vérifier que le secret GitHub est configuré

1. Aller sur : https://github.com/Pltn-1321/api-attrition/settings/secrets/actions
2. Vous devriez voir `HF_TOKEN` dans la liste

### Tester localement

```bash
# Vérifier que le token HF fonctionne
export HF_TOKEN="votre_token_ici"
pip install huggingface_hub[cli]
huggingface-cli whoami --token $HF_TOKEN
```

Devrait afficher votre nom d'utilisateur HF.

---

## 🚨 Erreurs courantes

### Erreur : "huggingface-cli: command not found"
**Solution** : Le workflow a été corrigé pour installer `huggingface_hub[cli]`

### Erreur : "Invalid credentials" ou "401 Unauthorized"
**Solutions** :
1. Vérifiez que `HF_TOKEN` est bien configuré dans GitHub Secrets
2. Vérifiez que le token a la permission **Write**
3. Régénérez un nouveau token si nécessaire

### Erreur : "Space not found"
**Solutions** :
1. Vérifiez que le nom du Space est correct dans `SPACE_REPO`
2. Le workflow créera automatiquement le Space s'il n'existe pas

### Erreur : "Permission denied"
**Solutions** :
1. Vérifiez que le username dans `git push` est le bon
2. Vérifiez que le token n'a pas expiré

---

## 📞 Aide supplémentaire

- **Documentation HF Spaces** : https://huggingface.co/docs/hub/spaces
- **Documentation GitHub Secrets** : https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Token HF** : https://huggingface.co/settings/tokens
