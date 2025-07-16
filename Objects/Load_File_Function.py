# MKQueue/Objects/Load_File_Function.py

"""
    INDICE DE FUNCIONES

    1. PROCESAMIENTO DE ARCHIVOS
    1.1 Procesar archivo Excel/CSV
    1.2 Validar estructura de datos
    1.3 Calcular MIR y CIR
    1.4 Generar vista previa con cálculos
"""

#! Importaciones
import flet as ft
import pandas as pd
import psycopg2 as ps
from Objects.Global_Function import navigate_to_queue_tree
from Database.querys import Connect_db

#! Procesamiento de Archivos

#? Procesar archivo Excel/CSV
def process_file_data(page, file_path, file_data):
    """
    Procesa el archivo cargado y valida su estructura
    """
    try:
        # Validar que el archivo tenga las columnas necesarias
        required_columns = ['ID CONTRATO', 'IP', 'MAC-ADDRESS', 'NOMBRE PLAN', 'MAX. BAJADA [kbps]', 'MAX. SUBIDA [kbps]', 'NOMBRE CLIENTE', 'ID CLIENTE', 'IDENTIFICADOR PERSONALIZABLE', 'EMAIL', 'IDENTIFICADOR NACIONAL', 'DIRECCIÓN DEL CLIENTE', 'TELÉFONOS', 'OBSERVACIONES', 'PPPOE HABILITADO', 'USUARIO PPPOE', 'SERVIDOR', 'NOMBRE OLT', 'INTERFACE MIKROTIK', 'PORCENTAJE CEIL DFL', 'ESTADO', 'CREADO EL', 'ULTIMA MODIFICACION', 'FECHA DE ALTA', 'LATITUD', 'LONGITUD', 'DIRRECIÓN DEL CONTRATO', 'ÍTEMS RECURRENTES', 'DESCUENTOS']
        
        # Verificar si todas las columnas requeridas están presentes
        missing_columns = [col for col in required_columns if col not in file_data.columns]
        
        if missing_columns:
            error_msg = f"El archivo no contiene las columnas requeridas: {', '.join(missing_columns)}"
            page.snack_bar = ft.SnackBar(content=ft.Text(error_msg))
            page.snack_bar.open = True
            page.update()
            return False
        
        # Si todas las validaciones pasan, generar vista previa con cálculos
        return generate_preview_with_calculations(page, file_data)
        
    except Exception as ex:
        error_msg = f"Error al procesar el archivo: {str(ex)}"
        page.snack_bar = ft.SnackBar(content=ft.Text(error_msg))
        page.snack_bar.open = True
        page.update()
        return False

#? Calcular factor de rebanado
def calculate_slicing_factor(client_count, parent_type):
    """
    Calcula el factor de rebanado basado en la cantidad de clientes y tipo de parent
    """
    if client_count <= 2:
        return 1
    elif 3 <= client_count <= 10:
        return 2
    else:
        # Más de 10 clientes
        if "microondas" in parent_type.lower() or "radio" in parent_type.lower():
            return 4
        else:
            return 8

#? Calcular MIR y CIR
def calculate_mir_cir(plan_speed, client_count, slicing_factor):
    """
    Calcula MIR y CIR basado en la velocidad del plan, cantidad de clientes y factor de rebanado
    """
    # MIR = (Velocidad del plan * Cantidad de clientes) / Factor de rebanado
    mir = (plan_speed * client_count) / slicing_factor
    
    # CIR = Velocidad del plan (garantizada por cliente)
    cir = mir*0.8
    
    return round(mir, 2), round(cir, 2)

#? Generar vista previa con cálculos
def generate_preview_with_calculations(page, file_data):
    """
    Genera una vista previa con los cálculos de MIR y CIR por plan y servidor
    """
    try:
        # Obtener datos de la base de datos para comparar
        conn = Connect_db()
        psql = conn.cursor()
        
        # Obtener todos los queue_tree existentes
        psql.execute("SELECT queuetree_name, queuetree_router, queuetree_parent, speed FROM queue_tree")
        existing_queues = psql.fetchall()
        
        # Crear diccionario de queues existentes por coincidencia exacta de queuetree_name
        queue_dict = {}
        for queue in existing_queues:
            # queue = (queuetree_name, queuetree_router, queuetree_parent, speed)
            queue_dict[queue[0]] = {
                'queue_name': queue[0],
                'parent': queue[2],
                'speed': queue[3]
            }
        
        psql.close()
        conn.close()
        
        # Crear lista de preview_data basada en todos los registros de la base de datos
        preview_data = []
        # Recorrer todos los registros de la base de datos
        for queue in existing_queues:
            queuetree_name = queue[0]
            queuetree_router = queue[1]
            queuetree_parent = queue[2]
            queuetree_speed = queue[3]
            # Buscar en el archivo los clientes que coincidan exactamente con queuetree_name y queuetree_router
            # Suponiendo que en el archivo hay columnas 'NOMBRE PLAN', 'SERVIDOR' y queuetree_router se corresponde con 'SERVIDOR'
            # y queuetree_name se corresponde con 'NOMBRE PLAN' + '_' + 'SERVIDOR'
            plan, servidor = None, None
            if '_' in queuetree_name:
                plan, servidor = queuetree_name.rsplit('_', 1)
            # Filtrar el archivo por coincidencia exacta
            if plan is not None and servidor is not None:
                clientes_df = file_data[(file_data['NOMBRE PLAN'] == plan) & (file_data['SERVIDOR'] == queuetree_router)]
            else:
                clientes_df = file_data[(file_data['NOMBRE PLAN'] == queuetree_name) & (file_data['SERVIDOR'] == queuetree_router)]
            client_count = len(clientes_df)
            # Usar la velocidad de la base de datos
            speed = queuetree_speed
            # Calcular slicing factor y MIR/CIR solo si hay clientes
            if client_count > 0:
                slicing_factor = calculate_slicing_factor(client_count, queuetree_parent)
                mir_download, cir_download = calculate_mir_cir(speed, client_count, slicing_factor)
                mir_upload, cir_upload = calculate_mir_cir(speed, client_count, slicing_factor)
            else:
                slicing_factor = 0
                mir_download = cir_download = mir_upload = cir_upload = 0
            preview_data.append({
                'QUEUE_NAME': queuetree_name,
                'ROUTER': queuetree_router,
                'PARENT': queuetree_parent,
                'VELOCIDAD_PLAN_MBPS': speed,
                'CLIENTES': client_count,
                'FACTOR_REBANADO': slicing_factor,
                'MIR_DOWNLOAD': mir_download,
                'CIR_DOWNLOAD': cir_download,
                'MIR_UPLOAD': mir_upload,
                'CIR_UPLOAD': cir_upload
            })
        
        # Crear DataFrame de vista previa
        preview_df = pd.DataFrame(preview_data)
        
        # Guardar datos para uso posterior
        page.session.set("preview_data", preview_df.to_dict('records'))
        page.session.set("original_file_data", file_data.to_dict('records'))
        
        return True
        
    except Exception as ex:
        error_msg = f"Error al generar vista previa: {str(ex)}"
        page.snack_bar = ft.SnackBar(content=ft.Text(error_msg))
        page.snack_bar.open = True
        page.update()
        return False

#? Validar estructura de archivo
def validate_file_structure(file_data):
    """
    Valida la estructura del archivo y retorna información sobre las columnas
    """
    validation_result = {
        'is_valid': True,
        'missing_columns': [],
        'extra_columns': [],
        'total_rows': len(file_data),
        'columns_info': {}
    }
    
    # Columnas requeridas para Wispro
    required_columns = ['ID CONTRATO', 'IP', 'MAC-ADDRESS', 'NOMBRE PLAN', 'MAX. BAJADA [kbps]', 'MAX. SUBIDA [kbps]', 'NOMBRE CLIENTE', 'ID CLIENTE', 'IDENTIFICADOR PERSONALIZABLE', 'EMAIL', 'IDENTIFICADOR NACIONAL', 'DIRECCIÓN DEL CLIENTE', 'TELÉFONOS', 'OBSERVACIONES', 'PPPOE HABILITADO', 'USUARIO PPPOE', 'SERVIDOR', 'NOMBRE OLT', 'INTERFACE MIKROTIK', 'PORCENTAJE CEIL DFL', 'ESTADO', 'CREADO EL', 'ULTIMA MODIFICACION', 'FECHA DE ALTA', 'LATITUD', 'LONGITUD', 'DIRRECIÓN DEL CONTRATO', 'ÍTEMS RECURRENTES', 'DESCUENTOS']
    
    # Verificar columnas faltantes
    validation_result['missing_columns'] = [
        col for col in required_columns if col not in file_data.columns
    ]
    
    # Verificar columnas extra
    validation_result['extra_columns'] = [
        col for col in file_data.columns if col not in required_columns
    ]
    
    # Información de cada columna
    for col in file_data.columns:
        validation_result['columns_info'][col] = {
            'type': str(file_data[col].dtype),
            'null_count': file_data[col].isnull().sum(),
            'unique_count': file_data[col].nunique()
        }
    
    # Determinar si el archivo es válido
    validation_result['is_valid'] = len(validation_result['missing_columns']) == 0
    
    return validation_result

#? Crear archivo de ejemplo
def create_sample_file():
    """
    Crea un archivo de ejemplo con la estructura correcta para Wispro
    """
    sample_data = {
        'ID CONTRATO': ['001', '002', '003', '004', '005'],
        'IP': ['10.0.1.1/24', '10.0.1.2/24', '10.0.1.3/24', '10.0.1.4/24', '10.0.1.5/24'],
        'MAC-ADDRESS': ['AA:BB:CC:DD:EE:01', 'AA:BB:CC:DD:EE:02', 'AA:BB:CC:DD:EE:03', 'AA:BB:CC:DD:EE:04', 'AA:BB:CC:DD:EE:05'],
        'NOMBRE PLAN': ['Plan Básico 10 Mbps', 'Plan Básico 10 Mbps', 'Plan Premium 20 Mbps', 'Plan Premium 20 Mbps', 'Plan Empresarial 50 Mbps'],
        'MAX. BAJADA [kbps]': [10000, 10000, 20000, 20000, 50000],
        'MAX. SUBIDA [kbps]': [10000, 10000, 20000, 20000, 50000],
        'NOMBRE CLIENTE': ['Cliente 1', 'Cliente 2', 'Cliente 3', 'Cliente 4', 'Cliente 5'],
        'ID CLIENTE': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'IDENTIFICADOR PERSONALIZABLE': ['ID001', 'ID002', 'ID003', 'ID004', 'ID005'],
        'EMAIL': ['cliente1@email.com', 'cliente2@email.com', 'cliente3@email.com', 'cliente4@email.com', 'cliente5@email.com'],
        'IDENTIFICADOR NACIONAL': ['V12345678', 'V87654321', 'V11223344', 'V44332211', 'V55667788'],
        'DIRECCIÓN DEL CLIENTE': ['Dirección 1', 'Dirección 2', 'Dirección 3', 'Dirección 4', 'Dirección 5'],
        'TELÉFONOS': ['+584123456789', '+584987654321', '+584112233445', '+584554433221', '+584667788990'],
        'OBSERVACIONES': ['', '', '', '', ''],
        'PPPOE HABILITADO': ['true', 'true', 'true', 'true', 'true'],
        'USUARIO PPPOE': ['user1', 'user2', 'user3', 'user4', 'user5'],
        'SERVIDOR': ['RBP-JGR', 'RBP-JGR', 'RBP-JGR', 'RBP-JGR', 'RBP-JGR'],
        'NOMBRE OLT': ['', '', '', '', ''],
        'INTERFACE MIKROTIK': ['12-SERVICIOS-JGR', '12-SERVICIOS-JGR', '12-SERVICIOS-JGR', '12-SERVICIOS-JGR', '12-SERVICIOS-JGR'],
        'PORCENTAJE CEIL DFL': ['70', '70', '70', '70', '70'],
        'ESTADO': ['Habilitado', 'Habilitado', 'Habilitado', 'Habilitado', 'Habilitado'],
        'CREADO EL': ['01/01/2025 00:00:00', '01/01/2025 00:00:00', '01/01/2025 00:00:00', '01/01/2025 00:00:00', '01/01/2025 00:00:00'],
        'ULTIMA MODIFICACION': ['01/01/2025 00:00:00', '01/01/2025 00:00:00', '01/01/2025 00:00:00', '01/01/2025 00:00:00', '01/01/2025 00:00:00'],
        'FECHA DE ALTA': ['01/01/2025', '01/01/2025', '01/01/2025', '01/01/2025', '01/01/2025'],
        'LATITUD': ['9.913484', '9.913484', '9.913484', '9.913484', '9.913484'],
        'LONGITUD': ['-67.358473', '-67.358473', '-67.358473', '-67.358473', '-67.358473'],
        'DIRRECIÓN DEL CONTRATO': ['San Juan de los Morros - Guárico', 'San Juan de los Morros - Guárico', 'San Juan de los Morros - Guárico', 'San Juan de los Morros - Guárico', 'San Juan de los Morros - Guárico'],
        'ÍTEMS RECURRENTES': ['', '', '', '', ''],
        'DESCUENTOS': ['', '', '', '', '']
    }
    
    df = pd.DataFrame(sample_data)
    
    # Guardar como Excel
    df.to_excel('ejemplo_wispro_contratos.xlsx', index=False)
    
    # Guardar como CSV
    df.to_csv('ejemplo_wispro_contratos.csv', index=False)
    
    return "Archivos de ejemplo creados: ejemplo_wispro_contratos.xlsx y ejemplo_wispro_contratos.csv"

