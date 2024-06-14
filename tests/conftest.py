import os
import time
from unittest.mock import patch

from pytest import fixture


@fixture
def mock_default_env_vars():
    with patch.dict(os.environ, {}):
        yield


@fixture
def clear_rate_limit():
    """
    Wait for the rate limit request count to reset, before and after the test
    """
    rate_limit_window_seconds = 1

    time.sleep(rate_limit_window_seconds)
    yield
    time.sleep(rate_limit_window_seconds)
