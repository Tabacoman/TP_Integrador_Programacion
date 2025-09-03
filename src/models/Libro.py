class Libro:
    def __init__(self, titulo, autor, anio, genero, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.genero = genero

    