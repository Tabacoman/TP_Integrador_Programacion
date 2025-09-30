from models.Libro import Libro
from models.User import User
from models.Errors import *

def log_in(db, user: User):
    try: 
        row = db.fetch_one(
            "SELECT * FROM usuarios WHERE username = ? AND password = ?",
            (user.username, user.password)
        )
        
        return User(row["username"], row["password"], row["rol"], row["id"])
    except TypeError as e:
        raise InvalidLoginError()
    except Exception as e:
        raise UnexpectedAppError(e) from e

def get_libros(db):
    try:
        Rows = db.fetch_all("SELECT * FROM libros")
        
        return [Libro(row["titulo"], row["autor"], row["anio"], row["genero"], row["id"]) for row in Rows]

    except Exception as e:
        raise UnexpectedAppError(e) from e
    
def insert_libro(db, libro: Libro):
    try:
        # Validación de campos vacíos
        if not libro.titulo or not libro.autor or not libro.genero or libro.anio is None:
            raise VoidInsertError("No puede haber campos vacíos.")

        # Validación de año inválido
        if not isinstance(libro.anio, int) or libro.anio <= 0:
            raise InvalidInsertError("El año debe ser un número entero positivo.")

        # Verificar si el libro ya existe
        libro_existente = db.fetch_one(
            "SELECT * FROM libros WHERE titulo = ? AND autor = ? AND anio = ? AND genero = ?",
            (libro.titulo, libro.autor, libro.anio, libro.genero)
        )
        if libro_existente:
            raise BookAlreadyExistsError(libro.titulo)

        # Insertar el libro si no existe
        db.execute_query(
            "INSERT INTO libros (titulo, autor, anio, genero) VALUES (?, ?, ?, ?)",
            (libro.titulo, libro.autor, libro.anio, libro.genero)
        )
        return True
    except AppError:
        raise
    except Exception as e:
        raise UnexpectedAppError(e) from e

def update_libro(db, libro: Libro):
    try:
        # Verificar si ya existe otro libro con los mismos datos
        libro_existente = db.fetch_one(
            "SELECT * FROM libros WHERE titulo = ? AND autor = ? AND anio = ? AND genero = ? AND id != ?",
            (libro.titulo, libro.autor, libro.anio, libro.genero, libro.id)
        )
        if libro_existente:
            raise BookAlreadyExistsError(libro.titulo)
        # Actualizar el libro
        db.execute_query(
            "UPDATE libros SET titulo = ?, autor = ?, anio = ?, genero = ? WHERE id = ?",
            (libro.titulo, libro.autor, libro.anio, libro.genero, libro.id)
        )
        return True
    
    except AppError:
        raise
    except Exception as e:
        raise UnexpectedAppError(e) from e

def delete_libro(db, libro: Libro):
    try:
        db.execute_query("DELETE FROM libros WHERE id = ?", (libro.id,))
        raise BookDeletedSuccessfully("Libro borrado correctamente.")
    except BookDeletedSuccessfully:
        raise
    except Exception as e:
        raise AppError(f"error no esperado:{e}") from e
    else:
        return True
    
def buscar_libros(db, libro: Libro):
    query = "SELECT * FROM libros WHERE 1=1"
    params = []
    if isinstance(libro, Libro):
        if libro.titulo:
            query += " AND titulo LIKE ?"
            params.append(f"%{libro.titulo}%")
        if libro.autor:
            query += " AND autor LIKE ?"
            params.append(f"%{libro.autor}%")
        if libro.anio:
            query += " AND anio = ?"
            params.append(libro.anio)
        if libro.genero:
            query += " AND genero LIKE ?"
            params.append(f"%{libro.genero}%")
    try:
        Rows = db.fetch_all(query, tuple(params))
        
        return [Libro(row["titulo"], row["autor"], row["anio"], row["genero"], row["id"]) for row in Rows]
 
    except Exception as e:
        raise UnexpectedAppError(e) from e

def agregar_favorito(db, user: User, libro: Libro):
    try:
        # Verificar si ya existe el favorito
        favorito_existente = db.fetch_one(
            "SELECT * FROM favoritos WHERE id_usuario = ? AND id_libro = ?",
            (user.id, libro.id)
        )
        if favorito_existente:
            raise AlreadyInFavoritesError(libro.titulo)

        # Insertar favorito
        db.execute_query(
            "INSERT INTO favoritos (id_usuario, id_libro) VALUES (?, ?)",
            (user.id, libro.id)
        )
        return True
    except AppError:
        raise
    except Exception as e:
        raise UnexpectedAppError(e) from e
    
def eliminar_favorito(db, user: User, libro: Libro):
    try:
        Filas_cambiadas = db.execute_query(
            "DELETE FROM favoritos WHERE id_usuario = ? AND id_libro = ?",
            (user.id, libro.id)
        )
        if Filas_cambiadas == 0:
            raise FavoriteNotFoundError(libro.titulo)
    except AppError as e:
        raise
    except Exception as e:
        raise UnexpectedAppError(e) from e
    else:
        return True
    
def get_favoritos(db, user: User):
    try:
        favoritos = db.fetch_all("""
            SELECT libros.id, libros.titulo, libros.autor, libros.anio, libros.genero
            FROM favoritos
            JOIN libros ON favoritos.id_libro = libros.id
            WHERE favoritos.id_usuario = ?
        """, (user.id,))
        return [Libro(f["titulo"], f["autor"], f["anio"], f["genero"], f["id"]) for f in favoritos]
    except Exception as e:
        raise UnexpectedAppError(e) from e

def insert_usuario(db, user: User):
    try:
        # Verificar si ya existe el usuario
        usuario_existente = db.fetch_one(
            "SELECT * FROM usuarios WHERE username = ?",
            (user.username,)
        )
        if usuario_existente:
            raise UserAlreadyExistsError(user.username)

        if len(user.password) < 6:
            raise InvalidPasswordError()

        # Insertar nuevo usuario
        db.execute_query(
            "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
            (user.username, user.password, user.rol)
        )
        
        return True
    except AppError:
        raise
    except Exception as e:
        raise UnexpectedAppError(e) from e