# MKQueue/Pages/QueueTree.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft
from Objects import Navigation_Bar
from Styles import styles
from Objects.Global_Function import navigate_to_add_new_queue_tree
from Objects.Queue_Tree_Function import ViewQueue, EditQueueFunction, DeleteQueueFunction

#! Pagina del Arbol de Colas
def QueueTree(page: ft.Page):
    #* Estilos de la pagina
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
    page.title = "MKQueue - Queue Tree"
    page.padding = ft.padding.all(0)

    #* Controles de la pagina

    #? Boton para cargar un archivo
    Load_File_Button = ft.ElevatedButton(
        style=styles.Primary_Button,
        text= "Load File",
        width= 160,
        height= 60,
        icon= ft.Icons.FOLDER,
        icon_color= ft.Colors.WHITE,
    )

    #? Boton para Sincronizar con el Router
    # Sync_Router_Button = ft.ElevatedButton(
    #     style=styles.Primary_Button,
    #     text= "Sync To Router",
    #     width= 160,
    #     height= 60,
    #     icon= ft.Icons.SYNC_ALT,
    #     icon_color= ft.Colors.WHITE,
    # )

    #? Boton para sincronizar desde el router
    # Sync_From_Router_Button = ft.ElevatedButton(
    #     style=styles.Primary_Button,
    #     text= "Sync From Router",
    #     width= 160,
    #     height= 60,
    #     icon= ft.Icons.SYNC,
    #     icon_color= ft.Colors.WHITE,
    # )

    #? Boton para Agregar una nueva cola
    Add_Queue_Button = ft.ElevatedButton(
        style=styles.Primary_Button,
        text= "Add New Queue Tree",
        width= 160,
        height= 60,
        icon= ft.Icons.ADD,
        icon_color= ft.Colors.WHITE,
    )
    Add_Queue_Button.on_click = lambda e: navigate_to_add_new_queue_tree(page)

     #? Lista de Queue Tree
    Queuetree_List = styles.List_tables(
        columns=[
            ft.DataColumn(ft.Text(style=styles.Page_Subtitle, value="Queue Tree Name")),
            ft.DataColumn(ft.Text(style=styles.Page_Subtitle, value="Queue Tree Router")),
            ft.DataColumn(ft.Text(style=styles.Page_Subtitle, value="Queue Tree Parent")),
            ft.DataColumn(ft.Text(style=styles.Page_Subtitle, value="Actions"))
        ]
    )

    #? Contenedor para Lista de Colas
    Queue_List_Container = styles.ContainerStyle(
        width= 1190,
        height= 700,
        content=ft.Column(
            [
                ft.Divider(height=10, color= ft.Colors.TRANSPARENT),
                ft.Text("Configured Queue Trees", style=styles.Page_Subtitle,),
                ft.Divider(height=10, color= ft.Colors.TRANSPARENT),
                ft.Column([Queuetree_List],scroll=ft.ScrollMode.AUTO, height=600)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    #* Limpieza de la Pagina y adición de controles
    page.clean()
    ViewQueue(page, Queuetree_List, EditQueueFunction, DeleteQueueFunction)
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
                                ft.Text("Queue Tree Management",style=styles.Page_Title, width= 200),
                                ft.VerticalDivider(width=630, color= ft.Colors.TRANSPARENT),
                                Load_File_Button,
                                #Sync_Router_Button,
                                #Sync_From_Router_Button,
                                Add_Queue_Button,
                            ],
                        ),
                        ft.Row(height=20),
                        Queue_List_Container
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(QueueTree)