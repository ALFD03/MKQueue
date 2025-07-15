#MKQueue/Pages/Sub-Pages/Add_Queue_tree.py


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
from Objects.Global_Function import navigate_to_queue_tree, clear_controls
from Objects.Queue_Tree_Function import ListParent, AddQueueTree
from Objects.Router_Function import ListRouter

def ValAddQueueTree(page, queuetree_name, queuetree_router, queuetree_parent, speed, download_queue, upload_queue):
    if all([queuetree_name, queuetree_router, queuetree_parent, speed, download_queue, upload_queue]):
            try:
                speed = int(speed)

            except:
                page.open(ft.SnackBar(ft.Text("La velocidad no es correcta")))

            try:
                AddQueueTree(queuetree_name, queuetree_router, queuetree_parent, speed, download_queue, upload_queue)
                page.open(ft.SnackBar(ft.Text("La cola fue cargado exitosamente.")))

            except ps.errors.UniqueViolation:
                page.open(ft.SnackBar(ft.Text("Ya existe la cola.")))

            except Exception as e:
                print(f"Hubo un error al cargar los datos: {e}")
    else:
        page.open(ft.SnackBar(ft.Text("Existe algun campo Vacio")))

#! Pagina de Dashboard
def Add_Queue_tree(page: ft.Page):
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
    Back_to_Queue_Tree_Button.on_click = lambda e: navigate_to_queue_tree(page)

    #? Controles de Formulario para Agregar Queue Tree

    #Nombre de Queue
    Name = styles.Settings_textfield(
        label= "Queue Tree Name",
        autofocus= True
    )

    #Seleccion de router
    router = styles.DropDown(
        label= "Router",
        on_change= lambda e: ListParent(page, Parent, router.value)
    )

    #Pariente
    Parent = styles.DropDown(
        label= "Parent",
        disabled=True,
        
    )

    #Velocidad
    Speed = styles.Settings_textfield(
        label= "Queue Speed",
        hint_text= "Only Numbers"
    )

    #Nombre de Cola Descarga
    Download_Queue = styles.Settings_textfield(
        label= "Download Queue"
    )

    #Nombre de Cola Subida
    Upload_Queue = styles.Settings_textfield(
        label= "Upload Queue"
    )

    #Limpieza de Fomulario
    clear= ft.ElevatedButton(
        text= "Clear",
        width= 585,
        height= 60,
        style=styles.Secundary_Button,
        on_click= lambda e: clear_controls(page, Add_Queue_tree)
    )

    #Creacion de Cola
    Save= ft.ElevatedButton(
        text= "Create Queue Tree",
        width= 585,
        height= 60,
        icon= ft.Icons.ADD,
        style= styles.Primary_Button,
        on_click= lambda e: ValAddQueueTree(page, Name.value, router.value, Parent.value, Speed.value, Download_Queue.value, Upload_Queue.value)
    )

    #? Contenedor para Formulario de Agregar Queue Tree
    Add_New_Queue_Tree_Container = styles.ContainerStyle(
        content= ft.Column(
            controls=[
                ft.Text("Queue Tree Details", style=styles.Page_Subtitle),
                ft.Row(height=20),
                Name,
                router,
                Parent,
                Speed,
                Download_Queue,
                Upload_Queue,
                ft.Row([clear,Save])
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=1200
    )

    #* Limpieza de la Pagina y adición de controles
    page.clean()
    ListRouter(page, router)
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
                                ft.VerticalDivider(width=810),
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
    ft.app(Add_Queue_tree)