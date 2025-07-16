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
from Objects.Global_Function import require_auth, navigate_to_load_file, navigate_to_add_new_queue_tree

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

    #* Obtener cantidad de queue trees y routers
    import psycopg2 as ps
    from Database.querys import Connect_db
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute("SELECT COUNT(*) FROM queue_tree")
    queue_tree_result = psql.fetchone()
    queue_tree_count = queue_tree_result[0] if queue_tree_result else 0
    psql.execute("SELECT COUNT(*) FROM router")
    router_result = psql.fetchone()
    router_count = router_result[0] if router_result else 0
    psql.close()
    conn.close()
    Value_Active_QueueTree.value = str(queue_tree_count)
    Value_Active_Router.value = str(router_count)

    #* Obtener lista de parents
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute("SELECT parent_name FROM parent LIMIT 10")
    parent_names = [row[0] for row in psql.fetchall()]
    psql.close()
    conn.close()

    #? Contenedor para acciones rápidas
    QuickActions_Container = styles.ContainerStyle(
        content=ft.Column(
            [
                ft.Text("Acciones rápidas", style=styles.Page_Subtitle),
                ft.Row([
                    ft.ElevatedButton(
                        text="Cargar archivo",
                        icon=ft.Icons.UPLOAD_FILE,
                        style=styles.Primary_Button,
                        on_click=lambda e: require_auth(page) and navigate_to_load_file(page)
                    ),
                    ft.ElevatedButton(
                        text="Agregar Queue Tree",
                        icon=ft.Icons.ADD,
                        style=styles.Primary_Button,
                        on_click=lambda e: require_auth(page) and navigate_to_add_new_queue_tree(page)
                    ),
                ], spacing=20),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text("Parents registrados", style=styles.Page_Subtitle),
                ft.ListView([
                    ft.ListTile(title=ft.Text(name)) for name in parent_names
                ], height=220, width=400)
            ],
            width=600,
            height=360,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=600,
        height=360,
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
                                QuickActions_Container,
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