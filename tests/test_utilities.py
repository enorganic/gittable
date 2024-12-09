import pytest

from gittable._utilities import update_url_user_password


def test_update_url_user_password() -> None:
    """
    Ensure that updating a setup.cfg file occurs without problems
    """
    assert (
        update_url_user_password(
            "https://host.com/path/file.ext?x=y#nowhere", "beetle", "juice"
        )
        == "https://beetle:juice@host.com/path/file.ext?x=y#nowhere"
    )


if __name__ == "__main__":
    pytest.main(["-vv", __file__])
