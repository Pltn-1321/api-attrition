#!/usr/bin/env python3
"""
Launcher complet pour l'application API Attrition
Lance l'API FastAPI et l'interface Streamlit depuis la racine du projet
"""
import os
import subprocess
import sys
import time
import signal
import socket

# Processus globaux pour la gestion du signal
api_process = None
streamlit_process = None

def check_port_available(port):
    """Vérifie si un port est disponible"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def signal_handler(_sig, _frame):
    """Gère l'arrêt propre des processus"""
    print("\n\n🛑 Arrêt des services...")

    if streamlit_process:
        print("   Arrêt de Streamlit...")
        streamlit_process.terminate()
        try:
            streamlit_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            streamlit_process.kill()

    if api_process:
        print("   Arrêt de l'API...")
        api_process.terminate()
        try:
            api_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            api_process.kill()

    print("👋 Services arrêtés proprement\n")
    sys.exit(0)

def main():
    global api_process, streamlit_process

    # Enregistrer le gestionnaire de signal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Obtenir le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Chemins
    main_py = os.path.join(script_dir, "main.py")
    app_path = os.path.join(script_dir, "streamlit_app", "app.py")

    # Vérifier que les fichiers existent
    if not os.path.exists(main_py):
        print(f"❌ Erreur: {main_py} n'existe pas")
        sys.exit(1)

    if not os.path.exists(app_path):
        print(f"❌ Erreur: {app_path} n'existe pas")
        sys.exit(1)

    # Vérifier les ports
    if not check_port_available(8000):
        print("⚠️  Le port 8000 (API) est déjà utilisé")
        print("   Arrêtez le processus avec: lsof -ti:8000 | xargs kill -9")
        sys.exit(1)

    if not check_port_available(8501):
        print("⚠️  Le port 8501 (Streamlit) est déjà utilisé")
        print("   Arrêtez le processus avec: lsof -ti:8501 | xargs kill -9")
        sys.exit(1)

    print("=" * 60)
    print("🚀 Lancement de l'application API Attrition")
    print("=" * 60)

    # Lancer l'API FastAPI
    print("\n📡 Démarrage de l'API FastAPI...")
    try:
        api_process = subprocess.Popen(
            ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("   ✅ API démarrée sur http://localhost:8000")
        print("   📖 Documentation: http://localhost:8000/docs")

        # Attendre que l'API soit prête
        print("   ⏳ Attente de la disponibilité de l'API...")
        time.sleep(3)

    except FileNotFoundError:
        print("\n❌ Uvicorn n'est pas installé. Installez-le avec:")
        print("   uv add uvicorn")
        sys.exit(1)

    # Lancer Streamlit
    print("\n🎨 Démarrage de l'interface Streamlit...")
    try:
        streamlit_process = subprocess.Popen(
            ["streamlit", "run", app_path],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("   ✅ Streamlit démarré sur http://localhost:8501")

    except FileNotFoundError:
        print("\n❌ Streamlit n'est pas installé. Installez-le avec:")
        print("   uv add streamlit")
        if api_process:
            api_process.terminate()
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✨ Application prête !")
    print("=" * 60)
    print("\n📍 URLs d'accès:")
    print("   🌐 Interface Streamlit: http://localhost:8501")
    print("   🔌 API FastAPI:         http://localhost:8000")
    print("   📚 Documentation API:   http://localhost:8000/docs")
    print("\n💡 Appuyez sur Ctrl+C pour arrêter les services")
    print("=" * 60 + "\n")

    # Garder le processus actif
    try:
        # Attendre que les processus se terminent
        api_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
