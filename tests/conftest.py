import os
import time
from unittest.mock import patch

from pytest import fixture

from src.common.consts import RATE_LIMIT_WINDOW_SIZE


@fixture
def mock_default_env_vars():
    with patch.dict(os.environ, {}):
        yield


@fixture
def clear_rate_limit():
    """
    Wait for the rate limit request count to reset, before and after the test
    """
    time.sleep(RATE_LIMIT_WINDOW_SIZE)
    yield
    time.sleep(RATE_LIMIT_WINDOW_SIZE)
