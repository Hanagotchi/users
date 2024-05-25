import unittest
from datetime import date, datetime


import pytest
from unittest.mock import Mock, MagicMock

from repository.Users import UsersRepository
from service.Users import UsersService
from schemas.Schemas import (
    CreateNotificationSchema,
    CreateUserSchema,
    UserSchema
)

from exceptions.UserException import (
    ForbiddenUser,
    InvalidData,
    ResourceNotFound,
    InvalidURL
)


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

alice = UserSchema(
    id=2,
    name="Alice",
    email="alice@mail.com",
    gender="female",
    photo="link.com",
    birthdate=date(1990, 5, 10),
    location={},
    nickname="alice",
    biography="una tipa",
    device_token="d3vic2to0k3n"
)

new_user = CreateUserSchema(
    name="Alice",
    email="alice@mail.com",
    location={"lat": 20, "long": 100}
)


class ServiceTests(unittest.TestCase):
    def test_get_user(self):
        attr_db = {"get_user.return_value": john}
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        user = service.get_user(1)

        self.assertEqual(user, john)
        mock_db.get_user.assert_called_once_with(1)

    def test_raise_user_not_found(self):
        attr_db = {"get_user.return_value": None}
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(ResourceNotFound):
            service.get_user(10)

    def test_get_all_users(self):
        attr_db = {"get_all_users.return_value": [john, alice]}
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        users = service.get_all_users()

        self.assertEqual(len(users), 2)
        mock_db.get_all_users.assert_called_once()

    def test_get_users_by_id(self):
        attr_db = {"get_users_by_ids.return_value": [john, alice]}
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        users = service.get_users_by_ids([1, 2])

        self.assertTrue(users.__contains__(john))
        self.assertTrue(users.__contains__(alice))
        mock_db.get_users_by_ids.assert_called_once_with([1, 2])

    def test_create_user(self):
        attr_db = {
            "add.return_value": None,
            "create_user.return_value": {"id": 3, "name": "Alice",
                                         "email": "alice@mail.com"},
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        user = service.create_user(new_user.dict())

        self.assertEqual(user["name"], "Alice")
        mock_db.create_user.assert_called_once()
        mock_db.rollback.assert_not_called()

    def test_create_user_rollback_if_failed(self):
        attr_db = {
            "create_user.side_effect": Exception(),
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(Exception):
            service.create_user(new_user.dict())

        mock_db.rollback.assert_called_once()

    def test_create_fails_if_invalid_location(self):
        attr_db = {"rollback.return_value": None}
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        invalid_user = CreateUserSchema(name="Alice", email="alice@mail.com",
                                        location={"lat": 20})

        with self.assertRaises(InvalidData):
            service.create_user(invalid_user.dict())
            mock_db.add.assert_not_called()

    def test_update_user(self):
        attr_db = {
            "add.return_value": None,
            "edit_user.return_value": None,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        service.update_user(1, {"nickname": "alice"})

        mock_db.edit_user.assert_called_once()
        mock_db.rollback.assert_not_called()

    def test_update_user_rollback_if_failed(self):
        attr_db = {
            "edit_user.side_effect": Exception(),
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(Exception):
            service.update_user(1, {"nickname": "alice"})

        mock_db.rollback.assert_called_once()

    def test_update_fails_if_invalid_location(self):
        attr_db = {"edit_user.return_value": None}
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        invalid_update = {"photo": "invalidlink"}

        with self.assertRaises(InvalidURL):
            service.update_user(1, invalid_update)

    def test_create_notification(self):
        attr_db = {
            "create_notification.return_value": None,
            "get_notifications.return_value": [
                {
                    "datetime": datetime(2023, 5, 17, 10, 30),
                    "content": 'Alarm'
                }
            ],
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        service.create_notification(
            1,
            CreateNotificationSchema(date_time=datetime(2023, 5, 17, 10, 30),
                                     content="Alarm")
        )

        notifications = service.get_notifications(1)
        notification = notifications.pop()

        self.assertEqual(notification["content"], "Alarm")
        mock_db.create_notification.assert_called_once()
        mock_db.rollback.assert_not_called()

    def test_delete_notification(self):
        attr_db = {
            "delete_notification.return_value": None,
            "get_notification_owner.return_value": 1,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        service.delete_notification(1, 1)

        mock_db.delete_notification.assert_called_once()
        mock_db.rollback.assert_not_called()

    def test_delete_notification_fails_if_not_authorized(self):
        attr_db = {
            "delete_notification.return_value": None,
            "get_notification_owner.return_value": 2,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(ForbiddenUser):
            service.delete_notification(1, 1)

    def test_delete_fails_if_notification_doesnt_exist(self):
        attr_db = {
            "delete_notification.return_value": None,
            "get_notification_owner.return_value": None,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(ResourceNotFound):
            service.delete_notification(1, 1)

    def test_update_notification(self):
        attr_db = {
            "edit_notification.return_value": None,
            "get_notification_owner.return_value": 1,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)
        service.update_notification(
            1,
            1,
            CreateNotificationSchema(
                date_time=datetime(2023, 6, 17, 10, 30),
                content="Alarm"
            )
        )

        mock_db.edit_notification.assert_called_once()
        mock_db.rollback.assert_not_called()

    def test_create_notification_rollback_if_failed(self):
        attr_db = {
            "create_notification.side_effect": Exception(),
            "get_notification_owner.return_value": 1,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(Exception):
            service.create_notification(
                1,
                CreateNotificationSchema(
                    date_time=datetime(2023, 5, 17, 10, 30),
                    content="Alarm")
            )

        mock_db.rollback.assert_called_once()

    def test_delete_notification_rollback_if_failed(self):
        attr_db = {
            "delete_notification.side_effect": Exception(),
            "get_notification_owner.return_value": 1,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(Exception):
            service.delete_notification(1, 1)

        mock_db.rollback.assert_called_once()

    def test_update_notification_rollback_if_failed(self):
        attr_db = {
            "edit_notification.side_effect": Exception(),
            "get_notification_owner.return_value": 1,
            "rollback.return_value": None
        }
        mock_db = get_mock(UsersRepository, attr_db)
        service = UsersService(mock_db)

        with self.assertRaises(Exception):
            service.update_notification(1, 1, {})

        mock_db.rollback.assert_called_once()
