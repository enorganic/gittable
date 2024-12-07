import argparse
import json
import os
import sys
from pathlib import Path
from shutil import which
from subprocess import check_call, check_output
from typing import Iterable, Optional, Union

from git_some._utilities import get_exception_text

_CURRENT_WORKING_DIRECTORY: Path = Path.cwd().resolve()


def _get_hatch_version(
    directory: Union[str, Path] = _CURRENT_WORKING_DIRECTORY,
) -> str:
    """
    Get the version of the package using `hatch`, if available
    """
    if isinstance(directory, Path):
        directory = str(Path(directory).resolve())
    current_directory: str = str(Path.cwd().resolve())
    os.chdir(directory)
    hatch: Optional[str] = which("hatch")
    try:
        return (
            check_output((hatch, "version"), text=True).strip()
            if hatch
            else ""
        )
    except Exception:
        return ""
    finally:
        os.chdir(current_directory)


def _get_poetry_version(
    directory: Union[str, Path] = _CURRENT_WORKING_DIRECTORY,
) -> str:
    """
    Get the version of the package using `poetry`, if available
    """
    if isinstance(directory, Path):
        directory = str(Path(directory).resolve())
    current_directory: str = str(Path.cwd().resolve())
    os.chdir(directory)
    poetry: Optional[str] = which("poetry")
    try:
        return (
            check_output((poetry, "version"), text=True).strip()
            if poetry
            else ""
        )
    except Exception:
        return ""
    finally:
        os.chdir(current_directory)


def _get_pip_version(
    directory: Union[str, Path] = _CURRENT_WORKING_DIRECTORY,
) -> str:
    """
    Get the version of a package using `pip`
    """
    if isinstance(directory, Path):
        directory = str(Path(directory).resolve())
    try:
        check_call(
            (
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-deps",
                "--no-compile",
                "-e",
                directory,
            ),
            text=True,
        )
        return json.loads(
            check_output(
                (
                    sys.executable,
                    "-m",
                    "pip",
                    "list",
                    "--format",
                    "json",
                    "--path",
                    directory,
                ),
                text=True,
            )
        )[0]["version"]
    except Exception as error:
        raise RuntimeError(
            "Unable to determine the project version "
            f"for: {directory}\n"
            f"{get_exception_text()}"
        ) from error


def _get_python_project_version(
    directory: Union[str, Path] = _CURRENT_WORKING_DIRECTORY,
) -> str:
    """
    Get a python project's version. Currently supports `hatch`, `poetry`, and
    any build tool compatible with `pip`.
    """
    return (
        _get_hatch_version(directory)
        or _get_poetry_version(directory)
        or _get_pip_version(directory)
    )


def tag_version(
    directory: Union[str, Path] = _CURRENT_WORKING_DIRECTORY, message: str = ""
) -> str:
    """
    Tag your project with the package version number *if* no pre-existing
    tag with that version number exists.

    Parameters:
        directory:
        message:

    Returns:
        The version number
    """
    if isinstance(directory, Path):
        directory = str(Path(directory).resolve())
    version: str = _get_python_project_version(directory)
    current_directory: str = str(_CURRENT_WORKING_DIRECTORY.resolve())
    os.chdir(directory)
    try:
        tags: Iterable[str] = map(
            str.strip,
            check_output(
                ("git", "tag"), encoding="utf-8", universal_newlines=True
            )
            .strip()
            .split("\n"),
        )
        if version not in tags:
            check_call(("git", "tag", "-a", version, "-m", message or version))
    finally:
        os.chdir(current_directory)
    return version


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="git-some tag-version",
        description=(
            "Tag your repo with the package version, if a tag "
            "for that version doesn't already exist."
        ),
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=_CURRENT_WORKING_DIRECTORY,
        type=str,
        help=(
            "Your project directory. If not provided, the current "
            "directory will be used."
        ),
    )
    parser.add_argument(
        "-m",
        "--message",
        default="",
        type=str,
        help=(
            "The tag message. If not provided, the new version number is "
            "used."
        ),
    )
    arguments: argparse.Namespace = parser.parse_args()
    tag_version(directory=arguments.directory, message=arguments.message)


if __name__ == "__main__":
    main()
