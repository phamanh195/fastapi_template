from app.core.security import generate_hashed_password, verify_password
from app.tests.factories.utils import faker


def test_generate_hashed_password_success():
    """
    Test generate_hashed_password successfully.
    """
    password = faker.password()
    hashed_password = generate_hashed_password(password=password)
    assert hashed_password
    assert isinstance(hashed_password, str)


def test_verify_password_with_valid_password():
    """
    Test verify_password with valid password.
    """
    password = faker.password()
    hashed_password = generate_hashed_password(password=password)
    assert hashed_password

    is_valid = verify_password(password=password, hashed_password=hashed_password)
    assert is_valid


def test_verify_password_with_invalid_password():
    """
    Test verify_password with invalid password.
    """
    password = faker.password()
    hashed_password = generate_hashed_password(password=password)
    assert hashed_password

    invalid_password = faker.password()
    is_valid = verify_password(
        password=invalid_password, hashed_password=hashed_password
    )
    assert not is_valid
