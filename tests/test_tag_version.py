from __future__ import annotations

import os
import sys
from pathlib import Path
from shutil import rmtree, which
from subprocess import check_call

import pytest

from gittable._utilities import check_output
from gittable.tag_version import tag_version

TEST_PROJECTS_DIRECTORY: Path = Path(__file__).resolve().parent / "projects"
GIT: str = which("git") or "git"


def _test_project_tag_version(project_directory: Path) -> None:
    current_directory: Path = Path.cwd()
    os.chdir(project_directory)
    try:
        # Delete git configuration files, if they exist
        rmtree(project_directory / ".git", ignore_errors=True)
        # Intialize a local git repository, and create a commit
        check_call((GIT, "init"))
        check_call((GIT, "config", "--local", "user.email", "you@example.com"))
        check_call((GIT, "config", "--local", "user.name", "Your Name"))
        check_call((GIT, "add", "."))
        check_call((GIT, "commit", "-m", "*"))
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
        tags: tuple[str, ...] = tuple(
            check_output(
                (GIT, "tag"),
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
    Test functionality used by the `gittable tag-version` command
    with setuptools built projects
    """
    _test_project_tag_version(TEST_PROJECTS_DIRECTORY / "test_project_a")
    _test_project_tag_version(TEST_PROJECTS_DIRECTORY / "test_project_b")


def test_hatch_project_tag_version() -> None:
    """
    Test functionality used by the `gittable tag-version` command
    with hatch built projects
    """
    try:
        _test_project_tag_version(
            TEST_PROJECTS_DIRECTORY / "hatch_test_project"
        )
    except Exception:
        if os.environ.get("CI", None) and sys.platform != "linux":
            pytest.skip("Skipping hatch project test on windows/mac CI")
        else:
            raise


def test_poetry_project_tag_version() -> None:
    """
    Test functionality used by the `gittable tag-version` command
    with poetry built projects
    """
    try:
        _test_project_tag_version(
            TEST_PROJECTS_DIRECTORY / "poetry_test_project"
        )
    except Exception:
        if os.environ.get("CI", None) and sys.platform != "linux":
            pytest.skip("Skipping hatch project test on windows/mac CI")
        else:
            raise


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
