# Consultas útiles para la base de datos

# Ver todos los usuarios
QUERY_SELECT_ALL_USERS = "SELECT * FROM usuarios"

# Ver todos los libros
QUERY_SELECT_ALL_BOOKS = "SELECT * FROM libros"

# Ver todos los favoritos
QUERY_SELECT_ALL_FAVORITOS = "SELECT * FROM favoritos"

# Buscar usuario por nombre de usuario
QUERY_SELECT_USER_BY_USERNAME = "SELECT * FROM usuarios WHERE username = ?"

# Buscar libro por título
QUERY_SELECT_BOOK_BY_TITLE = "SELECT * FROM libros WHERE titulo = ?"

# Insertar nuevo usuario
QUERY_INSERT_USER = "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)"

# Insertar nuevo libro
QUERY_INSERT_BOOK = "INSERT INTO libros (titulo, autor, anio, genero) VALUES (?, ?, ?, ?)"

# Insertar favorito
QUERY_INSERT_FAVORITO = "INSERT INTO favoritos (id_usuario, id_libro) VALUES (?, ?)"

# Eliminar usuario por id
QUERY_DELETE_USER_BY_ID = "DELETE FROM usuarios WHERE id = ?"

# Eliminar libro por id
QUERY_DELETE_BOOK_BY_ID = "DELETE FROM libros WHERE id = ?"

# Eliminar favorito por id
QUERY_DELETE_FAVORITO_BY_ID = "DELETE FROM favoritos WHERE id = ?"