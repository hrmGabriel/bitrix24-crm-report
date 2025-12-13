import requests
from typing import Any, Dict
from .config import BITRIX_URL, BITRIX_USER_ID, BITRIX_WEBHOOK

class BitrixClient:
    """
    Client to interact with Bitrix API.
    
    This client makes requests to the Bitrix API using a configured webhook.
    It can perform both simple calls and paginated calls to retrieve large data sets.

    This client expects the required environment variables to be correctly set.
    """
    def __init__(
        self,
        base_url: str = BITRIX_URL,
        user_id: str = BITRIX_USER_ID,
        webhook: str = BITRIX_WEBHOOK,
    ):
        """
        Initializes the client with API URL, user ID, and webhook.

        Arguments:
        - base_url: Base URL of the Bitrix API (default: BITRIX_URL).
        - user_id: User ID for Bitrix (default: BITRIX_USER_ID).
        - webhook: Webhook for authentication (default: BITRIX_WEBHOOK).

        Raises an error if any required value is missing.
        """
        if not base_url or not user_id or not webhook:
            raise RuntimeError("Configuration error: Missing required environment variables.")

        # Set the configuration for the client
        self.base_url = base_url.rstrip("/")  # Removes any trailing slash from the URL
        self.user_id = user_id
        self.webhook = webhook

    def _get_full_url(self, method: str) -> str:
        """
        Builds the full URL for a Bitrix API method call.
        
        Example:
        For the method 'profile', the URL would be:
        https://example.com/rest/{user_id}/{webhook}/profile
        
        Arguments:
        - method: The name of the method (e.g., "profile").
        
        Returns:
        - The full URL for the API call.
        """
        return f"{self.base_url}/rest/{self.user_id}/{self.webhook}/{method}"

    def call(self, method: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Makes a request to the Bitrix API and returns the response.

        Arguments:
        - method: The API method to be called (e.g., "profile").
        - payload: Data to be sent in the request (optional).
        
        Returns:
        - The API response (as a dictionary).
        
        Raises an error if the response contains an API error.
        """
        url = self._get_full_url(method)  # Get the full URL for the method
        response = requests.post(url, json=payload or {})  # Make the POST request

        # Check if there was an error in the HTTP response (e.g., 4xx or 5xx)
        response.raise_for_status()

        # Convert the response to JSON
        data = response.json()

        # Check if the API returned an error
        if "error" in data:
            raise RuntimeError(
                f"Bitrix API error: {data['error']} - {data.get('error_description')}"
            )

        return data

    def call_all(self, method: str, payload: Dict[str, Any] | None = None) -> list:
        """
        Makes paginated requests to the Bitrix API.

        This method makes multiple API calls to fetch all the results if the response is large 
        and split into several pages.

        Arguments:
        - method: The API method to be called (e.g., "list").
        - payload: Additional data to be sent (optional).
        
        Returns:
        - A list containing all the results from all pages.
        """
        results = []  # List to store all results
        start = 0  # Pagination control

        while True:
            # Prepare the request body with the "start" parameter for pagination
            body = payload.copy() if payload else {}
            body["start"] = start

            # Make the request and get the data
            data = self.call(method, body)

            # If the response does not contain "result", stop pagination
            if "result" not in data:
                break

            # Add the results to the list
            results.extend(data["result"])

            # If there is no "next" in the response, stop the loop
            if "next" not in data:
                break

            # Update "start" to fetch the next page of results
            start = data["next"]

        return results
