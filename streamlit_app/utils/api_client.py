"""Client API réutilisable pour communiquer avec l'API FastAPI."""

import requests
from typing import Optional, Dict, Any, List
from config import API_URL


class APIClient:
    """Client pour interagir avec l'API Attrition."""

    def __init__(self, base_url: str = API_URL):
        """
        Initialise le client API.

        Args:
            base_url: URL de base de l'API
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = 10

    def _make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Effectue une requête HTTP vers l'API.

        Args:
            method: Méthode HTTP (GET, POST, etc.)
            endpoint: Endpoint de l'API
            **kwargs: Arguments supplémentaires pour requests

        Returns:
            Réponse JSON ou None en cas d'erreur
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur API : {str(e)}")

    def health_check(self) -> Dict[str, Any]:
        """
        Vérifie l'état de l'API.

        Returns:
            Status de l'API et de la base de données
        """
        return self._make_request("GET", "/health")

    def get_employees(
        self, skip: int = 0, limit: int = 100
    ) -> Dict[str, Any]:
        """
        Récupère la liste des employés avec pagination.

        Args:
            skip: Nombre d'employés à ignorer
            limit: Nombre maximum d'employés à retourner

        Returns:
            Dictionnaire contenant 'total' et 'employees'
        """
        params = {"skip": skip, "limit": limit}
        return self._make_request("GET", "/employees", params=params)

    def get_employee(self, employee_id: int) -> Dict[str, Any]:
        """
        Récupère un employé spécifique par son ID.

        Args:
            employee_id: ID de l'employé

        Returns:
            Données de l'employé
        """
        return self._make_request("GET", f"/employees/{employee_id}")

    def filter_employees(
        self,
        departement: Optional[str] = None,
        poste: Optional[str] = None,
        age_min: Optional[int] = None,
        age_max: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Filtre les employés côté client (en attendant les filtres API).

        Args:
            departement: Filtre par département
            poste: Filtre par poste
            age_min: Âge minimum
            age_max: Âge maximum
            skip: Nombre d'employés à ignorer
            limit: Nombre maximum d'employés

        Returns:
            Liste d'employés filtrés
        """
        # Récupère tous les employés (ou un grand nombre)
        data = self.get_employees(skip=skip, limit=limit)
        employees = data.get("employees", [])

        # Applique les filtres
        filtered = employees

        if departement:
            filtered = [e for e in filtered if e.get("departement") == departement]

        if poste:
            filtered = [e for e in filtered if e.get("poste") == poste]

        if age_min is not None:
            filtered = [e for e in filtered if e.get("age", 0) >= age_min]

        if age_max is not None:
            filtered = [e for e in filtered if e.get("age", 999) <= age_max]

        return filtered
