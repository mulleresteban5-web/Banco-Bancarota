import tkinter as tk
from tkinter import messagebox, ttk
import json as js

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sistema de Login')
        self.geometry("850x600")
        self.configure(bg="#b5ddd8")
        
        # Contenedor principal para los frames
        self.contenedor = tk.Frame(self, bg="#b5ddd8")
        self.contenedor.pack(fill="both", expand=True)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        
        # Diccionario para almacenar los frames
        self.frames = {}
        
        # Variables para almacenar información del usuario
        self.usuario_actual = None
        self.tipo_usuario = None
        
        # Crear solo el frame de login inicialmente
        self.frames["LoginFrame"] = LoginFrame(parent=self.contenedor, controller=self)
        self.frames["LoginFrame"].grid(row=0, column=0, sticky="nsew")
        
        # Mostrar el frame de login inicialmente
        self.mostrar_frame("LoginFrame")
        
        # Centrar la ventana
        self.centrar_ventana()
    
    def mostrar_frame(self, nombre_pagina):
        """Muestra un frame específico"""
        # Si es el notebook y no está creado, crearlo según el tipo de usuario
        if nombre_pagina == "NotebookFrame" and nombre_pagina not in self.frames:
            self.frames["NotebookFrame"] = NotebookFrame(parent=self.contenedor, controller=self)
            self.frames["NotebookFrame"].grid(row=0, column=0, sticky="nsew")
        
        frame = self.frames[nombre_pagina]
        frame.tkraise()
        
        # Ajustar tamaño cuando se muestra el notebook
        if nombre_pagina == "NotebookFrame":
            self.geometry("1000x700")
            self.centrar_ventana()
        else:
            self.geometry("850x600")
            self.centrar_ventana()
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        ancho = self.winfo_width()
        alto = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f'{ancho}x{alto}+{x}+{y}')


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#b5ddd8")
        
        # Widgets del login
        self.crear_widgets()
    
    def crear_widgets(self):
        # Etiqueta y campo para nombre
        texto_nombre = tk.Label(self, text='Nombre: ', font=('Arial', 35, 'bold'), 
                               bg='#b5ddd8', fg='white')
        texto_nombre.pack(padx=25, pady=25)
        
        self.cuadro_texto_entrada_nombre = tk.Entry(self, width=15, font=('Arial', 35))
        self.cuadro_texto_entrada_nombre.pack(padx=25, pady=25)
        
        # Etiqueta y campo para contraseña
        texto_contraseña = tk.Label(self, text='Contraseña: ', font=('Arial', 35, 'bold'), 
                                   bg='#b5ddd8', fg='white')
        texto_contraseña.pack(padx=25, pady=25)
        
        self.cuadro_texto_entrada_contraseña = tk.Entry(self, width=15, font=('Arial', 35), show='*')
        self.cuadro_texto_entrada_contraseña.pack(padx=25, pady=25)
        
        # Botón para ingresar
        boton_ingresar = tk.Button(self, text='Ingresar', command=self.verificar_login, 
                                  font=('Arial', 20, 'bold'))
        boton_ingresar.pack(pady=20)
        
        # Etiqueta para mostrar mensajes
        self.texto = tk.Label(self, text='', font=('Comic Sans MS', 20), 
                             bg='#b5ddd8', fg='white')
        self.texto.pack()
        
        # Permitir login con Enter
        self.controller.bind('<Return>', lambda event: self.verificar_login())
    
    def verificar_login(self):
        """Función para verificar el login y manejar los datos"""
        nombre = self.cuadro_texto_entrada_nombre.get().strip()
        contraseña = self.cuadro_texto_entrada_contraseña.get().strip()

        # Validar que se ingresaron ambos campos
        if not nombre or not contraseña:
            messagebox.showerror("Error", "Por favor ingresa nombre y contraseña")
            return

        # Verificar si es gerente
        if nombre == "Gerente" and contraseña == "gerente123":
            self.controller.usuario_actual = nombre
            self.controller.tipo_usuario = "gerente"
            
            # Mostrar mensaje de éxito
            cadena_texto = f'Bienvenido Gerente: {nombre}'
            self.texto.config(text=cadena_texto)
            
            # Guardar datos del gerente
            try:
                with open("gerente.json", 'r') as archivo:
                    datos = js.load(archivo)
            except FileNotFoundError:
                datos = []
            
            diccionario_a_guardar = {'nombre': nombre, 'contraseña': contraseña, 'tipo': 'gerente'}
            datos.append(diccionario_a_guardar)

            with open("gerente.json", 'w') as archivo1:
                js.dump(datos, archivo1)

        else:
            # Es un cliente
            self.controller.usuario_actual = nombre
            self.controller.tipo_usuario = "cliente"
            
            # Mostrar mensaje de éxito
            cadena_texto = f'Bienvenido Cliente: {nombre}'
            self.texto.config(text=cadena_texto)
            
            # Guardar datos del cliente
            try:
                with open("cliente.json", 'r') as archivo:
                    datos2 = js.load(archivo)
            except FileNotFoundError:
                datos2 = []
            
            diccionario_a_guardar = {'nombre': nombre, 'contraseña': contraseña, 'tipo': 'cliente'}
            datos2.append(diccionario_a_guardar)

            with open("cliente.json", 'w') as archivo2:
                js.dump(datos2, archivo2)

        # Limpiar campos
        self.cuadro_texto_entrada_nombre.delete(0, tk.END)
        self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
        
        # Mostrar mensaje y cambiar al notebook
        messagebox.showinfo("Éxito", "Login exitoso")
        self.controller.mostrar_frame("NotebookFrame")


class NotebookFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Configurar el frame para expandirse
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Crear Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        
        # Crear frames para cada pestaña según el tipo de usuario
        if self.controller.tipo_usuario == "gerente":
            self.crear_interfaz_gerente()
        else:
            self.crear_interfaz_cliente()
        
        # Empacar el notebook
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Botón para cerrar sesión (volver al login)
        ttk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=10)
    
    def crear_interfaz_gerente(self):
        """Interfaz para el gerente con todas las funcionalidades"""
        # Pestaña 1 - Sucursales
        pestana1 = ttk.Frame(self.notebook)
        self.notebook.add(pestana1, text="Sucursales")
        
        ttk.Label(pestana1, text="Sucursales:", font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Variable para guardar la opción seleccionada
        self.opcion = tk.StringVar(value="Opción 1")
        
        # Crear el OptionMenu en la pestaña 1
        menu = tk.OptionMenu(pestana1, self.opcion, "Opción 1", "Opción 2", "Opción 3")
        menu.pack(pady=20)
        
        # Treeview para mostrar datos
        tree = ttk.Treeview(pestana1, columns=("nombre", "edad", "ciudad"))
        tree.heading("#0", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("edad", text="Edad")
        tree.heading("ciudad", text="Ciudad")

        # Ajustar anchos de columnas
        tree.column("#0", width=50)
        tree.column("nombre", width=100)
        tree.column("edad", width=80)
        tree.column("ciudad", width=100)

        # Insertar datos
        tree.insert("", "end", text="1", values=("Juan Pérez", "25", "Madrid"))
        tree.insert("", "end", text="2", values=("María García", "30", "Barcelona"))
        tree.insert("", "end", text="3", values=("Carlos López", "22", "Valencia"))

        tree.pack(pady=20, fill="both", expand=True)
        
        # Pestaña 2 - Clientes
        pestana2 = ttk.Frame(self.notebook)
        self.notebook.add(pestana2, text="Gestión de Clientes")
        
        ttk.Label(pestana2, text="Gestión Completa de Clientes", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(pestana2, text="Panel de administración para gerentes").pack(pady=10)
        
        # Pestaña 3 - Reportes
        pestana3 = ttk.Frame(self.notebook)
        self.notebook.add(pestana3, text="Reportes")
        
        ttk.Label(pestana3, text="Reportes del Sistema", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Button(pestana3, text="Generar Reporte Mensual").pack(pady=10)
        ttk.Button(pestana3, text="Estadísticas").pack(pady=10)
        
        # Pestaña 4 - Ayuda
        pestana4 = ttk.Frame(self.notebook)
        self.notebook.add(pestana4, text="Ayuda")
        
        ttk.Label(pestana4, text="Sistema de Ayuda - Modo Gerente", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(pestana4, text=f"Bienvenido: {self.controller.usuario_actual}").pack(pady=10)
    
    def crear_interfaz_cliente(self):
        """Interfaz para el cliente con funcionalidades limitadas"""
        # Pestaña 1 - Mi Cuenta
        pestana1 = ttk.Frame(self.notebook)
        self.notebook.add(pestana1, text="Mi Cuenta")
        
        ttk.Label(pestana1, text="Información Personal", font=('Arial', 14, 'bold')).pack(pady=20)
        
        ttk.Label(pestana1, text="Nombre:").pack(pady=5)
        nombre_entry = ttk.Entry(pestana1, width=30)
        nombre_entry.pack(pady=5)
        nombre_entry.insert(0, self.controller.usuario_actual)
        
        ttk.Label(pestana1, text="Email:").pack(pady=5)
        ttk.Entry(pestana1, width=30).pack(pady=5)
        
        ttk.Label(pestana1, text="Teléfono:").pack(pady=5)
        ttk.Entry(pestana1, width=30).pack(pady=5)
        
        # Pestaña 2 - Operaciones
        pestana2 = ttk.Frame(self.notebook)
        self.notebook.add(pestana2, text="Operaciones")
        
        ttk.Label(pestana2, text="Operaciones Bancarias", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Button(pestana2, text="Consultar Saldo").pack(pady=10)
        ttk.Button(pestana2, text="Transferencias").pack(pady=10)
        ttk.Button(pestana2, text="Pago de Servicios").pack(pady=10)
        
        # Pestaña 3 - Ayuda
        pestana3 = ttk.Frame(self.notebook)
        self.notebook.add(pestana3, text="Ayuda")
        
        ttk.Label(pestana3, text="Centro de Ayuda - Modo Cliente", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(pestana3, text=f"Bienvenido Cliente: {self.controller.usuario_actual}").pack(pady=10)
        ttk.Button(pestana3, text="Soporte al Cliente").pack(pady=10)
        ttk.Button(pestana3, text="Preguntas Frecuentes").pack(pady=10)
    
    def cerrar_sesion(self):
        """Volver a la pantalla de login"""
        self.controller.usuario_actual = None
        self.controller.tipo_usuario = None
        self.controller.mostrar_frame("LoginFrame")


# Ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()