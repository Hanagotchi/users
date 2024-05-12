from datetime import date

import pytest
from unittest.mock import Mock, MagicMock

from app.repository.Users import UsersRepository
from app.schemas.Schemas import UserSchema
from app.service.Users import UsersService


@pytest.fixture
def mock_user_repository():
    return Mock()


@pytest.fixture
def users_service(mock_user_repository):
    return UsersService(mock_user_repository)


def get_mock(classToMock, attributes=None):
    if attributes is None:
        attributes = {}
    mock = MagicMock(spec=classToMock)
    mock.configure_mock(**attributes)
    return mock


john = UserSchema(
    id=1,
    name="John",
    email="john@mail.com",
    gender="male",
    photo="link.com",
    birthdate=date(1990, 5, 12),
    location={},
    nickname="john",
    biography="un tipo",
    device_token="d3vic2to0k3n"
)


def test_get_user(mock_user_repository):
    attr_db = {
        "get_user.return_value": john}
    mock_db = get_mock(UsersRepository, attr_db)
    service = UsersService(mock_db)
    user = service.get_user(1)

    assert user == john
    mock_db.get_user.assert_called_once_with(1)
