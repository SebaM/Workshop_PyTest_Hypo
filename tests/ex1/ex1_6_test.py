import pytest
from source.ex1_6_database import Database, DuplicateUser

db = Database()

@pytest.fixture
def db_client():
    """Create a fresh instance of User Manager before each test"""
    # db = Database()
    yield db #  Provide the ficture instance
    db.clean() #  Clean up step, not needed for in-mem dbs needed for real


@pytest.mark.user
def test_add_user(db_client) -> None:
    assert db_client.add_user("John Doe", "john.doe@example.com") == True
    assert db_client.get_user_email("John Doe") == "john.doe@example.com"

@pytest.mark.user
@pytest.mark.negative
def test_add_duplicated_user(db_client) -> None:
    assert db_client.add_user("John Doe", "john.doe@example.com") == True
    with pytest.raises(DuplicateUser):
        assert db_client.add_user("John Doe", "john.doe@example.com") == True

@pytest.mark.user
@pytest.mark.negative
def test_delete_user(db_client) -> None:
    # Given
    db_client.add_user("John Doe", "john.doe@example.com")
    assert db_client.delete_user("John Doe") is True
    #Then
    assert db_client.delete_user("John Doe") is None