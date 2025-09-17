import pytest
import tempfile
import os
from db.database import Database   # ✅ db existe
from models.User import User
from models.Libro import Libro
from Utilities.funtions import (
    insert_usuario,
    log_in,
    insert_libro,
    update_libro,
    delete_libro,
    get_libros,
    agregar_favorito,
    eliminar_favorito,
    get_favoritos,
)
from models.Errors import (   # ✅ Errors está en models
    UserAlreadyExistsError,
    InvalidPasswordError,
    InvalidLoginError,
    BookAlreadyExistsError,
    BookNotFoundError,
    AlreadyInFavoritesError,
    FavoriteNotFoundError,
)

@pytest.fixture
def db():
    # Crea un archivo temporal para la base de datos de pruebas
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    database = Database(db_name=path)
    database.create_tables()
    yield database
    os.remove(path)

def test_insert_usuario_and_login(db):
    user = User("usuario1", "clave123", "user")
    assert insert_usuario(db, user) is True

    # Usuario duplicado
    with pytest.raises(UserAlreadyExistsError):
        insert_usuario(db, user)

    # Contraseña inválida
    with pytest.raises(InvalidPasswordError):
        insert_usuario(db, User("otro", "123", "user"))

    # Login correcto
    u = log_in(db, User("usuario1", "clave123", ""))
    assert isinstance(u, User)
    assert u.username == "usuario1"

    # Login inválido
    with pytest.raises(InvalidLoginError):
        log_in(db, User("usuario1", "wrong", ""))

def test_insert_and_update_libro(db):
    libro = Libro("1984", "George Orwell", 1949, "Ciencia ficción")
    assert insert_libro(db, libro) is True

    # Libro duplicado
    with pytest.raises(BookAlreadyExistsError):
        insert_libro(db, libro)

    # Update exitoso
    libro_db = get_libros(db)[0]
    libro_db.titulo = "1984 (editado)"
    assert update_libro(db, libro_db) is True

def test_delete_libro(db):
    libro = Libro("Cien años de soledad", "Gabriel García Márquez", 1967, "Realismo mágico")
    insert_libro(db, libro)
    libro_db = get_libros(db)[0]

    # Eliminación correcta
    assert delete_libro(db, libro_db) is True

    # Eliminar libro inexistente
    libro_inexistente = Libro("X", "Y", 2000, "Z", id=999)
    with pytest.raises(BookNotFoundError):
        delete_libro(db, libro_inexistente)

def test_favoritos(db):
    user = User("userfav", "clave123", "user")
    insert_usuario(db, user)
    user_db = log_in(db, User("userfav", "clave123", ""))

    libro = Libro("El principito", "Antoine de Saint-Exupéry", 1943, "Fábula")
    insert_libro(db, libro)
    libro_db = get_libros(db)[0]

    # Agregar favorito
    assert agregar_favorito(db, user_db, libro_db) is True

    # Duplicado en favoritos
    with pytest.raises(AlreadyInFavoritesError):
        agregar_favorito(db, user_db, libro_db)

    # Obtener favoritos
    favoritos = get_favoritos(db, user_db)
    assert len(favoritos) == 1
    assert favoritos[0].titulo == "El principito"

    # Eliminar favorito
    assert eliminar_favorito(db, user_db, libro_db) is True

    # Eliminar inexistente
    with pytest.raises(FavoriteNotFoundError):
        eliminar_favorito(db, user_db, libro_db)

def test_create_tables_crea_todas_las_tablas(db):
    with db.get_connection() as conn:
        tablas = [row["name"] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )]
    assert "usuarios" in tablas
    assert "libros" in tablas
    assert "favoritos" in tablas
