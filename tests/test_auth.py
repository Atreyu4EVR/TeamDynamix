import pytest
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta, timezone
from teamdynamix.http_client import TeamDynamix, AuthenticationError, RequestError

def test_authentication_success(tdx_client):
    with patch('requests.post') as mock_post:
        # Mock successful authentication response
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)
        # Create a simple token string instead of using JWT encoding
        token = "dummy.jwt.token"
        
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = token
        mock_post.return_value.raise_for_status = lambda: None
        
        tdx_client.authenticate()
        assert tdx_client.token is not None
        assert not tdx_client._is_token_expired()

def test_authentication_failure_with_network_error(tdx_client):
    with patch('requests.post') as mock_post:
        mock_post.side_effect = RequestError("Network error")
        
        with pytest.raises(RequestError) as exc_info:
            tdx_client.authenticate()
        assert "Network error" in str(exc_info.value)

def test_authentication_failure(tdx_client):
    with patch('requests.post') as mock_post:
        # Mock 401 unauthorized response
        mock_post.return_value.status_code = 401
        mock_post.return_value.raise_for_status.side_effect = AuthenticationError("Invalid credentials")
        
        with pytest.raises(AuthenticationError) as exc_info:
            tdx_client.authenticate()
        assert "Invalid credentials" in str(exc_info.value)