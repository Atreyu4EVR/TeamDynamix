import pytest
from teamdynamix.http_client import TeamDynamix

def test_import():
    import teamdynamix
    assert hasattr(teamdynamix, '__version__')

def test_client_initialization():
    client = TeamDynamix(
        base_url="https://test.teamdynamix.com",
        username="test_user",
        password="test_pass"
    )
    assert client.base_url == "https://test.teamdynamix.com"
    assert client.username == "test_user"
    assert client.password == "test_pass"

def test_client_initialization_missing_url():
    with pytest.raises(ValueError) as exc_info:
        TeamDynamix(base_url=None, username="test", password="test")
    assert "Base URL is required" in str(exc_info.value) 