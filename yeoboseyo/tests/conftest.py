# coding: utf-8
"""
   여보세요 - Tests
"""

import pytest


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio", {"debug": True}
