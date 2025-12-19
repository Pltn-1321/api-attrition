FROM python:3.11-slim

WORKDIR /app

# Installer dépendances système
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . .

# Exposer les ports
EXPOSE 7860 8000

# Variables d'environnement pour HF Spaces
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV API_URL=http://localhost:8000
ENV DB_TYPE=sqlite

# Lancer streamlit_launcher.py (adapté pour HF Spaces)
CMD ["python", "streamlit_launcher.py"]
