import os
import sys
from pathlib import Path
from shutil import rmtree
from subprocess import check_call, check_output
from typing import Tuple

import pytest

from git_some.tag_version import tag_version

TEST_PROJECTS_DIRECTORY: Path = Path(__file__).resolve().parent / "projects"


def _test_project_tag_version(project_directory: Path) -> None:
    current_directory: Path = Path.cwd()
    os.chdir(project_directory)
    try:
        # Delete git configuration files, if they exist
        rmtree(project_directory / ".git", ignore_errors=True)
        # Intialize a local git repository, and create a commit
        check_call(("git", "init"))
        check_call(
            ("git", "config", "--local", "user.email", "you@example.com")
        )
        check_call(("git", "config", "--local", "user.name", "Your Name"))
        check_call(("git", "add", "."))
        check_call(("git", "commit", "-m", "*"))
    finally:
        os.chdir(current_directory)
    # Tag the local git repo with the version number
    # Note: This is executed from the user's working directory
    # to avoid conflict with relative path environment variables
    version: str = tag_version(project_directory)
    # Return to the git project directory
    os.chdir(project_directory)
    try:
        # Verify that the tag was created successfully
        tags: Tuple[str, ...] = tuple(
            check_output(
                ("git", "tag"),
                text=True,
            )
            .strip()
            .split("\n")
        )
        assert version in tags, f"Version {version} not found in tags: {tags}"
    finally:
        os.chdir(current_directory)
        # Cleanup git configuration files
        rmtree(project_directory / ".git", ignore_errors=True)


def test_setuptools_project_tag_version() -> None:
    """
    Test functionality used by the `git-some tag-version` command
    with setuptools built projects
    """
    _test_project_tag_version(TEST_PROJECTS_DIRECTORY / "test_project_a")
    _test_project_tag_version(TEST_PROJECTS_DIRECTORY / "test_project_b")


def test_hatch_project_tag_version() -> None:
    """
    Test functionality used by the `git-some tag-version` command
    with hatch built projects
    """
    try:
        _test_project_tag_version(
            TEST_PROJECTS_DIRECTORY / "hatch_test_project"
        )
    except Exception:
        if os.environ.get("CI", None) and sys.platform != "linux":
            pytest.skip("Skipping hatch project test on windows/mac CI")


def test_poetry_project_tag_version() -> None:
    """
    Test functionality used by the `git-some tag-version` command
    with poetry built projects
    """
    try:
        _test_project_tag_version(
            TEST_PROJECTS_DIRECTORY / "poetry_test_project"
        )
    except Exception:
        if os.environ.get("CI", None) and sys.platform != "linux":
            pytest.skip("Skipping hatch project test on windows/mac CI")


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
