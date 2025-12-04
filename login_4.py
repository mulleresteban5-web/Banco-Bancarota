import tkinter as tk
from tkinter import messagebox, ttk
import json as js
import re  # Agregar esta importación para usar expresiones regulares
import random  # Agregar esta importación para generar números de cuenta aleatorios
from datetime import datetime  # Para la hora del préstamo

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

    def centrar_ventana_emergente(self, ventana):
        """Centra una ventana emergente en la pantalla"""
        ventana.update_idletasks()  # Asegura que Tkinter calcule el tamaño real
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#b5ddd8")
        
        # Widgets del login
        self.crear_widgets()
    
    def crear_widgets(self):
        # Cargar la imagen del logo usando tk.PhotoImage
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

        # Etiqueta y campo para nombre y apellido (cambiado de "Nombre:" a "Nombre y Apellido:")
        texto_nombre = tk.Label(self, text='Nombre y Apellido: ', font=('Arial', 30, 'bold'), 
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
        nombre_completo = self.cuadro_texto_entrada_nombre.get().strip()
        contraseña = self.cuadro_texto_entrada_contraseña.get().strip()

        # Validar que se ingresaron ambos campos
        if not nombre_completo or not contraseña:
            messagebox.showerror("Error", "Por favor ingresa nombre, apellido y contraseña")
            return
        
        # Validar que el nombre completo contenga al menos nombre y apellido (al menos dos palabras)
        if len(nombre_completo.split()) < 2:
            messagebox.showerror("Error", "El nombre debe incluir nombre y apellido, separados por espacio")
            return
        
        # Validar que el nombre completo no contenga caracteres especiales (solo letras, acentos y espacios)
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_completo):  # <-- CAMBIO: Agregado acentos y ñ
            messagebox.showerror("Error", "El nombre solo puede contener letras, acentos y espacios, sin números ni caracteres especiales")  # <-- CAMBIO: Mensaje actualizado
            return
        
        # Validar que la contraseña no contenga espacios ni caracteres especiales (solo letras y números)
        if not re.match(r'^[a-zA-Z0-9]+$', contraseña):
            messagebox.showerror("Error", "La contraseña solo puede contener letras y números, sin espacios ni caracteres especiales")
            return
    
        # Verificar si es gerente (con apellido y RUT)
        if nombre_completo == "Gerente Pérez":
            if contraseña == "gerente123":
                self.controller.usuario_actual = nombre_completo
                self.controller.tipo_usuario = "gerente"
            
                tipo = "gerente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json (agregado RUT)
                self.guardar_usuario(nombre_completo, "11111111-1", contraseña, tipo)

                # Limpiar el mensaje de bienvenido antes de cambiar al notebook
                self.texto.config(text="")  # <-- LÍNEA NUEVA: Borra el mensaje
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Gerente
                messagebox.showerror("Error", "Contraseña incorrecta para Gerente Pérez")
                self.texto.config(text="")
                return
        # Verificar si es cliente específico: Ana (con apellido y RUT)
        elif nombre_completo == "Ana López":
            if contraseña == "ana123":
                self.controller.usuario_actual = nombre_completo
                self.controller.tipo_usuario = "cliente"
            
                tipo = "cliente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json (agregado RUT)
                self.guardar_usuario(nombre_completo, "22222222-2", contraseña, tipo)
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Ana
                messagebox.showerror("Error", "Contraseña incorrecta para Ana López")
                self.texto.config(text="")
                return
        # Verificar si es cliente específico: Pedro
        elif nombre_completo == "Pedro García":
            if contraseña == "pedro123":
                self.controller.usuario_actual = nombre_completo
                self.controller.tipo_usuario = "cliente"
            
                tipo = "cliente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json (agregado RUT)
                self.guardar_usuario(nombre_completo, "33333333-3", contraseña, tipo)
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Pedro
                messagebox.showerror("Error", "Contraseña incorrecta para Pedro García")
                self.texto.config(text="")
                return
        # Verificar si es cliente específico: Juan (con apellido y RUT)
        elif nombre_completo == "Juan Martínez":
            if contraseña == "juan123":
                self.controller.usuario_actual = nombre_completo
                self.controller.tipo_usuario = "cliente"
            
                tipo = "cliente"
            
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json (agregado RUT)
                self.guardar_usuario(nombre_completo, "44444444-4", contraseña, tipo)
            
                # Mostrar notebook
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Juan
                messagebox.showerror("Error", "Contraseña incorrecta para Juan Martínez")
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
            rut_usuario = None  # Para obtener el RUT si se encuentra
            for usuario in datos:
                if usuario['nombre_completo'] == nombre_completo and usuario['contraseña'] == contraseña:
                    usuario_encontrado = True
                    rut_usuario = usuario['rut']
                    break
            
            if usuario_encontrado:
                self.controller.usuario_actual = nombre_completo
                self.controller.tipo_usuario = "cliente"
            
                tipo = "cliente"
        
                # Limpiar campos
                self.cuadro_texto_entrada_nombre.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
            
                # Guardar datos en usuarios_cuentas.json (usando RUT existente)
                self.guardar_usuario(nombre_completo, rut_usuario, contraseña, tipo)
            
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
        ventana_registro.geometry("400x350")
        ventana_registro.configure(bg="#b5ddd8")
        
        # Etiqueta y campo para nombre y apellido (cambiado de "Nombre de usuario:")
        ttk.Label(ventana_registro, text="Nombre y Apellido:", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_nombre = ttk.Entry(ventana_registro, width=20, font=('Arial', 12))
        entrada_nombre.pack(pady=5)

        # Etiqueta y campo para RUT (nuevo campo)
        ttk.Label(ventana_registro, text="RUT (ej: 12345678-9):", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_rut = ttk.Entry(ventana_registro, width=20, font=('Arial', 12))
        entrada_rut.pack(pady=5)
        
        # Etiqueta y campo para contraseña
        ttk.Label(ventana_registro, text="Contraseña:", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_contraseña = ttk.Entry(ventana_registro, width=20, font=('Arial', 12), show='*')
        entrada_contraseña.pack(pady=5)
        
        def confirmar_registro():
            nombre_completo = entrada_nombre.get().strip()  # Cambiado de 'nombre'
            rut = entrada_rut.get().strip()  # Nuevo
            contraseña = entrada_contraseña.get().strip()
            
            # Validar campos
            if not nombre_completo or not rut or not contraseña:
                messagebox.showerror("Error", "Por favor ingresa nombre y apellido, RUT y contraseña")
                return

            # Validar nombre completo
            if len(nombre_completo.split()) < 2:
                messagebox.showerror("Error", "El nombre debe incluir nombre y apellido, separados por espacio")
                return
            
            # Validar que el nombre completo no contenga caracteres especiales (solo letras y espacios)
            if not re.match(r'^[a-zA-Z\s]+$', nombre_completo):  # <-- CAMBIO: Ahora permite espacios (\s)
               messagebox.showerror("Error", "El nombre solo puede contener letras y espacios, sin números ni caracteres especiales")  # <-- CAMBIO: Mensaje actualizado
               return
            
            # Validar RUT (formato básico: dígitos-guion-dígito)
            if not re.match(r'^\d{7,8}-[\dKk]$', rut):
                messagebox.showerror("Error", "RUT inválido. Formato: 12345678-9 o 1234567-K")
                return
            
            #Validar contraseña
            if not re.match(r'^[a-zA-Z0-9]+$', contraseña):
                messagebox.showerror("Error", "La contraseña solo puede contener letras y números, sin espacios ni caracteres especiales")
                return
            
            # Verificar unicidad de nombre_completo y RUT (actualizado)
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos = js.load(archivo)
                    if not isinstance(datos, list):
                        datos = []
            except (FileNotFoundError, js.JSONDecodeError):
                datos = []
        
            for usuario in datos:
                if usuario['rut'] == rut:
                    messagebox.showerror("Error", "El RUT ya está registrado.")
                    return
                if usuario['contraseña'] == contraseña:  # <-- NUEVO: Verificar unicidad de contraseña
                    messagebox.showerror("Error", "La contraseña ya está en uso por otro usuario. Elige una contraseña diferente.")
                    return    
            # Verificar contra usuarios predefinidos (actualizado con apellidos y RUT)
            usuarios_predefinidos = [
                {"nombre_completo": "Gerente Pérez", "rut": "11111111-1"},
                {"nombre_completo": "Ana López", "rut": "22222222-2"},
                {"nombre_completo": "Pedro García", "rut": "33333333-3"},
                {"nombre_completo": "Juan Martínez", "rut": "44444444-4"}
            ]
            for pred in usuarios_predefinidos:
                if pred['nombre_completo'] == nombre_completo or pred['rut'] == rut:
                    messagebox.showerror("Error", "El ususario ya existe. Elige otro.")
                    return
            
            # Guardar nuevo usuario (actualizado con 'nombre_completo' y 'rut')
            diccionario_a_guardar = {'nombre_completo': nombre_completo, 'rut': rut, 'contraseña': contraseña, 'tipo': 'cliente', 'limite_prestamo': 500000, 'prestamos_activos': []}  # Agregar límite inicial}
            datos.append(diccionario_a_guardar)
            with open("usuarios_cuentas.json", 'w') as archivo:
                js.dump(datos, archivo)
            
            # Crear entrada vacía en cuentas.json para el nuevo usuario (usando nombre_completo como clave)
            try:
                with open("cuentas.json", 'r') as archivo:
                    cuentas_globales = js.load(archivo)
                    if not isinstance(cuentas_globales, dict):
                        cuentas_globales = {}
            except (FileNotFoundError, js.JSONDecodeError):
                cuentas_globales = {}
            
            cuentas_globales[nombre_completo] = []  # Lista vacía de cuentas
            with open("cuentas.json", 'w') as archivo:
                js.dump(cuentas_globales, archivo)

            messagebox.showinfo("Éxito", f"Usuario {nombre_completo} registrado exitosamente. Ahora puedes iniciar sesión.")
            ventana_registro.destroy()
        
        # Botones
        ttk.Button(ventana_registro, text="Registrar", command=confirmar_registro).pack(pady=20)
        ttk.Button(ventana_registro, text="Cancelar", command=ventana_registro.destroy).pack(pady=5)

        # <-- AGREGADO: Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_registro)
        
        # Centrar ventana emergente
        ventana_registro.transient(self)
        ventana_registro.grab_set()
        self.wait_window(ventana_registro)

    def guardar_usuario(self, nombre_completo, rut, contraseña, tipo):
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

        diccionario_a_guardar = {'nombre_completo': nombre_completo, 'rut': rut, 'contraseña': contraseña, 'tipo': tipo}
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

    def centrar_ventana_emergente(self, ventana):
        """Centra una ventana emergente en la pantalla"""
        ventana.update_idletasks()  # Asegura que Tkinter calcule el tamaño real
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
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
            "Juan Martínez": [
                {"id": "1", "tipo": "Cuenta Vista", "numero": "111111111", "saldo": "$10.000"},
                {"id": "2", "tipo": "Cuenta de Ahorros", "numero": "111111111", "saldo": "$50.000"}
            ],
            "Ana López": [
                {"id": "1", "tipo": "Cuenta Corriente", "numero": "222222222", "saldo": "$25.000"},
                {"id": "2", "tipo": "Cuenta Rut", "numero": "222222222", "saldo": "$5.000"},
                {"id": "3", "tipo": "Cuenta de Ahorros", "numero": "222222222", "saldo": "$100.000"}
            ],
            "Pedro García": [
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
        ttk.Button(pestana2, text="Préstamos", command=self.popup_prestamos).pack(pady=10)

        # Pestaña 3 - Ayuda
        pestana3 = ttk.Frame(self.notebook)
        self.notebook.add(pestana3, text="Ayuda")
    
        ttk.Label(pestana3, text="Centro de Ayuda", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(pestana3, text=f"Bienvenido Cliente: {self.controller.usuario_actual}").pack(pady=10)
        ttk.Button(pestana3, text="Soporte al Cliente").pack(pady=10)
        ttk.Button(pestana3, text="Preguntas Frecuentes").pack(pady=10)

    def pedir_prestamo(self):
        """Método para pedir un préstamo bancario"""
        # Verificar si el cliente tiene al menos una cuenta
        if not self.cuentas_data:
            messagebox.showerror("Error", "Debes tener al menos una cuenta para pedir un préstamo.")
            return
        
        # Cargar límite de préstamo del usuario
        usuario_actual = self.controller.usuario_actual
        limite_actual = 500000  # Valor por defecto
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
                if not isinstance(datos_usuarios, list):
                    datos_usuarios = []
            for usuario in datos_usuarios:
                if usuario['nombre_completo'] == usuario_actual:
                    limite_actual = usuario.get('limite_prestamo', 500000)  # Obtener límite o usar 500000 si no existe
                    break
        except (FileNotFoundError, js.JSONDecodeError):
            pass  # Usar valor por defecto

        # Verificar si el usuario tiene límite disponible
        if limite_actual <= 0:
            messagebox.showerror("Error", f"No tienes límite disponible para préstamos. Límite actual: ${limite_actual:,.0f}")
            return
        
        # Crear ventana emergente para pedir préstamo
        ventana_prestamo = tk.Toplevel(self)
        ventana_prestamo.title("Pedir Préstamo")
        ventana_prestamo.geometry("450x350")
        ventana_prestamo.configure(bg="#b5ddd8")

        # Mostrar límite disponible
        etiqueta_limite = ttk.Label(ventana_prestamo, 
                                    text=f"Límite disponible para préstamo: ${limite_actual:,.0f}",
                                    font=('Arial', 12, 'bold'),
                                    foreground="blue")
        etiqueta_limite.pack(pady=10)
        
        # Etiqueta y campo para monto del préstamo (ACTUALIZADO para mostrar límite máximo)
        etiqueta_monto = ttk.Label(ventana_prestamo, 
                                text=f"Monto del préstamo (máximo ${limite_actual:,.0f}):",
                                font=('Arial', 12, 'bold'))
        etiqueta_monto.pack(pady=10)
        entrada_monto = ttk.Entry(ventana_prestamo, width=20, font=('Arial', 12))
        entrada_monto.pack(pady=5)
        
        # Etiqueta y OptionMenu para seleccionar cuenta destino
        etiqueta_cuenta = ttk.Label(ventana_prestamo, text="Seleccione la cuenta para recibir el dinero:", font=('Arial', 12, 'bold'))
        etiqueta_cuenta.pack(pady=10)
        cuentas_opciones = [f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" for cuenta in self.cuentas_data]
        cuenta_var = tk.StringVar(value=cuentas_opciones[0] if cuentas_opciones else "")
        menu_cuenta = tk.OptionMenu(ventana_prestamo, cuenta_var, *cuentas_opciones)
        menu_cuenta.pack(pady=10)
        
        # Elementos para validación de contraseña (inicialmente ocultos)
        etiqueta_contraseña = ttk.Label(ventana_prestamo, text="Por favor ingrese su contraseña de usuario:", font=('Arial', 12, 'bold'))
        etiqueta_contraseña.pack_forget()
        entrada_contraseña = ttk.Entry(ventana_prestamo, width=20, font=('Arial', 12), show='*')
        entrada_contraseña.pack_forget()
        
        # Variables para almacenar datos validados (se usan después de la contraseña)
        datos_validos = {}
        
        def confirmar_prestamo():
            monto_str = entrada_monto.get().strip()
            cuenta_seleccionada = cuenta_var.get()
            
            # Validar monto
            if not monto_str:
                messagebox.showerror("Error", "Ingresa un monto para el préstamo.")
                return
            try:
                monto = int(monto_str)
                if monto < 1:
                    messagebox.showerror("Error", "El monto mínimo es 1")
                    return
                if monto > limite_actual:  # VERIFICAR CONTRA LÍMITE ACTUAL
                    messagebox.showerror("Error", 
                                        f"El monto excede tu límite disponible.\n"
                                        f"Monto solicitado: ${monto:,.0f}\n"
                                        f"Límite disponible: ${limite_actual:,.0f}")
                    return
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número entero válido.")
                return
            
            # Encontrar la cuenta seleccionada
            cuenta_destino = None
            for cuenta in self.cuentas_data:
                if f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" == cuenta_seleccionada:
                    cuenta_destino = cuenta
                    break
            if not cuenta_destino:
                messagebox.showerror("Error", "Cuenta destino no encontrada.")
                return
            
            # Almacenar datos validados para usar después de la contraseña
            datos_validos.update({
                'cuenta_destino': cuenta_destino,
                'monto': monto
            })
            
            # Ocultar elementos anteriores y mostrar campo de contraseña
            etiqueta_limite.pack_forget()
            etiqueta_monto.pack_forget()
            entrada_monto.pack_forget()
            etiqueta_cuenta.pack_forget()
            menu_cuenta.pack_forget()
            etiqueta_contraseña.pack(pady=10)
            entrada_contraseña.pack(pady=5)

            # "Olvidar" (ocultar) los botones para reordenarlos
            boton_confirmar.pack_forget()
            boton_cancelar.pack_forget()
            
            # Re-empaquetar los botones debajo del campo de contraseña
            boton_confirmar.pack(pady=20)
            boton_cancelar.pack(pady=5)
            
            # Cambiar el botón a "Validar Contraseña"
            boton_confirmar.config(text="Validar Contraseña", command=validar_contraseña)
        
        def validar_contraseña():
            contraseña_ingresada = entrada_contraseña.get().strip()
            if not contraseña_ingresada:
                messagebox.showerror("Error", "Ingresa tu contraseña.")
                return
            
            usuario_actual = self.controller.usuario_actual
            print(f"Usuario actual: {usuario_actual}")  # Debug
            print(f"Contraseña ingresada: {contraseña_ingresada}")  # Debug
            
            # Validar contraseña igual que en login: primero usuarios predefinidos, luego JSON
            contraseña_correcta = None
            if usuario_actual == "Gerente Pérez" and contraseña_ingresada == "gerente123":
                contraseña_correcta = "gerente123"
            elif usuario_actual == "Ana López" and contraseña_ingresada == "ana123":
                contraseña_correcta = "ana123"
            elif usuario_actual == "Pedro García" and contraseña_ingresada == "pedro123":
                contraseña_correcta = "pedro123"
            elif usuario_actual == "Juan Martínez" and contraseña_ingresada == "juan123":
                contraseña_correcta = "juan123"
            else:
                # Para usuarios registrados nuevos, buscar en usuarios_cuentas.json
                try:
                    with open("usuarios_cuentas.json", 'r') as archivo:
                        datos_usuarios = js.load(archivo)
                        if not isinstance(datos_usuarios, list):
                            datos_usuarios = []
                except (FileNotFoundError, js.JSONDecodeError):
                    datos_usuarios = []
                for usuario in datos_usuarios:
                    if usuario['nombre_completo'] == usuario_actual:
                        contraseña_correcta = usuario['contraseña']
                        break
            
            if contraseña_ingresada != contraseña_correcta:
                messagebox.showerror("Error", "Contraseña incorrecta. Préstamo cancelado.")
                ventana_prestamo.destroy()
                return
            
            # Proceder con el préstamo
            cuenta_destino = datos_validos['cuenta_destino']
            monto = datos_validos['monto']
            
            # Actualizar saldo de la cuenta destino
            saldo_actual = float(cuenta_destino['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            nuevo_saldo = saldo_actual + monto
            cuenta_destino['saldo'] = f"${nuevo_saldo:,.0f}".replace(',', '.')

            # Reducir el límite de préstamo y guardar en usuarios_cuentas.json
            nuevo_limite = limite_actual - monto

            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos_usuarios = js.load(archivo)
                    if not isinstance(datos_usuarios, list):
                        datos_usuarios = []
                
                usuario_encontrado = False
                for usuario in datos_usuarios:
                    if usuario['nombre_completo'] == usuario_actual:
                        usuario['limite_prestamo'] = nuevo_limite
                        usuario_encontrado = True
                        break

                # Si no encuentra al usuario, agregarlo
                if not usuario_encontrado:
                    datos_usuarios.append({
                        'nombre_completo': usuario_actual,
                        'limite_prestamo': nuevo_limite,
                        'tipo': 'cliente'
                    })
                
                with open("usuarios_cuentas.json", 'w') as archivo:
                    js.dump(datos_usuarios, archivo)
                    
                print(f"Límite actualizado para {usuario_actual}: {nuevo_limite}")  # Para debugging
            
            except (FileNotFoundError, js.JSONDecodeError) as e:
                print(f"Error al guardar límite: {e}")
                # Continuar con la operación aunque falle guardar el límite

            # Agregar el préstamo a la lista de préstamos activos
            prestamo_id = str(int(datetime.now().timestamp()))  # ID único basado en timestamp
            nuevo_prestamo = {
                'id': prestamo_id,
                'monto': monto,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'cuenta_destino': cuenta_destino['numero'],
                'saldo_pendiente': monto  # Inicialmente, el monto total pendiente
            }
            
            # Cargar y actualizar prestamos_activos
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos_usuarios = js.load(archivo)
                    if not isinstance(datos_usuarios, list):
                        datos_usuarios = []
                
                for usuario in datos_usuarios:
                    if usuario['nombre_completo'] == usuario_actual:
                        if 'prestamos_activos' not in usuario:
                            usuario['prestamos_activos'] = []
                        usuario['prestamos_activos'].append(nuevo_prestamo)
                        break
                
                with open("usuarios_cuentas.json", 'w') as archivo:
                    js.dump(datos_usuarios, archivo)
            except Exception as e:
                print(f"Error al guardar préstamo: {e}")
            
            # Actualizar treeview
            self.actualizar_treeview()
            
            # Guardar cambios en cuentas.json
            self.guardar_cuentas()
            
            messagebox.showinfo("Éxito", f"Préstamo de ${monto:,.0f} aprobado y depositado en la cuenta {cuenta_destino['tipo']} - {cuenta_destino['numero']}.")
            ventana_prestamo.destroy()
        
        # Botón para confirmar
        boton_confirmar = ttk.Button(ventana_prestamo, text="Confirmar Préstamo", command=confirmar_prestamo)
        boton_confirmar.pack(pady=20)

        # Botón para cancelar
        boton_cancelar = ttk.Button(ventana_prestamo, text="Cancelar", command=ventana_prestamo.destroy)  # Asignar a variable
        boton_cancelar.pack(pady=5)  # Usar la variable para pack()

        # Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_prestamo)
        
        # Centrar ventana emergente
        ventana_prestamo.transient(self)
        ventana_prestamo.grab_set()
        self.wait_window(ventana_prestamo)

    def pagar_prestamo(self):
        """Método para pagar un préstamo activo"""
        usuario_actual = self.controller.usuario_actual
        
        # Recargar préstamos activos del usuario desde el archivo (para asegurar datos actualizados)
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
                if not isinstance(datos_usuarios, list):
                    datos_usuarios = []
            prestamos_activos = []
            for usuario in datos_usuarios:
                if usuario['nombre_completo'] == usuario_actual:
                    prestamos_activos = usuario.get('prestamos_activos', [])
                    break
        except (FileNotFoundError, js.JSONDecodeError) as e:
            messagebox.showerror("Error", f"No se pudieron cargar los préstamos: {e}")
            prestamos_activos = []
        
        if not prestamos_activos:
            messagebox.showinfo("Información", "No tienes préstamos activos para pagar.")
            return
        
        # Crear ventana emergente para pagar préstamo
        ventana_pagar = tk.Toplevel(self)
        ventana_pagar.title("Pagar Préstamo")
        ventana_pagar.geometry("500x400")
        ventana_pagar.configure(bg="#b5ddd8")
        
        ttk.Label(ventana_pagar, text="Selecciona un préstamo para pagar:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Treeview para mostrar préstamos activos
        tree_prestamos = ttk.Treeview(ventana_pagar, columns=("id", "monto", "fecha", "cuenta", "pendiente"), show="headings")
        tree_prestamos.heading("id", text="ID Préstamo")
        tree_prestamos.heading("monto", text="Monto Original")
        tree_prestamos.heading("fecha", text="Fecha")
        tree_prestamos.heading("cuenta", text="Cuenta Destino")
        tree_prestamos.heading("pendiente", text="Saldo Pendiente")
        
        for prestamo in prestamos_activos:

            # Formatear los montos con punto como separador de miles y sin decimales
            monto_formateado = f"${prestamo['monto']:,.0f}".replace(',', '.')
            pendiente_formateado = f"${prestamo['saldo_pendiente']:,.0f}".replace(',', '.')
            
            tree_prestamos.insert("", "end", values=(prestamo['id'], monto_formateado, prestamo['fecha'], prestamo['cuenta_destino'], pendiente_formateado))
        
        tree_prestamos.pack(pady=10, fill="both", expand=True)
        
        # Etiqueta y campo para monto a pagar
        ttk.Label(ventana_pagar, text="Monto a pagar:", font=('Arial', 12, 'bold')).pack(pady=10)
        entrada_monto_pago = ttk.Entry(ventana_pagar, width=20, font=('Arial', 12))
        entrada_monto_pago.pack(pady=5)
        
        def confirmar_pago():
            seleccion = tree_prestamos.selection()
            if not seleccion:
                messagebox.showerror("Error", "Selecciona un préstamo para pagar.")
                return
            
            item = tree_prestamos.item(seleccion[0])
            prestamo_id = str(item['values'][0])
            saldo_pendiente = float(item['values'][4].replace('$', '').replace('.', ''))

            print(f"DEBUG: prestamo_id seleccionado: {prestamo_id} (tipo: {type(prestamo_id)})")  # Debug
            print(f"DEBUG: IDs en prestamos_activos: {[p['id'] for p in prestamos_activos]}")  # Debug
            
            monto_pago_str = entrada_monto_pago.get().strip()
            try:
                monto_pago = float(monto_pago_str)
                if monto_pago <= 0 or monto_pago > saldo_pendiente:
                    messagebox.showerror("Error", f"El monto debe ser mayor a 0 y no exceder el saldo pendiente (${saldo_pendiente:,.0f}).")
                    return
            except ValueError:
                messagebox.showerror("Error", "Ingresa un monto válido.")
                return
            
            # Verificar que el usuario tenga saldo suficiente en alguna cuenta
            saldo_total = sum(float(cuenta['saldo'].replace('$', '').replace('.', '').replace(',', '')) for cuenta in self.cuentas_data)
            if monto_pago > saldo_total:
                messagebox.showerror("Error", "Saldo insuficiente en tus cuentas para realizar el pago.")
                return
            
            # Actualizar saldo pendiente del préstamo
            nuevo_saldo_pendiente = saldo_pendiente - monto_pago
            
            # Recargar datos_usuarios desde el archivo para asegurar datos actualizados
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos_usuarios = js.load(archivo)
                    if not isinstance(datos_usuarios, list):
                        datos_usuarios = []
            except (FileNotFoundError, js.JSONDecodeError) as e:
                messagebox.showerror("Error", f"No se pudieron cargar los datos del usuario: {e}")
                return
            
            # Actualizar en usuarios_cuentas.json
            usuario_encontrado = False
            prestamo_actualizado = False
            for usuario in datos_usuarios:
                if usuario['nombre_completo'] == usuario_actual:
                    usuario_encontrado = True
                    if 'prestamos_activos' not in usuario:
                        usuario['prestamos_activos'] = []
                    for prestamo in usuario['prestamos_activos']:
                        if prestamo['id'] == prestamo_id:
                            prestamo['saldo_pendiente'] = nuevo_saldo_pendiente
                            prestamo_actualizado = True
                            if nuevo_saldo_pendiente <= 0:
                                usuario['prestamos_activos'].remove(prestamo)  # Eliminar si pagado completamente
                                print(f"Préstamo {prestamo_id} eliminado completamente.")  # Debug
                            else:
                                print(f"Saldo pendiente actualizado para préstamo {prestamo_id}: {nuevo_saldo_pendiente}")  # Debug
                            break
                    if not prestamo_actualizado:
                        messagebox.showerror("Error", "Préstamo no encontrado para actualizar.")
                        return
                    break
            
            if not usuario_encontrado:
                messagebox.showerror("Error", "Usuario no encontrado en la base de datos.")
                return
            
            # Guardar cambios en usuarios_cuentas.json
            try:
                with open("usuarios_cuentas.json", 'w') as archivo:
                    js.dump(datos_usuarios, archivo)
                print(f"Datos guardados correctamente para {usuario_actual}.")  # Debug
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar los cambios en préstamos: {e}")
                return
            
            # Restar el monto de las cuentas (simplificado: restar de la primera cuenta con saldo suficiente)
            for cuenta in self.cuentas_data:
                saldo_cuenta = float(cuenta['saldo'].replace('$', '').replace('.', '').replace(',', ''))
                if saldo_cuenta >= monto_pago:
                    cuenta['saldo'] = f"${saldo_cuenta - monto_pago:,.0f}".replace(',', '.')
                    break
            
            # Actualizar treeview de cuentas
            self.actualizar_treeview()
            self.guardar_cuentas()
            
            messagebox.showinfo("Éxito", f"Pago de ${monto_pago:,.0f} realizado. Saldo pendiente: ${max(0, nuevo_saldo_pendiente):,.0f}")
            ventana_pagar.destroy()
        
        ttk.Button(ventana_pagar, text="Confirmar Pago", command=confirmar_pago).pack(pady=20)
        ttk.Button(ventana_pagar, text="Cancelar", command=ventana_pagar.destroy).pack(pady=5)

        # Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_pagar)
        
        # Centrar ventana emergente
        ventana_pagar.transient(self)
        ventana_pagar.grab_set()
        self.wait_window(ventana_pagar)


    def popup_prestamos(self):
        """Popup para seleccionar Pedir o Pagar préstamo"""
        ventana_popup = tk.Toplevel(self)
        ventana_popup.title("Opciones de Préstamos")
        ventana_popup.geometry("300x200")
        ventana_popup.configure(bg="#b5ddd8")
        
        ttk.Label(ventana_popup, text="Selecciona una opción:", font=('Arial', 14, 'bold')).pack(pady=20)
        
        ttk.Button(ventana_popup, text="Pedir préstamo", command=lambda: [ventana_popup.destroy(), self.pedir_prestamo()]).pack(pady=10)
        ttk.Button(ventana_popup, text="Pagar préstamo", command=lambda: [ventana_popup.destroy(), self.pagar_prestamo()]).pack(pady=10)
        
        # Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_popup)

        # Centrar ventana emergente
        ventana_popup.transient(self)
        ventana_popup.grab_set()
        self.wait_window(ventana_popup)
    
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
            
            # Obtener el RUT del usuario actual desde usuarios_cuentas.json
            usuario_actual = self.controller.usuario_actual
            rut_usuario = None
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos_usuarios = js.load(archivo)
                    if not isinstance(datos_usuarios, list):
                        datos_usuarios = []
                for usuario in datos_usuarios:
                    if usuario['nombre_completo'] == usuario_actual:
                        rut_usuario = usuario['rut']
                        break
            except (FileNotFoundError, js.JSONDecodeError):
                messagebox.showerror("Error", "No se pudo acceder a los datos del usuario.")
                return
        
            if not rut_usuario:
                messagebox.showerror("Error", "RUT del usuario no encontrado.")
                return
        
            # Generar número de cuenta: si es "Cuenta Rut", usar el RUT sin guión; de lo contrario, aleatorio
            if tipo_seleccionado == "Cuenta Rut":
                numero_cuenta = rut_usuario.replace("-", "")  # Usar RUT sin guión como número de cuenta
            else:
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

        # <-- AGREGADO: Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_crear)
    
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
        
        # Verificar si hay más de una cuenta en total
        if len(self.cuentas_data) <= 1:
            messagebox.showerror("Error", "No puedes eliminar tu única cuenta. Debes tener al menos una cuenta activa.")
            return
    
        # Para cada cuenta seleccionada, manejar la transferencia de saldo si es necesario
        for cuenta in cuentas_seleccionadas:
            saldo = float(cuenta['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            if saldo > 0:
                # Obtener cuentas disponibles para transferir (excluyendo las seleccionadas para eliminar)
                cuentas_disponibles = [c for c in self.cuentas_data if c not in cuentas_seleccionadas]
                if not cuentas_disponibles:
                    messagebox.showerror("Error", f"No hay cuentas disponibles para transferir el saldo de {cuenta['tipo']} ({cuenta['numero']}). Cancela la eliminación de otras cuentas primero.")
                    return
    
                # Mostrar diálogo para elegir cuenta destino
                destino_elegido = self.elegir_cuenta_destino(cuentas_disponibles, cuenta)
                if not destino_elegido:
                    # Usuario canceló
                    return
    
                # Transferir saldo completo a la cuenta elegida
                saldo_destino = float(destino_elegido['saldo'].replace('$', '').replace('.', '').replace(',', ''))
                nuevo_saldo_destino = saldo_destino + saldo
                destino_elegido['saldo'] = f"${nuevo_saldo_destino:,.0f}".replace(',', '.')
                cuenta['saldo'] = "$0"  # Dejar saldo en 0 antes de eliminar
    
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

    def elegir_cuenta_destino(self, cuentas_disponibles, cuenta_origen):
        """Diálogo para elegir cuenta destino para transferir saldo"""
        ventana_destino = tk.Toplevel(self)
        ventana_destino.title("Elegir Cuenta Destino")
        ventana_destino.geometry("400x200")
        ventana_destino.configure(bg="#b5ddd8")
    
        ttk.Label(ventana_destino, text=f"Transferir saldo de {cuenta_origen['tipo']} ({cuenta_origen['numero']}) a:", font=('Arial', 12, 'bold')).pack(pady=10)
    
        opciones = [f"{c['tipo']} - {c['numero']} - Saldo: {c['saldo']}" for c in cuentas_disponibles]
        destino_var = tk.StringVar(value=opciones[0] if opciones else "")
        menu_destino = tk.OptionMenu(ventana_destino, destino_var, *opciones)
        menu_destino.pack(pady=10)
    
        cuenta_elegida = None
    
        def confirmar():
            nonlocal cuenta_elegida
            seleccion = destino_var.get()
            for c in cuentas_disponibles:
                if f"{c['tipo']} - {c['numero']} - Saldo: {c['saldo']}" == seleccion:
                    cuenta_elegida = c
                    break
            ventana_destino.destroy()

        ttk.Button(ventana_destino, text="Confirmar", command=confirmar).pack(pady=10)
        ttk.Button(ventana_destino, text="Cancelar", command=ventana_destino.destroy).pack(pady=5)

        # <-- AGREGADO: Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_destino)
    
        # Centrar y esperar
        ventana_destino.transient(self)
        ventana_destino.grab_set()
        self.wait_window(ventana_destino)
    
        return cuenta_elegida

    def limpiar_checkbuttons(self):
        """Limpia los checkbuttons y variables"""
        for var in self.variables_cuentas:
            var.set(False)

    def realizar_transferencia(self):
        """Función para realizar una transferencia entre cuentas de usuarios registrados"""
        # Crear ventana emergente para transferencia
        ventana_transferencia = tk.Toplevel(self)
        ventana_transferencia.title("Realizar Transferencia")
        ventana_transferencia.geometry("650x550")
        ventana_transferencia.configure(bg="#b5ddd8")

        # Etiqueta y OptionMenu para seleccionar cuenta de origen
        etiqueta_origen = ttk.Label(ventana_transferencia, text="Seleccione la cuenta de origen:", font=('Arial', 12, 'bold'))
        etiqueta_origen.pack(pady=10)
        cuentas_origen = [f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" for cuenta in self.cuentas_data]
        if not cuentas_origen:
            messagebox.showerror("Error", "No tienes cuentas disponibles para transferir.")
            ventana_transferencia.destroy()
            return
        origen_var = tk.StringVar(value=cuentas_origen[0])
        menu_origen = tk.OptionMenu(ventana_transferencia, origen_var, *cuentas_origen)
        menu_origen.pack(pady=10)

        # Etiqueta y Combobox para seleccionar tipo de cuenta de destino (antes del destinatario)
        etiqueta_tipo = ttk.Label(ventana_transferencia, text="Seleccione el tipo de cuenta de destino:", font=('Arial', 12, 'bold'))
        etiqueta_tipo.pack(pady=10)
        tipos_cuenta = ["Cuenta Vista", "Cuenta de Ahorros", "Cuenta Corriente", "Cuenta Rut"]
        tipo_destino_var = tk.StringVar()
        combobox_tipo = ttk.Combobox(ventana_transferencia, textvariable=tipo_destino_var, values=tipos_cuenta, state="readonly")
        combobox_tipo.pack(pady=10)
        combobox_tipo.set(tipos_cuenta[0])  # Valor por defecto

        # Etiqueta y campo para nombre del destinatario
        etiqueta_destinatario = ttk.Label(ventana_transferencia, text="Nombre del destinatario:", font=('Arial', 12, 'bold'))
        etiqueta_destinatario.pack(pady=10)
        entrada_destinatario = ttk.Entry(ventana_transferencia, width=20, font=('Arial', 12))
        entrada_destinatario.pack(pady=5)

        # Agregar etiqueta y campo para RUT del destinatario
        etiqueta_rut = ttk.Label(ventana_transferencia, text="RUT del destinatario (ej: 12345678-9):", font=('Arial', 12, 'bold'))
        etiqueta_rut.pack(pady=10)
        entrada_rut = ttk.Entry(ventana_transferencia, width=20, font=('Arial', 12))
        entrada_rut.pack(pady=5)

        # Etiqueta y campo para monto
        etiqueta_monto = ttk.Label(ventana_transferencia, text="Monto a transferir (ej: 1000):", font=('Arial', 12, 'bold'))
        etiqueta_monto.pack(pady=10)
        entrada_monto = ttk.Entry(ventana_transferencia, width=20, font=('Arial', 12))
        entrada_monto.pack(pady=5)

        # Elementos para validación de contraseña (inicialmente ocultos)
        etiqueta_contraseña = ttk.Label(ventana_transferencia, text="Por favor ingrese su contraseña de usuario:", font=('Arial', 12, 'bold'))
        etiqueta_contraseña.pack_forget()
        entrada_contraseña = ttk.Entry(ventana_transferencia, width=20, font=('Arial', 12), show='*')
        entrada_contraseña.pack_forget()
        
        # Variables para almacenar datos validados (se usan después de la contraseña)
        datos_validos = {}

        def confirmar_transferencia():
            # Obtener datos
            origen_seleccionado = origen_var.get()
            tipo_destino = tipo_destino_var.get()
            destinatario = entrada_destinatario.get().strip()
            rut_destinatario = entrada_rut.get().strip()
            monto_str = entrada_monto.get().strip()
            # Validar que se haya seleccionado tipo
            if not tipo_destino:
                messagebox.showerror("Error", "Selecciona un tipo de cuenta de destino.")
                return
            # Validar nombre de destinatario
            if not destinatario:
                messagebox.showerror("Error", "Ingresa el nombre del destinatario.")
                return
            
            # Validar RUT (formato y presencia)
            if not rut_destinatario:
                messagebox.showerror("Error", "Ingresa el RUT del destinatario.")
                return
            if not re.match(r'^\d{7,8}-[\dKk]$', rut_destinatario):
                messagebox.showerror("Error", "RUT inválido. Formato: 12345678-9 o 1234567-K")
                return
            
            # Verificar que el nombre y RUT coincidan exactamente con un usuario registrado
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos_usuarios = js.load(archivo)
                    if not isinstance(datos_usuarios, list):
                        datos_usuarios = []
            except (FileNotFoundError, js.JSONDecodeError):
                datos_usuarios = []
            
            usuario_encontrado = None
            for u in datos_usuarios:
                if u['nombre_completo'] == destinatario and u['rut'] == rut_destinatario:
                    usuario_encontrado = u
                    break
            
            if not usuario_encontrado:
                messagebox.showerror("Error", "Usuario no registrado o nombre y RUT no coinciden.")
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
            # Verificar que el destinatario tenga al menos una cuenta del tipo seleccionado
            cuentas_filtradas = [cuenta for cuenta in cuentas_destino if cuenta['tipo'] == tipo_destino]
            if not cuentas_filtradas:
                messagebox.showerror("Error", f"El destinatario no tiene una cuenta de tipo '{tipo_destino}'.")
                return
            
            # Usar la primera cuenta del tipo seleccionado (no selección específica)
            cuenta_destino = cuentas_filtradas[0]

            # Validar monto: solo enteros, sin decimales
            if '.' in monto_str or ',' in monto_str:
                messagebox.showerror("Error", "El monto debe ser un número entero, sin decimales.")
                return
            try:
                monto = int(monto_str)
                if monto < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto entero mayor o igual a 1.")
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

            # Verificar que la cuenta de origen no sea la misma que la de destino
            if cuenta_origen['numero'] == cuenta_destino['numero']:
               messagebox.showerror("Error", "No puedes transferir dinero a la misma cuenta.")
               return
            
            # Almacenar datos validados para usar después de la contraseña
            datos_validos.update({
                'cuenta_origen': cuenta_origen,
                'cuenta_destino': cuenta_destino,
                'monto': monto,
                'saldo_origen': saldo_origen,
                'destinatario': destinatario,
                'tipo_destino': tipo_destino,
                'datos_cuentas': datos_cuentas,
                'cuentas_destino': cuentas_destino
            })

            # Ocultar elementos anteriores y mostrar campo de contraseña
            etiqueta_origen.pack_forget()  #Ocultar etiqueta de origen
            menu_origen.pack_forget()
            etiqueta_tipo.pack_forget()  #Ocultar etiqueta de tipo
            combobox_tipo.pack_forget()
            etiqueta_destinatario.pack_forget()  #Ocultar etiqueta de destinatario
            entrada_destinatario.pack_forget()
            etiqueta_monto.pack_forget()  #Ocultar etiqueta de monto
            entrada_monto.pack_forget()
            etiqueta_contraseña.pack(pady=10)
            entrada_contraseña.pack(pady=5)

            # Botón "Validar Contraseña"
            boton_confirmar.config(text="Validar Contraseña", command=validar_contraseña)

        def validar_contraseña():
            contraseña_ingresada = entrada_contraseña.get().strip()
            if not contraseña_ingresada:
                messagebox.showerror("Error", "Ingresa tu contraseña.")
                return
            
            usuario_actual = self.controller.usuario_actual
            print(f"Usuario actual: {usuario_actual}")  # Debug
            print(f"Contraseña ingresada: {contraseña_ingresada}")  # Debug
            
            # Validar contraseña igual que en login: primero usuarios predefinidos, luego JSON
            contraseña_correcta = None
            if usuario_actual == "Gerente Pérez" and contraseña_ingresada == "gerente123":
                contraseña_correcta = "gerente123"
            elif usuario_actual == "Ana López" and contraseña_ingresada == "ana123":
                contraseña_correcta = "ana123"
            elif usuario_actual == "Pedro García" and contraseña_ingresada == "pedro123":
                contraseña_correcta = "pedro123"
            elif usuario_actual == "Juan Martínez" and contraseña_ingresada == "juan123":
                contraseña_correcta = "juan123"
            else:
                # Para usuarios registrados nuevos, buscar en usuarios_cuentas.json
                try:
                    with open("usuarios_cuentas.json", 'r') as archivo:
                        datos_usuarios = js.load(archivo)
                        if not isinstance(datos_usuarios, list):
                            datos_usuarios = []
                except (FileNotFoundError, js.JSONDecodeError):
                    datos_usuarios = []
                for usuario in datos_usuarios:
                    if usuario['nombre_completo'] == usuario_actual:
                        contraseña_correcta = usuario['contraseña']
                        break

            if contraseña_ingresada != contraseña_correcta:
                messagebox.showerror("Error", "Contraseña incorrecta. Transferencia cancelada.")
                ventana_transferencia.destroy()
                return
            
            # Proceder con la transferencia
            cuenta_origen = datos_validos['cuenta_origen']
            cuenta_destino = datos_validos['cuenta_destino']
            monto = datos_validos['monto']
            saldo_origen = datos_validos['saldo_origen']
            destinatario = datos_validos['destinatario']
            tipo_destino = datos_validos['tipo_destino']
            datos_cuentas = datos_validos['datos_cuentas']
            cuentas_destino = datos_validos['cuentas_destino']

            # Realizar transferencia
            nuevo_saldo_origen = saldo_origen - monto
            saldo_destino = float(cuenta_destino['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            nuevo_saldo_destino = saldo_destino + monto

            # Actualizar saldos
            cuenta_origen['saldo'] = f"${nuevo_saldo_origen:,.0f}".replace(',', '.')
            cuenta_destino['saldo'] = f"${nuevo_saldo_destino:,.0f}".replace(',', '.')

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
        boton_confirmar = ttk.Button(ventana_transferencia, text="Confirmar Transferencia", command=confirmar_transferencia)
        boton_confirmar.pack(pady=20)

        # Botón para cancelar
        ttk.Button(ventana_transferencia, text="Cancelar", command=ventana_transferencia.destroy).pack(pady=5)

        # Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_transferencia)

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