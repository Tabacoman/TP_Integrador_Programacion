from models.Libro import Libro
from models.User import User

def log_in(db, user: User):
    try: 
        row = db.fetch_one(
            "SELECT * FROM usuarios WHERE username = ? AND password = ?",
            (user.username, user.password)
        )
        
        return User(row["username"], row["password"], row["rol"], row["id"])
    except Exception as e:
        print(e)
        return False

def get_libros(db):
    try:
        Rows = db.fetch_all("SELECT * FROM libros")
        
        return [Libro(row["titulo"], row["autor"], row["anio"], row["genero"], row["id"]) for row in Rows]

    except Exception as e:
        print(e)
    
def insert_libro(db, libro: Libro):
    try:
        # Verificar si el libro ya existe
        libro_existente = db.fetch_one(
            "SELECT * FROM libros WHERE titulo = ? AND autor = ? AND anio = ? AND genero = ?",
            (libro.titulo, libro.autor, libro.anio, libro.genero)
        )
        if libro_existente:
            print("Error: El libro ya existe en la base de datos.")
            return False
        # Insertar el libro si no existe
        db.execute_query(
            "INSERT INTO libros (titulo, autor, anio, genero) VALUES (?, ?, ?, ?)",
            (libro.titulo, libro.autor, libro.anio, libro.genero)
        )
        print("Libro insertado correctamente.")
        return True
    except Exception as e:
        print(f"Error al insertar libro: {e}")
        return False

def update_libro(db, libro: Libro):
    try:
        # Verificar si ya existe otro libro con los mismos datos
        libro_existente = db.fetch_one(
            "SELECT * FROM libros WHERE titulo = ? AND autor = ? AND anio = ? AND genero = ? AND id != ?",
            (libro.titulo, libro.autor, libro.anio, libro.genero, libro.id)
        )
        if libro_existente:
            print("Error: Ya existe otro libro con esos datos.")
            return False
        # Actualizar el libro
        db.execute_query(
            "UPDATE libros SET titulo = ?, autor = ?, anio = ?, genero = ? WHERE id = ?",
            (libro.titulo, libro.autor, libro.anio, libro.genero, libro.id)
        )
        print("Libro actualizado correctamente.")
        return True
    except Exception as e:
        print(f"Error al actualizar libro: {e}")
        return False

def delete_libro(db, libro: Libro):
    try:
        db.execute_query(
            "DELETE FROM libros WHERE id = ?",
            (libro.id,)
        )
        print("Libro eliminado correctamente.")
        return True
    except Exception as e:
        print(f"Error al eliminar libro: {e}")

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
        print(f"Error al buscar libros: {e}")
        return []

def agregar_favorito(db, user: User, libro: Libro):
    try:
        # Verificar si ya existe el favorito
        favorito_existente = db.fetch_one(
            "SELECT * FROM favoritos WHERE id_usuario = ? AND id_libro = ?",
            (user.id, libro.id)
        )
        if favorito_existente:
            print("Error: El libro ya está en favoritos.")
            return False
        # Insertar favorito
        db.execute_query(
            "INSERT INTO favoritos (id_usuario, id_libro) VALUES (?, ?)",
            (user.id, libro.id)
        )
        print("Libro agregado a favoritos correctamente.")
        return True
    except Exception as e:
        print(f"Error al agregar a favoritos: {e}")
        return False

def eliminar_favorito(db, user: User, libro: Libro):
    try:
        db.execute_query(
            "DELETE FROM favoritos WHERE id_usuario = ? AND id_libro = ?",
            (user.id, libro.id)
        )
        print("Libro eliminado de favoritos correctamente.")
        return True
    except Exception as e:
        print(f"Error al eliminar de favoritos: {e}")
        return False

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
        print(e)
        return []

def insert_usuario(db, user: User):
    try:
        # Verificar si ya existe el usuario
        usuario_existente = db.fetch_one(
            "SELECT * FROM usuarios WHERE username = ?",
            (user.id,)
        )
        if usuario_existente:
            print("Error: El usuario ya existe.")
            return False

        if len(user.password) < 6:
            print("Error: La contraseña debe tener al menos 6 caracteres.")
            return False

        # Insertar nuevo usuario
        db.execute_query(
            "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
            (user.id, user.password, user.rol)
        )
        print("Usuario registrado correctamente.")
        return True
    except Exception as e:
        print(f"Error al insertar usuario: {e}")
        return False
