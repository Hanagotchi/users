import pytest
from unittest.mock import Mock, MagicMock

from app.repository.Users import UsersRepository
from app.service.Users import UsersService

@pytest.fixture
def mock_user_repository():
    return Mock()

@pytest.fixture
def users_service(mock_user_repository):
    return UsersService(mock_user_repository)


def getMock(classToMock, attributes=None):
    if attributes is None:
        attributes = {}
    mock = MagicMock(spec=classToMock)
    mock.configure_mock(**attributes)
    return mock


def test_get_user(mock_user_repository):
    attr_db = {
        "get_user.return_value":  {"id": 1, "name": "John"}}
    mock_db = getMock(UsersRepository, attr_db)
    service = UsersService(mock_db)
    user = service.get_user(1)

    assert user == {"id": 1, "name": "John"}
    mock_db.get_user.assert_called_once_with(1)
