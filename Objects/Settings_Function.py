#MKQueue/Objects/Settings_Function.py

"""
    INDICE DE FUNCIONES

    1. EVENTOS
    1.1 Funcion de Agregar user
"""

#! Importaciones
import flet as ft
import psycopg2 as ps
from Styles import styles
from Objects.Global_Function import navigate_to_settings
from Database.querys import Connect_db


#! Eventos

#? Funcion de Agregar user
def AddNewUser (page, Username, Email, Name, Last_name, Password, Confirm_Password):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "INSERT INTO users (username, email, name, last_name, password, confirm_password) VALUES (%s, %s, %s, %s, %s, %s)",
        (
            Username,
            Email,
            Name,
            Last_name,
            Password,
            Confirm_Password,
        )
    )
    conn.commit()
    psql.close()
    conn.close()
    navigate_to_settings(page)

#? Funcion para listar user
def ViewUser(page, DataTable, Edit_Function, Delete_Function):
    conn = Connect_db()
    psql = conn.cursor()
    psql.execute(
        "SELECT username, email, name, last_name, password, confirm_password FROM users"
    )
    users = psql.fetchall()
    psql.close()
    conn.close()

    for user in users:
        iduser= user[0]
        username= user[0]
        email = user[1]
        name = user[2]
        last_name = user[3]
        password = user[4]
        Cpassword = user[5]

        Edit_btn = styles.Edit_button(on_click= lambda e, ruser= username, remail= email, rname= name, rlast= last_name, rpass= password, rcpass= Cpassword, rid= iduser: Edit_Function(page,ruser,remail,rname,rlast,rpass,rcpass,rid))
        Delete_btn = styles.delete_button(on_click= lambda e, rid= iduser: Delete_Function(page, rid))

        Action_Container = styles.ContainerAction(
            content= ft.Row([Edit_btn,Delete_btn])
        )

        DataTable.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(user[0])),
                    ft.DataCell(ft.Text(user[1])),
                    ft.DataCell(ft.Text(user[2])),
                    ft.DataCell(ft.Text(user[3])),
                    ft.DataCell(Action_Container)
                ]
            )
        )
#? Funcion para Editar Router
def EditUserFuction(page, username, email, name, last_name, password, Cpassword, iduser):

    #* Funcion para Editar user y sincronizar base de Datos
    def EditUser(page, username, email, name, last_name, password, Cpassword, iduser, dialog):
        conn = Connect_db()
        psql = conn.cursor()
        try:
            psql.execute(
                "UPDATE users SET username = %s email = %s name = %s last_name = %s password = %s Cpassword = %s WHERE username = %s",
                (
                    username,
                    email,
                    name,
                    last_name,
                    password,
                    Cpassword,
                    iduser
                )
            )
            conn.commit()
            psql.close()
            conn.close()
            page.close(dialog)
            navigate_to_settings(page)

        except ps.errors.UniqueViolation:
            page.open(ft.SnackBar(ft.Text("No se pudo editar ya que el nombre del router ya existe")))

    TxtF_username = styles.Login_textfield(label= "Username", value= username)
    TxtF_email = styles.Login_textfield(label= "Email", value= email)
    TxtF_name = styles.Login_textfield(label= "Name", value= name)
    TxtF_last_name = styles.Login_textfield(label= "Last Name", value= last_name)
    TxtF_password = styles.Login_textfield(label= "Password", value= password)
    TxtF_Cpassword = styles.Login_textfield(label= "Confirm Password", value= Cpassword)

    cancel= ft.ElevatedButton(
        style=styles.Secundary_Button, 
        text="Cancel",
        on_click= lambda e: page.close(EditDialog)
    )

    edit= ft.ElevatedButton(
        style=styles.Primary_Button, 
        text="Edit Router", 
        on_click=lambda e: EditUser(page, TxtF_username.value, TxtF_email.value, TxtF_name.value, TxtF_last_name.value, TxtF_password.value, TxtF_Cpassword.value, iduser, EditDialog)
    )

    EditDialog = ft.AlertDialog(
        modal= True,
        title= ft.Text("Edit Router", style=styles.Page_Subtitle),
        alignment=ft.alignment.center,
        content= ft.Column(
            [
                TxtF_username,
                TxtF_email,
                TxtF_name,
                TxtF_last_name,
                TxtF_password,
                TxtF_Cpassword
            ],
            height=350
        ),
        actions_alignment= ft.MainAxisAlignment.END,
        actions= [
            cancel,
            edit
        ],
        on_dismiss= lambda e: page.close(EditDialog),
    )

    page.open(EditDialog)

#? Funcion para borrar user
def DeleteUserFunction(page, iduser):

    #* Funcion para borar user y sinconizar base de datos
    def DeleteUser(page, dialog):
        conn = Connect_db()
        psql = conn.cursor()
        psql.execute(
            "DELETE FROM users WHERE username = %s",
            (iduser,)
        )
        conn.commit()
        psql.close()
        conn.close()
        page.close(dialog)
        navigate_to_settings(page)
    
    confirmation_Dialog= ft.AlertDialog(
        modal= True,
        title= ft.Text(style=styles.Page_Subtitle, value="Confirmation Delete"),
        actions_alignment= ft.MainAxisAlignment.END,
        actions=[
            ft.ElevatedButton(style= styles.Secundary_Button, text="Cancel", on_click= lambda e: page.close(confirmation_Dialog)),
            ft.ElevatedButton("Confirm", style= styles.Primary_Button, on_click=lambda e: DeleteUser(page, confirmation_Dialog))
        ]
    )

    page.open(confirmation_Dialog)
