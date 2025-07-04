#MKQueue/Pages/Sub-Pages/Add_Queue_tree.py


#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, app_root)

import flet as ft
from Styles import styles
from Objects import Navigation_Bar

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
    page.title = "MKQueue - Add Queue Tree"
    page.padding = ft.padding.all(0)
    
    #* Controles de la pagina
    
    #? Boton para regresar a la lista de las Queue Tree
    Back_to_Queue_Tree_Button = styles.Back_to_the_list_Button()

    #? Controles de Formulario para Agregar Queue Tree

    #Nombre de Queue
    Name = styles.Settings_textfield(
        label= "Queue Tree Name",
        autofocus= True
    )

    #Seleccion de router
    router = styles.DropDown(
        label= "Router"
    )

    #Tipo de Cola
    Queue_type = styles.DropDown(
        label= "Queue Type"
    )

    #Pariente
    Parent = styles.DropDown(
        label= "Parent"
    )

    #Marcado de paquete
    Packet_Marks = styles.DropDown(
        label= "Packet Marks"
    )

    #Limite Maximo de Traffico
    Max_Limit = styles.Settings_textfield(
        label= "Max Limit"
    )

    #Limite Minimo de Trafico
    Limit_at = styles.Settings_textfield(
        label= "Limit At"
    )

    #Prioridad de la Cola'
    Priority = styles.Settings_textfield(
        label= "Priority"
    )

    #Limpieza de Fomulario
    clear= ft.ElevatedButton(
        text= "Clear",
        width= 585,
        height= 60,
        style=styles.Secundary_Button
    )

    #Creacion de Cola
    Save= ft.ElevatedButton(
        text= "Create Queue Tree",
        width= 585,
        height= 60,
        icon= ft.Icons.ADD,
        style= styles.Primary_Button
    )

    #? Contenedor para Formulario de Agregar Queue Tree
    Add_New_Queue_Tree_Container = styles.ContainerStyle(
        content= ft.Column(
            controls=[
                ft.Text("Queue Tree Details", style=styles.Page_Subtitle),
                ft.Row(height=20),
                Name,
                router,
                Queue_type,
                Parent,
                Packet_Marks,
                Max_Limit,
                Limit_at,
                Priority,
                ft.Row([clear,Save])
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=1200
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
                        ft.Row(
                            controls=[
                                ft.Text("Add Queue Tree", style=styles.Page_Title,),
                                ft.VerticalDivider(width=830),
                                Back_to_Queue_Tree_Button
                            ]
                        ),
                        ft.Row(height= 20),
                        Add_New_Queue_Tree_Container
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