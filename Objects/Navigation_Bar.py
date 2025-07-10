# MKQueue/Objects/Navigation_Bar.py

#! importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft
from Objects import function

#! Definicion de los destinos de la barra de navegacion

#? Destino del Dashboard
Dashboard = ft. NavigationRailDestination(
    label_content= ft.Text(
        "Dashboard",
        size= 14,
        weight= ft.FontWeight.W_700,
    ),
    icon= ft.Image(
        src= "Recursos/Iconos/DashboardIcon.png",
        width= 40,
        height= 40,
        fit= ft.ImageFit.CONTAIN,
    ),
)

#? Destino del Queue Tree
Queue_Tree = ft.NavigationRailDestination(
    label_content= ft.Text(
        "Queue Tree",
        size= 14,
        weight= ft.FontWeight.W_700,
    ),
    icon= ft.Image(
        src= "Recursos/Iconos/QueueTreeIcon.png",
        width= 30,
        height= 30,
        fit= ft.ImageFit.CONTAIN,
    ),
)

#? Destino del Queue Type
# Queue_type = ft.NavigationRailDestination(
#     label_content= ft.Text(
#         "Queue Type",
#         size= 14,
#         weight= ft.FontWeight.W_700,
#     ),
#     icon= ft.Image(
#         src= "Recursos/Iconos/QueueTypeIcon.png",
#         width= 30,
#         height= 30,
#         fit= ft.ImageFit.CONTAIN,
        
#     ),
# )

#? Destino del Router
Router = ft.NavigationRailDestination(
    label_content= ft.Text(
        "Router",
        size= 14,
        weight= ft.FontWeight.W_700,
    ),
    icon= ft.Image(
        src= "Recursos/Iconos/RouterIcon.png",
        width= 30,
        height= 30,
        fit= ft.ImageFit.CONTAIN,
    ),
)

#? Destino de Configuraciones
Settings = ft.NavigationRailDestination(
    label_content= ft.Text(
        "Configuration",
        size= 14,
        weight= ft.FontWeight.W_700,
    ),
    icon= ft.Icons.SETTINGS,
)

def Navigation_Change(page, index):
    if index == 0:
        function.navigate_to_dashboard(page)
    elif index == 1:
        function.navigate_to_queue_tree(page)
    # elif index == 2:
    #     function.navigate_to_queue_type(page)
    elif index == 2:
        function.navigate_to_router(page)
    elif index == 3:
        function.navigate_to_settings(page)

#! Definicion de la barra de navegacion
Navigation_Bar = ft.NavigationRail(
    extended= True,
    width= 300,
    height= 900,
    leading= ft.Column(
        [
            ft.Divider(height=10, color= ft.Colors.TRANSPARENT),
            ft.Text("MKQueue", size= 20, weight= ft.FontWeight.W_900, color= ft.Colors.BLACK),
            ft.Divider(height=10, color= ft.Colors.TRANSPARENT),
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
    ),
    bgcolor= "#f5eeee",
    destinations= [
        Dashboard,
        Queue_Tree,
        #Queue_type,
        Router,
        Settings
    ],
    on_change= lambda e: Navigation_Change(e.page, e.control.selected_index),
)