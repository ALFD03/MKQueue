#MKQueue/Styles/styles.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft

#! Estilo de Boton predeterminado Principal
Primary_Button = ft.ButtonStyle(
    color= ft.Colors.WHITE,
    bgcolor= '#1098f7',
    padding= ft.padding.only(20, 10, 20, 10),
    alignment= ft.alignment.center,
    shape= ft.RoundedRectangleBorder(radius= ft.border_radius.all(10)),
    text_style= ft.TextStyle(
        weight= ft.FontWeight.W_700,
        size= 16,
    )
)

#! Estilo de Campo de texto para el Login
class Login_textfield(ft.TextField):
    def __init__(self, **kwargs):
        super().__init__(
            border_radius=ft.border_radius.all(10),
            border_color='#D3D0CB',
            border_width=0.5,
            height=50,
            width=300,
            hint_style= ft.TextStyle(
                color="#DBDAD8FF",
                weight= ft.FontWeight.W_700,
                size= 12,
            ), 
            label_style= ft.TextStyle(
                color= ft.Colors.BLACK,
                weight= ft.FontWeight.W_900,
                italic= True,
                size=12
            ),
            text_style= ft.TextStyle(
                color= ft.Colors.BLACK,
                weight= ft.FontWeight.W_500,
                size= 12,
            ),
            **kwargs
        )

#! Estilo de Texto para el Titulo de la pagina
Page_Title = ft.TextStyle(
    color= ft.Colors.BLACK,
    weight= ft.FontWeight.W_900,
    size= 22,
    italic= True,
)

Values_Style = ft.TextStyle(
    color= ft.Colors.BLACK,
    size= 18,
    weight= ft.FontWeight.W_800,
)

ContainerLabel_style = ft.TextStyle(
    color= "#858585",
    size= 16,
    weight= ft.FontWeight.W_500,
)

Page_Subtitle = ft.TextStyle(
    color= ft.Colors.BLACK,
    weight= ft.FontWeight.W_700,
    size= 20,
    )

class ContainerStyle1(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(
            width= 280,
            height= 200,
            bgcolor= "#FBFAF9",
            border_radius= ft.border_radius.all(10),
            border= ft.border.all(2, "#EDEDED"),
            padding=ft.padding.all(10),
            **kwargs
        )

class ContainerStyles2(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(
            width= 900,
            height= 500,
            bgcolor= "#FBFAF9",
            border_radius= ft.border_radius.all(10),
            border= ft.border.all(2, "#EDEDED"),
            padding=ft.padding.all(10),
            **kwargs
            )
