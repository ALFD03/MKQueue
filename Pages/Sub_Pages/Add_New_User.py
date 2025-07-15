#MKQueue/Pages/Sub-Pages/Add_New_User.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, app_root)

import flet as ft
import psycopg2 as ps
from Styles import styles
from Objects import Navigation_Bar
from Objects.Global_Function import clear_controls, navigate_to_settings
from Objects.Settings_Function import AddNewUser

def ValAddNewUser(page, Username, Email, Name, Last_Name, Password, Confirm_Password):
    if all([Username, Email, Name, Last_Name, Password, Confirm_Password]):
        if Password == Confirm_Password:
            try:
                AddNewUser(page, Username, Email, Name, Last_Name, Password, Confirm_Password)
                page.open(ft.SnackBar(ft.Text("El usuario fue cargado exitosamente.")))

            except ps.errors.UniqueViolation:
                page.open(ft.SnackBar(ft.Text("Ya existe el usuario.")))

            except Exception as e:
                print(f"Hubo un error al cargar los datos: {e}")
        else:
            page.open(ft.SnackBar(ft.Text("Las contraseñas no coinciden.")))
    else:
        page.open(ft.SnackBar(ft.Text("Existe algun campo Vacio")))


#! Pagina de Dashboard
def Add_New_User(page: ft.Page):
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
    page.title = "MKQueue - Add New User"
    page.padding = ft.padding.all(0)
    
    #* Controles de la pagina
    
    #? Boton para regresar a las configuraciones
    Back_to_Settings_Button = styles.Back_to_the_list_Button()
    Back_to_Settings_Button.on_click = lambda e: navigate_to_settings(page)

    #? Controles de Formulario para Agregar Usuario

    #Nombre de Usuario
    Username = styles.Settings_textfield(
        label= "Username",
        autofocus= True
    )

    #Email del Usuario
    Email = styles.Settings_textfield(
        label= "Email"
    )

    #Nombre
    Name = styles.Settings_textfield(
        label= "Name"
    )

    #Apellido
    Last_name = styles.Settings_textfield(
        label= "Last Name"
    )
    #Contraseña del Usuario
    Password = styles.Settings_textfield(
        label= "Password"
    )

    #Confirmar Contraseña del Usuario
    Confirm_Password = styles.Settings_textfield(
        label= "Confirm Password"
    )

    #Limpieza de Fomulario
    clear= ft.ElevatedButton(
        text= "Clear",
        width= 585,
        height= 60,
        style=styles.Secundary_Button,
        on_click= lambda e: clear_controls(page, Add_New_User)
    )

    #Creacion de Usuario
    Save= ft.ElevatedButton(
        text= "Create User",
        width= 585,
        height= 60,
        icon= ft.Icons.ADD,
        style= styles.Primary_Button,
        on_click= lambda e: ValAddNewUser(page, Username.value,Email.value,Name.value,Last_name.value,Password.value,Confirm_Password.value)

    )

    #? Contenedor para Formulario de Agregar Queue Tree
    Add_New_User_Container = styles.ContainerStyle(
        content= ft.Column(
            controls=[
                ft.Text("User Details", style=styles.Page_Subtitle),
                ft.Row(height=20),
                Username,
                Email,
                Name,
                Last_name,
                Password,
                Confirm_Password,
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
                                ft.Text("Add New User", style=styles.Page_Title,),
                                ft.VerticalDivider(width=830),
                                Back_to_Settings_Button
                            ]
                        ),
                        ft.Row(height= 20),
                        Add_New_User_Container
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),    
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(Add_New_User)