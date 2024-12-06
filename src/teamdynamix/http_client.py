import os
import jwt
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from teamdynamix.tdnext.core import TDNext

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

class RequestError(Exception):
    """Raised when an API request fails"""
    pass

class TokenError(Exception):
    """Raised when token handling fails"""
    pass

class TeamDynamix:

    def __init__(self, base_url: Any, 
                 username: Optional[Any] = None, 
                 password: Optional[Any] = None,
                 beid: Optional[str] = None,
                 web_services_key: Optional[str] = None):
        """
        TeamDynamix API Client for interacting with TeamDynamix services.

        Args:
            base_url: Base URL for the TeamDynamix API (will be converted to string)
            username: Username for API authentication (will be converted to string)
            password: Password for API authentication (will be converted to string)
            beid: BEID for admin authentication (optional)
            web_services_key: Web Services Key for admin authentication (optional)

        Raises:
            ValueError: If no valid credentials are provided
        """
        # Convert inputs to strings and validate
        self.base_url = str(base_url).rstrip("/") if base_url else ""
        self.username = str(username) if username else ""
        self.password = str(password) if password else ""
        
        # Admin credentials
        self._beid = beid or os.environ.get('BEID')
        self._web_services_key = web_services_key or os.environ.get('WEB_SERVICES_KEY')

        # Validate that we have at least one set of credentials
        if not self.base_url:
            raise ValueError("Base URL is required")
        if not (
            (self.username and self.password) or 
            (self._beid and self._web_services_key)
        ):
            raise ValueError(
                "Either username/password or BEID/WebServicesKey must be provided"
            )

        self.token: Optional[str] = None
        self.token_expiration: Optional[datetime] = None
        self._token_refresh_buffer = timedelta(minutes=5)
        self.tdnext = TDNext(self)

    @classmethod
    def login_admin(cls, beid: str, web_services_key: str, base_url: str) -> str:
        """Admin authentication implementation..."""
        try:
            response = requests.post(
                f"{base_url}/api/auth/loginadmin",
                json={
                    "BEID": beid,
                    "WebServicesKey": web_services_key
                },
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            response.raise_for_status()
            
            if not response.text:
                raise AuthenticationError("Empty response received")
                
            return response.text.strip()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid administrative credentials")
            raise RequestError(f"Admin authentication failed: {e}")
        except requests.exceptions.RequestException as e:
            raise RequestError(f"Admin authentication request failed: {e}")

    def authenticate(self) -> None:
        """
        Authenticate with TeamDynamix API to retrieve a Bearer token.
        Will try admin authentication first if credentials are available.
        
        Raises:
            AuthenticationError: If authentication fails
            RequestError: If the request fails
        """
        try:
            if self._beid and self._web_services_key:
                self.token = self.login_admin(self._beid, self._web_services_key, self.base_url)
            else:
                auth_endpoint = f"{self.base_url}/api/auth"
                headers = {"Content-Type": "application/json; charset=utf-8"}
                payload = {"username": self.username, "password": self.password}

                response = requests.post(auth_endpoint, json=payload, headers=headers)
                response.raise_for_status()
                
                if not response.text:
                    raise AuthenticationError("Empty response received")
                    
                self.token = response.text.strip()
                
            assert isinstance(self.token, str)  # Type assertion
            self.token_expiration = self._decode_token_expiration(self.token)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid credentials")
            raise RequestError(f"Authentication failed: {e}")
        except requests.exceptions.RequestException as e:
            raise RequestError(f"Authentication request failed: {e}")

    def _decode_token_expiration(self, token: str) -> datetime:
        """
        Decode the JWT token to extract its expiration time (exp claim).
        
        Args:
            token: The JWT token string
        
        Returns:
            datetime: Token expiration time (24 hours from issuance)
        
        Raises:
            TokenError: If token cannot be decoded or is missing expiration claim
        """
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            exp_timestamp = decoded.get("exp")
            if not exp_timestamp:
                raise TokenError("Token missing expiration claim")
            return datetime.fromtimestamp(exp_timestamp, timezone.utc)
        except jwt.PyJWTError as e:
            raise TokenError(f"Failed to decode token: {e}")

    def _is_token_expired(self) -> bool:
        """
        Check if the current token is expired or needs refresh.
        Includes a 5-minute buffer before actual expiration.

        Returns:
            bool: True if token needs refresh, False otherwise
        """
        if not self.token or not self.token_expiration:
            return True
        
        refresh_time = self.token_expiration - self._token_refresh_buffer
        current_time = datetime.now(timezone.utc)
        return current_time >= refresh_time

    def _get_headers(self) -> Dict[str, str]:
        """
        Get the authorization headers, refreshing the token if necessary.
        
        Example:
        Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...

        Returns:
            Dict containing required headers for API requests
        
        Raises:
            AuthenticationError: If token refresh fails
        """
        if self._is_token_expired():
            self.authenticate()
            
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def request(self, method: str, endpoint: str, 
                params: Optional[Dict] = None, 
                data: Optional[Dict] = None, 
                json: Optional[Dict] = None,
                files: Optional[Dict] = None) -> Any:
        """
        Make an HTTP request to the TeamDynamix API.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                files=files
            )

            # Only log errors
            if response.status_code >= 400:
                print(f"Error Response: {response.status_code}")
                print(f"Response body: {response.text}")

                
            if response.status_code == 401:
                self.token = None
                headers = self._get_headers()
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    data=data,
                    json=json,
                    files=files
                )
                
            response.raise_for_status()
            return response.json() if response.text else None
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Token expired and refresh failed")
            raise RequestError(f"HTTP request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise RequestError(f"Request failed: {e}")

    def get(self, endpoint: str, **kwargs) -> Any:
        """Convenience method for GET requests"""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Any:
        """Convenience method for POST requests"""
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Any:
        """Convenience method for PUT requests"""
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Any:
        """Convenience method for PATCH requests"""
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Any:
        """Convenience method for DELETE requests"""
        return self.request("DELETE", endpoint, **kwargs)