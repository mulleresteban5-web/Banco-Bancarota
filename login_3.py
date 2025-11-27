import tkinter as tk
from tkinter import messagebox, ttk
import json as js
import re  # Agregar esta importación para usar expresiones regulares
import random  # Agregar esta importación para generar números de cuenta aleatorios

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
        # Cargar la imagen del logo usando tk.PhotoImage
        # Reemplaza "logo.png" con la ruta a tu imagen si es diferente
        try:
            self.logo_image = tk.PhotoImage(file="logoBBR(3).png")
        except tk.TclError:
            # Si no se encuentra la imagen, mostrar un mensaje de error y continuar sin ella
            print("Error: No se pudo cargar la imagen 'logoBBR(3).png'. Asegúrate de que el archivo exista.")
            self.logo_image = None
        
        # Etiqueta para mostrar la imagen del logo (arriba de todo)
        if self.logo_image:
            logo_label = tk.Label(self, image=self.logo_image, bg="#b5ddd8")
            logo_label.pack(pady=(20, 10))  # Espaciado superior e inferior

        # Etiqueta y campo para nombre
        texto_nombre = tk.Label(self, text='Nombre: ', font=('Arial', 30, 'bold'), 
                               bg='#b5ddd8', fg='white')
        texto_nombre.pack(padx=25, pady=25)
        
        self.cuadro_texto_entrada_nombre = tk.Entry(self, width=13, font=('Arial', 20))
        self.cuadro_texto_entrada_nombre.pack(padx=25, pady=25)
        
        # Etiqueta y campo para contraseña
        texto_contraseña = tk.Label(self, text='Contraseña: ', font=('Arial', 30, 'bold'), 
                                   bg='#b5ddd8', fg='white')
        texto_contraseña.pack(padx=25, pady=25)
        
        self.cuadro_texto_entrada_contraseña = tk.Entry(self, width=13, font=('Arial', 20), show='*')
        self.cuadro_texto_entrada_contraseña.pack(padx=25, pady=25)
        
        # Frame para botones
        frame_botones = tk.Frame(self, bg="#b5ddd8")
        frame_botones.pack(pady=20)
        
        # Botón para ingresar
        boton_ingresar = tk.Button(frame_botones, text='Ingresar', command=self.verificar_login, 
                                  font=('Arial', 20, 'bold'))
        boton_ingresar.pack(side=tk.LEFT, padx=10)
        
        # Botón para registrarse
        boton_registrarse = tk.Button(frame_botones, text='Registrarse', command=self.registrar_usuario, 
                                     font=('Arial', 20, 'bold'))
        boton_registrarse.pack(side=tk.LEFT, padx=10)
        
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
        
        # Validar que el nombre no contenga espacios ni caracteres especiales (solo letras y números)
        if not re.match(r'^[a-zA-Z0-9]+$', nombre):
            messagebox.showerror("Error", "El nombre solo puede contener letras y números, sin espacios ni caracteres especiales")
            return
        
        # Validar que la contraseña no contenga espacios ni caracteres especiales (solo letras y números)
        if not re.match(r'^[a-zA-Z0-9]+$', contraseña):
            messagebox.showerror("Error", "La contraseña solo puede contener letras y números, sin espacios ni caracteres especiales")
            return
    
        # Verificar si es gerente
        if nombre == "Gerente":
            if contraseña == "gerente123":
                self.controller.usuario_actual = nombre
                self.controller.tipo_usuario = "gerente"
            
                # Mostrar mensaje de éxito
                cadena_texto = f'Bienvenido Gerente: {nombre}'
                self.texto.config(text=cadena_texto)
            
                tipo = "gerente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json
                self.guardar_usuario(nombre, contraseña, tipo)

                # Limpiar el mensaje de bienvenido antes de cambiar al notebook
                self.texto.config(text="")  # <-- LÍNEA NUEVA: Borra el mensaje
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Gerente
                messagebox.showerror("Error", "Contraseña incorrecta para Gerente")
                self.texto.config(text="")
                return
        # Verificar si es cliente específico: Ana
        elif nombre == "Ana":
            if contraseña == "ana123":
                self.controller.usuario_actual = nombre
                self.controller.tipo_usuario = "cliente"
            
                # Mostrar mensaje de éxito
                cadena_texto = f'Bienvenido Cliente: {nombre}'
                self.texto.config(text=cadena_texto)
            
                tipo = "cliente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json
                self.guardar_usuario(nombre, contraseña, tipo)
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Ana
                messagebox.showerror("Error", "Contraseña incorrecta para Ana")
                self.texto.config(text="")
                return
        # Verificar si es cliente específico: Pedro
        elif nombre == "Pedro":
            if contraseña == "pedro123":
                self.controller.usuario_actual = nombre
                self.controller.tipo_usuario = "cliente"
            
                # Mostrar mensaje de éxito
                cadena_texto = f'Bienvenido Cliente: {nombre}'
                self.texto.config(text=cadena_texto)
            
                tipo = "cliente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json
                self.guardar_usuario(nombre, contraseña, tipo)
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Pedro
                messagebox.showerror("Error", "Contraseña incorrecta para Pedro")
                self.texto.config(text="")
                return
        # Verificar si es cliente específico: Juan
        elif nombre == "Juan":
            if contraseña == "juan123":
                self.controller.usuario_actual = nombre
                self.controller.tipo_usuario = "cliente"
            
                # Mostrar mensaje de éxito
                cadena_texto = f'Bienvenido Cliente: {nombre}'
                self.texto.config(text=cadena_texto)
            
                tipo = "cliente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json
                self.guardar_usuario(nombre, contraseña, tipo)
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Juan
                messagebox.showerror("Error", "Contraseña incorrecta para Juan")
                self.texto.config(text="")
                return
        else:
            # Verificar si es un usuario registrado en el JSON
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos = js.load(archivo)
                    if not isinstance(datos, list):
                        datos = []
            except (FileNotFoundError, js.JSONDecodeError):
                datos = []
            
            usuario_encontrado = False
            for usuario in datos:
                if usuario['nombre'] == nombre and usuario['contraseña'] == contraseña:
                    usuario_encontrado = True
                    break
            
            if usuario_encontrado:
                self.controller.usuario_actual = nombre
                self.controller.tipo_usuario = "cliente"
            
                # Mostrar mensaje de éxito
                cadena_texto = f'Bienvenido Cliente: {nombre}'
                self.texto.config(text=cadena_texto)
            
                tipo = "cliente"
        
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json (aunque ya existe, se reescribe)
                self.guardar_usuario(nombre, contraseña, tipo)
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Usuario no registrado
                messagebox.showerror("Error", "Usuario no registrado. Por favor regístrese primero.")
                self.texto.config(text="")
                return
    def registrar_usuario(self):
        """Función para registrar un nuevo usuario"""
        # Crear ventana emergente para registro
        ventana_registro = tk.Toplevel(self)
        ventana_registro.title("Registro de Usuario")
        ventana_registro.geometry("400x300")
        ventana_registro.configure(bg="#b5ddd8")
        
        # Etiqueta y campo para nombre
        ttk.Label(ventana_registro, text="Nombre de usuario:", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_nombre = ttk.Entry(ventana_registro, width=20, font=('Arial', 12))
        entrada_nombre.pack(pady=5)
        
        # Etiqueta y campo para contraseña
        ttk.Label(ventana_registro, text="Contraseña:", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_contraseña = ttk.Entry(ventana_registro, width=20, font=('Arial', 12), show='*')
        entrada_contraseña.pack(pady=5)
        
        def confirmar_registro():
            nombre = entrada_nombre.get().strip()
            contraseña = entrada_contraseña.get().strip()
            
            # Validar campos
            if not nombre or not contraseña:
                messagebox.showerror("Error", "Por favor ingresa nombre y contraseña")
                return

            # Validar formato
            if not re.match(r'^[a-zA-Z0-9]+$', nombre):
                messagebox.showerror("Error", "El nombre solo puede contener letras y números, sin espacios ni caracteres especiales")
                return
            if not re.match(r'^[a-zA-Z0-9]+$', contraseña):
                messagebox.showerror("Error", "La contraseña solo puede contener letras y números, sin espacios ni caracteres especiales")
                return
            
            # Verificar unicidad
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos = js.load(archivo)
                    if not isinstance(datos, list):
                        datos = []
            except (FileNotFoundError, js.JSONDecodeError):
                datos = []
            
            for usuario in datos:
                if usuario['nombre'] == nombre:
                    messagebox.showerror("Error", "El nombre de usuario ya existe. Elige otro.")
                    return
            # Verificar contra usuarios predefinidos
            usuarios_predefinidos = ["Gerente", "Ana", "Pedro", "Juan"]
            if nombre in usuarios_predefinidos:
                messagebox.showerror("Error", "El nombre de usuario ya existe. Elige otro.")
                return
            
            # Guardar nuevo usuario
            diccionario_a_guardar = {'nombre': nombre, 'contraseña': contraseña, 'tipo': 'cliente'}
            datos.append(diccionario_a_guardar)
            with open("usuarios_cuentas.json", 'w') as archivo:
                js.dump(datos, archivo)
            
            # Crear entrada vacía en cuentas.json para el nuevo usuario
            try:
                with open("cuentas.json", 'r') as archivo:
                    cuentas_globales = js.load(archivo)
                    if not isinstance(cuentas_globales, dict):
                        cuentas_globales = {}
            except (FileNotFoundError, js.JSONDecodeError):
                cuentas_globales = {}
            
            cuentas_globales[nombre] = []  # Lista vacía de cuentas
            with open("cuentas.json", 'w') as archivo:
                js.dump(cuentas_globales, archivo)

            messagebox.showinfo("Éxito", f"Usuario {nombre} registrado exitosamente. Ahora puedes iniciar sesión.")
            ventana_registro.destroy()
        
        # Botones
        ttk.Button(ventana_registro, text="Registrar", command=confirmar_registro).pack(pady=20)
        ttk.Button(ventana_registro, text="Cancelar", command=ventana_registro.destroy).pack(pady=5)
        
        # Centrar ventana emergente
        ventana_registro.transient(self)
        ventana_registro.grab_set()
        self.wait_window(ventana_registro)

    def guardar_usuario(self, nombre, contraseña, tipo):
        """Función auxiliar para guardar usuario en el archivo JSON"""
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos = js.load(archivo)
                # Verificar que sea una lista; si no, reinicializar
                if not isinstance(datos, list):
                    datos = []
        except (FileNotFoundError, js.JSONDecodeError):
            # Si no existe o está corrupto, iniciar con lista vacía
            datos = []

        diccionario_a_guardar = {'nombre': nombre, 'contraseña': contraseña, 'tipo': tipo}
        datos.append(diccionario_a_guardar)

        with open("usuarios_cuentas.json", 'w') as archivo:
            js.dump(datos, archivo)

        # Limpiar campos
        self.cuadro_texto_entrada_nombre.delete(0, tk.END)
        self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
    
        # Mostrar mensaje y cambiar al notebook
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
    
        # Treeview para mostrar cuentas (hacerlo atributo de clase para poder acceder desde otros métodos)
        self.tree2 = ttk.Treeview(pestana1, columns=("cuenta", "N°cuenta", "saldo"))
        self.tree2.heading("cuenta", text="Tipo de Cuenta")
        self.tree2.heading("N°cuenta", text="N° de cuenta")
        self.tree2.heading("saldo", text="Saldo disponible")

        # Ajustar anchos de columnas
        self.tree2.column("#0", width=50)
        self.tree2.column("cuenta", width=100)
        self.tree2.column("N°cuenta", width=80)
        self.tree2.column("saldo", width=100)

        # Diccionario de cuentas iniciales por usuario (agrega más usuarios aquí)
        cuentas_por_defecto = {
            "Juan": [
                {"id": "1", "tipo": "Cuenta Vista", "numero": "111111111", "saldo": "$10.000"},
                {"id": "2", "tipo": "Cuenta de Ahorros", "numero": "111111111", "saldo": "$50.000"}
            ],
            "Ana": [
                {"id": "1", "tipo": "Cuenta Corriente", "numero": "222222222", "saldo": "$25.000"},
                {"id": "2", "tipo": "Cuenta Rut", "numero": "222222222", "saldo": "$5.000"},
                {"id": "3", "tipo": "Cuenta de Ahorros", "numero": "222222222", "saldo": "$100.000"}
            ],
            "Pedro": [
                {"id": "1", "tipo": "Cuenta Vista", "numero": "333333333", "saldo": "$15.000"},
                {"id": "2", "tipo": "Cuenta Corriente", "numero": "333333333", "saldo": "$75.000"},
                {"id": "3", "tipo": "Cuenta Rut", "numero": "333333333", "saldo": "$20.000"},
                {"id": "4", "tipo": "Cuenta de Ahorros", "numero": "333333333", "saldo": "$200.000"}
            ]
        }

        # Cargar datos iniciales desde cuentas.json o usar cuentas por defecto
        usuario = self.controller.usuario_actual  # Nombre del usuario logueado
        try:
            with open("cuentas.json", 'r') as archivo:
                datos_globales = js.load(archivo)
                # Verificar que sea un diccionario válido
                if not isinstance(datos_globales, dict):
                    raise ValueError("Datos inválidos en cuentas.json")
                # Obtener cuentas del usuario actual
                self.cuentas_data = datos_globales.get(usuario, cuentas_por_defecto.get(usuario, []))
        except (FileNotFoundError, js.JSONDecodeError, ValueError):
            # Si no existe o está corrupto, usar cuentas por defecto o lista genérica
            self.cuentas_data = cuentas_por_defecto.get(usuario, [
                {"id": "1", "tipo": "Cuenta Vista", "numero": "000000001", "saldo": "$0.000"},
                {"id": "2", "tipo": "Cuenta de Ahorros", "numero": "000000002", "saldo": "$0.000"}
            ])

        # Llenar el treeview con los datos
        self.actualizar_treeview()

        self.tree2.pack(pady=20, fill="both", expand=True)
    
        # Pestaña 2 - Operaciones
        pestana2 = ttk.Frame(self.notebook)
        self.notebook.add(pestana2, text="Operaciones")
    
        ttk.Label(pestana2, text="Operaciones Bancarias", font=('Arial', 14, 'bold')).pack(pady=20)
    
        # Frame para contener el botón y la lista con checkbuttons
        frame_eliminar = ttk.Frame(pestana2)
        frame_eliminar.pack(pady=10)

        # Botón para eliminar cuenta
        boton_eliminar = ttk.Button(frame_eliminar, text="Eliminar Cuenta", command=self.mostrar_lista_cuentas)
        boton_eliminar.pack(pady=5)

        # Frame para contener los checkbuttons (inicialmente oculto)
        self.frame_cuentas = ttk.Frame(pestana2)
        self.frame_cuentas.pack(pady=5, fill=tk.X, padx=20)
        self.frame_cuentas.pack_forget()  # Ocultar inicialmente

        # Variables para los checkbuttons
        self.variables_cuentas = []

        # Botón para confirmar eliminación
        self.boton_confirmar = ttk.Button(pestana2, text="Confirmar Eliminación", command=self.eliminar_cuentas_seleccionadas)
        self.boton_confirmar.pack(pady=5)
        self.boton_confirmar.pack_forget()  # Ocultar inicialmente
    
        ttk.Button(pestana2, text="Crear cuenta", command=self.crear_cuenta).pack(pady=10)
        ttk.Button(pestana2, text="Transferencias", command=self.realizar_transferencia).pack(pady=10)

        # Pestaña 3 - Ayuda
        pestana3 = ttk.Frame(self.notebook)
        self.notebook.add(pestana3, text="Ayuda")
    
        ttk.Label(pestana3, text="Centro de Ayuda - Modo Cliente", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(pestana3, text=f"Bienvenido Cliente: {self.controller.usuario_actual}").pack(pady=10)
        ttk.Button(pestana3, text="Soporte al Cliente").pack(pady=10)
        ttk.Button(pestana3, text="Preguntas Frecuentes").pack(pady=10)
    
    def crear_cuenta(self):
        """Método para crear una nueva cuenta bancaria"""
        # Crear una ventana emergente para ingresar datos de la nueva cuenta
        ventana_crear = tk.Toplevel(self)
        ventana_crear.title("Crear Nueva Cuenta")
        ventana_crear.geometry("400x300")
        ventana_crear.configure(bg="#b5ddd8")
    
        # Etiqueta y OptionMenu para seleccionar tipo de cuenta
        ttk.Label(ventana_crear, text="Seleccione el tipo de cuenta:", font=('Arial', 12, 'bold')).pack(pady=10)
        tipos_cuenta = ["Cuenta Vista", "Cuenta de Ahorros", "Cuenta Corriente", "Cuenta Rut"]
        tipo_var = tk.StringVar(value=tipos_cuenta[0])
        menu_tipo = tk.OptionMenu(ventana_crear, tipo_var, *tipos_cuenta)
        menu_tipo.pack(pady=10)
    
        # Función para confirmar creación
        def confirmar_creacion():
            tipo_seleccionado = tipo_var.get()

            # Verificar si ya existe una cuenta del mismo tipo
            for cuenta in self.cuentas_data:
                if cuenta["tipo"] == tipo_seleccionado:
                    messagebox.showerror("Error", f"Ya tienes una cuenta de tipo '{tipo_seleccionado}'. No puedes crear otra del mismo tipo.")
                    return            
        
            # Generar un número de cuenta único (9 dígitos aleatorios)
            numero_cuenta = str(random.randint(100000000, 999999999))
        
            # Verificar que el número no exista ya para este usuario
            for cuenta in self.cuentas_data:
                if cuenta["numero"] == numero_cuenta:
                    numero_cuenta = str(random.randint(100000000, 999999999))  # Generar otro si choca
        
            # Crear nueva cuenta con saldo 0
            nueva_cuenta = {
                "id": str(len(self.cuentas_data) + 1),  # ID incremental
                "tipo": tipo_seleccionado,
                "numero": numero_cuenta,
                "saldo": "$0"
            }
        
            # Agregar a la lista de cuentas
            self.cuentas_data.append(nueva_cuenta)
        
            # Actualizar el treeview
            self.actualizar_treeview()
        
            # Guardar cambios en cuentas.json
            self.guardar_cuentas()
        
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Cuenta {tipo_seleccionado} creada exitosamente.\nNúmero de cuenta: {numero_cuenta}")
        
            # Cerrar ventana
            ventana_crear.destroy()
    
        # Botón para confirmar
        ttk.Button(ventana_crear, text="Crear Cuenta", command=confirmar_creacion).pack(pady=20)
    
        # Botón para cancelar
        ttk.Button(ventana_crear, text="Cancelar", command=ventana_crear.destroy).pack(pady=10)
    
        # Centrar la ventana emergente
        ventana_crear.transient(self)
        ventana_crear.grab_set()
        self.wait_window(ventana_crear)

    def actualizar_treeview(self):
        """Actualiza el treeview con los datos actuales de cuentas"""
        # Limpiar treeview
        for item in self.tree2.get_children():
            self.tree2.delete(item)
        
        # Insertar datos actualizados
        for cuenta in self.cuentas_data:
            self.tree2.insert("", "end", text=cuenta["id"], 
                            values=(cuenta["tipo"], cuenta["numero"], cuenta["saldo"]))

    def mostrar_lista_cuentas(self):
        """Muestra u oculta la lista de cuentas con checkbuttons"""
        if self.frame_cuentas.winfo_ismapped():
            # Si está visible, ocultarla
            self.frame_cuentas.pack_forget()
            self.boton_confirmar.pack_forget()
            self.limpiar_checkbuttons()
        else:
            # Si está oculta, mostrarla y crear checkbuttons
            self.crear_checkbuttons_cuentas()
            self.frame_cuentas.pack(pady=5, fill=tk.X, padx=20)
            self.boton_confirmar.pack(pady=5)

    def crear_checkbuttons_cuentas(self):
        """Crea los checkbuttons para cada cuenta basándose en el treeview"""
        # Limpiar frame existente
        for widget in self.frame_cuentas.winfo_children():
            widget.destroy()
    
        # Limpiar variables
        self.variables_cuentas = []
    
        # Título
        ttk.Label(self.frame_cuentas, text="Seleccione las cuentas a eliminar:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))
    
        # Crear checkbutton para cada cuenta del treeview
        for cuenta in self.cuentas_data:
            var = tk.BooleanVar()
            self.variables_cuentas.append(var)
        
            texto_cuenta = f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}"
        
            check = ttk.Checkbutton(self.frame_cuentas, 
                               text=texto_cuenta,
                               variable=var)
            check.pack(anchor=tk.W, pady=2)

    def eliminar_cuentas_seleccionadas(self):
        """Elimina las cuentas seleccionadas tanto de la lista como del treeview"""
        indices_a_eliminar = []
        cuentas_seleccionadas = []
    
        # Obtener índices de las cuentas seleccionadas
        for i, var in enumerate(self.variables_cuentas):
            if var.get():
                indices_a_eliminar.append(i)
                cuentas_seleccionadas.append(self.cuentas_data[i])
    
        if not cuentas_seleccionadas:
            messagebox.showwarning("Advertencia", "Por favor seleccione al menos una cuenta para eliminar")
            return
    
        # Mostrar confirmación
        mensaje = "¿Está seguro que desea eliminar las siguientes cuentas?\n\n"
        for cuenta in cuentas_seleccionadas:
            mensaje += f"- {cuenta['tipo']} ({cuenta['numero']})\n"
    
        if messagebox.askyesno("Confirmar Eliminación", mensaje):
            # Eliminar las cuentas seleccionadas (en orden inverso para evitar problemas de índices)
            for index in sorted(indices_a_eliminar, reverse=True):
                self.cuentas_data.pop(index)
            
            # Actualizar el treeview
            self.actualizar_treeview()
            
            # Actualizar los checkbuttons
            self.crear_checkbuttons_cuentas()
            
            messagebox.showinfo("Éxito", f"Se eliminaron {len(cuentas_seleccionadas)} cuenta(s) correctamente")
        
        # Guardar cambios en cuentas.json
        self.guardar_cuentas()

    def limpiar_checkbuttons(self):
        """Limpia los checkbuttons y variables"""
        for var in self.variables_cuentas:
            var.set(False)

    def realizar_transferencia(self):
        """Función para realizar una transferencia entre cuentas de usuarios registrados"""
        # Crear ventana emergente para transferencia
        ventana_transferencia = tk.Toplevel(self)
        ventana_transferencia.title("Realizar Transferencia")
        ventana_transferencia.geometry("500x400")
        ventana_transferencia.configure(bg="#b5ddd8")

        # Etiqueta y OptionMenu para seleccionar cuenta de origen
        ttk.Label(ventana_transferencia, text="Seleccione la cuenta de origen:", font=('Arial', 12, 'bold')).pack(pady=10)
        cuentas_origen = [f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" for cuenta in self.cuentas_data]
        if not cuentas_origen:
            messagebox.showerror("Error", "No tienes cuentas disponibles para transferir.")
            ventana_transferencia.destroy()
            return
        origen_var = tk.StringVar(value=cuentas_origen[0])
        menu_origen = tk.OptionMenu(ventana_transferencia, origen_var, *cuentas_origen)
        menu_origen.pack(pady=10)

        # Etiqueta y campo para nombre del destinatario
        ttk.Label(ventana_transferencia, text="Nombre del destinatario:", font=('Arial', 12, 'bold')).pack(pady=10)
        entrada_destinatario = ttk.Entry(ventana_transferencia, width=20, font=('Arial', 12))
        entrada_destinatario.pack(pady=5)

        # Etiqueta y campo para monto
        ttk.Label(ventana_transferencia, text="Monto a transferir (ej: 1000):", font=('Arial', 12, 'bold')).pack(pady=10)
        entrada_monto = ttk.Entry(ventana_transferencia, width=20, font=('Arial', 12))
        entrada_monto.pack(pady=5)

        # Variable para cuenta de destino (se llenará después de validar destinatario)
        destino_var = tk.StringVar()
        menu_destino = tk.OptionMenu(ventana_transferencia, destino_var, "")
        menu_destino.pack(pady=10)
        menu_destino.pack_forget()  # Ocultar inicialmente

        def validar_destinatario():
            destinatario = entrada_destinatario.get().strip()
            if not destinatario:
                messagebox.showerror("Error", "Ingresa el nombre del destinatario.")
                return

            # Verificar si el destinatario está registrado (en usuarios_cuentas.json)
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos_usuarios = js.load(archivo)
                    if not isinstance(datos_usuarios, list):
                        datos_usuarios = []
            except (FileNotFoundError, js.JSONDecodeError):
                datos_usuarios = []

            usuario_encontrado = any(u['nombre'] == destinatario for u in datos_usuarios)
            if not usuario_encontrado:
                messagebox.showerror("Error", "Usuario no registrado.")
                return

            # Cargar cuentas del destinatario
            try:
                with open("cuentas.json", 'r') as archivo:
                    datos_cuentas = js.load(archivo)
                    if not isinstance(datos_cuentas, dict):
                        datos_cuentas = {}
            except (FileNotFoundError, js.JSONDecodeError):
                datos_cuentas = {}

            cuentas_destino = datos_cuentas.get(destinatario, [])
            if not cuentas_destino:
                messagebox.showerror("Error", "El destinatario no tiene cuentas disponibles.")
                return

            # Mostrar OptionMenu para cuenta de destino
            opciones_destino = [f"{cuenta['tipo']} - {cuenta['numero']}" for cuenta in cuentas_destino]
            menu_destino['menu'].delete(0, 'end')
            for opcion in opciones_destino:
                menu_destino['menu'].add_command(label=opcion, command=tk._setit(destino_var, opcion))
            destino_var.set(opciones_destino[0])
            menu_destino.pack(pady=10)

        # Botón para validar destinatario
        ttk.Button(ventana_transferencia, text="Validar Destinatario", command=validar_destinatario).pack(pady=10)

        def confirmar_transferencia():
            # Obtener datos
            origen_seleccionado = origen_var.get()
            destinatario = entrada_destinatario.get().strip()
            monto_str = entrada_monto.get().strip()
            destino_seleccionado = destino_var.get()

            # Validar monto
            try:
                monto = float(monto_str)
                if monto <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingresa un monto válido mayor a 0.")
                return

            # Encontrar cuenta de origen
            cuenta_origen = None
            for cuenta in self.cuentas_data:
                if f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" == origen_seleccionado:
                    cuenta_origen = cuenta
                    break
            if not cuenta_origen:
                messagebox.showerror("Error", "Cuenta de origen no encontrada.")
                return

            # Verificar saldo suficiente
            saldo_origen = float(cuenta_origen['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            if monto > saldo_origen:
                messagebox.showerror("Error", "Saldo insuficiente en la cuenta de origen.")
                return

            # Cargar cuentas del destinatario
            try:
                with open("cuentas.json", 'r') as archivo:
                    datos_cuentas = js.load(archivo)
                    if not isinstance(datos_cuentas, dict):
                        datos_cuentas = {}
            except (FileNotFoundError, js.JSONDecodeError):
                datos_cuentas = {}

            cuentas_destino = datos_cuentas.get(destinatario, [])
            cuenta_destino = None
            for cuenta in cuentas_destino:
                if f"{cuenta['tipo']} - {cuenta['numero']}" == destino_seleccionado:
                    cuenta_destino = cuenta
                    break
            if not cuenta_destino:
                messagebox.showerror("Error", "Cuenta de destino no encontrada.")
                return

            # Realizar transferencia
            nuevo_saldo_origen = saldo_origen - monto
            saldo_destino = float(cuenta_destino['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            nuevo_saldo_destino = saldo_destino + monto

            # Actualizar saldos
            cuenta_origen['saldo'] = f"${nuevo_saldo_origen:,.0f}"
            cuenta_destino['saldo'] = f"${nuevo_saldo_destino:,.0f}"

            # Guardar cambios
            datos_cuentas[self.controller.usuario_actual] = self.cuentas_data
            datos_cuentas[destinatario] = cuentas_destino
            with open("cuentas.json", 'w') as archivo:
                js.dump(datos_cuentas, archivo)

            # Actualizar treeview
            self.actualizar_treeview()

            messagebox.showinfo("Éxito", f"Transferencia de ${monto:,.0f} realizada exitosamente a {destinatario}.")
            ventana_transferencia.destroy()

        # Botón para confirmar
        ttk.Button(ventana_transferencia, text="Confirmar Transferencia", command=confirmar_transferencia).pack(pady=20)

        # Botón para cancelar
        ttk.Button(ventana_transferencia, text="Cancelar", command=ventana_transferencia.destroy).pack(pady=5)

        # Centrar ventana emergente
        ventana_transferencia.transient(self)
        ventana_transferencia.grab_set()
        self.wait_window(ventana_transferencia)

    def guardar_cuentas(self):
        """Guarda la lista de cuentas en cuentas.json para el usuario actual"""
        usuario = self.controller.usuario_actual
        if not usuario:
            messagebox.showerror("Error", "Usuario no identificado. No se pueden guardar cambios.")
            return
        try:
            with open("cuentas.json", 'r') as archivo:
                datos_globales = js.load(archivo)
            if not isinstance(datos_globales, dict):
                datos_globales = {}
        except (FileNotFoundError, js.JSONDecodeError):
            datos_globales = {}
    
        # Actualizar las cuentas del usuario actual
        datos_globales[usuario] = self.cuentas_data
    
        try:
            with open("cuentas.json", 'w') as archivo:
                js.dump(datos_globales, archivo)
            # Debug: Mostrar confirmación (puedes quitar esto después de probar)
            print(f"Cuentas guardadas para {usuario}: {self.cuentas_data}")
            messagebox.showinfo("Guardado", f"Cambios guardados para {usuario}.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {str(e)}")        
    
    def cerrar_sesion(self):
        """Volver a la pantalla de login"""
        self.controller.usuario_actual = None
        self.controller.tipo_usuario = None
        # Destruir el NotebookFrame para forzar recreación en el próximo login
        if "NotebookFrame" in self.controller.frames:
            self.controller.frames["NotebookFrame"].destroy()
            del self.controller.frames["NotebookFrame"]
        self.controller.mostrar_frame("LoginFrame")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()