import pytest
from pathlib import Path


@pytest.fixture
def tmp_project(tmp_path):
    """Provides a temporary directory for project scaffolding tests."""
    return tmp_path