def log_in(db, usuario, contrasena):
    try: 
        user = db.fetch_one(
            "SELECT * FROM usuarios WHERE username = ? AND password = ?",
            (usuario, contrasena)
        )
        print(user)
        return user
    except Exception as e:
        print(e)
        return False

def get_libros(db):
    try:
        libros = db.fetch_all("SELECT * FROM libros")
        print(libros)
        return libros
    except Exception as e:
        print(e)
    
def insert_libro(db, titulo, autor, anio, genero):
    try:
        # Verificar si el libro ya existe
        libro_existente = db.fetch_one(
            "SELECT * FROM libros WHERE titulo = ? AND autor = ? AND anio = ? AND genero = ?",
            (titulo, autor, anio, genero)
        )
        if libro_existente:
            print("Error: El libro ya existe en la base de datos.")
            return False
        # Insertar el libro si no existe
        db.execute_query(
            "INSERT INTO libros (titulo, autor, anio, genero) VALUES (?, ?, ?, ?)",
            (titulo, autor, anio, genero)
        )
        print("Libro insertado correctamente.")
        return True
    except Exception as e:
        print(f"Error al insertar libro: {e}")
        return False

def update_libro(db, id_libro, titulo, autor, anio, genero):
    try:
        # Verificar si ya existe otro libro con los mismos datos
        libro_existente = db.fetch_one(
            "SELECT * FROM libros WHERE titulo = ? AND autor = ? AND anio = ? AND genero = ? AND id != ?",
            (titulo, autor, anio, genero, id_libro)
        )
        if libro_existente:
            print("Error: Ya existe otro libro con esos datos.")
            return False
        # Actualizar el libro
        db.execute_query(
            "UPDATE libros SET titulo = ?, autor = ?, anio = ?, genero = ? WHERE id = ?",
            (titulo, autor, anio, genero, id_libro)
        )
        print("Libro actualizado correctamente.")
        return True
    except Exception as e:
        print(f"Error al actualizar libro: {e}")
        return False

def delete_libro(db, id_libro):
    try:
        db.execute_query(
            "DELETE FROM libros WHERE id = ?",
            (id_libro,)
        )
        print("Libro eliminado correctamente.")
        return True
    except Exception as e:
        print(f"Error al eliminar libro: {e}")

def buscar_libros(db, titulo=None, autor=None, anio=None, genero=None):
    query = "SELECT * FROM libros WHERE 1=1"
    params = []
    if titulo:
        query += " AND titulo LIKE ?"
        params.append(f"%{titulo}%")
    if autor:
        query += " AND autor LIKE ?"
        params.append(f"%{autor}%")
    if anio:
        query += " AND anio = ?"
        params.append(anio)
    if genero:
        query += " AND genero LIKE ?"
        params.append(f"%{genero}%")
    try:
        libros = db.fetch_all(query, tuple(params))
        print(libros)
        return libros
    except Exception as e:
        print(f"Error al buscar libros: {e}")
        return []

def agregar_favorito(db, id_usuario, id_libro):
    try:
        # Verificar si ya existe el favorito
        favorito_existente = db.fetch_one(
            "SELECT * FROM favoritos WHERE id_usuario = ? AND id_libro = ?",
            (id_usuario, id_libro)
        )
        if favorito_existente:
            print("Error: El libro ya está en favoritos.")
            return False
        # Insertar favorito
        db.execute_query(
            "INSERT INTO favoritos (id_usuario, id_libro) VALUES (?, ?)",
            (id_usuario, id_libro)
        )
        print("Libro agregado a favoritos correctamente.")
        return True
    except Exception as e:
        print(f"Error al agregar a favoritos: {e}")
        return False

def eliminar_favorito(db, id_usuario, id_libro):
    try:
        db.execute_query(
            "DELETE FROM favoritos WHERE id_usuario = ? AND id_libro = ?",
            (id_usuario, id_libro)
        )
        print("Libro eliminado de favoritos correctamente.")
        return True
    except Exception as e:
        print(f"Error al eliminar de favoritos: {e}")
        return False

