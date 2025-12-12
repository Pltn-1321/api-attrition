#!/usr/bin/env python3
"""
Point d'entrée pour Hugging Face Spaces
Lance l'API FastAPI et l'interface Streamlit dans un seul espace
"""
import os
import subprocess
import sys
import time
import signal
import threading

# Processus globaux pour la gestion du signal
api_process = None
streamlit_process = None


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


def stream_output(process, prefix):
    """Stream la sortie d'un processus ligne par ligne"""
    for line in iter(process.stdout.readline, b''):
        if line:
            print(f"{prefix}: {line.decode().strip()}")


def main():
    global api_process, streamlit_process

    # Enregistrer le gestionnaire de signal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Configuration des ports pour HF Spaces
    API_PORT = 8000
    STREAMLIT_PORT = 7860  # Port exposé par HF Spaces

    # S'assurer que DB_TYPE est SQLite (par défaut pour HF Spaces)
    os.environ["DB_TYPE"] = "sqlite"

    # Configurer l'URL de l'API pour Streamlit (localhost car dans le même container)
    os.environ["API_URL"] = f"http://localhost:{API_PORT}"

    # Obtenir le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Chemins
    main_py = os.path.join(script_dir, "main.py")
    app_path = os.path.join(script_dir, "streamlit_app", "app.py")

    print("=" * 70)
    print("🚀 Lancement de l'application API Attrition sur Hugging Face Spaces")
    print("=" * 70)

    # Lancer l'API FastAPI
    print(f"\n📡 Démarrage de l'API FastAPI sur le port {API_PORT}...")
    try:
        api_process = subprocess.Popen(
            [
                "uvicorn", "main:app",
                "--host", "0.0.0.0",
                "--port", str(API_PORT),
                "--log-level", "info"
            ],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1
        )
        print(f"   ✅ API démarrée sur http://localhost:{API_PORT}")

        # Lancer le thread pour streamer les logs de l'API
        api_thread = threading.Thread(
            target=stream_output,
            args=(api_process, "API"),
            daemon=True
        )
        api_thread.start()

        # Attendre que l'API soit prête
        print("   ⏳ Attente de la disponibilité de l'API...")
        time.sleep(5)

    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage de l'API: {e}")
        sys.exit(1)

    # Lancer Streamlit sur le port exposé par HF Spaces
    print(f"\n🎨 Démarrage de l'interface Streamlit sur le port {STREAMLIT_PORT}...")
    try:
        streamlit_process = subprocess.Popen(
            [
                "streamlit", "run", app_path,
                "--server.port", str(STREAMLIT_PORT),
                "--server.address", "0.0.0.0",
                "--server.headless", "true",
                "--browser.serverAddress", "0.0.0.0",
                "--browser.gatherUsageStats", "false"
            ],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1
        )
        print(f"   ✅ Streamlit démarré sur http://localhost:{STREAMLIT_PORT}")

        # Lancer le thread pour streamer les logs de Streamlit
        streamlit_thread = threading.Thread(
            target=stream_output,
            args=(streamlit_process, "STREAMLIT"),
            daemon=True
        )
        streamlit_thread.start()

    except Exception as e:
        print(f"\n❌ Erreur lors du démarrage de Streamlit: {e}")
        if api_process:
            api_process.terminate()
        sys.exit(1)

    print("\n" + "=" * 70)
    print("✨ Application prête sur Hugging Face Spaces !")
    print("=" * 70)
    print(f"\n📍 Configuration:")
    print(f"   🌐 Interface principale (Streamlit): Port {STREAMLIT_PORT}")
    print(f"   🔌 API Backend (FastAPI):            Port {API_PORT}")
    print(f"   💾 Base de données:                  SQLite (database.db)")
    print("=" * 70 + "\n")

    # Garder le processus actif en surveillant les sous-processus
    try:
        while True:
            # Vérifier si les processus sont toujours actifs
            if api_process.poll() is not None:
                print("❌ L'API s'est arrêtée de manière inattendue")
                if streamlit_process:
                    streamlit_process.terminate()
                sys.exit(1)

            if streamlit_process.poll() is not None:
                print("❌ Streamlit s'est arrêté de manière inattendue")
                if api_process:
                    api_process.terminate()
                sys.exit(1)

            time.sleep(1)

    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


if __name__ == "__main__":
    main()
