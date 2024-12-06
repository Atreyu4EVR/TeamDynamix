import os

from dotenv import load_dotenv
import pytest
from teamdynamix.tdnext import TeamDynamix

load_dotenv()

username = os.getenv('TDX_USERNAME')
password = os.getenv('TDX_PASSWORD')

@pytest.fixture
def tdx_client():
    """Create a TeamDynamix client instance for testing"""
    client = TeamDynamix(
        base_url="https://ensign.teamdynamix.com/TDWebApi",
        username=username,
        password=password
    )
    return client