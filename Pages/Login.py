# MKQueue/Pages/Login.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft
from Styles import styles
from Objects.function import Authentication

#! Pagina de Login
def Login(page: ft.Page):
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
    page.title = "MKQueue - Login"

    #* Controles de la pagina
    #? Cuadro de texto para el usuario
    Username = styles.Login_textfield(
        label = "Username",
        hint_text = "Enter your username",
        autofocus = True,
    )

    #? cuadro de texto para la contraseña
    Password = styles.Login_textfield(
        label = "Password",
        password = True,
        can_reveal_password = True,
    )

    #? Formulario de inicio de sesion
    Form_login = styles.ContainerStyle(
        content=ft.Column(
            controls=[
                ft.Text("Login to your Account", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(height=30,color= ft.Colors.TRANSPARENT),
                Username,
                Password,
                ft.Divider(height=10,color= ft.Colors.TRANSPARENT),
                ft.ElevatedButton("Login", width=300, style= styles.Primary_Button, height=50, on_click=lambda e: Authentication(page, Username.value, Password.value))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        alignment=ft.alignment.center,
        width=450,
        height=400,
    )
    #* Limpieza de la pagina y adición de controles
    page.clean()
    page.add(
        ft.Container(
            height=900,
            width=1600,
            alignment=ft.alignment.center,
            content=Form_login
        ),
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(target=Login)