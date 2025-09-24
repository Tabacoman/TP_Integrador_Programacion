import pytest
from models.Errors import (   # ✅ models.Errors
    AppError,
    UserAlreadyExistsError,
    InvalidPasswordError,
    InvalidLoginError,
    BookAlreadyExistsError,
    BookNotFoundError,
    AlreadyInFavoritesError,
    FavoriteNotFoundError,
    UnexpectedAppError,
)


def test_user_already_exists_error():
    with pytest.raises(UserAlreadyExistsError) as exc:
        raise UserAlreadyExistsError("usuario1")
    assert "usuario1" in str(exc.value)

def test_invalid_password_error():
    with pytest.raises(InvalidPasswordError):
        raise InvalidPasswordError()

def test_invalid_login_error():
    with pytest.raises(InvalidLoginError):
        raise InvalidLoginError()

def test_book_already_exists_error():
    with pytest.raises(BookAlreadyExistsError) as exc:
        raise BookAlreadyExistsError("Cien años de soledad")
    assert "Cien años de soledad" in str(exc.value)

def test_book_not_found_error():
    with pytest.raises(BookNotFoundError):
        raise BookNotFoundError(999)

def test_already_in_favorites_error():
    with pytest.raises(AlreadyInFavoritesError):
        raise AlreadyInFavoritesError("1984")

def test_favorite_not_found_error():
    with pytest.raises(FavoriteNotFoundError):
        raise FavoriteNotFoundError("El principito")

def test_unexpected_app_error():
    try:
        1 / 0
    except Exception as e:
        with pytest.raises(UnexpectedAppError) as exc:
            raise UnexpectedAppError(e)
        assert "division by zero" in str(exc.value)
        assert isinstance(exc.value.original_exception, Exception)
