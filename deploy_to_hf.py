#!/usr/bin/env python3
"""
Script de déploiement automatique vers Hugging Face Spaces
Utilise l'API Python huggingface_hub au lieu du CLI
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from huggingface_hub import HfApi, login, create_repo, repo_exists


# Configuration
HF_USERNAME = "Pedro1321"
SPACE_NAME = "Api-Technova"
SPACE_REPO_ID = f"{HF_USERNAME}/{SPACE_NAME}"
SPACE_SDK = "streamlit"


def print_step(message):
    """Affiche un message formaté"""
    print(f"\n{'='*70}")
    print(f"  {message}")
    print(f"{'='*70}\n")


def check_token():
    """Vérifie que le token HF est disponible"""
    token = os.getenv("HF_TOKEN")
    if not token:
        print("❌ Erreur: Variable d'environnement HF_TOKEN non définie")
        sys.exit(1)
    return token


def prepare_files(source_dir, dest_dir):
    """Copie les fichiers nécessaires en excluant certains dossiers"""
    print_step("📋 Préparation des fichiers pour le déploiement")

    # Créer le répertoire de destination
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Fichiers et dossiers à exclure
    exclude_patterns = {
        '.git', '.github', '__pycache__', '.pytest_cache',
        'hf_space', 'docker-compose.yml', 'start.sh',
        'streamlit_launcher.py', 'README_HF.md', 'deploy_to_hf.py',
        '.venv', 'venv', '*.pyc', '.DS_Store'
    }

    # Copier tous les fichiers sauf les exclus
    for item in source_dir.iterdir():
        if item.name in exclude_patterns or any(item.match(p) for p in exclude_patterns):
            print(f"  ⏭️  Ignoré: {item.name}")
            continue

        dest_item = dest_dir / item.name

        if item.is_dir():
            print(f"  📁 Copie du dossier: {item.name}")
            shutil.copytree(item, dest_item, dirs_exist_ok=True)
        else:
            print(f"  📄 Copie du fichier: {item.name}")
            shutil.copy2(item, dest_item)

    # Copier README_HF.md vers README.md
    readme_hf = source_dir / "README_HF.md"
    if readme_hf.exists():
        print(f"  📝 Copie de README_HF.md → README.md")
        shutil.copy2(readme_hf, dest_dir / "README.md")

    # Vérifier que database.db existe
    db_file = dest_dir / "database.db"
    if not db_file.exists():
        print("  ⚠️  database.db manquant, génération...")
        # Copier depuis la source si disponible
        source_db = source_dir / "database.db"
        if source_db.exists():
            shutil.copy2(source_db, db_file)
        else:
            print("  ❌ Erreur: database.db introuvable")
            sys.exit(1)

    print(f"\n✅ Fichiers préparés dans: {dest_dir}")

    # Afficher la liste des fichiers
    print("\n📦 Fichiers à déployer:")
    for item in sorted(dest_dir.rglob("*")):
        if item.is_file():
            size = item.stat().st_size / 1024  # en KB
            print(f"  - {item.relative_to(dest_dir)} ({size:.1f} KB)")


def deploy_to_space(token, deploy_dir):
    """Déploie les fichiers vers Hugging Face Spaces"""
    print_step(f"🚀 Déploiement vers Hugging Face Spaces: {SPACE_REPO_ID}")

    try:
        # Connexion à Hugging Face
        print("🔐 Authentification à Hugging Face...")
        login(token=token, add_to_git_credential=True)

        # Initialiser l'API
        api = HfApi()

        # Vérifier si le Space existe
        space_exists = False
        try:
            api.repo_info(repo_id=SPACE_REPO_ID, repo_type="space", token=token)
            space_exists = True
            print(f"✅ Space existant trouvé: {SPACE_REPO_ID}")
        except Exception:
            print(f"🆕 Le Space n'existe pas, création en cours...")

        # Créer le Space s'il n'existe pas
        if not space_exists:
            try:
                create_repo(
                    repo_id=SPACE_REPO_ID,
                    repo_type="space",
                    space_sdk=SPACE_SDK,
                    private=False,
                    token=token
                )
                print(f"✅ Space créé: {SPACE_REPO_ID}")
            except Exception as e:
                print(f"⚠️  Erreur lors de la création (peut déjà exister): {e}")

        # Cloner le repository
        clone_dir = Path("/tmp/hf_space")
        if clone_dir.exists():
            shutil.rmtree(clone_dir)

        print(f"\n📥 Clonage du Space...")
        clone_url = f"https://huggingface.co/spaces/{SPACE_REPO_ID}"

        subprocess.run(
            ["git", "clone", clone_url, str(clone_dir)],
            check=True,
            capture_output=True
        )

        print(f"✅ Space cloné dans: {clone_dir}")

        # Copier les fichiers
        print("\n📋 Copie des fichiers vers le Space...")

        # Supprimer les anciens fichiers (sauf .git)
        for item in clone_dir.iterdir():
            if item.name != ".git":
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

        # Copier les nouveaux fichiers
        for item in deploy_dir.iterdir():
            dest_item = clone_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest_item)

        # Configurer Git LFS pour database.db
        print("\n🔧 Configuration de Git LFS...")
        os.chdir(clone_dir)

        subprocess.run(["git", "lfs", "install"], check=True)
        subprocess.run(["git", "lfs", "track", "*.db"], check=True)

        # Ajouter tous les fichiers
        print("\n➕ Ajout des fichiers au commit...")
        subprocess.run(["git", "add", "."], check=True)

        # Vérifier s'il y a des changements
        result = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            capture_output=True
        )

        if result.returncode == 0:
            print("ℹ️  Aucun changement à déployer")
            return

        # Créer le commit
        print("\n💾 Création du commit...")
        from datetime import datetime
        commit_msg = f"🚀 Deploy from GitHub Actions - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True
        )

        # Pousser vers HF Spaces
        print("\n⬆️  Push vers Hugging Face Spaces...")
        push_url = f"https://{HF_USERNAME}:{token}@huggingface.co/spaces/{SPACE_REPO_ID}"

        subprocess.run(
            ["git", "push", push_url, "main"],
            check=True
        )

        print_step("✅ Déploiement réussi sur Hugging Face Spaces!")
        print(f"🔗 URL du Space: https://huggingface.co/spaces/{SPACE_REPO_ID}")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erreur lors de l'exécution de la commande Git:")
        print(f"   Commande: {e.cmd}")
        print(f"   Code de sortie: {e.returncode}")
        if e.stdout:
            print(f"   Stdout: {e.stdout.decode()}")
        if e.stderr:
            print(f"   Stderr: {e.stderr.decode()}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur lors du déploiement: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Point d'entrée principal"""
    print_step("🚀 Déploiement automatique vers Hugging Face Spaces")

    # Vérifier le token
    token = check_token()

    # Répertoires
    source_dir = Path.cwd()
    deploy_dir = Path("/tmp/hf_deploy")

    # Nettoyer le répertoire de déploiement s'il existe
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)

    # Préparer les fichiers
    prepare_files(source_dir, deploy_dir)

    # Déployer vers HF Spaces
    deploy_to_space(token, deploy_dir)

    print_step("🎉 Déploiement terminé avec succès!")


if __name__ == "__main__":
    main()
