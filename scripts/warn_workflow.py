# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Script to warn when a scheduled workflow is about to be disabled."""

import datetime
import sys

import dateutil.parser
import dateutil.tz
import requests


def warn_workflow(
    repository_name: str, workflow_filename: str, main_branch: str, days_elapsed: int, token: str
) -> None:
    """Warn when a scheduled workflow is about to be disabled."""
    if token != "":
        headers = {"Authorization": f"token {token}"}
    else:
        headers = None
    # Get latest workflow update
    workflow_response = requests.get(
        f"https://api.github.com/repos/{repository_name}/actions/workflows/{workflow_filename}",
        headers=headers).json()
    assert "path" in workflow_response, f"Response is {workflow_response} and does not contain 'path'"
    assert workflow_response["path"] == f".github/workflows/{workflow_filename}", (
        f"Path is {workflow_response['path']}")
    assert "updated_at" in workflow_response, f"Response is {workflow_response} and does not contain 'updated_at'"
    workflow_latest_update = dateutil.parser.parse(workflow_response["updated_at"])
    workflow_latest_update = workflow_latest_update.astimezone(dateutil.tz.tzutc())
    # Get latest commit on the main branch
    main_branch_response = requests.get(
        f"https://api.github.com/repos/{repository_name}/branches/{main_branch}", headers=headers).json()
    assert "name" in main_branch_response, f"Response is {main_branch_response} and does not contain 'name'"
    assert main_branch_response["name"] == main_branch, f"Name is {main_branch_response['name']}"
    assert "commit" in main_branch_response, f"Response is {main_branch_response} and does not contain 'commit'"
    assert "commit" in main_branch_response["commit"], (
        f"Commit is {main_branch_response['commit']} and does not contain 'commit'")
    assert "committer" in main_branch_response["commit"]["commit"], (
        f"Commit is {main_branch_response['commit']['commit']} and does not contain 'committer'")
    assert "date" in main_branch_response["commit"]["commit"]["committer"], (
        f"Commit is {main_branch_response['commit']['commit']['committer']} and does not contain 'date'")
    main_branch_latest_update = dateutil.parser.parse(main_branch_response["commit"]["commit"]["committer"]["date"])
    main_branch_latest_update = main_branch_latest_update.astimezone(dateutil.tz.tzutc())
    # Determine how many days have passed since the latest update
    assert workflow_latest_update.tzinfo == main_branch_latest_update.tzinfo
    now = datetime.datetime.now(workflow_latest_update.tzinfo)
    days_diff = (now - max(workflow_latest_update, main_branch_latest_update)).days
    if days_diff >= days_elapsed:
        raise RuntimeError(
            f"Workflow {workflow_filename} is going to be disabled in {60 - days_diff} days. "
            + "To prevent this, please temporarily manually disable the workflow and then immediately re-enable it."
        )


if __name__ == "__main__":
    assert len(sys.argv) == 6
    warn_workflow(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5])
