import pytest
from source.ex1_5_user_manager import UserManager, DuplicateUser


def test_add_user() -> None:
    um = UserManager()
    assert um.add_user("John Doe", "john.doe@example.com") == True
    assert um.get_user_email("John Doe") == "john.doe@example.com"

def test_add_duplicated_user() -> None:
    um = UserManager()
    assert um.add_user("John Doe", "john.doe@example.com") == True
    with pytest.raises(DuplicateUser, match="User already exist"):
        assert um.add_user("John Doe", "john.doe@example.com") == None