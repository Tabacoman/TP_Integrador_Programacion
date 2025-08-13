import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_name="biblioteca.db"):
        """
        Inicializa la base de datos.
        
        Args:
            db_name (str): Nombre del archivo de la base de datos (default: "biblioteca.db")
        """
        self.db_name = db_name
        self.create_tables()
        self.insert_initial_data()

    def get_connection(self):
        """
        Establece una conexión con la base de datos.
        
        Returns:
            sqlite3.Connection: Objeto de conexión a la base de datos
        """
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        """Crea las tablas necesarias si no existen."""
        with self.get_connection() as conn:
            # Tabla de usuarios
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    rol TEXT NOT NULL CHECK(rol IN ('admin', 'user'))
                )
            """)
            
            # Tabla de libros
            conn.execute("""
                CREATE TABLE IF NOT EXISTS libros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    anio INTEGER,
                    genero TEXT NOT NULL
                )
            """)
            
            # Tabla de favoritos (relación muchos a muchos)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS favoritos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    id_libro INTEGER NOT NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
                    FOREIGN KEY (id_libro) REFERENCES libros(id),
                    UNIQUE(id_usuario, id_libro)  -- Evita duplicados
                )
            """)

    def insert_initial_data(self):
        """Inserta datos iniciales (usuarios y libros de ejemplo)."""
        with self.get_connection() as conn:
            # Insertar usuarios iniciales si no existen
            usuarios = [
                ('admin', 'admin123', 'admin'),
                ('usuario1', 'user123', 'user')
            ]
            
            for user in usuarios:
                try:
                    conn.execute(
                        "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                        user
                    )
                except sqlite3.IntegrityError:
                    pass  # Usuario ya existe
            
            # Insertar libros iniciales si no existen
            libros = [
                ('Cien años de soledad', 'Gabriel García Márquez', 1967, 'Realismo mágico'),
                ('1984', 'George Orwell', 1949, 'Ciencia ficción'),
                ('El principito', 'Antoine de Saint-Exupéry', 1943, 'Fábula')
            ]
            
            for libro in libros:
                conn.execute(
                    "INSERT INTO libros (titulo, autor, anio, genero) VALUES (?, ?, ?, ?)",
                    libro
                )

    def execute_query(self, query, params=()):
        """
        Ejecuta una consulta que no retorna datos (INSERT, UPDATE, DELETE).
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta
        """
        with self.get_connection() as conn:
            conn.execute(query, params)

    def fetch_all(self, query, params=()):
        """
        Ejecuta una consulta y retorna todas las filas.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta
            
        Returns:
            list: Lista de diccionarios con los resultados
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query, params=()):
        """
        Ejecuta una consulta y retorna la primera fila.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple): Parámetros para la consulta
            
        Returns:
            dict: Diccionario con la primera fila o None si no hay resultados
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None