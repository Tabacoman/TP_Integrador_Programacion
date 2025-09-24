# Errors.py

class AppError(Exception):
    """Clase base para todos los errores personalizados de la aplicación."""
    pass

# --- Errores no esperados ---
class UnexpectedAppError(AppError):
    """Se lanza cuando ocurre un error inesperado en la aplicación."""
    def __init__(self, original_exception):
        super().__init__(f"Error no esperado: {original_exception}")
        self.original_exception = original_exception


# --- Errores de Usuarios ---
class UserAlreadyExistsError(AppError):
    """Se lanza cuando se intenta registrar un usuario que ya existe."""
    def __init__(self, username):
        super().__init__(f"El usuario '{username}' ya existe.")


class InvalidPasswordError(AppError):
    """Se lanza cuando la contraseña no cumple los requisitos."""
    def __init__(self):
        super().__init__("La contraseña debe tener al menos 6 caracteres.")


class InvalidLoginError(AppError):
    """Se lanza cuando el usuario o contraseña no son válidos."""
    def __init__(self):
        super().__init__("Usuario o contraseña incorrectos.")


# --- Errores de Libros ---
class BookAlreadyExistsError(AppError):
    """Se lanza cuando se intenta insertar un libro duplicado."""
    def __init__(self, titulo):
        super().__init__(f"El libro '{titulo}' ya existe en la base de datos.")

class BookNotFoundError(AppError):
    """Se lanza cuando no se encuentra un libro en la base de datos."""
    def __init__(self, id_libro):
        super().__init__(f"No se encontró el libro con ID {id_libro}.")

class InvalidInsertError(AppError):
    """se lanza cuando se ingresan campos incorrectos"""
    def __init__(self):
        super().__init__(f"Los datos ingresados son incorrectos")

class VoidInsertError(AppError):
    """se lanza cuando no se ingresa algun dato"""
    def __init__(self):
        super().__init__(f"Falta ingresar 1 o más datos")
# --- Errores de Favoritos ---
class AlreadyInFavoritesError(AppError):
    """Se lanza cuando un libro ya está en favoritos del usuario."""
    def __init__(self, titulo):
        super().__init__(f"El libro '{titulo}' ya está en favoritos.")


class FavoriteNotFoundError(AppError):
    """Se lanza cuando se intenta eliminar un favorito inexistente."""
    def __init__(self, titulo):
        super().__init__(f"El libro '{titulo}' no está en favoritos.")
