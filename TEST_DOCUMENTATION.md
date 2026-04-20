# Unit Tests Documentation

Comprehensive unit tests for the FastAPI Example application covering domain entities, services, handlers, and infrastructure components.

## Table of Contents

- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Test Categories](#test-categories)
- [Fixtures](#fixtures)
- [Best Practices](#best-practices)

## Test Structure

```
test/
└── unit/
    ├── conftest.py                                              # Global fixtures and configuration
    ├── domain/
    │   └── test_user_entity.py                                 # Domain entity tests (5 tests)
    ├── application/
    │   ├── services/
    │   │   ├── test_token_jwt_service.py                       # JWT token service tests (9 tests)
    │   │   └── test_rate_limiter_service.py                    # Rate limiter service tests (5 tests)
    │   └── features/
    │       ├── auth/
    │       │   └── test_create_access_token_handler.py         # Auth handler tests (6 tests)
    │       └── users/
    │           ├── test_create_user_handler.py                 # User creation handler tests (5 tests)
    │           ├── test_get_user_handler.py                    # User retrieval handler tests (5 tests)
    │           ├── test_update_user_handler.py                 # User update handler tests (7 tests)
    │           └── test_delete_user_handler.py                 # User deletion handler tests (6 tests)
    └── infrastructure/
        └── test_argon_hasher.py                                # Password hasher tests (9 tests)
```

**Total: 55 tests across 9 test files**

## Running Tests

### Quick Start

Install dependencies with test extras and run all tests:

```bash
uv sync --all-extras
uv run pytest test/unit -v
```

### Run Specific Test Categories

```bash
# Domain tests
uv run pytest test/unit/domain -v

# Application layer tests
uv run pytest test/unit/application -v

# Service tests only
uv run pytest test/unit/application/services -v

# Feature handler tests
uv run pytest test/unit/application/features -v

# User handlers
uv run pytest test/unit/application/features/users -v

# Auth handlers
uv run pytest test/unit/application/features/auth -v

# Infrastructure tests
uv run pytest test/unit/infrastructure -v
```

### Run Specific Test File

```bash
uv run pytest test/unit/application/features/users/test_create_user_handler.py -v
```

### Run Specific Test

```bash
uv run pytest test/unit/application/features/users/test_create_user_handler.py::TestCreateUserHandler::test_create_user_success -v
```

### Generate Coverage Report

```bash
uv run pytest test/unit --cov=src/fastapi_example --cov-report=html
```

The HTML report will be generated in the `htmlcov/` directory.

### Other Useful Options

```bash
# Stop on first failure
uv run pytest test/unit -x

# Show local variables in tracebacks
uv run pytest test/unit -l

# Run with minimal output
uv run pytest test/unit -q

# Show slowest tests
uv run pytest test/unit --durations=10
```

## Test Coverage

**Current Status:** 55 tests, all passing ✅

**Coverage:** 42% (983 statements analyzed, 572 not covered)

Core modules with high coverage:
- `src/fastapi_example/domain/entities/` - 100%
- `src/fastapi_example/application/services/` - 100%
- `src/fastapi_example/infrastructure/security/` - 100%
- `src/fastapi_example/infrastructure/cache/` - Covered by service tests
- `src/fastapi_example/application/features/` - 40-100%

## Test Categories

### Domain Tests (5 tests)

File: `test/unit/domain/test_user_entity.py`

Tests for the `User` domain entity:

- **test_create_user_with_all_fields** - Verify user creation with all fields
- **test_create_user_with_none_timestamps** - Verify user creation with null timestamps
- **test_user_dataclass_equality** - Verify dataclass equality comparison
- **test_user_different_users_not_equal** - Verify different users are not equal
- **test_user_with_special_characters** - Verify support for special characters in username and email

#### Create Access Token Handler (6 tests)

File: `test/unit/application/features/auth/test_create_access_token_handler.py`

Tests for authentication token creation:

- **test_create_access_token_success** - Verify successful token generation
- **test_create_access_token_user_not_found** - Verify error when user not found
- **test_create_access_token_wrong_password** - Verify error on invalid password
- **test_create_access_token_with_scopes** - Verify token creation with scopes
- **test_create_access_token_verifies_password** - Verify password verification is called
- **test_create_access_token_empty_username** - Verify error on empty username

### Service Tests (14 tests)

#### JWT Token Service (9 tests)

File: `test/unit/application/services/test_token_jwt_service.py`

Tests for JWT token creation and verification:

- **test_create_access_token_success** - Verify successful token creation
- **test_create_access_token_with_scopes** - Verify token creation with scopes
- **test_verify_token_success** - Verify successful token verification
- **test_verify_token_invalid** - Verify rejection of invalid tokens
- **test_verify_token_expired** - Verify rejection of expired tokens
- **test_verify_token_missing_subject** - Verify rejection of tokens without subject
- **test_get_user_id_from_token_success** - Verify extraction of user ID from token
- **test_get_user_id_from_token_invalid** - Verify error handling for invalid tokens
- **test_get_user_id_from_token_invalid_uuid_format** - Verify error on invalid UUID format

#### Rate Limiter Service (5 tests)

File: `test/unit/application/services/test_rate_limiter_service.py`

Tests for request rate limiting:

- **test_check_within_limit** - Verify requests within limit are allowed
- **test_check_at_limit** - Verify requests at limit boundary are allowed
- **test_check_exceeds_limit** - Verify requests exceeding limit are rejected
- **test_check_zero_requests** - Verify first request is allowed
- **test_check_creates_correct_key** - Verify cache key is formatted correctly

### Handler Tests (23 tests)

#### Create User Handler (5 tests)

File: `test/unit/application/features/users/test_create_user_handler.py`

Tests for user creation command handler:

- **test_create_user_success** - Verify successful user creation
- **test_create_user_already_exists** - Verify error when user already exists
- **test_create_user_hashes_password** - Verify password is hashed before storage
- **test_create_user_checks_username_and_email** - Verify both username and email are checked
- **test_create_user_with_special_characters** - Verify support for special characters

#### Get User Handler (5 tests)

File: `test/unit/application/features/users/test_get_user_handler.py`

Tests for user retrieval query handler:

- **test_get_user_success** - Verify successful user retrieval by ID
- **test_get_user_not_found** - Verify error when user not found
- **test_get_user_with_timestamps** - Verify timestamps are returned correctly
- **test_get_user_with_special_characters** - Verify special characters in username/email
- **test_get_user_calls_transaction_manager** - Verify transaction context is used

#### Update User Handler (7 tests)

File: `test/unit/application/features/users/test_update_user_handler.py`

Tests for user update command handler:

- **test_update_user_success** - Verify successful user update
- **test_update_user_not_found** - Verify error when user not found
- **test_update_user_username_already_exists** - Verify conflict on duplicate username
- **test_update_user_email_already_exists** - Verify conflict on duplicate email
- **test_update_user_partial** - Verify partial updates (only some fields)
- **test_update_user_same_username** - Verify updating with same username doesn't check exists
- **test_update_user_uses_for_update** - Verify row is locked for update during transaction

#### Delete User Handler (6 tests)

File: `test/unit/application/features/users/test_delete_user_handler.py`

Tests for user deletion command handler:

- **test_delete_user_success** - Verify successful user deletion
- **test_delete_user_not_found** - Verify error when user not found
- **test_delete_user_wrong_password** - Verify error on wrong password confirmation
- **test_delete_user_verifies_password** - Verify password verification is called
- **test_delete_user_empty_password** - Verify error on empty password
- **test_delete_user_requires_for_update** - Verify row is locked during deletion

### Infrastructure Tests (9 tests)

File: `test/unit/infrastructure/test_argon_hasher.py`

Tests for Argon2 password hashing:

- **test_hash_password** - Verify password hashing creates a hash
- **test_hash_password_different_hashes** - Verify same password produces different hashes (salt)
- **test_verify_password_success** - Verify successful password verification
- **test_verify_password_failure** - Verify rejection of wrong password
- **test_verify_password_case_sensitive** - Verify password verification is case-sensitive
- **test_verify_password_empty_password** - Verify empty password fails verification
- **test_hash_empty_password** - Verify empty password can be hashed
- **test_hash_long_password** - Verify long passwords are handled correctly
- **test_hash_special_characters** - Verify special characters in passwords are handled

## Fixtures

Global fixtures defined in `test/unit/conftest.py`:

### `jwt_settings`
Provides JWT settings with test RSA keys for token generation/verification.

```python
@pytest.fixture
def jwt_settings() -> JWTSettings:
    return JWTSettings(
        algorithm="RS256",
        expiration=30,
    )
```

### `mock_transaction_manager`
Provides an async context manager mock for database transactions.

```python
@pytest.fixture
def mock_transaction_manager():
    mock = MagicMock()
    mock.__aenter__ = AsyncMock(return_value=mock)
    mock.__aexit__ = AsyncMock(return_value=None)
    return mock
```

### `mock_users_repository`
Provides an async mock for the users repository.

```python
@pytest.fixture
def mock_users_repository():
    return AsyncMock()
```

### `mock_cache_repository`
Provides an async mock for the cache repository.

```python
@pytest.fixture
def mock_cache_repository():
    return AsyncMock()
```

### `mock_hasher`
Provides a mock for password hasher with default implementations.

```python
@pytest.fixture
def mock_hasher():
    mock = MagicMock()
    mock.hash_password = MagicMock(return_value="hashed_password")
    mock.verify_password = MagicMock(return_value=True)
    return mock
```

## Best Practices

### Test Naming
- Use descriptive names that explain what is being tested
- Follow the pattern: `test_<function>_<scenario>`
- Example: `test_create_access_token_wrong_password`

### Arrange-Act-Assert Pattern
Tests follow the AAA pattern:

```python
# Arrange - Set up test data and mocks
user_id = uuid4()
cmd = CreateUserCommand(...)

# Act - Execute the code being tested
result = await handler.execute(cmd)

# Assert - Verify the results
assert result.username == cmd.username
```

### Mocking Strategy
- Mock external dependencies (repositories, services)
- Use real implementations for domain logic when possible
- Mock async functions with `AsyncMock`
- Mock regular functions with `MagicMock`

### Test Isolation
- Each test is independent and can run in any order
- No shared state between tests
- Use fixtures for common setup
- Clean data in teardown if needed

### Async Testing
- Mark async tests with `@pytest.mark.asyncio`
- Use `async def` for async test functions
- Use `await` for async operations

### Assertions
- One logical assertion per test when possible
- Use context managers for exception testing: `with pytest.raises(ExceptionType)`
- Check both positive and negative cases

### Error Messages
- Assertions include clear error messages
- Use `match` parameter in `pytest.raises` for specific error messages
- Example: `pytest.raises(UnAuthorizedError, match="Incorrect login")`

## Pytest Configuration

Configuration in `pytest.ini`:

- **testpaths:** `test/unit` - Where to find tests
- **python_files:** `test_*.py` - Test file naming pattern
- **python_classes:** `Test*` - Test class naming pattern
- **python_functions:** `test_*` - Test function naming pattern
- **asyncio_mode:** `auto` - Automatic asyncio mode for async tests
- **Coverage options:** Generate HTML reports and show missing lines
- **Markers:** Define async, unit, and integration test markers

## Dependencies

Test dependencies are installed via `uv sync --all-extras`:

- **pytest** (8.4.2) - Testing framework
- **pytest-asyncio** (0.24.0) - Async test support
- **pytest-cov** (5.0.0) - Code coverage analysis
- **unittest.mock** (built-in) - Mocking framework

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

```bash
# Install dependencies
uv sync --all-extras

# Run tests with coverage
uv run pytest test/unit --cov=src/fastapi_example --cov-report=term-missing
```

## Troubleshooting

### Tests Not Found
Ensure pytest can find the tests:
```bash
uv run pytest test/unit --collect-only
```

### Import Errors
Verify the package is installed:
```bash
uv run pytest -v --tb=short
```

### Async Tests Not Running
Ensure `@pytest.mark.asyncio` is on async test functions and `asyncio_mode=auto` in pytest.ini.

### Mock Not Working
Verify mock is assigned before the test execution, not after.