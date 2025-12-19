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
import requests

# Processus globaux pour la gestion du signal
api_process = None
streamlit_process = None


def check_port_available(port):
    """Vérifie si un port est disponible"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) != 0


def wait_for_api(port, max_retries=30, retry_interval=1):
    """
    Attend que l'API soit prête en vérifiant le endpoint /health.

    Args:
        port: Port de l'API
        max_retries: Nombre maximum de tentatives (défaut: 30)
        retry_interval: Intervalle entre les tentatives en secondes (défaut: 1)

    Returns:
        bool: True si l'API est prête, False sinon
    """
    api_url = f"http://localhost:{port}/health"
    print(f"   ⏳ Attente de la disponibilité de l'API (max {max_retries}s)...")

    for retry_count in range(max_retries):
        try:
            response = requests.get(api_url, timeout=1)
            if response.status_code == 200:
                print(f"   ✅ API est prête ! (démarrage en {retry_count + 1}s)")
                return True
        except (requests.ConnectionError, requests.Timeout):
            pass

        # Afficher un message de progression toutes les 5 secondes
        if (retry_count + 1) % 5 == 0:
            print(f"   ⏳ Toujours en attente de l'API... ({retry_count + 1}s)")

        time.sleep(retry_interval)

    print(f"   ⚠️  L'API n'a pas démarré après {max_retries}s")
    return False


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

    # Configuration des ports
    # HF Spaces utilise le port 7860, développement local utilise 8501
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    API_PORT = 8000

    # Obtenir le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Chemins
    main_py = os.path.join(script_dir, "main.py")
    app_path = os.path.join(script_dir, "app.py")

    # Vérifier que les fichiers existent
    if not os.path.exists(main_py):
        print(f"❌ Erreur: {main_py} n'existe pas")
        sys.exit(1)

    if not os.path.exists(app_path):
        print(f"❌ Erreur: {app_path} n'existe pas")
        sys.exit(1)

    # Vérifier les ports
    if not check_port_available(API_PORT):
        print(f"⚠️  Le port {API_PORT} (API) est déjà utilisé")
        print(f"   Arrêtez le processus avec: lsof -ti:{API_PORT} | xargs kill -9")
        sys.exit(1)

    if not check_port_available(STREAMLIT_PORT):
        print(f"⚠️  Le port {STREAMLIT_PORT} (Streamlit) est déjà utilisé")
        print(f"   Arrêtez le processus avec: lsof -ti:{STREAMLIT_PORT} | xargs kill -9")
        sys.exit(1)

    print("=" * 60)
    print("🚀 Lancement de l'application API Attrition")
    print("=" * 60)

    # Lancer l'API FastAPI
    print(f"\n📡 Démarrage de l'API FastAPI sur le port {API_PORT}...")
    try:
        api_process = subprocess.Popen(
            ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", str(API_PORT)],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"   ✅ API démarrée sur http://localhost:{API_PORT}")
        print(f"   📖 Documentation: http://localhost:{API_PORT}/docs")

        # Attendre que l'API soit prête avec retry logic
        api_ready = wait_for_api(API_PORT, max_retries=30, retry_interval=1)
        if not api_ready:
            print("   ⚠️  L'API n'est pas disponible, mais on continue le lancement de Streamlit...")

    except FileNotFoundError:
        print("\n❌ Uvicorn n'est pas installé. Installez-le avec:")
        print("   uv add uvicorn")
        sys.exit(1)

    # Lancer Streamlit
    print(f"\n🎨 Démarrage de l'interface Streamlit sur le port {STREAMLIT_PORT}...")
    try:
        streamlit_process = subprocess.Popen(
            [
                "streamlit",
                "run",
                app_path,
                "--server.port",
                str(STREAMLIT_PORT),
                "--server.address",
                "0.0.0.0",
                "--server.headless",
                "true",
            ],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"   ✅ Streamlit démarré sur http://localhost:{STREAMLIT_PORT}")

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
    print(f"   🌐 Interface Streamlit: http://localhost:{STREAMLIT_PORT}")
    print(f"   🔌 API FastAPI:         http://localhost:{API_PORT}")
    print(f"   📚 Documentation API:   http://localhost:{API_PORT}/docs")
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
