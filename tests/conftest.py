# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""pytest configuration file for tests."""

import pytest


def pytest_addoption(parser: pytest.Parser, pluginmanager: pytest.PytestPluginManager) -> None:
    """Add options to set the token to be used while running tests."""
    parser.addoption("--token", type=str, default="", help="Token to be used while running tests")
