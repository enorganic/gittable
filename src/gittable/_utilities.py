from __future__ import annotations

import sys
from subprocess import DEVNULL, PIPE, list2cmdline, run
from traceback import format_exception
from typing import TYPE_CHECKING, Callable
from urllib.parse import ParseResult, urlparse, urlunparse
from urllib.parse import quote as _quote

if TYPE_CHECKING:
    from pathlib import Path


def update_url_user_password(
    url: str,
    user: str,
    password: str = "",
    quote: Callable[[str], str] = _quote,
) -> str:
    """
    Update a URL's user and password and return the result.

    Parameters:

    - url (str)
    - user (str)
    - password (str) = "": (optional)
    - quote = urllib.parse.quote: A function to use for escaping
      invalid character (defaults to `urllib.parse.quote`)
    """
    if not (url and user):
        raise ValueError(url, user)
    parse_result: ParseResult = urlparse(url)
    host: str = parse_result.netloc.rpartition("@")[-1]
    user_password: str = quote(user)
    if password:
        user_password = f"{user_password}:{quote(password)}"
    return urlunparse(
        (
            parse_result.scheme,
            f"{user_password}@{host}",
            parse_result.path,
            parse_result.params,
            parse_result.query,
            parse_result.fragment,
        )
    )


def get_exception_text() -> str:
    """
    When called within an exception, this function returns a text
    representation of the error matching what is found in
    `traceback.print_exception`, but is returned as a string value rather than
    printing.
    """
    return "".join(format_exception(*sys.exc_info()))


def check_output(
    args: tuple[str, ...],
    cwd: str | Path = "",
    *,
    echo: bool = False,
    env: dict[str, str] | None = None,
) -> str:
    """
    This function mimics `subprocess.check_output`, but redirects stderr
    to DEVNULL, and ignores unicode decoding errors.

    Parameters:

    - command (Tuple[str, ...]): The command to run
    """
    if echo:
        if cwd:
            print("$", "cd", cwd, "&&", list2cmdline(args))  # noqa: T201
        else:
            print("$", list2cmdline(args))  # noqa: T201
    output: str = run(
        args,
        stdout=PIPE,
        stderr=DEVNULL,
        check=True,
        cwd=cwd or None,
        env=env,
    ).stdout.decode("utf-8", errors="ignore")
    if echo:
        print(output)  # noqa: T201
    return output
