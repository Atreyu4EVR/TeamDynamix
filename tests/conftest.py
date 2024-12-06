import os

import pytest
from teamdynamix.http_client import TeamDynamix


@pytest.fixture
def tdx_client():
    """
    Create a TeamDynamix client fixture for testing.
    Uses dummy values that will be mocked in tests.
    """
    client = TeamDynamix(
        base_url="https://test.teamdynamix.com",  # Add dummy base URL
        username="test_user",
        password="test_pass"
    )
    return client