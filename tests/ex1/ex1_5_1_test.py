import pytest
from source.ex1_5_user_manager import UserManager, DuplicateUser

@pytest.fixture
def user_manager():
    """Create a fresh instance of User Manager before each test"""
    return UserManager()
#     # um = UserManager()
#     # um.add_user("John Doe", "john.doe@example.com")
#     # return um

# user_manager = UserManager()
@pytest.mark.user
def test_add_user(user_manager) -> None:
    assert user_manager.add_user("John Doe", "john.doe@example.com") == True
    assert user_manager.get_user_email("John Doe") == "john.doe@example.com"

@pytest.mark.user
@pytest.mark.negative
def test_add_duplicated_user(user_manager) -> None:
    assert user_manager.add_user("John Doe", "john.doe@example.com") == True
    with pytest.raises(DuplicateUser):
        assert user_manager.add_user("John Doe", "john.doe@example.com") == True