from Utilities.funtions import get_libros, insert_libro, update_libro, delete_libro
import flet as ft
from models.Libro import Libro
from models.Errors import BookAlreadyExistsError, AppError, InvalidInsertError, VoidInsertError

def abm_libros_view(page: ft.Page, db, volver_al_menu):
    libro_editando = {"id": None}  # guarda el libro que se está editando

    def abrir_formulario(e, libro=None):
        """Abrir formulario en modo agregar o editar"""
        if libro:  # MODO EDITAR
            libro_editando["id"] = libro.id
            titulo.value = libro.titulo
            autor.value = libro.autor
            anio.value = str(libro.anio)
            genero.value = libro.genero
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
        try:
            if _anio and not _anio.isdigit():
                raise AppError("El año debe ser numérico.")
            if libro_editando["id"] is None:
                insert_libro(
                    db, Libro(
                        titulo.value.strip(),
                        autor.value.strip(),
                        int(_anio) if _anio else "",
                        genero.value.strip()
                    )
                )
            else:
                update_libro(
                    db, Libro(
                        libro_editando["id"],
                        titulo.value.strip(),
                        autor.value.strip(),
                        int(_anio) if _anio else "",
                        genero.value.strip()
                    )
                )
            for tf in (titulo, autor, anio, genero):
                tf.value = ""
            page.close(dlg)
            refrescar()
            page.open(ft.SnackBar(ft.Text("Libro guardado correctamente."), bgcolor="green"))
        except BookAlreadyExistsError as err:
            page.open(ft.SnackBar(ft.Text(str(err)), bgcolor="red"))
        except InvalidInsertError as err:
            page.open(ft.SnackBar(ft.Text(str(err)), bgcolor="red"))
        except VoidInsertError as err:
            page.open(ft.SnackBar(ft.Text(str(err)), bgcolor="red"))
        except AppError as err:
            page.open(ft.SnackBar(ft.Text(str(err)), bgcolor="red"))
        except Exception as err:
            page.open(ft.SnackBar(ft.Text(f"Error inesperado: {err}"), bgcolor="red"))
        page.update()

    def eliminar_libro(e, libro):
        try:
            delete_libro(db, libro)
            # ✅ Confirmación cuando se elimina correctamente
            page.open(ft.SnackBar(ft.Text(f"Libro '{libro.titulo}' eliminado correctamente."), bgcolor="green"))
        except AppError as err:
            page.open(ft.SnackBar(ft.Text(str(err)), bgcolor="red"))
        except Exception as err:
            page.open(ft.SnackBar(ft.Text(f"Error inesperado: {err}"), bgcolor="red"))
        refrescar()
        page.update()

    def refrescar(e=None):
        """Recargar libros desde la BD y actualizar la tabla"""
        libros = get_libros(db) or []
        contenido = []
        for libro in libros:
            contenido.append(
                ft.Container(
                    ft.Row([
                        ft.Column([
                            ft.Text(f"Título: {libro.titulo}", size=18, weight="bold"),
                            ft.Text(f"Autor: {libro.autor}"),
                            ft.Text(f"Año: {libro.anio}"),
                            ft.Text(f"Género: {libro.genero}"),
                        ], expand=True),
                        ft.Row([
                            ft.IconButton(
                                icon="edit",
                                tooltip="Editar",
                                on_click=lambda e, l=libro: abrir_formulario(e, l),
                                icon_color="#568ec7"
                            ),
                            ft.IconButton(
                                icon="delete",
                                tooltip="Eliminar",
                                on_click=lambda e, l=libro: eliminar_libro(e, l),
                                icon_color="#e53e3e"
                            ),
                        ])
                    ], alignment="spaceBetween"),
                    padding=10,
                    margin=ft.margin.symmetric(vertical=8, horizontal=0),
                    bgcolor="#f4f4f4",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=4, color="#00000022", offset=ft.Offset(0, 2))
                )
            )
        libros_scroll = ft.Column(
            contenido,
            expand=True,
            scroll="auto",
            alignment="center",
            horizontal_alignment="center",
            spacing=10
        )
        # Pon el botón volver después del scroll
        main_column.controls[2:] = [libros_scroll, btn_volver]
        page.update()

    page.title = "Gestión de Libros (ABM)"
    page.clean()

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
    main_column = ft.Column([
        ft.Text("📚 Gestión de Libros", size=28, weight="bold", color="#2d3e50", font_family="Georgia", text_align="center"),
        ft.Row([btn_agregar], alignment="center"),
    ], alignment="center", horizontal_alignment="center", expand=True, spacing=20)

    main_content = ft.Container(
        content=main_column,
        bgcolor="#faf9e3",
        border_radius=30,
        padding=40,
        expand=True,
        alignment=ft.alignment.center,
        height=600
    )

    page.add(
        ft.Column([main_content], expand=True, alignment="center", horizontal_alignment="center")
    )

    # Cargar datos
    refrescar()
    page.update()
