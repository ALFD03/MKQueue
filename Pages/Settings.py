# MKQueue/Pages/Setting.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft
from Objects import Navigation_Bar
from Styles import styles
from Objects.function import navigate_to_add_new_user

#! Pagina de Configuraciones
def Settings(page: ft.Page):
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
    page.title = "MKQueue - Settings"
    page.padding = ft.padding.all(0)

    #* Controles de la pagina

    #? Controles del Formulario de Datos usuario actual
    #Usuario
    Username = styles.Settings_textfield(
        label= "Username",
    )
    #Email
    Email = styles.Settings_textfield(
        label= "Email",
    )
    #Nombres
    Names = styles.Settings_textfield(
        label= "Name",
    )
    #Apellidos
    Last_Name = styles.Settings_textfield(
        label= "Last Name",
    )
    Privileges = styles.DropDown(
        label= "Privilegios"
    )

    #Boton para cambiar contraseña
    Change_Password= ft.ElevatedButton(
        style= styles.Secundary_Button,
        text="Change Password",
        height=60,
        width=160
    )
    
    #Boton para cancelar edicion
    Cancel_Edit = ft.ElevatedButton(
        style= styles.Secundary_Button,
        text= "Cancel",
        height=60,
        width=160 
    )

    #Boton para guardar cambios
    Save_Change = ft.ElevatedButton(
        style=styles.Primary_Button,
        text= "Save Change",
        height=60,
        width=840
    )

    #? Contenedor para formulario de Datos de Usuario Actual
    Current_User_Data_Container = styles.ContainerStyle(
        width= 1200,
        content=ft.Column([
            ft.Text("Current User Data", style=styles.Page_Subtitle),
            Username,
            Email,
            Names,
            Last_Name,
            Privileges,
            ft.Row([Change_Password,Cancel_Edit,Save_Change])
        ]

        )
    )

    #? Controles para formulario de Lista de Usuaios
    New_User_Button = ft.ElevatedButton(
        style= styles.Primary_Button,
        text= "Add New User",
        height= 50,
        width= 1200,
        icon= ft.Icons.ADD
    )
    New_User_Button.on_click = lambda e: navigate_to_add_new_user(page)
    
    #? Contenedor de formulario lista de Usuarios
    User_List_Container = styles.ContainerStyle(
        width= 1200,
        height=300,
        content= ft.Column(
            [
                ft.Text("User List", style=styles.Page_Subtitle),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                New_User_Button,
            ],
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
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
                                ft.Text("Settings",style=styles.Page_Title, width= 200),
                            ],
                        ),
                        ft.Row(height=20),
                        ft.Row(
                            controls=[
                                Current_User_Data_Container
                            ]
                        ),
                        ft.Row(height=5),
                        ft.Row(
                            controls=[
                                User_List_Container
                            ]
                        )
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START
        )
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(Settings)