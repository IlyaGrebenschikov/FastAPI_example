import pytest
from pwdlib import PasswordHash

from fastapi_example.infrastructure.security.argon_hasher import Argon2Hasher


class TestArgon2Hasher:
    @pytest.fixture
    def password_hash(self) -> PasswordHash:
        return PasswordHash.recommended()

    @pytest.fixture
    def hasher(self, password_hash: PasswordHash) -> Argon2Hasher:
        return Argon2Hasher(password_hash)

    def test_hash_password(self, hasher: Argon2Hasher):
        password = "TestPassword123!"
        hashed = hasher.hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password

    def test_hash_password_different_hashes(self, hasher: Argon2Hasher):
        password = "TestPassword123!"
        hash1 = hasher.hash_password(password)
        hash2 = hasher.hash_password(password)

        assert hash1 != hash2

    def test_verify_password_success(self, hasher: Argon2Hasher):
        password = "TestPassword123!"
        hashed = hasher.hash_password(password)

        assert hasher.verify_password(password, hashed) is True

    def test_verify_password_failure(self, hasher: Argon2Hasher):
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = hasher.hash_password(password)

        assert hasher.verify_password(wrong_password, hashed) is False

    def test_verify_password_case_sensitive(self, hasher: Argon2Hasher):
        password = "TestPassword123!"
        hashed = hasher.hash_password(password)
        wrong_case = "testpassword123!"

        assert hasher.verify_password(wrong_case, hashed) is False

    def test_verify_password_empty_password(self, hasher: Argon2Hasher):
        password = "TestPassword123!"
        hashed = hasher.hash_password(password)

        assert hasher.verify_password("", hashed) is False

    def test_hash_empty_password(self, hasher: Argon2Hasher):
        hashed = hasher.hash_password("")

        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_long_password(self, hasher: Argon2Hasher):
        long_password = "x" * 1000
        hashed = hasher.hash_password(long_password)

        assert hasher.verify_password(long_password, hashed) is True

    def test_hash_special_characters(self, hasher: Argon2Hasher):
        password = "P@ssw0rd!@#$%^&*()"
        hashed = hasher.hash_password(password)

        assert hasher.verify_password(password, hashed) is True
