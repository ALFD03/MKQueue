# MKQueue/Pages/Router.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft
from Objects import Navigation_Bar
from Styles import styles

#! Pagina de Router
def Router(page: ft.Page):
    #* Estilos de la pagina
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = '#FFFFFF'
    page.window.width = ft.Window.width
    page.window.height = 900
    page.window.resizable = False
    page.window.maximizable = False
    page.fonts = {
        "Inter": "Recursos/Fuentes/Inter.ttf",
    }
    page.theme = ft.Theme(font_family="Inter")
    page.title = "MKQueue - Router"
    page.padding = ft.padding.all(0)

    #* Controles de la pagina

    #? Boton para agregar un router
    Add_New_Router = ft.ElevatedButton(
        style=styles.Primary_Button,
        text= "Add New Router",
        width= 160,
        height= 60,
        icon= ft.Icons.ADD,
        icon_color= ft.Colors.WHITE,
    )

    #? Contenedor para Lista de Routers
    Router_List_Container = ft.Container(
        width= 900,
        height= 700,
        bgcolor= "#FBFAF9",
        border_radius= ft.border_radius.all(10),
        border= ft.border.all(2, "#EDEDED"),
        padding=ft.padding.all(10),
        content=ft.Column(
            [
                ft.Divider(height=10, color= ft.Colors.TRANSPARENT),
                ft.Text("Configured Router", style=styles.Page_Subtitle,),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    #* Limpieza de la Pagina y adición de controles
    page.clean()
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        Navigation_Bar.Navigation_Bar,
                    ],
                ),
                ft.Column(
                    controls=[
                        ft.VerticalDivider(width=25)
                    ]
                ),
                ft.Column(
                    controls=[
                        ft.Row(height=10),
                        ft.Row(
                            controls=[
                                ft.Text("Router Management",style=styles.Page_Title, width= 200),
                                ft.VerticalDivider(width=520, color= ft.Colors.TRANSPARENT),
                                Add_New_Router,
                            ],
                        ),
                        ft.Row(height=20),
                        Router_List_Container
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(Router)