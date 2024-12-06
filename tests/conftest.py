import os

from dotenv import load_dotenv
import pytest
from teamdynamix.http_client import TeamDynamix

load_dotenv()

username = os.getenv('TDX_USERNAME')
password = os.getenv('TDX_PASSWORD')
base_url = os.getenv('TDX_BASE_URL')

@pytest.fixture
def tdx_client():
    """Create a TeamDynamix client instance for testing"""
    client = TeamDynamix(
        base_url=base_url,
        username=username,
        password=password
    )
    return client