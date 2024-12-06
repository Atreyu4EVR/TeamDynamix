import pytest
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta, timezone

def test_authentication_success(tdx_client):
    with patch('requests.post') as mock_post:
        # Mock successful authentication response
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = jwt.encode(
            {'exp': datetime.now(timezone.utc) + timedelta(hours=1)},
            'secret'
        )
        
        tdx_client.authenticate()
        assert tdx_client.token is not None
        assert not tdx_client._is_token_expired()

def test_authentication_failure_with_network_error(tdx_client):
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Network error")
        
        with pytest.raises(Exception) as exc_info:
            tdx_client.authenticate()
        assert "Network error" in str(exc_info.value)

def test_authentication_failure(tdx_client):
    with patch('requests.post') as mock_post:
        # Mock the authentication failure
        mock_post.side_effect = Exception("Authentication failed")
        
        with pytest.raises(Exception) as exc_info:
            tdx_client.authenticate()
        assert "Authentication failed" in str(exc_info.value)