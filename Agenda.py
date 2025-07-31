# Agenda de contactos (Java o Python + MySQL)
# Guarda nombre, teléfono, mail y dirección.
# Permite buscar, editar y eliminar contactos.
# → Demuestra manejo de CRUD + conexión a base de datos.

import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Función para obtener un nuevo cursor
def get_cursor():
    return conexion.cursor(buffered=True)

# Insertamos los datos a la tabla
def agendar_contacto():
    nombre = entrada_nombre.get()
    telefono = entrada_telefono.get()
    mail = entrada_mail.get()
    direccion = entrada_direccion.get()    

    if nombre and direccion:
        try:
            cursor = get_cursor()
            cursor.execute(
                "INSERT INTO contactos (nombre, telefono, mail, direccion) VALUES (%s, %s, %s, %s)",
                (nombre, telefono, mail, direccion)
            )
            conexion.commit()
            messagebox.showinfo("Éxito", "Contacto agendado correctamente")
            
            entrada_nombre.delete(0, tk.END)
            entrada_telefono.delete(0, tk.END)
            entrada_mail.delete(0, tk.END)
            entrada_direccion.delete(0, tk.END)
            
            cursor.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo guardar el contacto: {error}")
    else:
        messagebox.showwarning("Atención", "Debés ingresar al menos el nombre y el teléfono")

# Función para editar contacto (VERSIÓN CORREGIDA)
def editar_contacto():
    ventana2 = tk.Toplevel()
    ventana2.title("Editar contacto")
    ventana2.geometry("500x300")
    ventana2.minsize(500, 300)
    ventana2.resizable(0,0)

    frame2 = tk.Frame(ventana2)
    frame2.configure(width=500, height=300, bg="grey", bd=6)
    frame2.pack()

    tk.Label(frame2, text="Elija qué dato quiere editar", bg="grey").pack()
    tk.Label(frame2, text="¿Qué contacto quiere editar?", bg="grey").pack()
    editar_persona = tk.Entry(frame2, width=30)
    editar_persona.pack()

    tk.Label(frame2, text="Nuevo nombre", bg="grey").pack()
    editar_nombre = tk.Entry(frame2, width=30)
    editar_nombre.pack()

    tk.Label(frame2, text="Nuevo teléfono", bg="grey").pack()
    editar_telefono = tk.Entry(frame2, width=30)
    editar_telefono.pack()

    tk.Label(frame2, text="Nuevo mail", bg="grey").pack()
    editar_mail = tk.Entry(frame2, width=30)
    editar_mail.pack()

    tk.Label(frame2, text="Nueva dirección", bg="grey").pack()
    editar_direccion = tk.Entry(frame2, width=30)
    editar_direccion.pack()

    def confirmar_editar():
        nombre_original = editar_persona.get().strip()
        nuevo_nombre = editar_nombre.get().strip()
        nuevo_telefono = editar_telefono.get().strip()
        nuevo_mail = editar_mail.get().strip()
        nueva_direccion = editar_direccion.get().strip()

        if not nombre_original:
            messagebox.showwarning("Atención", "Debés ingresar el nombre del contacto que querés editar")
            return
            
        try:
            # Verificar si el contacto existe
            cursor = get_cursor()
            cursor.execute("SELECT id FROM contactos WHERE nombre = %s", (nombre_original,))
            if not cursor.fetchone():
                cursor.close()
                messagebox.showwarning("Atención", f"No se encontró el contacto '{nombre_original}'")
                return
            cursor.close()

            # Construir la consulta de actualización
            updates = []
            params = []
            
            if nuevo_nombre:
                updates.append("nombre = %s")
                params.append(nuevo_nombre)
            if nuevo_telefono:
                updates.append("telefono = %s")
                params.append(nuevo_telefono)
            if nuevo_mail:
                updates.append("mail = %s")
                params.append(nuevo_mail)
            if nueva_direccion:
                updates.append("direccion = %s")
                params.append(nueva_direccion)
            
            if updates:
                cursor = get_cursor()
                query = "UPDATE contactos SET " + ", ".join(updates) + " WHERE nombre = %s"
                params.append(nombre_original)
                cursor.execute(query, tuple(params))
                conexion.commit()
                cursor.close()
                
                messagebox.showinfo("Éxito", f"Contacto '{nombre_original}' actualizado correctamente")
                ventana2.destroy()
            else:
                messagebox.showwarning("Atención", "No ingresaste ningún dato para modificar")
                
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"No se pudo editar el contacto: {error}")

    tk.Button(frame2, text="Confirmar edición", command=confirmar_editar).pack(pady=10)

# Función para eliminar contacto
def eliminar_contacto():
    ventana3 = tk.Toplevel()
    ventana3.title("Eliminar contacto")
    ventana3.geometry("300x200")
    ventana3.minsize(300, 200)
    ventana3.resizable(0,0)

    frame3 = tk.Frame(ventana3)
    frame3.configure(width=500, height=300, bg="grey", bd=6)
    frame3.pack()

    tk.Label(frame3, text="Ingrese el nombre del contacto a eliminar", bg="grey").pack()
    eliminar_nombre = tk.Entry(frame3, width=30)
    eliminar_nombre.pack()

    def confirmar_eliminar():
        nombre = eliminar_nombre.get().strip()
        if nombre:
            try:
                cursor = get_cursor()
                cursor.execute("DELETE FROM contactos WHERE nombre = %s", (nombre,))
                conexion.commit()
                
                if cursor.rowcount > 0:
                    messagebox.showinfo("Exito", f"Contacto '{nombre}' eliminado")
                    ventana3.destroy()
                else:
                    messagebox.showwarning("Atencion", f"No se encontro el contacto '{nombre}'")
                cursor.close()
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"No se pudo eliminar el contacto: {error}")
        else:
            messagebox.showwarning("Atención", "Debes ingresar el nombre del contacto a eliminar")

    tk.Button(frame3, text="Eliminar", command=confirmar_eliminar).pack(pady=10)

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Agenda")
ventana.geometry("500x400")
ventana.minsize(500, 400)
ventana.resizable(0,0)

# Frame principal
frame1 = tk.Frame(ventana, width=500, height=300, bg="grey", bd=6)
frame1.pack()

# Campos del formulario
tk.Label(frame1, text="Agendar nuevo contacto", bg="grey").pack()

tk.Label(frame1, text="Ingrese el nombre", bg="grey").pack()
entrada_nombre = tk.Entry(frame1, width=30)
entrada_nombre.pack()

tk.Label(frame1, text="Ingrese el telefono", bg="grey").pack()
entrada_telefono = tk.Entry(frame1, width=30)
entrada_telefono.pack()

tk.Label(frame1, text="Ingrese el mail", bg="grey").pack()
entrada_mail = tk.Entry(frame1, width=30)
entrada_mail.pack()

tk.Label(frame1, text="Ingrese la direccion", bg="grey").pack()
entrada_direccion = tk.Entry(frame1, width=30)
entrada_direccion.pack()

# Botones
tk.Label(frame1, text=" ", bg="grey").pack()
tk.Button(frame1, text="Agendar contacto", command=agendar_contacto).pack()

tk.Label(frame1, text=" ", bg="grey").pack()
tk.Button(frame1, text="Editar contacto", command=editar_contacto).pack()

tk.Label(frame1, text=" ", bg="grey").pack()
tk.Button(frame1, text="Eliminar contacto", command=eliminar_contacto).pack()

# Conexión a la base de datos
try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="AGENDA"
    )
    
    # Crear tabla si no existe
    cursor = get_cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contactos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(20),
        telefono VARCHAR(20),
        mail VARCHAR(30),
        direccion VARCHAR(30)
    )
    """)
    cursor.close()
    
except mysql.connector.Error as err:
    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
    ventana.destroy()

# Cerrar conexión al salir
def on_closing():
    if 'conexion' in globals() and conexion.is_connected():
        conexion.close()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", on_closing)
ventana.mainloop()