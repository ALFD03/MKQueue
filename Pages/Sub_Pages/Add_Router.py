# MKQueue/Pages/Sub-Pages/Add_Router.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, app_root)

import flet as ft
import psycopg2 as ps
import ipaddress as ip
from Styles import styles
from Objects import Navigation_Bar
from Objects.Global_Function import navigate_to_router, clear_controls
from Objects.Router_Function import AddRouter

def ValAddRouter(page, Name, router, User, Password, Port):
    try:
        try:
            Port = int(Port)
        except:
            page.open(ft.SnackBar(ft.Text("El numero de puerto no es correcto")))

        ip.IPv4Address(router)
        if all([Name, router, User, Password, Port]):
            try:
                AddRouter(Name, router, User, Password, Port)
                page.open(ft.SnackBar(ft.Text("El router fue cargado exitosamente.")))

            except ps.errors.UniqueViolation:
                page.open(ft.SnackBar(ft.Text("Ya existe el router.")))

            except Exception as e:
                print(f"Hubo un error al cargar los datos: {e}")
        else:
            page.open(ft.SnackBar(ft.Text("Existe algun campo Vacio")))

    except ValueError:
        page.open(ft.SnackBar(ft.Text("La dirrecion IP no esta en formato correcto")))

#! Pagina de Dashboard
def Add_Router(page: ft.Page):
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
    page.title = "MKQueue - Add Router"
    page.padding = ft.padding.all(0)
    
    #* Controles de la pagina
    
    #? Boton para regresar a la lista de los Routers
    Back_to_the_router_list = styles.Back_to_the_list_Button()
    Back_to_the_router_list.on_click = lambda e: navigate_to_router(page)

    #? Controles de Formulario para Agregar Router

    #Nombre de Router
    Name = styles.Settings_textfield(
        label= "Router Name",
        autofocus= True
    )

    #Direccion IP del Router
    router = styles.Settings_textfield(
        label= "Router IP",
        hint_text= "Se tiene que escribir en formato IP"
    )

    #Usuario de acceso al Router
    User = styles.Settings_textfield(
        label= "User"
    )

    #Contraseña de acceso al Router
    Password = styles.Settings_textfield(
        label= "Password"
    )

    #Numero de Puerto de acceso al Router
    Port = styles.Settings_textfield(
        label= "Port"
    )

    #Limpieza de Fomulario
    clear= ft.ElevatedButton(
        text= "Clear",
        width= 585,
        height= 60,
        style=styles.Secundary_Button,
        on_click=lambda e: clear_controls(page, Add_Router)
    )

    #Creacion de Router
    Save= ft.ElevatedButton(
        text= "Create Router",
        width= 585,
        height= 60,
        icon= ft.Icons.ADD,
        style= styles.Primary_Button,
        on_click=lambda e: ValAddRouter(page, Name.value, router.value, User.value, Password.value, Port.value)
    )

    #? Contenedor para Formulario de Agregar Router
    Add_New_Router_Container = styles.ContainerStyle(
        content= ft.Column(
            controls=[
                ft.Text("Router Details", style=styles.Page_Subtitle),
                ft.Row(height=20),
                Name,
                router,
                User,
                Password,
                Port,
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
                                ft.Text("Add Router", style=styles.Page_Title,),
                                ft.VerticalDivider(width=860),
                                Back_to_the_router_list
                            ]
                        ),
                        ft.Row(height= 20),
                        Add_New_Router_Container
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),    
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(Add_Router)