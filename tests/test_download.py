from __future__ import annotations

import os
from shutil import rmtree
from subprocess import check_output
from tempfile import mkdtemp

import pytest

from gittable.download import download

PROJECT_DIRECTORY: str = os.path.join(
    os.path.dirname(os.path.dirname(__file__))
)
RELATIVE_FILE_PATH: str = os.path.relpath(
    os.path.abspath(__file__), PROJECT_DIRECTORY
)


def test_git_download() -> None:
    """
    Test functionality used by the `gittable download` command
    """
    temp_directory: str
    if os.name == "nt" and ("CI" in os.environ):
        # Github Windows test runners temp directory isn't writable for
        # some reason, so we create a temp directory under the current
        # directory, and plug it into the environment variables
        # from which python looks for a temp directory
        temp_directory = os.path.join(os.path.abspath(os.path.curdir), "TEMP")
        os.makedirs(temp_directory, exist_ok=True)
        os.environ["TMPDIR"] = os.environ["TEMP"] = os.environ["TMP"] = (
            temp_directory
        )
    temp_directory = mkdtemp(prefix="test_git_download_")
    current_directory: str = os.path.abspath(os.path.curdir)
    os.chdir(PROJECT_DIRECTORY)
    try:
        # Use this project's repo to test the download command
        origin: str = check_output(
            ("git", "remote", "get-url", "origin"),
            encoding="utf-8",
            universal_newlines=True,
        ).strip()
        py_paths: list[str] = download(
            origin, files="**/*.py", directory=temp_directory
        )
        assert py_paths
        path: str
        for path in py_paths:
            assert path.endswith(".py")
    finally:
        os.chdir(current_directory)
        rmtree(temp_directory, ignore_errors=True)


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
