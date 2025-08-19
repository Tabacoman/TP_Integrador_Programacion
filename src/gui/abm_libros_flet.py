import flet as ft
from Utilities.funtions import get_libros, insert_libro, update_libro, delete_libro


def abm_libros_view(page: ft.Page, db, volver_al_menu):
    libro_editando = {"id": None}  # guarda el libro que se está editando

    def abrir_formulario(e, libro=None):
        """Abrir formulario en modo agregar o editar"""
        if libro:  # MODO EDITAR
            libro_editando["id"] = libro["id"]
            titulo.value = libro["titulo"]
            autor.value = libro["autor"]
            anio.value = str(libro["anio"])
            genero.value = libro["genero"]
            dlg.title = ft.Text("Editar libro")
        else:  # MODO AGREGAR
            libro_editando["id"] = None
            for tf in (titulo, autor, anio, genero):
                tf.value = ""
            dlg.title = ft.Text("Agregar libro")

        page.open(dlg)
        page.update()

    def cerrar_dialogo(e=None):
        page.close(dlg)

    def guardar_libro(e):
        _anio = anio.value.strip()
        if _anio and not _anio.isdigit():
            page.snack_bar = ft.SnackBar(ft.Text("El año debe ser numérico."))
            page.snack_bar.open = True
            page.update()
            return

        if libro_editando["id"] is None:
            # INSERTAR
            insert_libro(
                db,
                titulo.value.strip(),
                autor.value.strip(),
                int(_anio) if _anio else "",
                genero.value.strip()
            )
        else:
            # EDITAR
            update_libro(
                db,
                libro_editando["id"],
                titulo.value.strip(),
                autor.value.strip(),
                int(_anio) if _anio else "",
                genero.value.strip()
            )

        # limpiar
        for tf in (titulo, autor, anio, genero):
            tf.value = ""

        page.close(dlg)
        refrescar()
        page.update()

    def eliminar_libro(libro):
        delete_libro(db, libro["id"])
        refrescar()
        page.update()

    def refrescar(e=None):
        """Recargar libros desde la BD y actualizar la tabla"""
        libros = get_libros(db) or []
        tabla.rows.clear()

        for libro in libros:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(libro.get("id", "")))),
                        ft.DataCell(ft.Text(libro.get("titulo", ""))),
                        ft.DataCell(ft.Text(libro.get("autor", ""))),
                        ft.DataCell(ft.Text(str(libro.get("anio", "")))),
                        ft.DataCell(ft.Text(libro.get("genero", ""))),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon="edit",
                                        tooltip="Editar",
                                        on_click=lambda e, l=libro: abrir_formulario(e, l)
                                    ),
                                    ft.IconButton(
                                        icon="delete",
                                        tooltip="Eliminar",
                                        on_click=lambda e, l=libro: eliminar_libro(l)
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
        page.update()

    page.title = "Gestión de Libros (ABM)"
    page.clean()

    # --- Tabla
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Autor")),
            ft.DataColumn(ft.Text("Año")),
            ft.DataColumn(ft.Text("Género")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    # --- Formulario
    titulo = ft.TextField(label="Título", autofocus=True)
    autor = ft.TextField(label="Autor")
    anio = ft.TextField(label="Año", keyboard_type=ft.KeyboardType.NUMBER)
    genero = ft.TextField(label="Género")

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar libro"),
        content=ft.Column([titulo, autor, anio, genero], tight=True, scroll="adaptive"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Guardar", on_click=guardar_libro),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # --- Botones
    btn_agregar = ft.ElevatedButton("Agregar libro", icon="add", on_click=abrir_formulario)

    btn_volver = ft.ElevatedButton(
        "Volver",
        icon="arrow_back",
        on_click=lambda e: volver_al_menu()
    )

    # --- Layout
    elementos = [
        ft.Text("📚 Gestión de Libros", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([btn_agregar], alignment="center"),
        tabla,
        btn_volver
    ]

    page.add(ft.Column(elementos, alignment="center", horizontal_alignment="center", expand=True))

    # Cargar datos
    refrescar()
    page.update()
