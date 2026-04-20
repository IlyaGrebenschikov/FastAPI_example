from datetime import datetime, timezone
from uuid import uuid4

import pytest

from fastapi_example.domain.entities import User


class TestUserEntity:
    def test_create_user_with_all_fields(self):
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=now,
            updated_at=now,
        )

        assert user.id == user_id
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "hashed_password"
        assert user.created_at == now
        assert user.updated_at == now

    def test_create_user_with_none_timestamps(self):
        user_id = uuid4()

        user = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=None,
            updated_at=None,
        )

        assert user.id == user_id
        assert user.created_at is None
        assert user.updated_at is None

    def test_user_dataclass_equality(self):
        user_id = uuid4()
        now = datetime.now(timezone.utc)

        user1 = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=now,
            updated_at=now,
        )

        user2 = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            created_at=now,
            updated_at=now,
        )

        assert user1 == user2

    def test_user_different_users_not_equal(self):
        user1 = User(
            id=uuid4(),
            username="user1",
            email="user1@example.com",
            password="hash1",
            created_at=None,
            updated_at=None,
        )

        user2 = User(
            id=uuid4(),
            username="user2",
            email="user2@example.com",
            password="hash2",
            created_at=None,
            updated_at=None,
        )

        assert user1 != user2

    def test_user_with_special_characters(self):
        user = User(
            id=uuid4(),
            username="user.name-123",
            email="user+tag@example.com",
            password="$2b$12$KIX....",
            created_at=None,
            updated_at=None,
        )

        assert user.username == "user.name-123"
        assert user.email == "user+tag@example.com"
