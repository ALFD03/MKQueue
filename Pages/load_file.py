# MKQueue/Pages/load_file.py

#! Importaciones
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
app_root = os.path.dirname(current_dir)
sys.path.insert(0, app_root)

import flet as ft
import pandas as pd
from Styles import styles
from Objects import Navigation_Bar
from Objects.Global_Function import navigate_to_queue_tree, require_auth
from Objects.Load_File_Function import process_file_data, validate_file_structure
import psycopg2 as ps
from Database.querys import Connect_db

#! Pagina de Carga de Archivos
def Load_File(page: ft.Page):
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
    page.title = "MKQueue - Load File"
    page.padding = ft.padding.all(0)

    #? Verificar autenticación
    if not require_auth(page):
        return

    #* Variables globales
    file_path = None
    file_data = None
    preview_data = None

    #* Controles de la pagina

    #? Boton para regresar a Queue Tree
    Back_to_Queue_Tree_Button = styles.Back_to_the_list_Button()
    Back_to_Queue_Tree_Button.on_click = lambda e: navigate_to_queue_tree(page)

    #? Selector de archivo
    File_Picker = ft.FilePicker(
        on_result=lambda e: handle_file_selection(e, page)
    )
    page.overlay.append(File_Picker)

    #? Boton para seleccionar archivo
    Select_File_Button = ft.ElevatedButton(
        style=styles.Primary_Button,
        text="Select File",
        width=160,
        height=60,
        icon=ft.Icons.FOLDER_OPEN,
        icon_color=ft.Colors.WHITE,
        on_click=lambda e: File_Picker.pick_files(
            allowed_extensions=["xlsx", "xls", "csv"],
            allow_multiple=False
        )
    )

    #? Información del archivo seleccionado
    File_Info = ft.Text(
        "No file selected",
        style=styles.Page_Subtitle,
        color=ft.Colors.GREY_600
    )

    #? Botón para procesar archivo
    Process_File_Button = ft.ElevatedButton(
        style=styles.Primary_Button,
        text="Process File",
        width=160,
        height=60,
        icon=ft.Icons.PLAY_ARROW,
        icon_color=ft.Colors.WHITE,
        disabled=True,
        on_click=lambda e: process_selected_file(page)
    )

    #? Tabla de vista previa con cálculos
    Preview_Table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(ft.Text("Queue Name", text_align=ft.TextAlign.CENTER), width=300)),
            ft.DataColumn(ft.Container(ft.Text("Router", text_align=ft.TextAlign.CENTER), width=100)),
            ft.DataColumn(ft.Container(ft.Text("Parent", text_align=ft.TextAlign.CENTER), width=280)),
            ft.DataColumn(ft.Container(ft.Text("Velocidad Plan", text_align=ft.TextAlign.CENTER), width=100)),
            ft.DataColumn(ft.Container(ft.Text("Clientes", text_align=ft.TextAlign.CENTER), width=60)),
            ft.DataColumn(ft.Container(ft.Text("Factor Rebanado", text_align=ft.TextAlign.CENTER), width=80)),
            ft.DataColumn(ft.Container(ft.Text("MIR", text_align=ft.TextAlign.CENTER), width=100)),
            ft.DataColumn(ft.Container(ft.Text("CIR", text_align=ft.TextAlign.CENTER), width=100)),
        ],
        rows=[],
        column_spacing=5,
        heading_row_height=40,
        border=ft.border.all(1, ft.Colors.GREY_300),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        show_checkbox_column=False,
    )

    # Contenedor para vista previa de QueueTree con ancho 600 y altura 540
    Preview_Container = styles.ContainerStyle(
        content=ft.Column([
            ft.Row(
                [Preview_Table],
                scroll=ft.ScrollMode.ALWAYS,
                width=1190,
            )
        ],
        scroll=ft.ScrollMode.ALWAYS,
        width=1190,
        height=400
        ),
        width=1190,
        height=400,
    )

    #* Tabla de Parents
    Parent_Table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(ft.Text("Parent", text_align=ft.TextAlign.CENTER), width=220)),
            ft.DataColumn(ft.Container(ft.Text("Parent ID", text_align=ft.TextAlign.CENTER), width=80)),
            ft.DataColumn(ft.Container(ft.Text("Router", text_align=ft.TextAlign.CENTER), width=120)),
            ft.DataColumn(ft.Container(ft.Text("MIR", text_align=ft.TextAlign.CENTER), width=120)),
            ft.DataColumn(ft.Container(ft.Text("CIR", text_align=ft.TextAlign.CENTER), width=120)),
        ],
        rows=[],
        column_spacing=5,
        heading_row_height=40,
        border=ft.border.all(1, ft.Colors.GREY_300),
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_300),
        show_checkbox_column=False,
    )

    # Contenedor para vista previa de Parents con ancho 600 y altura 540
    Parent_Container = styles.ContainerStyle(
        content=ft.Column([
            ft.Row(
                [Parent_Table],
                scroll=ft.ScrollMode.ALWAYS,
                width=780,
            )
        ],
        scroll=ft.ScrollMode.ALWAYS,
        width=780,
        height=400
        ),
        width=780,
        height=400,
    )

    #* Funciones de manejo de eventos

    #? Manejar selección de archivo
    def handle_file_selection(e, page):
        nonlocal file_path, file_data
        
        if e.files:
            file_path = e.files[0].path
            file_name = e.files[0].name
            
            try:
                # Leer archivo según su extensión
                if file_name.endswith('.csv'):
                    file_data = pd.read_csv(file_path)
                else:
                    file_data = pd.read_excel(file_path)
                
                # Validar estructura del archivo
                validation = validate_file_structure(file_data)
                
                if validation['is_valid']:
                    File_Info.value = f"File loaded: {file_name} ({validation['total_rows']} rows)"
                    File_Info.color = ft.Colors.GREEN_600
                    Process_File_Button.disabled = False
                else:
                    File_Info.value = f"Invalid file structure. Missing columns: {', '.join(validation['missing_columns'])}"
                    File_Info.color = ft.Colors.RED_600
                    Process_File_Button.disabled = True
                
                page.update()
                
            except Exception as ex:
                File_Info.value = f"Error reading file: {str(ex)}"
                File_Info.color = ft.Colors.RED_600
                Process_File_Button.disabled = True
                page.update()

    #? Procesar archivo seleccionado
    def process_selected_file(page):
        nonlocal file_data, preview_data
        
        if file_data is not None:
            if process_file_data(page, file_path, file_data):
                preview_data = page.session.get("preview_data")
                
                if preview_data:
                    Preview_Table.rows = []
                    for idx, row in enumerate(preview_data):
                        queue_name = row['QUEUE_NAME']
                        parent = row['PARENT']
                        velocidad = row['VELOCIDAD_PLAN_MBPS']
                        router = row['ROUTER']
                        Preview_Table.rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Container(ft.Text(str(queue_name)), width=200, padding=ft.Padding(0, 12, 0, 12))),
                                    ft.DataCell(ft.Container(ft.Text(str(router)), width=100, padding=ft.Padding(0, 12, 0, 12))),
                                    ft.DataCell(ft.Container(ft.Text(str(parent)), width=280, padding=ft.Padding(0, 12, 0, 12))),
                                    ft.DataCell(ft.Container(ft.Text(f"{int(round(velocidad))} Mbps"), width=100, padding=ft.Padding(0, 12, 0, 12))),
                                    ft.DataCell(ft.Container(ft.Text(str(row['CLIENTES'])), width=60, padding=ft.Padding(0, 12, 0, 12))),
                                    ft.DataCell(ft.Container(ft.Text(str(row['FACTOR_REBANADO'])), width=80, padding=ft.Padding(0, 12, 0, 12))),
                                    ft.DataCell(ft.Container(ft.Text(f"{int(round(row['MIR_DOWNLOAD']))} Mbps"), width=100, padding=ft.Padding(0, 12, 0, 12))),
                                    ft.DataCell(ft.Container(ft.Text(f"{int(round(row['CIR_DOWNLOAD']))} Mbps"), width=100, padding=ft.Padding(0, 12, 0, 12))),
                                ]
                            )
                        )
                    # Llenar la tabla de parents
                    fill_parent_table()
                    page.update()
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"File processed successfully. {len(preview_data)} queue configurations calculated."))
                    page.snack_bar.open = True
                    page.update()

    # Diálogo para editar el factor de rebanado
    def show_edit_slicing_factor_dialog(row_idx):
        nonlocal preview_data
        if not preview_data or row_idx >= len(preview_data):
            return
        row = preview_data[row_idx]
        slicing_factor_field = ft.TextField(
            label="Nuevo factor de rebanado",
            value=str(row['FACTOR_REBANADO']) if row['FACTOR_REBANADO'] is not None else "1",
            keyboard_type=ft.KeyboardType.NUMBER
        )
        def save_factor(e):
            try:
                if not preview_data or row_idx >= len(preview_data):
                    return
                new_factor = int(slicing_factor_field.value or 1)
                if new_factor < 1:
                    raise ValueError
                plan_speed = row['VELOCIDAD_PLAN_MBPS']
                client_count = row['CLIENTES']
                mir_download, cir_download = plan_speed * client_count / new_factor, plan_speed
                mir_upload, cir_upload = plan_speed * client_count / new_factor, plan_speed
                row['FACTOR_REBANADO'] = new_factor
                row['MIR_DOWNLOAD'] = round(mir_download, 2)
                row['CIR_DOWNLOAD'] = round(cir_download, 2)
                row['MIR_UPLOAD'] = round(mir_upload, 2)
                row['CIR_UPLOAD'] = round(cir_upload, 2)
                preview_data[row_idx] = row
                process_selected_file(page)
                page.close(dialog)
            except Exception:
                slicing_factor_field.error_text = "Debe ser un número entero mayor a 0"
                page.update()
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar factor de rebanado", style=styles.Page_Subtitle),
            content=ft.Column([
                ft.Text(f"Queue: {row['QUEUE_NAME']} | Router: {row['ROUTER']}"),
                slicing_factor_field
            ],height=100),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
                ft.TextButton("Guardar", on_click=save_factor)
            ]
        )
        page.open(dialog)

    #* Lógica para poblar la tabla de parents (recursiva, usando id)
    def fill_parent_table():
        if not preview_data:
            return
        # Obtener todos los parents de la base de datos y construir jerarquía
        conn = Connect_db()
        psql = conn.cursor()
        psql.execute("SELECT id, parent_name, parent, router FROM parent")
        parents_raw = psql.fetchall()
        psql.close()
        conn.close()
        # parent_dict: id -> {parent_name, parent_id (nombre), router}
        parent_dict = {}
        for id_, parent_name, parent_id, router in parents_raw:
            # Si el parent es WAN, no tiene parent
            if parent_name.strip().upper() == 'WAN':
                parent_id = None
            parent_dict[id_] = {"parent_name": parent_name, "parent_id": parent_id, "router": router}
        # Eliminar prints de depuración
        # Mapear parent_name+router a id para lookup rápido
        name_router_to_id = {(info['parent_name'], info['router']): id_ for id_, info in parent_dict.items()}
        # Mapear los CIR/MIR de las colas hijas por parent_name y router
        parent_cir_map = {}
        for row in preview_data:
            key = (row['PARENT'], row['ROUTER'])
            if key not in name_router_to_id:
                continue
            parent_id = name_router_to_id[key]
            parent_key = (row['PARENT'], row['ROUTER'])
            cir_down = row['CIR_DOWNLOAD']
            cir_up = row['CIR_UPLOAD']
            mir_down = row['MIR_DOWNLOAD']
            mir_up = row['MIR_UPLOAD']
            if parent_key not in parent_cir_map:
                parent_cir_map[parent_key] = {'cir_down': 0, 'cir_up': 0, 'mir_down': 0, 'mir_up': 0}
            parent_cir_map[parent_key]['cir_down'] += cir_down
            parent_cir_map[parent_key]['cir_up'] += cir_up
            parent_cir_map[parent_key]['mir_down'] += mir_down
            parent_cir_map[parent_key]['mir_up'] += mir_up
        # Llenar la tabla
        Parent_Table.rows = []
        parent_agg_cache = {}
        def aggregate_cir_mir(parent_name, router):
            if (parent_name, router) in parent_agg_cache:
                return parent_agg_cache[(parent_name, router)]
            mir_down = mir_up = cir_down = cir_up = 0
            key = (parent_name, router)
            if key in parent_cir_map:
                mir_down += parent_cir_map[key]['mir_down']
                mir_up += parent_cir_map[key]['mir_up']
                cir_down += parent_cir_map[key]['cir_down']
                cir_up += parent_cir_map[key]['cir_up']
            # Buscar hijos por parent_id (nombre) y router
            for child_id, info in parent_dict.items():
                if info['parent_id'] == parent_name and info['router'] == router:
                    c_mir_down, c_mir_up, c_cir_down, c_cir_up = aggregate_cir_mir(info['parent_name'], router)
                    mir_down += c_mir_down
                    mir_up += c_mir_up
                    cir_down += c_cir_down
                    cir_up += c_cir_up
            parent_agg_cache[(parent_name, router)] = (mir_down, mir_up, cir_down, cir_up)
            return mir_down, mir_up, cir_down, cir_up
        for id_, info in parent_dict.items():
            parent_name = info["parent_name"]
            router = info["router"]
            parent_id = info["parent_id"]
            mir_down, mir_up, cir_down, cir_up = aggregate_cir_mir(parent_name, router)
            Parent_Table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(ft.Text(str(parent_name)), width=220, padding=ft.Padding(0, 12, 0, 12))),
                        ft.DataCell(ft.Container(ft.Text(str(parent_id)), width=80, padding=ft.Padding(0, 12, 0, 12))),
                        ft.DataCell(ft.Container(ft.Text(str(router)), width=120, padding=ft.Padding(0, 12, 0, 12))),
                        ft.DataCell(ft.Container(ft.Text(f"{int(round(mir_down))} Mbps"), width=120, padding=ft.Padding(0, 12, 0, 12))),
                        ft.DataCell(ft.Container(ft.Text(f"{int(round(cir_down))} Mbps"), width=120, padding=ft.Padding(0, 12, 0, 12))),
                    ]
                )
            )

    #* Limpieza de la Pagina y adición de controles
    page.clean()
    page.add(
        ft.Column([
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
                                    ft.Text("Load File", style=styles.Page_Title, width=200),
                                    ft.VerticalDivider(width=780, color=ft.Colors.TRANSPARENT),
                                    Back_to_Queue_Tree_Button,
                                ],
                            ),
                            ft.Row(height=20),
                            ft.Row(
                                controls=[
                                    Select_File_Button,
                                    ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
                                    Process_File_Button,
                                ],
                            ),
                            ft.Row(height=10),
                            File_Info,
                            ft.Row(height=20),
                            ft.Column([
                                ft.Row([Preview_Container,],width=1210),
                                ft.Row([Parent_Container],width=1210)
                            ],scroll= ft.ScrollMode.ALWAYS,height=400)
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ], scroll=ft.ScrollMode.ALWAYS)
    )

#! Ejecutar la aplicacion siempre que se ejecute desde este archivo
if __name__ == "__main__":
    ft.app(Load_File) 