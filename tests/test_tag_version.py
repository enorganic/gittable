import os
from pathlib import Path
from shutil import rmtree
from subprocess import check_call, check_output

import pytest

from git_some.tag_version import tag_version

TEST_PROJECTS_DIRECTORY: Path = Path(__file__).resolve().parent / "projects"


def test_tag_version() -> None:
    """
    Test functionality used by the `git-some tag-version` command
    """
    current_directory: Path = Path.cwd()
    project_directory: Path
    for project_directory in map(
        Path.resolve, filter(Path.is_dir, TEST_PROJECTS_DIRECTORY.iterdir())
    ):
        os.chdir(project_directory)
        try:
            # Delete git configuration files, if they exist
            rmtree(project_directory / ".git", ignore_errors=True)
            # Intialize a local git repository, and create a commit
            check_call(("git", "init"))
            check_call(("git", "add", "."))
            check_call(("git", "commit", "-m", "*"))
            check_call(("git", "config", "user.email", "you@example.com"))
            check_call(("git", "config", "user.name", "Your Name"))
            # Tag the local git repo with the version number
            version: str = tag_version()
            # Verify that the tag was created successfully
            assert version in check_output(
                ("git", "tag"),
                text=True,
            ).strip().split("\n"), f"Version {version} not found in tags"
        finally:
            os.chdir(current_directory)
            # Cleanup git configuration files
            rmtree(project_directory / ".git", ignore_errors=True)


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
