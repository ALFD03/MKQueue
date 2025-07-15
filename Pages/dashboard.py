#MKQueue/Pages/dashboard.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft
from Styles import styles
from Objects import Navigation_Bar
from Objects.Global_Function import require_auth

#! Pagina de Dashboard
def Dashboard(page: ft.Page):
    #*Estilos de la pagina
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = '#FFFFFF'
    page.window.width = 1600
    page.window.height = 900
    page.window.resizable = False
    page.window.maximizable = False
    page.fonts = {
        "Inter": "Recursos/Fuentes/Inter.ttf",
    }
    page.theme = ft.Theme(font_family="Inter")
    page.title = "MKQueue - Dashboard"
    page.padding = ft.padding.all(0)
    
    #? Verificar autenticación
    if not require_auth(page):
        return
    
    #* Controles de la pagina

    #? Contenedor para las queue trees activas
    Value_Active_QueueTree = ft.Text(style=styles.Values_Style)
    Active_QueueTree = styles.ContainerStyle(
        content=ft.Column(
            [
                ft.Image(src="Recursos/Iconos/QueueTreeIcon.png", width=40, height=80, fit=ft.ImageFit.CONTAIN),
                Value_Active_QueueTree,
                ft.Text("Active Queue Tree", style=styles.ContainerLabel_style)
            ],
            width= 570,
            height= 200,
            )
    )

    #? Contenedor para las queue types activas
    # Value_Active_QueueType = ft.Text(style=styles.Values_Style)
    # Active_QueueType = styles.ContainerStyle(
    #     content=ft.Column(
    #         [
    #             ft.Image(src="Recursos/Iconos/QueueTypeIcon.png", width=40, height=80, fit=ft.ImageFit.CONTAIN),
    #             Value_Active_QueueType,
    #             ft.Text("Active Queue Type", style=styles.ContainerLabel_style)
    #         ],
    #         width= 360,
    #         height= 200,
    #         )
    # )

    #? Contenedor para los router activos
    Value_Active_Router = ft.Text(style=styles.Values_Style)
    Active_Router = styles.ContainerStyle(
        content=ft.Column(
            [
                ft.Image(src="Recursos/Iconos/RouterIcon.png", width=40, height=80, fit=ft.ImageFit.CONTAIN),
                Value_Active_Router,
                ft.Text("Active Router", style=styles.ContainerLabel_style)
            ],
            width= 570,
            height= 200,
            )
    )

    #? Conetendor para la Grafica de tendencia en WAN
    Traffic_WAN = styles.ContainerStyle(
        content=ft.Column(
            [
                ft.Divider(height=10, color= ft.Colors.TRANSPARENT),
                ft.Text("Traffic WAN", style=styles.Page_Subtitle,),
            ],
            width= 1190,
            height= 450,
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
                        ft.Row(height= 10),
                        ft.Text("Dashboard", style=styles.Page_Title,),
                        ft.Row(height= 20),
                        ft.Row(
                            [
                                Active_QueueTree,
                                #Active_QueueType,
                                Active_Router
                            ],
                            spacing= 30,
                        ),
                        ft.Row(height= 20),
                        ft.Row(
                            [
                                Traffic_WAN,
                            ]
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),    
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(Dashboard)