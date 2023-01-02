# Copyright (C) 2021-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the warn_workflow script."""

import importlib
import os
import sys
import types

import _pytest.fixtures
import pytest


@pytest.fixture
def root_directory() -> str:
    """Return the root directory of the repository."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def warn_workflow(root_directory: str) -> types.ModuleType:
    """Load the check_metadata module."""
    sys.path.insert(0, os.path.join(root_directory, "scripts"))
    warn_workflow = importlib.import_module("warn_workflow")
    sys.path.pop(0)
    return warn_workflow


@pytest.fixture
def token(request: _pytest.fixtures.SubRequest) -> str:
    """Get token passed on the command line."""
    return request.config.getoption("--token")  # type: ignore[no-any-return]


def test_warn_workflow_success(warn_workflow: types.ModuleType, token: str) -> None:
    """
    Test the warn_workflow function on the current repository with days_elapsed=60 (current GitHub limit).

    This test will surely pass on GitHub Actions, because the workflow must be active in order for CI to run.
    This test will pass on a local clone of the repository if the workflow in this repository is being kept active.
    """
    warn_workflow.warn_workflow(
        "fem-on-colab/warn-workflow-about-to-be-disabled-action", "ci.yml", "main", 60, token)


def test_check_metadata_fail(warn_workflow: types.ModuleType, token: str) -> None:
    """Test the warn_workflow function on the current repository with days_elapsed=-1, which forces failure."""
    with pytest.raises(RuntimeError) as excinfo:
        warn_workflow.warn_workflow(
            "fem-on-colab/warn-workflow-about-to-be-disabled-action", "ci.yml", "main", -1, token)
    assert "Workflow ci.yml is going to be disabled in" in str(excinfo.value)
