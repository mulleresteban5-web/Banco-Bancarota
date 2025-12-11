import tkinter as tk
from tkinter import messagebox, ttk
import json as js
import re  # Agregar esta importación para usar expresiones regulares
import random  # Agregar esta importación para generar números de cuenta aleatorios
from datetime import datetime  # Para la hora del préstamo

#Diferencia con login_4: Validación de RUT con módulo 11

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sistema de Login')
        self.geometry("850x600")
        self.configure(bg="#b5ddd8")

        # Inicializar usuarios predefinidos en los JSON
        self.inicializar_predefinidos()
        
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

    def inicializar_predefinidos(self):
        """Crea los usuarios predefinidos en usuarios_cuentas.json si no existen"""
        usuarios_predefinidos = [
            {"nombre_completo": "Gerente Pérez", "rut": "11111111-1", "contraseña": "gerente123", "tipo": "gerente"},
            {"nombre_completo": "Ana López", "rut": "22222222-2", "contraseña": "ana123", "tipo": "cliente", "sucursal": "Osorno"},
            {"nombre_completo": "Pedro García", "rut": "33333333-3", "contraseña": "pedro123", "tipo": "cliente", "sucursal": "Valdivia"},
            {"nombre_completo": "Juan Martínez", "rut": "44444444-4", "contraseña": "juan123", "tipo": "cliente", "sucursal": "Temuco"}
        ]

        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos = js.load(archivo)
                if not isinstance(datos, list):
                    datos = []
        except (FileNotFoundError, js.JSONDecodeError):
            datos = []

        # Agregar los predefinidos si no están
        for pred in usuarios_predefinidos:
            if not any(u['rut'] == pred['rut'] for u in datos):
                datos.append(pred)

        with open("usuarios_cuentas.json", 'w') as archivo:
            js.dump(datos, archivo)

        # Inicializar limites_prestamos.json
        try:
            with open("limites_prestamos.json", 'r') as archivo:
                limites = js.load(archivo)
                if not isinstance(limites, dict):
                    limites = {}
        except (FileNotFoundError, js.JSONDecodeError):
            limites = {}

        for pred in usuarios_predefinidos:
            if pred["rut"] not in limites:
                limites[pred["rut"]] = {"limite_prestamo": 500000, "prestamos_activos": []}

        with open("limites_prestamos.json", 'w') as archivo:
            js.dump(limites, archivo)

        # Inicializar sucursales.json con sucursales predefinidas (sin teléfono ni gerente)
        sucursales_predefinidas = [
            {"nombre": "Osorno", "direccion": "Dirección de Osorno", "clientes": []},
            {"nombre": "Valdivia", "direccion": "Dirección de Valdivia", "clientes": []},
            {"nombre": "Temuco", "direccion": "Dirección de Temuco", "clientes": []}
        ]

        try:
            with open("sucursales.json", 'r') as archivo:
                datos_sucursales = js.load(archivo)
                if not isinstance(datos_sucursales, list):
                    datos_sucursales = []
        except (FileNotFoundError, js.JSONDecodeError):
            datos_sucursales = []

        # Agregar predefinidas si no existen
        for pred in sucursales_predefinidas:
            if pred['nombre'] not in [s['nombre'] for s in datos_sucursales]:
                datos_sucursales.append(pred)

        with open("sucursales.json", 'w') as archivo:
            js.dump(datos_sucursales, archivo)

    
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

        # Etiqueta y campo para RUT de usuario
        texto_rut = tk.Label(self, text='RUT de usuario: ', font=('Arial', 30, 'bold'), 
                           bg='#b5ddd8', fg='white')
        texto_rut.pack(padx=25, pady=25)
        self.cuadro_texto_entrada_rut = tk.Entry(self, width=13, font=('Arial', 20))  # CAMBIO: Nuevo nombre de variable
        self.cuadro_texto_entrada_rut.pack(padx=25, pady=25)
        
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
        
        # Permitir login con Enter
        self.controller.bind('<Return>', lambda event: self.verificar_login())
    
    def verificar_login(self):
        """Función para verificar el login y manejar los datos"""
        rut_usuario = self.cuadro_texto_entrada_rut.get().strip()
        contraseña = self.cuadro_texto_entrada_contraseña.get().strip()

        # Validar que se ingresaron ambos campos
        if not rut_usuario or not contraseña:
            messagebox.showerror("Error", "Por favor ingresa RUT y contraseña")
            return
        
        # Validar formato de RUT
        if not re.match(r'^\d{7,8}-[\dKk]$', rut_usuario):
            messagebox.showerror("Error", "RUT inválido. Formato: 12345678-9 o 1234567-K")
            return
        
        # Validar que la contraseña no contenga espacios ni caracteres especiales (solo letras y números)
        if not re.match(r'^[a-zA-Z0-9]+$', contraseña):
            messagebox.showerror("Error", "La contraseña solo puede contener letras y números, sin espacios ni caracteres especiales")
            return

        # Verificar si es gerente (por RUT fijo)
        if rut_usuario == "11111111-1":
            if contraseña == "gerente123":
                self.controller.usuario_actual = "Gerente Pérez"  # Setear nombre completo
                self.controller.tipo_usuario = "gerente"
                
                # Verificar bloqueo antes de proceder
                try:
                    with open("usuarios_cuentas.json", 'r') as archivo:
                        datos = js.load(archivo)
                        if not isinstance(datos, list):
                            datos = []
                except (FileNotFoundError, js.JSONDecodeError):
                    datos = []
                
                usuario_encontrado = None
                for u in datos:
                    if u['rut'] == rut_usuario:
                        usuario_encontrado = u
                        break
                
                if usuario_encontrado and usuario_encontrado.get('bloqueado', False):
                    messagebox.showwarning("Usuario bloqueado", "Usuario bloqueado, sospecha de fraude")
                    self.cuadro_texto_entrada_rut.delete(0, tk.END)
                    self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                    return
                
                # Limpiar campos y mostrar notebook
                self.cuadro_texto_entrada_rut.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Gerente
                messagebox.showerror("Error", "Contraseña incorrecta para Gerente Pérez")
                return
            
        # Verificar si es cliente específico: Ana (por RUT fijo)
        elif rut_usuario == "22222222-2":
            if contraseña == "ana123":
                self.controller.usuario_actual = "Ana López"  # Setear nombre completo
                self.controller.tipo_usuario = "cliente"
                
                # Verificar bloqueo antes de proceder
                try:
                    with open("usuarios_cuentas.json", 'r') as archivo:
                        datos = js.load(archivo)
                        if not isinstance(datos, list):
                            datos = []
                except (FileNotFoundError, js.JSONDecodeError):
                    datos = []
                
                usuario_encontrado = None
                for u in datos:
                    if u['rut'] == rut_usuario:
                        usuario_encontrado = u
                        break
                
                if usuario_encontrado and usuario_encontrado.get('bloqueado', False):
                    messagebox.showwarning("Usuario bloqueado", "Usuario bloqueado, sospecha de fraude")
                    self.cuadro_texto_entrada_rut.delete(0, tk.END)
                    self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                    return
                
                # Limpiar campos y mostrar notebook
                self.cuadro_texto_entrada_rut.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Ana
                messagebox.showerror("Error", "Contraseña incorrecta para Ana López")
                return
            
        # Verificar si es cliente específico: Pedro (por RUT fijo)
        elif rut_usuario == "33333333-3":
            if contraseña == "pedro123":
                self.controller.usuario_actual = "Pedro García"  # Setear nombre completo
                self.controller.tipo_usuario = "cliente"
                
                # Verificar bloqueo antes de proceder
                try:
                    with open("usuarios_cuentas.json", 'r') as archivo:
                        datos = js.load(archivo)
                        if not isinstance(datos, list):
                            datos = []
                except (FileNotFoundError, js.JSONDecodeError):
                    datos = []
                
                usuario_encontrado = None
                for u in datos:
                    if u['rut'] == rut_usuario:
                        usuario_encontrado = u
                        break
                
                if usuario_encontrado and usuario_encontrado.get('bloqueado', False):
                    messagebox.showwarning("Usuario bloqueado", "Usuario bloqueado, sospecha de fraude")
                    self.cuadro_texto_entrada_rut.delete(0, tk.END)
                    self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                    return
                
                # Limpiar campos y mostrar notebook
                self.cuadro_texto_entrada_rut.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Pedro
                messagebox.showerror("Error", "Contraseña incorrecta para Pedro García")
                return
            
        # Verificar si es cliente específico: Juan (por RUT fijo)
        elif rut_usuario == "44444444-4":
            if contraseña == "juan123":
                self.controller.usuario_actual = "Juan Martínez"  # Setear nombre completo
                self.controller.tipo_usuario = "cliente"
                
                # Verificar bloqueo antes de proceder
                try:
                    with open("usuarios_cuentas.json", 'r') as archivo:
                        datos = js.load(archivo)
                        if not isinstance(datos, list):
                            datos = []
                except (FileNotFoundError, js.JSONDecodeError):
                    datos = []
                
                usuario_encontrado = None
                for u in datos:
                    if u['rut'] == rut_usuario:
                        usuario_encontrado = u
                        break
                
                if usuario_encontrado and usuario_encontrado.get('bloqueado', False):
                    messagebox.showwarning("Usuario bloqueado", "Usuario bloqueado, sospecha de fraude")
                    self.cuadro_texto_entrada_rut.delete(0, tk.END)
                    self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                    return
                
                # Limpiar campos y mostrar notebook
                self.cuadro_texto_entrada_rut.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Contraseña incorrecta para Juan
                messagebox.showerror("Error", "Contraseña incorrecta para Juan Martínez")
                return
        else:
            # Verificar si es un usuario registrado en el JSON (Buscar por RUT)
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:
                    datos = js.load(archivo)
                    if not isinstance(datos, list):
                        datos = []
            except (FileNotFoundError, js.JSONDecodeError):
                datos = []
            
            usuario_encontrado = False
            nombre_completo_usuario = None  # Para obtener el nombre completo
            for usuario in datos:
                if usuario['rut'] == rut_usuario and usuario['contraseña'] == contraseña:  # Comparar por RUT
                    usuario_encontrado = True
                    nombre_completo_usuario = usuario['nombre_completo']  # Obtener nombre
                    break
            
            if usuario_encontrado:
                self.controller.usuario_actual = nombre_completo_usuario  # Setear nombre completo
                self.controller.tipo_usuario = "cliente"
                
                # NUEVO: Verificar bloqueo antes de proceder
                usuario_bloqueado = None
                for u in datos:
                    if u['rut'] == rut_usuario:
                        usuario_bloqueado = u
                        break
                
                if usuario_bloqueado and usuario_bloqueado.get('bloqueado', False):
                    messagebox.showwarning("Usuario bloqueado", "Usuario bloqueado, sospecha de fraude")
                    self.cuadro_texto_entrada_rut.delete(0, tk.END)
                    self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                    return
                
                # Limpiar campos y mostrar notebook
                self.cuadro_texto_entrada_rut.delete(0, tk.END)
                self.cuadro_texto_entrada_contraseña.delete(0, tk.END)
                self.controller.mostrar_frame("NotebookFrame")
            else:
                # Usuario no registrado
                messagebox.showerror("Error", "RUT o contraseña incorrectos. Verifica tus datos.")
                return

    def registrar_usuario(self):
        """Función para registrar un nuevo usuario"""
        # Crear ventana emergente para registro
        ventana_registro = tk.Toplevel(self)
        ventana_registro.title("Registro de Usuario")
        ventana_registro.geometry("400x450")  # Aumenté la altura para el nuevo campo
        ventana_registro.configure(bg="#b5ddd8")
        
        # Etiqueta y campo para nombre y apellido
        ttk.Label(ventana_registro, text="Nombre y Apellido:", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_nombre = ttk.Entry(ventana_registro, width=20, font=('Arial', 12))
        entrada_nombre.pack(pady=5)

        # Etiqueta y campo para RUT
        ttk.Label(ventana_registro, text="RUT (ej: 12345678-9):", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_rut = ttk.Entry(ventana_registro, width=20, font=('Arial', 12))
        entrada_rut.pack(pady=5)
        
        # Etiqueta y campo para contraseña
        ttk.Label(ventana_registro, text="Contraseña:", font=('Arial', 14, 'bold')).pack(pady=10)
        entrada_contraseña = ttk.Entry(ventana_registro, width=20, font=('Arial', 12), show='*')
        entrada_contraseña.pack(pady=5)
        
        # Etiqueta y Combobox para sucursal (cargar dinámicamente desde sucursales.json)
        ttk.Label(ventana_registro, text="Sucursal:", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Función para cargar sucursales desde JSON
        def cargar_sucursales_opciones():
            try:
                with open("sucursales.json", 'r') as archivo:
                    datos_sucursales = js.load(archivo)
                    if not isinstance(datos_sucursales, list):
                        datos_sucursales = []
                return [s.get('nombre', '') for s in datos_sucursales if s.get('nombre')]
            except (FileNotFoundError, js.JSONDecodeError):
                return ["Osorno", "Valdivia", "Temuco"]  # Fallback a predefinidas si no existe el archivo
        
        sucursales_opciones = cargar_sucursales_opciones()
        sucursal_var = tk.StringVar()
        combobox_sucursal = ttk.Combobox(ventana_registro, textvariable=sucursal_var, values=sucursales_opciones, state="readonly", width=18, font=('Arial', 12))
        combobox_sucursal.pack(pady=5)
        combobox_sucursal.set("")  # Sin selección por defecto
        
        def confirmar_registro():
            nombre_completo = entrada_nombre.get().strip()
            rut = entrada_rut.get().strip()
            contraseña = entrada_contraseña.get().strip()
            sucursal = sucursal_var.get().strip()
            
            # Validar campos
            if not nombre_completo or not rut or not contraseña or not sucursal:
                messagebox.showerror("Error", "Por favor ingresa nombre y apellido, RUT, contraseña y sucursal")
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
                if usuario['contraseña'] == contraseña:
                    messagebox.showerror("Error", "La contraseña ya está en uso por otro usuario. Elige una contraseña diferente.")
                    return
            
            # Verificar contra usuarios predefinidos
            usuarios_predefinidos = [
                {"nombre_completo": "Gerente Pérez", "rut": "11111111-1"},
                {"nombre_completo": "Ana López", "rut": "22222222-2"},
                {"nombre_completo": "Pedro García", "rut": "33333333-3"},
                {"nombre_completo": "Juan Martínez", "rut": "44444444-4"}
            ]
            for pred in usuarios_predefinidos:
                if pred['nombre_completo'] == nombre_completo or pred['rut'] == rut:
                    messagebox.showerror("Error", "El usuario ya existe. Elige otro.")
                    return
            
            # Guardar nuevo usuario con sucursal
            diccionario_a_guardar = {
                'nombre_completo': nombre_completo, 
                'rut': rut, 
                'contraseña': contraseña, 
                'tipo': 'cliente', 
                'sucursal': sucursal  # Nuevo campo
            }
            datos.append(diccionario_a_guardar)
            with open("usuarios_cuentas.json", 'w') as archivo:
                js.dump(datos, archivo)

            # Inicializar límites de préstamo en limites_prestamos.json
            try:
                with open("limites_prestamos.json", 'r') as archivo:
                    limites = js.load(archivo)
                    if not isinstance(limites, dict):
                        limites = {}
            except (FileNotFoundError, js.JSONDecodeError):
                limites = {}

            limites[rut] = {"limite_prestamo": 500000, "prestamos_activos": []}
            with open("limites_prestamos.json", 'w') as archivo:
                js.dump(limites, archivo)
            
            # Inicializar cuentas.json
            try:
                with open("cuentas.json", 'r') as archivo:
                    cuentas_globales = js.load(archivo)
                    if not isinstance(cuentas_globales, dict):
                        cuentas_globales = {}
            except (FileNotFoundError, js.JSONDecodeError):
                cuentas_globales = {}
            
            cuentas_globales[nombre_completo] = []
            with open("cuentas.json", 'w') as archivo:
                js.dump(cuentas_globales, archivo)

            # Inicializar historial de transferencias
            try:
                with open("historial_transferencias.json", 'r') as archivo:
                    historial_global = js.load(archivo)
                    if not isinstance(historial_global, dict):
                        historial_global = {}
            except (FileNotFoundError, js.JSONDecodeError):
                historial_global = {}

            historial_global[rut] = []
            with open("historial_transferencias.json", 'w') as archivo:
                js.dump(historial_global, archivo)

            # Inicializar historial de pagos de préstamos
            try:
                with open("historial_pagos_prestamos.json", 'r') as archivo:
                    historial_pagos = js.load(archivo)
                    if not isinstance(historial_pagos, dict):
                        historial_pagos = {}
            except (FileNotFoundError, js.JSONDecodeError):
                historial_pagos = {}

            historial_pagos[rut] = []
            with open("historial_pagos_prestamos.json", 'w') as archivo:
                js.dump(historial_pagos, archivo)

            messagebox.showinfo("Éxito", f"Usuario {nombre_completo} registrado exitosamente en {sucursal}. Ahora puedes iniciar sesión.")
            ventana_registro.destroy()
        
        # Botones
        ttk.Button(ventana_registro, text="Registrar", command=confirmar_registro).pack(pady=20)
        ttk.Button(ventana_registro, text="Cancelar", command=ventana_registro.destroy).pack(pady=5)

        # Centrar ventana
        self.controller.centrar_ventana_emergente(ventana_registro)
        ventana_registro.transient(self)
        ventana_registro.grab_set()
        self.wait_window(ventana_registro)

    def guardar_usuario(self, nombre_completo, rut, contraseña, tipo):
        """Función auxiliar para guardar usuario en el archivo JSON"""
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos = js.load(archivo) # Convierte el contenido del archivo JSON a una variable de Python.
                # Verificar que sea una lista; si no, reinicializar
                if not isinstance(datos, list): # Verifica que datos sea una lista
                    datos = []
        except (FileNotFoundError, js.JSONDecodeError):
            # Si no existe o está corrupto, iniciar con lista vacía
            datos = []

        diccionario_a_guardar = {'nombre_completo': nombre_completo, 'rut': rut, 'contraseña': contraseña, 'tipo': tipo} # Crea un diccionario con los datos del usuario
        datos.append(diccionario_a_guardar) # Agrega ese diccionario a la lista datos.

        with open("usuarios_cuentas.json", 'w') as archivo: 
            js.dump(datos, archivo) # Guarda (escribe) la variable datos dentro del archivo en formato JSON.
    
        # Mostrar mensaje y cambiar al notebook
        self.controller.mostrar_frame("NotebookFrame") #Jeremias final

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
        
        ttk.Label(pestana1, text="Administración de Sucursales", font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Frame para botones de sucursales
        frame_botones_sucursal = ttk.Frame(pestana1)
        frame_botones_sucursal.pack(pady=10)
        
        ttk.Button(frame_botones_sucursal, text="Agregar Sucursal", command=self.agregar_sucursal).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_sucursal, text="Actualizar", command=self.actualizar_sucursales).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_sucursal, text="Eliminar Sucursal", command=self.eliminar_sucursal).pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar sucursales (quitar columnas telefono y gerente)
        self.tree_sucursales = ttk.Treeview(pestana1, columns=("nombre", "direccion", "clientes"), show="headings", height=12)
        self.tree_sucursales.heading("nombre", text="Nombre")
        self.tree_sucursales.heading("direccion", text="Dirección")
        self.tree_sucursales.heading("clientes", text="Clientes")
        self.tree_sucursales.column("nombre", width=120)
        self.tree_sucursales.column("direccion", width=150)
        self.tree_sucursales.column("clientes", width=80)
        self.tree_sucursales.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Pestaña 2 - Clientes
        pestana2 = ttk.Frame(self.notebook)
        self.notebook.add(pestana2, text="Gestión de Clientes")
        
        ttk.Label(pestana2, text="Gestión de Clientes por Sucursal", font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Frame para selector de sucursal
        frame_selector = ttk.Frame(pestana2)
        frame_selector.pack(pady=10, fill=tk.X, padx=20)
        
        ttk.Label(frame_selector, text="Sucursal:", font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        self.combo_sucursales = ttk.Combobox(frame_selector, state="readonly", width=30)
        self.combo_sucursales.pack(side=tk.LEFT, padx=5)
                
        # Cargar sucursales en el combo inmediatamente
        self.actualizar_combo_sucursales()
        
        ttk.Button(frame_selector, text="Asignar Cliente a Sucursal", command=self.asignar_cliente_sucursal).pack(side=tk.LEFT, padx=5)
        
        # Botón para cargar clientes. Si hay una sucursal seleccionada, carga solo esa sucursal;
        # de lo contrario, carga todos los clientes.
        def _cargar_clientes_segun_sucursal():
            if self.combo_sucursales.get():
                self.cargar_clientes_por_sucursal()
            else:
                self.cargar_clientes()

        ttk.Button(pestana2, text="Cargar Clientes", command=_cargar_clientes_segun_sucursal).pack(pady=10)
        
        # Treeview para mostrar clientes (hacerlo atributo de clase para poder acceder desde otros métodos)
        self.tree_clientes = ttk.Treeview(pestana2, 
        columns=("nombre", "rut", "tipo", "limite", "prestamos", "sucursal"), 
        show="headings", height=12)

        self.tree_clientes.heading("nombre", text="Nombre")
        self.tree_clientes.heading("rut", text="RUT")
        self.tree_clientes.heading("tipo", text="Tipo")
        self.tree_clientes.heading("limite", text="Límite Préstamo")
        self.tree_clientes.heading("prestamos", text="Préstamos Activos")
        self.tree_clientes.heading("sucursal", text="Sucursal")

        self.tree_clientes.column("nombre", width=120)
        self.tree_clientes.column("rut", width=90)
        self.tree_clientes.column("tipo", width=70)
        self.tree_clientes.column("limite", width=90)
        self.tree_clientes.column("prestamos", width=100)
        self.tree_clientes.column("sucursal", width=100)

        self.tree_clientes.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame para botones de acciones
        frame_acciones = ttk.Frame(pestana2)
        frame_acciones.pack(pady=10)
    
        ttk.Button(frame_acciones, text="Modificar Límite", 
               command=self.modificar_limite).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_acciones, text="Ver Cuentas del Cliente", 
               command=self.ver_cuentas_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_acciones, text="Bloquear/Desbloquear", 
               command=self.bloquear_cliente).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_acciones, text="Eliminar Cuenta", 
               command=self.eliminar_cliente).pack(side=tk.LEFT, padx=5)

        # Pestaña 3 - Reportes
        pestana3 = ttk.Frame(self.notebook)
        self.notebook.add(pestana3, text="Reportes")
        
        ttk.Label(pestana3, text="Reportes del Sistema", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Button(pestana3, text="Generar Reporte Mensual").pack(pady=10)
        ttk.Button(pestana3, text="Estadísticas").pack(pady=10)
        
        # Pestaña 4 - Cuentas Eliminadas
        pestana4 = ttk.Frame(self.notebook)
        self.notebook.add(pestana4, text="Cuentas Eliminadas")
        
        ttk.Label(pestana4, text="Cuentas Eliminadas (Papelera)", font=('Arial', 14, 'bold')).pack(pady=20)
        
        # Botón para cargar cuentas eliminadas
        ttk.Button(pestana4, text="Cargar Cuentas Eliminadas", command=self.cargar_cuentas_eliminadas).pack(pady=10)
        
        # Treeview para mostrar cuentas eliminadas
        self.tree_eliminadas = ttk.Treeview(pestana4, 
        columns=("nombre", "rut", "tipo", "limite", "fecha_eliminacion"), 
        show="headings", height=15)

        self.tree_eliminadas.heading("nombre", text="Nombre")
        self.tree_eliminadas.heading("rut", text="RUT")
        self.tree_eliminadas.heading("tipo", text="Tipo")
        self.tree_eliminadas.heading("limite", text="Límite Préstamo")
        self.tree_eliminadas.heading("fecha_eliminacion", text="Fecha Eliminación")

        self.tree_eliminadas.column("nombre", width=150)
        self.tree_eliminadas.column("rut", width=100)
        self.tree_eliminadas.column("tipo", width=80)
        self.tree_eliminadas.column("limite", width=100)
        self.tree_eliminadas.column("fecha_eliminacion", width=130)

        self.tree_eliminadas.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame para botones de acciones en papelera
        frame_papelera = ttk.Frame(pestana4)
        frame_papelera.pack(pady=10)
    
        ttk.Button(frame_papelera, text="Restaurar Cuenta", 
               command=self.restaurar_cuenta_eliminada).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_papelera, text="Vaciar Papelera", 
               command=self.vaciar_papelera).pack(side=tk.LEFT, padx=5)
        
        # Pestaña 5 - Ayuda
        pestana5 = ttk.Frame(self.notebook)
        self.notebook.add(pestana5, text="Ayuda")
        
        ttk.Label(pestana5, text="Sistema de Ayuda - Modo Gerente", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(pestana5, text=f"Bienvenido: {self.controller.usuario_actual}").pack(pady=10)

        # Mostrar sucursales de inmediato
        self.cargar_sucursales()
        self.actualizar_sucursales()
        self.cargar_clientes()

    def cargar_clientes(self):
        """Carga los clientes desde usuarios_cuentas.json y los muestra en el treeview"""
        # Limpiar el treeview primero
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Configurar etiquetas (tags) para filas bloqueadas
        self.tree_clientes.tag_configure('bloqueado', background='#ffcccc', foreground='#660000')
        
        # Cargar datos de usuarios_cuentas.json
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return
        
        # Cargar sucursales para obtener información
        try:
            with open("sucursales.json", 'r') as archivo:
                datos_sucursales = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            datos_sucursales = []
        
        # Filtrar solo los clientes (excluir gerentes)
        clientes = [u for u in datos_usuarios if u.get('tipo') == 'cliente']
        
        # Cargar límites de préstamos desde limites_prestamos.json
        try:
            with open("limites_prestamos.json", 'r') as archivo:
                limites = js.load(archivo)
                if not isinstance(limites, dict):
                    limites = {}
        except (FileNotFoundError, js.JSONDecodeError):
            limites = {}
        
        # Asegurar que todos los clientes tengan un límite inicializado (si no existe, establecer $500000)
        for usuario in clientes:
            rut = usuario.get('rut')
            if rut not in limites:
                limites[rut] = {"limite_prestamo": 500000, "prestamos_activos": []}
        
        # Guardar los límites actualizados en caso de que se hayan agregado nuevos
        try:
            with open("limites_prestamos.json", 'w') as archivo:
                js.dump(limites, archivo, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los límites actualizados: {e}")
        
        # Insertar cada cliente en el treeview
        for usuario in clientes:
            nombre = usuario.get('nombre_completo', 'N/A')
            rut = usuario.get('rut', 'N/A')
            tipo = usuario.get('tipo', 'N/A')
            
            # Obtener límite desde limites_prestamos.json (ahora garantizado que existe)
            limite = limites.get(rut, {}).get("limite_prestamo", 0)
            prestamos = len(limites.get(rut, {}).get("prestamos_activos", []))
            
            bloqueado = usuario.get('bloqueado', False)
            sucursal = usuario.get('sucursal', 'Sin asignar')
            
            # Agregar indicador visual si está bloqueado
            if bloqueado:
                nombre = f"🔒 {nombre}"
            
            # Formatear límite con separador de miles
            limite_formateado = f"${limite:,.0f}".replace(',', '.')
            
            # Insertar con tag si está bloqueado
            if bloqueado:
                self.tree_clientes.insert("", "end", values=(nombre, rut, tipo, limite_formateado, prestamos, sucursal), tags=('bloqueado',))
            else:
                self.tree_clientes.insert("", "end", values=(nombre, rut, tipo, limite_formateado, prestamos, sucursal))
        
        # Actualizar combo de sucursales
        self.actualizar_combo_sucursales()
        
    def modificar_limite(self):
        """Modifica el límite de préstamo de un cliente seleccionado"""
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona un cliente")
            return
        
        item = self.tree_clientes.item(seleccion[0])
        nombre = item['values'][0]
        rut = item['values'][1]
        
        # Remover el candado del nombre si está presente
        nombre = nombre.replace("🔒 ", "").strip()
        
        # Cargar usuarios desde JSON
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return
        
        # Buscar al usuario
        usuario_encontrado = None
        for usuario in datos_usuarios:
            if usuario.get('nombre_completo') == nombre and usuario.get('rut') == rut:
                usuario_encontrado = usuario
                break
        
        if not usuario_encontrado:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        
        # Crear ventana emergente para ingresar nuevo límite
        ventana_limite = tk.Toplevel(self)
        ventana_limite.title("Modificar Límite de Préstamo")
        ventana_limite.geometry("400x250")
        ventana_limite.configure(bg="#b5ddd8")
        
        # Centrar ventana
        self.controller.centrar_ventana_emergente(ventana_limite)
        
        # Etiqueta con información del cliente
        ttk.Label(ventana_limite, text=f"Cliente: {nombre}", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Mostrar límite actual
        limite_actual = usuario_encontrado.get('limite_prestamo', 0)
        limite_formateado = f"${limite_actual:,.0f}".replace(',', '.')
        ttk.Label(ventana_limite, text=f"Límite Actual: {limite_formateado}", font=('Arial', 11)).pack(pady=5)
        
        # Frame para nuevo límite
        frame_limite = ttk.Frame(ventana_limite)
        frame_limite.pack(pady=15)
        
        ttk.Label(frame_limite, text="Nuevo Límite ($):").pack(side=tk.LEFT, padx=5)
        entrada_limite = ttk.Entry(frame_limite, width=15)
        entrada_limite.pack(side=tk.LEFT, padx=5)
        entrada_limite.focus()
        
        # Variable para almacenar el resultado
        resultado = {'guardado': False}
        
        def guardar_nuevo_limite():
            """Guarda el nuevo límite después de validación"""
            try:
                nuevo_limite = int(entrada_limite.get().replace(".", "").replace(",", ""))
                
                if nuevo_limite < 0:
                    messagebox.showerror("Error", "El límite debe ser un número positivo")
                    return
                
                # Actualizar límite en datos
                usuario_encontrado['limite_prestamo'] = nuevo_limite
                
                # Guardar en JSON
                try:
                    with open("usuarios_cuentas.json", 'w') as archivo:
                        js.dump(datos_usuarios, archivo, indent=2)
                    
                    nuevo_limite_formateado = f"${nuevo_limite:,.0f}".replace(',', '.')
                    messagebox.showinfo("Éxito", f"Límite actualizado a {nuevo_limite_formateado}")
                    
                    # Recargar tabla
                    self.cargar_clientes()
                    ventana_limite.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
            
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa un número válido")
        
        # Frame para botones
        frame_botones = ttk.Frame(ventana_limite)
        frame_botones.pack(pady=20)
        
        ttk.Button(frame_botones, text="Guardar", command=guardar_nuevo_limite).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Cancelar", command=ventana_limite.destroy).pack(side=tk.LEFT, padx=5)

    def ver_cuentas_cliente(self):
        """Muestra información detallada del cliente seleccionado en una ventana emergente"""
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona un cliente")
            return
        
        item = self.tree_clientes.item(seleccion[0])
        nombre = item['values'][0]
        rut = item['values'][1]
        
        # Remover el candado del nombre si está presente
        nombre = nombre.replace("🔒 ", "").strip()
        
        # Cargar datos del cliente desde usuarios_cuentas.json
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return
        
        # Buscar al cliente
        cliente = None
        for u in datos_usuarios:
            if u.get('nombre_completo') == nombre and u.get('rut') == rut:
                cliente = u
                break
        
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        
        # Cargar cuentas del cliente desde cuentas.json
        try:
            with open("cuentas.json", 'r') as archivo:
                datos_cuentas = js.load(archivo)
                if not isinstance(datos_cuentas, dict):
                    datos_cuentas = {}
        except (FileNotFoundError, js.JSONDecodeError):
            datos_cuentas = {}
        
        cuentas_cliente = datos_cuentas.get(cliente['nombre_completo'], [])
        
        # Crear ventana emergente para mostrar información
        ventana_info = tk.Toplevel(self)
        ventana_info.title(f"Información de {cliente['nombre_completo']}")
        ventana_info.geometry("500x400")
        ventana_info.configure(bg="#b5ddd8")
        
        self.controller.centrar_ventana_emergente(ventana_info)
        
        # Etiquetas con información básica
        ttk.Label(ventana_info, text=f"Nombre: {cliente['nombre_completo']}", font=('Arial', 12, 'bold')).pack(pady=5)
        ttk.Label(ventana_info, text=f"RUT: {cliente['rut']}", font=('Arial', 12)).pack(pady=5)
        ttk.Label(ventana_info, text=f"Tipo: {cliente['tipo']}", font=('Arial', 12)).pack(pady=5)
        ttk.Label(ventana_info, text=f"Sucursal: {cliente.get('sucursal', 'Sin asignar')}", font=('Arial', 12)).pack(pady=5)
        ttk.Label(ventana_info, text=f"Bloqueado: {'Sí' if cliente.get('bloqueado', False) else 'No'}", font=('Arial', 12)).pack(pady=5)
        
        # Sección de cuentas
        ttk.Label(ventana_info, text="Cuentas:", font=('Arial', 12, 'bold')).pack(pady=10)
        
        if cuentas_cliente:
            for cuenta in cuentas_cliente:
                ttk.Label(ventana_info, text=f"- {cuenta['tipo']}: {cuenta['numero']} (Saldo: {cuenta['saldo']})", font=('Arial', 11)).pack(pady=2)
        else:
            ttk.Label(ventana_info, text="No tiene cuentas registradas", font=('Arial', 11)).pack(pady=5)
        
        # Botón para cerrar
        ttk.Button(ventana_info, text="Cerrar", command=ventana_info.destroy).pack(pady=20)
        
        ventana_info.transient(self)
        ventana_info.grab_set()
        self.wait_window(ventana_info)
        

    def bloquear_cliente(self):
        """Bloquea o desbloquea un cliente seleccionado"""
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona un cliente")
            return
        
        item = self.tree_clientes.item(seleccion[0])
        nombre = item['values'][0]
        rut = item['values'][1]
        
        # Remover el candado del nombre si está presente
        nombre = nombre.replace("🔒 ", "").strip()
        
        # Cargar usuarios desde JSON
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return
        
        # Buscar y actualizar el estado de bloqueo del usuario
        usuario_encontrado = False
        for usuario in datos_usuarios:
            if usuario.get('nombre_completo') == nombre and usuario.get('rut') == rut:
                # Alternar estado de bloqueo
                bloqueado = usuario.get('bloqueado', False)
                usuario['bloqueado'] = not bloqueado
                usuario_encontrado = True
                
                # Guardar cambios
                try:
                    with open("usuarios_cuentas.json", 'w') as archivo:
                        js.dump(datos_usuarios, archivo, indent=2)
                    
                    estado = "bloqueado" if usuario['bloqueado'] else "desbloqueado"
                    messagebox.showinfo("Éxito", f"Cliente {nombre} {estado} correctamente")
                    
                    # Recargar la tabla
                    self.cargar_clientes()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
                break
        
        if not usuario_encontrado:
            messagebox.showerror("Error", "Cliente no encontrado")

    def cargar_sucursales(self):
        """Carga y muestra las sucursales desde sucursales.json"""
        # Limpiar el treeview primero
        for item in self.tree_sucursales.get_children():
            self.tree_sucursales.delete(item)
        
        # Cargar datos de sucursales.json
        try:
            with open("sucursales.json", 'r') as archivo:
                datos_sucursales = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showinfo("Info", "No hay sucursales registradas")
            return
        
        # Insertar cada sucursal en el treeview
        for sucursal in datos_sucursales:
            nombre = sucursal.get('nombre', 'N/A')
            direccion = sucursal.get('direccion', 'N/A')
            clientes_count = len(sucursal.get('clientes', []))
            
            self.tree_sucursales.insert("", "end", values=(nombre, direccion, clientes_count))
        
    def actualizar_sucursales(self):
        """Actualiza el contador de clientes por sucursal"""
        # Cargar usuarios desde usuarios_cuentas.json
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return
        
        # Cargar sucursales
        try:
            with open("sucursales.json", 'r') as archivo:
                datos_sucursales = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showinfo("Info", "No hay sucursales registradas")
            return
        
        # Recalcular clientes por sucursal
        for sucursal in datos_sucursales:
            nombre_sucursal = sucursal.get('nombre')
            clientes_en_sucursal = [u for u in datos_usuarios if u.get('sucursal') == nombre_sucursal]
            sucursal['clientes'] = [c.get('rut') for c in clientes_en_sucursal]
        
        # Guardar cambios
        try:
            with open("sucursales.json", 'w') as archivo:
                js.dump(datos_sucursales, archivo, indent=2)
            
            self.cargar_sucursales()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")

    def agregar_sucursal(self):
        """Abre una ventana para agregar una nueva sucursal"""
        ventana_agregar = tk.Toplevel(self)
        ventana_agregar.title("Agregar Nueva Sucursal")
        ventana_agregar.geometry("450x350")
        ventana_agregar.configure(bg="#b5ddd8")
        
        self.controller.centrar_ventana_emergente(ventana_agregar)
        
        # Campos de entrada
        ttk.Label(ventana_agregar, text="Nombre de Sucursal:", font=('Arial', 11, 'bold')).pack(pady=5)
        entrada_nombre = ttk.Entry(ventana_agregar, width=30)
        entrada_nombre.pack(pady=5)
        
        ttk.Label(ventana_agregar, text="Dirección:", font=('Arial', 11, 'bold')).pack(pady=5)
        entrada_direccion = ttk.Entry(ventana_agregar, width=30)
        entrada_direccion.pack(pady=5)
        
        def guardar_sucursal():
            nombre = entrada_nombre.get().strip()
            direccion = entrada_direccion.get().strip()
            
            if not nombre or not direccion:
                messagebox.showerror("Error", "Por favor completa todos los campos obligatorios")
                return
            
            # Cargar sucursales existentes
            try:
                with open("sucursales.json", 'r') as archivo:
                    datos_sucursales = js.load(archivo)
                    if not isinstance(datos_sucursales, list):
                        datos_sucursales = []
            except (FileNotFoundError, js.JSONDecodeError):
                datos_sucursales = []
            
            # Verificar que la sucursal no exista
            for sucursal in datos_sucursales:
                if sucursal.get('nombre').lower() == nombre.lower():
                    messagebox.showerror("Error", "Esta sucursal ya existe")
                    return
            
            # Agregar nueva sucursal
            nueva_sucursal = {
                'nombre': nombre,
                'direccion': direccion,
                'clientes': []
            }
            datos_sucursales.append(nueva_sucursal)
            
            # Guardar en JSON
            try:
                with open("sucursales.json", 'w') as archivo:
                    js.dump(datos_sucursales, archivo, indent=2)
                
                messagebox.showinfo("Éxito", f"Sucursal '{nombre}' agregada correctamente")
                self.cargar_sucursales()
                ventana_agregar.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la sucursal: {e}")
        
        ttk.Button(ventana_agregar, text="Guardar Sucursal", command=guardar_sucursal).pack(pady=20)
        ttk.Button(ventana_agregar, text="Cancelar", command=ventana_agregar.destroy).pack(pady=5)

    def eliminar_sucursal(self):
        """Elimina una sucursal seleccionada"""
        seleccion = self.tree_sucursales.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona una sucursal")
            return
        
        item = self.tree_sucursales.item(seleccion[0])
        nombre_sucursal = item['values'][0]
        
        respuesta = messagebox.askyesno("Confirmar", f"¿Deseas eliminar la sucursal '{nombre_sucursal}'?")
        if not respuesta:
            return
        
        # Cargar sucursales
        try:
            with open("sucursales.json", 'r') as archivo:
                datos_sucursales = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de sucursales")
            return
        
        # Buscar y eliminar sucursal
        for i, sucursal in enumerate(datos_sucursales):
            if sucursal.get('nombre') == nombre_sucursal:
                datos_sucursales.pop(i)
                
                # Guardar cambios
                try:
                    with open("sucursales.json", 'w') as archivo:
                        js.dump(datos_sucursales, archivo, indent=2)
                    
                    messagebox.showinfo("Éxito", f"Sucursal '{nombre_sucursal}' eliminada correctamente")
                    self.cargar_sucursales()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
                break

    def actualizar_combo_sucursales(self):
        """Actualiza el combo de sucursales en la pestaña de clientes con opciones fijas y dinámicas"""
        # Sucursales fijas
        sucursales_fijas = ["Osorno", "Valdivia", "Temuco"]
        
        # Sucursales dinámicas desde sucursales.json
        try:
            with open("sucursales.json", 'r') as archivo:
                datos_sucursales = js.load(archivo)
            sucursales_dinamicas = [s.get('nombre', '') for s in datos_sucursales if s.get('nombre')]
        except (FileNotFoundError, js.JSONDecodeError):
            sucursales_dinamicas = []
        
        # Combinar fijas y dinámicas (sin duplicados)
        todas_sucursales = list(set(sucursales_fijas + sucursales_dinamicas))
        self.combo_sucursales['values'] = todas_sucursales
        
        if todas_sucursales:
            self.combo_sucursales.current(0)

    def cargar_clientes_por_sucursal(self):
        """Carga solo los clientes de la sucursal seleccionada"""
        sucursal_seleccionada = self.combo_sucursales.get()
        
        if not sucursal_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una sucursal")
            return
        
        # Limpiar treeview
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Cargar usuarios
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return
        
        # Filtrar clientes de la sucursal seleccionada
        clientes_sucursal = [u for u in datos_usuarios if u.get('tipo') == 'cliente' and u.get('sucursal') == sucursal_seleccionada]
        
        # Cargar límites de préstamos desde limites_prestamos.json
        try:
            with open("limites_prestamos.json", 'r') as archivo:
                limites = js.load(archivo)
                if not isinstance(limites, dict):
                    limites = {}
        except (FileNotFoundError, js.JSONDecodeError):
            limites = {}
        
        # Mostrar clientes
        for usuario in clientes_sucursal:
            nombre = usuario.get('nombre_completo', 'N/A')
            rut = usuario.get('rut', 'N/A')
            tipo = usuario.get('tipo', 'N/A')
            
            # Obtener límite desde limites_prestamos.json
            limite = limites.get(rut, {}).get("limite_prestamo", 0)
            prestamos = len(limites.get(rut, {}).get("prestamos_activos", []))
            
            bloqueado = usuario.get('bloqueado', False)
            sucursal = usuario.get('sucursal', 'Sin asignar')
            
            if bloqueado:
                nombre = f"🔒 {nombre}"
            
            limite_formateado = f"${limite:,.0f}".replace(',', '.')
            
            if bloqueado:
                self.tree_clientes.insert("", "end", values=(nombre, rut, tipo, limite_formateado, prestamos, sucursal), tags=('bloqueado',))
            else:
                self.tree_clientes.insert("", "end", values=(nombre, rut, tipo, limite_formateado, prestamos, sucursal))

    def asignar_cliente_sucursal(self):
        """Abre una ventana para asignar un cliente a una sucursal"""
        sucursal_seleccionada = self.combo_sucursales.get()
        
        if not sucursal_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor selecciona una sucursal primero")
            return
        
        ventana_asignar = tk.Toplevel(self)
        ventana_asignar.title("Asignar Cliente a Sucursal")
        ventana_asignar.geometry("450x300")
        ventana_asignar.configure(bg="#b5ddd8")
        
        self.controller.centrar_ventana_emergente(ventana_asignar)
        
        ttk.Label(ventana_asignar, text=f"Asignar cliente a: {sucursal_seleccionada}", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Cargar clientes disponibles
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return

        clientes = [u for u in datos_usuarios if u.get('tipo') == 'cliente']

        ttk.Label(ventana_asignar, text="Selecciona un cliente:", font=('Arial', 11, 'bold')).pack(pady=5)
        combo_clientes = ttk.Combobox(ventana_asignar, width=40)

        # Construir valores mostrando la sucursal actual de cada cliente
        # Formato estético: "Nombre (RUT) (Sucursal X)" cuando tenga sucursal
        valores = []
        for c in clientes:
            nombre = c.get('nombre_completo')
            rut = c.get('rut')
            base = f"{nombre} ({rut})"
            current = c.get('sucursal')
            if current:
                # Mostrar la sucursal entre paréntesis solamente
                label = f"{base} ({current})"
            else:
                label = base
            valores.append(label)

        combo_clientes['values'] = valores
        combo_clientes.pack(pady=10)

        def guardar_asignacion():
            cliente_seleccionado = combo_clientes.get()

            if not cliente_seleccionado:
                messagebox.showerror("Error", "Por favor selecciona un cliente")
                return

            # Extraer RUT desde la selección (formato: Nombre (RUT) ...)
            m = re.search(r"\(([^)]+)\)", cliente_seleccionado)
            if not m:
                messagebox.showerror("Error", "Formato de cliente inválido")
                return
            rut_seleccionado = m.group(1)

            # Encontrar el cliente por RUT
            cliente_encontrado = None
            for cliente in clientes:
                if cliente.get('rut') == rut_seleccionado:
                    cliente_encontrado = cliente
                    break

            if not cliente_encontrado:
                messagebox.showerror("Error", "Cliente no encontrado")
                return

            # Si ya pertenece a la sucursal, informar y no reasignar
            if cliente_encontrado.get('sucursal') == sucursal_seleccionada:
                messagebox.showinfo("Info", f"El cliente ya pertenece a {sucursal_seleccionada}")
                return

            # Si pertenece a otra sucursal, pedir confirmación para mover
            origen = cliente_encontrado.get('sucursal')
            if origen and origen != sucursal_seleccionada:
                mover = messagebox.askyesno("Confirmar movimiento", f"El cliente actualmente pertenece a '{origen}'.\n¿Deseas moverlo a '{sucursal_seleccionada}'?")
                if not mover:
                    return

            # Actualizar cliente con la sucursal
            cliente_encontrado['sucursal'] = sucursal_seleccionada

            # Guardar cambios en usuarios
            try:
                with open("usuarios_cuentas.json", 'w') as archivo:
                    js.dump(datos_usuarios, archivo, indent=2)

                # Recalcular y guardar clientes por sucursal
                try:
                    self.actualizar_sucursales()
                except Exception:
                    # Si hay algún fallo, al menos recargar vista
                    pass

                messagebox.showinfo("Éxito", f"Cliente asignado a {sucursal_seleccionada}")
                self.cargar_clientes_por_sucursal()
                ventana_asignar.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")

        ttk.Button(ventana_asignar, text="Asignar", command=guardar_asignacion).pack(pady=20)
        ttk.Button(ventana_asignar, text="Cancelar", command=ventana_asignar.destroy).pack(pady=5)

    def eliminar_cliente(self):
        """Envía un cliente a la papelera (no elimina definitivamente)"""
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona un cliente")
            return
        
        item = self.tree_clientes.item(seleccion[0])
        nombre = item['values'][0]
        rut = item['values'][1]
        
        # Remover el candado del nombre si está presente
        nombre = nombre.replace("🔒 ", "").strip()
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar", f"¿Deseas eliminar la cuenta de {nombre}?\nEsta acción se puede deshacer desde la papelera.")
        if not respuesta:
            return
        
        # Cargar usuarios desde JSON
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de usuarios")
            return
        
        # Cargar papelera (archivo de eliminados)
        try:
            with open("cuentas_eliminadas.json", 'r') as archivo:
                datos_eliminados = js.load(archivo)
                if not isinstance(datos_eliminados, list):
                    datos_eliminados = []
        except (FileNotFoundError, js.JSONDecodeError):
            datos_eliminados = []
        
        # Buscar y mover usuario a papelera
        usuario_encontrado = False
        for usuario in datos_usuarios:
            if usuario.get('nombre_completo') == nombre and usuario.get('rut') == rut:
                # Agregar fecha de eliminación
                usuario['fecha_eliminacion'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                # Agregar a papelera
                datos_eliminados.append(usuario)
                
                # Eliminar de usuarios_cuentas.json
                datos_usuarios.remove(usuario)
                usuario_encontrado = True
                
                # Guardar cambios
                try:
                    with open("usuarios_cuentas.json", 'w') as archivo:
                        js.dump(datos_usuarios, archivo, indent=2)
                    
                    with open("cuentas_eliminadas.json", 'w') as archivo:
                        js.dump(datos_eliminados, archivo, indent=2)
                    
                    messagebox.showinfo("Éxito", f"Cuenta de {nombre} eliminada y enviada a papelera")
                    
                    # Recargar la tabla
                    self.cargar_clientes()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
                break
        
        if not usuario_encontrado:
            messagebox.showerror("Error", "Cliente no encontrado")

    def cargar_cuentas_eliminadas(self):
        """Carga las cuentas eliminadas desde cuentas_eliminadas.json"""
        # Limpiar el treeview primero
        for item in self.tree_eliminadas.get_children():
            self.tree_eliminadas.delete(item)
        
        # Configurar etiqueta para cuentas bloqueadas en papelera
        self.tree_eliminadas.tag_configure('bloqueado', background='#ffcccc', foreground='#660000')
        
        # Cargar datos de cuentas_eliminadas.json
        try:
            with open("cuentas_eliminadas.json", 'r') as archivo:
                datos_eliminados = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showinfo("Info", "No hay cuentas eliminadas")
            return
        
        # Insertar cada cuenta eliminada en el treeview
        for usuario in datos_eliminados:
            nombre = usuario.get('nombre_completo', 'N/A')
            rut = usuario.get('rut', 'N/A')
            tipo = usuario.get('tipo', 'N/A')
            limite = usuario.get('limite_prestamo', 0)
            fecha_eliminacion = usuario.get('fecha_eliminacion', 'N/A')
            bloqueado = usuario.get('bloqueado', False)
            
            # Agregar indicador visual si está bloqueado
            if bloqueado:
                nombre = f"🔒 {nombre}"
            
            # Formatear límite con separador de miles
            limite_formateado = f"${limite:,.0f}".replace(',', '.')
            
            # Insertar con tag si está bloqueado
            if bloqueado:
                self.tree_eliminadas.insert("", "end", values=(nombre, rut, tipo, limite_formateado, fecha_eliminacion), tags=('bloqueado',))
            else:
                self.tree_eliminadas.insert("", "end", values=(nombre, rut, tipo, limite_formateado, fecha_eliminacion))
        
        messagebox.showinfo("Éxito", f"Se cargaron {len(datos_eliminados)} cuentas eliminadas")

    def restaurar_cuenta_eliminada(self):
        """Restaura una cuenta desde la papelera"""
        seleccion = self.tree_eliminadas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor selecciona una cuenta para restaurar")
            return
        
        item = self.tree_eliminadas.item(seleccion[0])
        nombre = item['values'][0]
        rut = item['values'][1]
        
        # Remover el candado del nombre si está presente
        nombre = nombre.replace("🔒 ", "").strip()
        
        # Confirmar restauración
        respuesta = messagebox.askyesno("Confirmar", f"¿Deseas restaurar la cuenta de {nombre}?")
        if not respuesta:
            return
        
        # Cargar eliminados desde JSON
        try:
            with open("cuentas_eliminadas.json", 'r') as archivo:
                datos_eliminados = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showerror("Error", "No se pudo cargar el archivo de cuentas eliminadas")
            return
        
        # Cargar usuarios actuales
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos_usuarios = js.load(archivo)
                if not isinstance(datos_usuarios, list):
                    datos_usuarios = []
        except (FileNotFoundError, js.JSONDecodeError):
            datos_usuarios = []
        
        # Buscar y restaurar usuario
        usuario_encontrado = False
        for usuario in datos_eliminados:
            if usuario.get('nombre_completo') == nombre and usuario.get('rut') == rut:
                # Remover fecha de eliminación
                if 'fecha_eliminacion' in usuario:
                    del usuario['fecha_eliminacion']
                
                # Restaurar a usuarios_cuentas.json
                datos_usuarios.append(usuario)
                
                # Eliminar de cuentas_eliminadas.json
                datos_eliminados.remove(usuario)
                usuario_encontrado = True
                
                # Guardar cambios
                try:
                    with open("usuarios_cuentas.json", 'w') as archivo:
                        js.dump(datos_usuarios, archivo, indent=2)
                    
                    with open("cuentas_eliminadas.json", 'w') as archivo:
                        js.dump(datos_eliminados, archivo, indent=2)
                    
                    messagebox.showinfo("Éxito", f"Cuenta de {nombre} restaurada correctamente")
                    
                    # Recargar las tablas
                    self.cargar_clientes()
                    self.cargar_cuentas_eliminadas()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")
                break
        
        if not usuario_encontrado:
            messagebox.showerror("Error", "Cuenta no encontrada en papelera")

    def vaciar_papelera(self):
        """Vacía la papelera eliminando definitivamente todas las cuentas"""
        try:
            with open("cuentas_eliminadas.json", 'r') as archivo:
                datos_eliminados = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            messagebox.showinfo("Info", "La papelera ya está vacía")
            return
        
        if not datos_eliminados:
            messagebox.showinfo("Info", "La papelera ya está vacía")
            return
        
        # Confirmar vaciado definitivo
        respuesta = messagebox.askyesno("Confirmar", 
            f"¿Deseas eliminar definitivamente {len(datos_eliminados)} cuenta(s)?\nEsta acción NO se puede deshacer.")
        if not respuesta:
            return
        
        try:
            # Crear archivo vacío
            with open("cuentas_eliminadas.json", 'w') as archivo:
                js.dump([], archivo, indent=2)
            
            messagebox.showinfo("Éxito", "Papelera vaciada correctamente. Las cuentas fueron eliminadas definitivamente.")
            
            # Recargar la tabla
            self.cargar_cuentas_eliminadas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo vaciar la papelera: {e}")

    
    def crear_interfaz_cliente(self):
        """Interfaz para el cliente con funcionalidades limitadas"""
        # Pestaña 1 - Mi Cuenta
        pestana1 = ttk.Frame(self.notebook)
        self.notebook.add(pestana1, text="Mi Cuenta")

        # Mensaje de bienvenida al usuario
        ttk.Label(pestana1, text=f"Bienvenido {self.controller.usuario_actual}", font=('Arial', 16, 'bold')).pack(pady=10)
    
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

        # Contenedor principal para la pestaña Ayuda (agregado para que las funciones funcionen)
        self.frame_ayuda = ttk.Frame(pestana3)
        self.frame_ayuda.pack(fill="both", expand=True)

        ttk.Label(self.frame_ayuda, text="Historial de movimientos", font=('Arial', 14, 'bold')).pack(pady=20)

        # Botones con command asignado
        ttk.Button(self.frame_ayuda, text="Historial de Transferencias", command=self.mostrar_historial_transferencias).pack(pady=10)
        ttk.Button(self.frame_ayuda, text="Historial de Préstamos", command=self.mostrar_historial_prestamos).pack(pady=10)

        # Frame para el Treeview de historial (inicialmente oculto)
        self.frame_historial = ttk.Frame(pestana3)
        self.frame_historial.pack(fill="both", expand=True)
        self.frame_historial.pack_forget()  # Ocultar inicialmente

    def mostrar_historial_transferencias(self):
        """Muestra el historial de transferencias en un Treeview"""
        # Ocultar contenido inicial
        self.frame_ayuda.pack_forget()
        self.frame_historial.pack(fill="both", expand=True)
    
        # Limpiar frame_historial si ya tiene widgets
        for widget in self.frame_historial.winfo_children():
            widget.destroy()
    
        # Etiqueta de título
        ttk.Label(self.frame_historial, text="Historial de Transferencias", font=('Arial', 14, 'bold')).pack(pady=10)
    
        # Obtener RUT del usuario actual
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
            pass
    
        if not rut_usuario:
            messagebox.showerror("Error", "RUT del usuario no encontrado.")
            self.volver_ayuda()  # Volver si no se encuentra
            return
    
        # Cargar datos del historial desde historial_transferencias.json usando RUT
        try:
            with open("historial_transferencias.json", 'r') as archivo:
                historial_global = js.load(archivo)
                if not isinstance(historial_global, dict):
                    historial_global = {}
        except (FileNotFoundError, js.JSONDecodeError):
            historial_global = {}
    
        historial = historial_global.get(rut_usuario, [])
    
        # Treeview para historial
        tree_historial = ttk.Treeview(self.frame_historial, columns=("Nombre", "Tipo_Cuenta", "Monto", "Fecha"), show="headings")
        tree_historial.heading("Nombre", text="Nombre")
        tree_historial.heading("Tipo_Cuenta", text="Tipo de Cuenta")
        tree_historial.heading("Monto", text="Monto")
        tree_historial.heading("Fecha", text="Fecha") 
    
        # Ajustar anchos
        tree_historial.column("Nombre", width=150)
        tree_historial.column("Tipo_Cuenta", width=120)
        tree_historial.column("Monto", width=100)
        tree_historial.column("Fecha", width=150)
    
        # Poblar Treeview
        for trans in historial:
            nombre = trans['destinatario'] if trans['tipo'] == 'enviada' else trans['remitente']
            tipo_cuenta = trans['tipo_cuenta']
            monto = f"-${trans['monto']:,.0f}" if trans['tipo'] == 'enviada' else f"{trans['monto']:,.0f}"
            fecha = trans['fecha']
            tree_historial.insert("", "end", values=(nombre, tipo_cuenta, monto, fecha))
    
        tree_historial.pack(fill="both", expand=True, pady=10)
    
        # Botón para volver
        ttk.Button(self.frame_historial, text="Volver", command=self.volver_ayuda).pack(pady=10)

    def mostrar_historial_prestamos(self):
        """Muestra el historial de préstamos en un Treeview"""
        # Ocultar contenido inicial
        self.frame_ayuda.pack_forget()
        self.frame_historial.pack(fill="both", expand=True)

        # Limpiar frame_historial
        for widget in self.frame_historial.winfo_children():
            widget.destroy()

        # Etiqueta de título
        ttk.Label(self.frame_historial, text="Historial de Préstamos", font=('Arial', 14, 'bold')).pack(pady=10)

        # Obtener RUT del usuario actual
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
            pass

        if not rut_usuario:
            messagebox.showerror("Error", "RUT del usuario no encontrado.")
            self.volver_ayuda()
            return

        # Cargar historial de pagos
        try:
            with open("historial_pagos_prestamos.json", 'r') as archivo:
                historial_pagos = js.load(archivo)
                if not isinstance(historial_pagos, dict):
                    historial_pagos = {}
        except (FileNotFoundError, js.JSONDecodeError):
            historial_pagos = {}

        pagos_usuario = historial_pagos.get(rut_usuario, [])

        # Agrupar pagos por id_prestamo
        prestamos_agrupados = {}
        for pago in pagos_usuario:
            id_prestamo = pago['id_prestamo']
            if id_prestamo not in prestamos_agrupados:
                prestamos_agrupados[id_prestamo] = []
            prestamos_agrupados[id_prestamo].append(pago)

        # Cargar préstamos activos desde limites_prestamos.json para obtener montos originales
        try:
            with open("limites_prestamos.json", 'r') as archivo:
                limites = js.load(archivo)
                if not isinstance(limites, dict):
                    limites = {}
        except (FileNotFoundError, js.JSONDecodeError):
            limites = {}

        prestamos_activos = limites.get(rut_usuario, {}).get("prestamos_activos", [])

        # Treeview para préstamos
        tree_prestamos = ttk.Treeview(self.frame_historial, columns=("ID", "Monto_Original", "Fecha_Pago", "Monto_Pagado"), show="headings")
        tree_prestamos.heading("ID", text="ID")
        tree_prestamos.heading("Monto_Original", text="Monto Original")
        tree_prestamos.heading("Fecha_Pago", text="Fecha de Pago")
        tree_prestamos.heading("Monto_Pagado", text="Monto Pagado")

        # Poblar Treeview
        for id_prestamo, pagos in prestamos_agrupados.items():
            # Obtener monto original del préstamo desde limites_prestamos.json
            monto_original = "N/A"
            for prestamo in prestamos_activos:
                if prestamo['id'] == id_prestamo:
                    monto_original = f"${prestamo['monto']:,.0f}".replace(',', '.')
                    break

            ultimo_pago = pagos[-1]  # Último pago
            fecha_pago = ultimo_pago['fecha_pago']
            monto_pagado = f"${ultimo_pago['monto_pagado']:,.0f}".replace(',', '.')
            tree_prestamos.insert("", "end", values=(id_prestamo, monto_original, fecha_pago, monto_pagado))

        tree_prestamos.pack(fill="both", expand=True, pady=10)

        # Botón para volver
        ttk.Button(self.frame_historial, text="Volver", command=self.volver_ayuda).pack(pady=10)

     
    def volver_ayuda(self):
        """Vuelve al contenido inicial de la pestaña Ayuda"""
        self.frame_historial.pack_forget()
        self.frame_ayuda.pack(fill="both", expand=True)

    def pedir_prestamo(self):
        """Método para pedir un préstamo bancario"""
        # Verificar si el cliente tiene al menos una cuenta
        if not self.cuentas_data:
            messagebox.showerror("Error", "Debes tener al menos una cuenta para pedir un préstamo.")
            return
        
        # Cargar límite de préstamo del usuario desde limites_prestamos.json
        usuario_actual = self.controller.usuario_actual
        limite_actual = 500000  # Valor por defecto si no existe
        rut_usuario = None
        
        # Obtener RUT del usuario actual
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
            pass
        
        if not rut_usuario:
            messagebox.showerror("Error", "RUT del usuario no encontrado.")
            return
        
        # Cargar límites desde limites_prestamos.json
        try:
            with open("limites_prestamos.json", 'r') as archivo:
                limites = js.load(archivo)
                if not isinstance(limites, dict):
                    limites = {}
        except (FileNotFoundError, js.JSONDecodeError):
            limites = {}
        
        # Inicializar si no existe
        if rut_usuario not in limites:
            limites[rut_usuario] = {"limite_prestamo": 500000, "prestamos_activos": []}
        
        limite_actual = limites[rut_usuario]["limite_prestamo"]
        
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
        
        # Etiqueta y campo para monto del préstamo
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
        
        # Variables para almacenar datos validados
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
                if monto > limite_actual:
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
            
            # Almacenar datos validados
            datos_validos.update({
                'cuenta_destino': cuenta_destino,
                'monto': monto
            })
            
            # Ocultar elementos y mostrar contraseña
            etiqueta_limite.pack_forget()
            etiqueta_monto.pack_forget()
            entrada_monto.pack_forget()
            etiqueta_cuenta.pack_forget()
            menu_cuenta.pack_forget()
            etiqueta_contraseña.pack(pady=10)
            entrada_contraseña.pack(pady=5)
            boton_confirmar.pack_forget()
            boton_cancelar.pack_forget()
            boton_confirmar.pack(pady=20)
            boton_cancelar.pack(pady=5)
            boton_confirmar.config(text="Validar Contraseña", command=validar_contraseña)
        
        def validar_contraseña():
            contraseña_ingresada = entrada_contraseña.get().strip()
            if not contraseña_ingresada:
                messagebox.showerror("Error", "Ingresa tu contraseña.")
                return
            
            usuario_actual = self.controller.usuario_actual
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

            # Reducir el límite en limites_prestamos.json
            nuevo_limite = limite_actual - monto
            limites[rut_usuario]["limite_prestamo"] = nuevo_limite
            
            # Agregar el préstamo a prestamos_activos en limites_prestamos.json
            prestamo_id = str(int(datetime.now().timestamp()))
            nuevo_prestamo = {
                'id': prestamo_id,
                'monto': monto,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'cuenta_destino': cuenta_destino['numero'],
                'saldo_pendiente': monto,
                'pagos': []
            }
            limites[rut_usuario]["prestamos_activos"].append(nuevo_prestamo)
            
            # Guardar limites_prestamos.json
            with open("limites_prestamos.json", 'w') as archivo:
                js.dump(limites, archivo)
            
            # Actualizar treeview y guardar cuentas
            self.actualizar_treeview()
            self.guardar_cuentas()
            
            messagebox.showinfo("Éxito", f"Préstamo de ${monto:,.0f} aprobado y depositado en la cuenta {cuenta_destino['tipo']} - {cuenta_destino['numero']}.")
            ventana_prestamo.destroy()
        
        # Botones
        boton_confirmar = ttk.Button(ventana_prestamo, text="Confirmar Préstamo", command=confirmar_prestamo)
        boton_confirmar.pack(pady=20)
        boton_cancelar = ttk.Button(ventana_prestamo, text="Cancelar", command=ventana_prestamo.destroy)
        boton_cancelar.pack(pady=5)

        # Centrar ventana
        self.controller.centrar_ventana_emergente(ventana_prestamo)
        ventana_prestamo.transient(self)
        ventana_prestamo.grab_set()
        self.wait_window(ventana_prestamo)


    def pagar_prestamo(self):
        """Método para pagar un préstamo activo"""
        usuario_actual = self.controller.usuario_actual
        
        # Obtener RUT del usuario actual
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
            pass
        
        if not rut_usuario:
            messagebox.showerror("Error", "RUT del usuario no encontrado.")
            return
        
        # Cargar límites y préstamos activos desde limites_prestamos.json
        try:
            with open("limites_prestamos.json", 'r') as archivo:
                limites = js.load(archivo)
                if not isinstance(limites, dict):
                    limites = {}
        except (FileNotFoundError, js.JSONDecodeError):
            limites = {}
        
        # Inicializar si no existe
        if rut_usuario not in limites:
            limites[rut_usuario] = {"limite_prestamo": 500000, "prestamos_activos": []}
        
        prestamos_activos = limites[rut_usuario]["prestamos_activos"]
        
        if not prestamos_activos:
            messagebox.showinfo("Información", "No tienes préstamos activos para pagar.")
            return
        
        # Crear ventana emergente para pagar préstamo
        ventana_pagar = tk.Toplevel(self)
        ventana_pagar.title("Pagar Préstamo")
        ventana_pagar.geometry("800x600")
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

        # Agregar selección de cuenta de origen (solo con saldo disponible)
        cuentas_con_saldo = [cuenta for cuenta in self.cuentas_data if float(cuenta['saldo'].replace('$', '').replace('.', '').replace(',', '')) > 0]
        if not cuentas_con_saldo:
            messagebox.showerror("Error", "No tienes cuentas con saldo disponible para realizar el pago.")
            ventana_pagar.destroy()
            return
        
        ttk.Label(ventana_pagar, text="Seleccione la cuenta de origen:", font=('Arial', 12, 'bold')).pack(pady=10)
        opciones_origen = [f"{c['tipo']} - {c['numero']} - Saldo: {c['saldo']}" for c in cuentas_con_saldo]
        origen_var = tk.StringVar(value=opciones_origen[0])
        menu_origen = tk.OptionMenu(ventana_pagar, origen_var, *opciones_origen)
        menu_origen.pack(pady=10)
    
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
            
            # Obtener la cuenta de origen seleccionada
            cuenta_origen_seleccionada = None
            for cuenta in cuentas_con_saldo:
                if f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" == origen_var.get():
                    cuenta_origen_seleccionada = cuenta
                    break
            if not cuenta_origen_seleccionada:
                messagebox.showerror("Error", "Cuenta de origen no encontrada.")
                return
            # Verificar saldo suficiente en la cuenta seleccionada
            saldo_cuenta_origen = float(cuenta_origen_seleccionada['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            if monto_pago > saldo_cuenta_origen:
                messagebox.showerror("Error", f"Saldo insuficiente en la cuenta seleccionada (${saldo_cuenta_origen:,.0f}).")
                return
            
            # Verificar que el usuario tenga saldo suficiente en alguna cuenta
            saldo_total = sum(float(cuenta['saldo'].replace('$', '').replace('.', '').replace(',', '')) for cuenta in self.cuentas_data)
            if monto_pago > saldo_total:
                messagebox.showerror("Error", "Saldo insuficiente en tus cuentas para realizar el pago.")
                return
            
            # Actualizar saldo pendiente del préstamo en limites_prestamos.json
            nuevo_saldo_pendiente = saldo_pendiente - monto_pago
            
            # Buscar y actualizar el préstamo en limites_prestamos.json
            prestamo_actualizado = False
            for prestamo in prestamos_activos:
                if prestamo['id'] == prestamo_id:
                    prestamo['saldo_pendiente'] = nuevo_saldo_pendiente
                    if nuevo_saldo_pendiente <= 0:
                        prestamos_activos.remove(prestamo)  # Eliminar si pagado completamente
                        print(f"Préstamo {prestamo_id} eliminado completamente.")  # Debug
                    prestamo_actualizado = True
                    break
            
            if not prestamo_actualizado:
                messagebox.showerror("Error", "Préstamo no encontrado para actualizar.")
                return
            
            # Guardar cambios en limites_prestamos.json
            try:
                with open("limites_prestamos.json", 'w') as archivo:
                    js.dump(limites, archivo)
                print(f"Datos guardados correctamente para {usuario_actual}.")  # Debug
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar los cambios en préstamos: {e}")
                return
            
            # Restar el monto de la cuenta seleccionada
            cuenta_origen_seleccionada['saldo'] = f"${saldo_cuenta_origen - monto_pago:,.0f}".replace(',', '.')
            
            # Actualizar treeview de cuentas
            self.actualizar_treeview()
            self.guardar_cuentas()

            # Guardar pago en historial_pagos_prestamos.json
            try:
                with open("historial_pagos_prestamos.json", 'r') as archivo:
                    historial_pagos = js.load(archivo)
                    if not isinstance(historial_pagos, dict):
                        historial_pagos = {}
            except (FileNotFoundError, js.JSONDecodeError):
                historial_pagos = {}

            if rut_usuario not in historial_pagos:
                historial_pagos[rut_usuario] = []

            pago_realizado = {
                'id_prestamo': prestamo_id,
                'fecha_pago': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'monto_pagado': monto_pago
            }
            historial_pagos[rut_usuario].append(pago_realizado)

            with open("historial_pagos_prestamos.json", 'w') as archivo:
                js.dump(historial_pagos, archivo)
            
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
    
    def crear_cuenta(self): #se crea una clase dentro de la principal
        """Método para crear una nueva cuenta bancaria"""
        # Crear una ventana emergente para ingresar datos de la nueva cuenta
        ventana_crear = tk.Toplevel(self) #se crea una ventana emergente con el toplavel
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
                if cuenta["tipo"] == tipo_seleccionado: #si alguna de las cuentas q el usuario tiene es igual a la seleccionada sale el mensagebox
                    messagebox.showerror("Error", f"Ya tienes una cuenta de tipo '{tipo_seleccionado}'. No puedes crear otra del mismo tipo.")
                    return
            
            # Obtener el RUT del usuario actual desde usuarios_cuentas.json
            usuario_actual = self.controller.usuario_actual 
            rut_usuario = None# se le asigna un valor nulo para iniciar la variable antes de que se busque por el json
            try:
                with open("usuarios_cuentas.json", 'r') as archivo:#se abre el archivo json en modo lectura
                    datos_usuarios = js.load(archivo)#convierte el json en una estructura de datos de python
                    if not isinstance(datos_usuarios, list): 
                        datos_usuarios = [] # al no ser una lista se le asigna un dato vacio
                for usuario in datos_usuarios:
                    if usuario['nombre_completo'] == usuario_actual: 
                        rut_usuario = usuario['rut']
                        break
            except (FileNotFoundError, js.JSONDecodeError): #archivo no encontrado o no formato de json
                messagebox.showerror("Error", "No se pudo acceder a los datos del usuario.")
                return
        
            if not rut_usuario: #verifica si el usuario sigue siendo none(no se encontro usuario)
                messagebox.showerror("Error", "RUT del usuario no encontrado.")
                return
        
            # Generar número de cuenta: si es "Cuenta Rut", usar el RUT sin guión; de lo contrario, aleatorio
            if tipo_seleccionado == "Cuenta Rut":
                numero_cuenta = rut_usuario.replace("-", "")
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

        # Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_crear)
    
        # Centrar la ventana emergente
        ventana_crear.transient(self)#ventana transitoria
        ventana_crear.grab_set()
        self.wait_window(ventana_crear) #Pausa la ejecución del código en la ventana padre hasta que se cierre la ventana secundaria

    def actualizar_treeview(self):
        """Actualiza el treeview con los datos actuales de cuentas"""
        # Limpiar treeview
        for item in self.tree2.get_children(): # Para cada elemento obtenido, lo elimina del treeview
            self.tree2.delete(item) #elimina el dato especifico del treeview
        
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

        # Centrar la ventana emergente después de agregar widgets
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

        # Frame inicial para los botones de selección
        frame_seleccion = ttk.Frame(ventana_transferencia)
        frame_seleccion.pack(pady=20)

        ttk.Label(frame_seleccion, text="Selecciona el tipo de transferencia:", font=('Arial', 14, 'bold')).pack(pady=10)

        # Botón para Transferir entre cuentas
        ttk.Button(frame_seleccion, text="Transferir entre cuentas", command=lambda: self.mostrar_transferencia_entre_cuentas(ventana_transferencia, frame_seleccion)).pack(pady=10)

        # Botón para Transferir a otros
        ttk.Button(frame_seleccion, text="Transferir a otros", command=lambda: self.mostrar_transferencia_a_otros(ventana_transferencia, frame_seleccion)).pack(pady=10)

        # Centrar la ventana emergente después de agregar widgets
        self.controller.centrar_ventana_emergente(ventana_transferencia)

        # Centrar ventana emergente
        ventana_transferencia.transient(self)
        ventana_transferencia.grab_set()
        self.wait_window(ventana_transferencia)

    def mostrar_transferencia_a_otros(self, ventana, frame_seleccion):
        """Función para mostrar el contenido de 'Transferir a otros' en la ventana emergente existente"""
        # Ocultar el frame de selección inicial
        frame_seleccion.pack_forget()

        # Etiqueta y OptionMenu para seleccionar cuenta de origen
        etiqueta_origen = ttk.Label(ventana, text="Seleccione la cuenta de origen:", font=('Arial', 12, 'bold'))
        etiqueta_origen.pack(pady=10)
        cuentas_origen = [f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" for cuenta in self.cuentas_data]
        if not cuentas_origen:
            messagebox.showerror("Error", "No tienes cuentas disponibles para transferir.")
            ventana.destroy()
            return
        origen_var = tk.StringVar(value=cuentas_origen[0])
        menu_origen = tk.OptionMenu(ventana, origen_var, *cuentas_origen)
        menu_origen.pack(pady=10)

        # Etiqueta y Combobox para seleccionar tipo de cuenta de destino (antes del destinatario)
        etiqueta_tipo = ttk.Label(ventana, text="Seleccione el tipo de cuenta de destino:", font=('Arial', 12, 'bold'))
        etiqueta_tipo.pack(pady=10)
        tipos_cuenta = ["Cuenta Vista", "Cuenta de Ahorros", "Cuenta Corriente", "Cuenta Rut"]
        tipo_destino_var = tk.StringVar()
        combobox_tipo = ttk.Combobox(ventana, textvariable=tipo_destino_var, values=tipos_cuenta, state="readonly")
        combobox_tipo.pack(pady=10)
        combobox_tipo.set(tipos_cuenta[0])  # Valor por defecto

        # Agregar etiqueta y campo para RUT del destinatario
        etiqueta_rut = ttk.Label(ventana, text="RUT del destinatario (ej: 12345678-9):", font=('Arial', 12, 'bold'))
        etiqueta_rut.pack(pady=10)
        entrada_rut = ttk.Entry(ventana, width=20, font=('Arial', 12))
        entrada_rut.pack(pady=5)

        # Etiqueta y campo para monto
        etiqueta_monto = ttk.Label(ventana, text="Monto a transferir (ej: 1000):", font=('Arial', 12, 'bold'))
        etiqueta_monto.pack(pady=10)
        entrada_monto = ttk.Entry(ventana, width=20, font=('Arial', 12))
        entrada_monto.pack(pady=5)

        # Elementos para validación de contraseña (inicialmente ocultos)
        etiqueta_contraseña = ttk.Label(ventana, text="Por favor ingrese su contraseña de usuario:", font=('Arial', 12, 'bold'))
        etiqueta_contraseña.pack_forget()
        entrada_contraseña = ttk.Entry(ventana, width=20, font=('Arial', 12), show='*')
        entrada_contraseña.pack_forget()
        
        # Variables para almacenar datos validados (se usan después de la contraseña)
        datos_validos = {}

        def confirmar_transferencia():
            # Obtener datos
            origen_seleccionado = origen_var.get()
            tipo_destino = tipo_destino_var.get()
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
                if u['rut'] == rut_destinatario:
                    usuario_encontrado = u
                    break
            
            if not usuario_encontrado:
                messagebox.showerror("Error", "Usuario no registrado o nombre y RUT no coinciden.")
                return
            
            # Asignar destinatario después de encontrar usuario
            destinatario = usuario_encontrado['nombre_completo']

            # Ahora validar destinatario (después de asignarlo)
            if not destinatario:
                messagebox.showerror("Error", "Ingresa el nombre del destinatario.")
                return
            
            # Cargar cuentas del destinatario
            try:
                with open("cuentas.json", 'r') as archivo:
                    datos_cuentas = js.load(archivo)
                    if not isinstance(datos_cuentas, dict):
                        datos_cuentas = {}
            except (FileNotFoundError, js.JSONDecodeError):
                datos_cuentas = {}

            # Se definen las cuentas predefinidas
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
            # Usar cuentas del archivo o por defecto si no existen
            cuentas_destino = datos_cuentas.get(destinatario, cuentas_por_defecto.get(destinatario, []))
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
                'cuentas_destino': cuentas_destino,
                'datos_usuarios': datos_usuarios
            })

            # Ocultar elementos anteriores y mostrar campo de contraseña
            etiqueta_origen.pack_forget()  #Ocultar etiqueta de origen
            menu_origen.pack_forget()
            etiqueta_tipo.pack_forget()  #Ocultar etiqueta de tipo
            combobox_tipo.pack_forget()
            etiqueta_rut.pack_forget()  # Ocultar etiqueta de RUT
            entrada_rut.pack_forget()  # Ocultar entrada de RUT
            etiqueta_monto.pack_forget()  #Ocultar etiqueta de monto
            entrada_monto.pack_forget()
            etiqueta_contraseña.pack(pady=10)
            entrada_contraseña.pack(pady=5)

            # "Olvidar" (ocultar) los botones para reordenarlos
            boton_confirmar.pack_forget()
            boton_cancelar.pack_forget()
            # Re-empaquetar los botones debajo del campo de contraseña
            boton_confirmar.pack(pady=20)
            boton_cancelar.pack(pady=5)

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

            # Obtener datos_usuarios desde datos_validos
            datos_usuarios = datos_validos['datos_usuarios']
            
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
                ventana.destroy()
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
            # Obtener RUTs
            rut_usuario = None
            rut_destinatario = None
            for usuario in datos_usuarios:  # datos_usuarios ya está cargado
                if usuario['nombre_completo'] == usuario_actual:
                    rut_usuario = usuario['rut']
                if usuario['nombre_completo'] == destinatario:
                    rut_destinatario = usuario['rut']
            
            if not rut_usuario or not rut_destinatario:
                messagebox.showerror("Error", "RUT no encontrado para guardar historial.")
                return
            
            # Guardar en historial_transferencias.json
            try:
                with open("historial_transferencias.json", 'r') as archivo:
                    historial_global = js.load(archivo)
                    if not isinstance(historial_global, dict):
                        historial_global = {}
            except (FileNotFoundError, js.JSONDecodeError):
                historial_global = {}
            
            # Para el remitente (usuario actual)
            if rut_usuario not in historial_global:
                historial_global[rut_usuario] = []
            nueva_trans_enviada = {
                'tipo': 'enviada',
                'destinatario': destinatario,
                'tipo_cuenta': tipo_destino,
                'monto': monto,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            historial_global[rut_usuario].append(nueva_trans_enviada)
            
            # Para el destinatario
            if rut_destinatario not in historial_global:
                historial_global[rut_destinatario] = []
            nueva_trans_recibida = {
                'tipo': 'recibida',
                'remitente': usuario_actual,
                'tipo_cuenta': tipo_destino,
                'monto': monto,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            historial_global[rut_destinatario].append(nueva_trans_recibida)
            
            with open("historial_transferencias.json", 'w') as archivo:
                js.dump(historial_global, archivo)
     
            ventana.destroy()

            # Agregar al historial
            nueva_trans = {
                'tipo': 'enviada',
                'destinatario': destinatario,
                'tipo_cuenta': tipo_destino,
                'monto': monto,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            # Guardar en usuarios_cuentas.json
            for usuario in datos_usuarios:
                if usuario['nombre_completo'] == usuario_actual:
                    if 'historial_transferencias' not in usuario:
                        usuario['historial_transferencias'] = []
                    usuario['historial_transferencias'].append(nueva_trans)
                    break
            with open("usuarios_cuentas.json", 'w') as archivo:
                js.dump(datos_usuarios, archivo)

            # Para el destinatario (transferencia recibida)
            for usuario in datos_usuarios:
                if usuario['nombre_completo'] == destinatario:
                    nueva_trans_recibida = {
                        'tipo': 'recibida',
                        'remitente': usuario_actual,
                        'tipo_cuenta': tipo_destino,
                        'monto': monto,
                        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    if 'historial_transferencias' not in usuario:
                        usuario['historial_transferencias'] = []
                    usuario['historial_transferencias'].append(nueva_trans_recibida)
                    break
            with open("usuarios_cuentas.json", 'w') as archivo:
                js.dump(datos_usuarios, archivo)

        # Botón para confirmar
        boton_confirmar = ttk.Button(ventana, text="Confirmar Transferencia", command=confirmar_transferencia)
        boton_confirmar.pack(pady=20)

        # Botón para cancelar
        boton_cancelar = ttk.Button(ventana, text="Cancelar", command=ventana.destroy)
        boton_cancelar.pack(pady=5)

    def mostrar_transferencia_entre_cuentas(self, ventana, frame_seleccion):
        # Ocultar frame de selección
        frame_seleccion.pack_forget()

        # Etiqueta y OptionMenu para cuenta de origen (solo con dinero)
        cuentas_con_dinero = [cuenta for cuenta in self.cuentas_data if float(cuenta['saldo'].replace('$', '').replace('.', '').replace(',', '')) > 0]
        if not cuentas_con_dinero:
            messagebox.showerror("Error", "No tienes cuentas con saldo disponible para transferir.")
            ventana.destroy()
            return

        etiqueta_origen = ttk.Label(ventana, text="Seleccione la cuenta de origen:", font=('Arial', 12, 'bold'))
        etiqueta_origen.pack(pady=10)
        opciones_origen = [f"{c['tipo']} - {c['numero']} - Saldo: {c['saldo']}" for c in cuentas_con_dinero]
        origen_var = tk.StringVar(value=opciones_origen[0])
        menu_origen = tk.OptionMenu(ventana, origen_var, *opciones_origen)
        menu_origen.pack(pady=10)

        # Etiqueta y OptionMenu para cuenta de destino (todas las cuentas)
        etiqueta_destino = ttk.Label(ventana, text="Seleccione la cuenta de destino:", font=('Arial', 12, 'bold'))
        etiqueta_destino.pack(pady=10)
        opciones_destino = [f"{c['tipo']} - {c['numero']} - Saldo: {c['saldo']}" for c in self.cuentas_data]
        destino_var = tk.StringVar(value=opciones_destino[0])
        menu_destino = tk.OptionMenu(ventana, destino_var, *opciones_destino)
        menu_destino.pack(pady=10)

        # Etiqueta y campo para monto
        etiqueta_monto = ttk.Label(ventana, text="Monto a transferir (ej: 1000):", font=('Arial', 12, 'bold'))
        etiqueta_monto.pack(pady=10)
        entrada_monto = ttk.Entry(ventana, width=20, font=('Arial', 12))
        entrada_monto.pack(pady=5)

        # Elementos para validación de contraseña (inicialmente ocultos)
        etiqueta_contraseña = ttk.Label(ventana, text="Por favor ingrese su contraseña de usuario:", font=('Arial', 12, 'bold'))
        etiqueta_contraseña.pack_forget()
        entrada_contraseña = ttk.Entry(ventana, width=20, font=('Arial', 12), show='*')
        entrada_contraseña.pack_forget()

        # Variables para almacenar datos validados
        datos_validos = {}

        def confirmar_transferencia_entre():
            """Función para confirmar la transferencia entre cuentas propias"""
            # Obtener datos
            origen_seleccionado = origen_var.get()
            destino_seleccionado = destino_var.get()
            monto_str = entrada_monto.get().strip()

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
            for cuenta in cuentas_con_dinero:  # Usar la lista filtrada de cuentas con dinero
                if f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" == origen_seleccionado:
                    cuenta_origen = cuenta
                    break
            if not cuenta_origen:
                messagebox.showerror("Error", "Cuenta de origen no encontrada.")
                return

            # Encontrar cuenta de destino
            cuenta_destino = None
            for cuenta in self.cuentas_data:  # Todas las cuentas del usuario
                if f"{cuenta['tipo']} - {cuenta['numero']} - Saldo: {cuenta['saldo']}" == destino_seleccionado:
                    cuenta_destino = cuenta
                    break
            if not cuenta_destino:
                messagebox.showerror("Error", "Cuenta de destino no encontrada.")
                return

            # Verificar saldo suficiente
            saldo_origen = float(cuenta_origen['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            if monto > saldo_origen:
                messagebox.showerror("Error", "Saldo insuficiente en la cuenta de origen.")
                return

            # Verificar que la cuenta de origen no sea la misma que la de destino
            if cuenta_origen['tipo'] == cuenta_destino['tipo'] and cuenta_origen['numero'] == cuenta_destino['numero']:
                messagebox.showerror("Error", "No puedes transferir dinero a la misma cuenta.")
                return

            # Almacenar datos validados para usar después de la contraseña
            datos_validos.update({
                'cuenta_origen': cuenta_origen,
                'cuenta_destino': cuenta_destino,
                'monto': monto,
                'saldo_origen': saldo_origen
            })

            # Ocultar elementos anteriores y mostrar campo de contraseña
            etiqueta_origen.pack_forget()
            menu_origen.pack_forget()
            etiqueta_destino.pack_forget()
            menu_destino.pack_forget()
            etiqueta_monto.pack_forget()
            entrada_monto.pack_forget()
            etiqueta_contraseña.pack(pady=10)
            entrada_contraseña.pack(pady=5)

            # "Olvidar" (ocultar) los botones para reordenarlos
            boton_confirmar.pack_forget()
            boton_cancelar.pack_forget()
            # Re-empaquetar los botones debajo del campo de contraseña
            boton_confirmar.pack(pady=20)
            boton_cancelar.pack(pady=5)

            # Cambiar el botón a "Validar Contraseña"
            boton_confirmar.config(text="Validar Contraseña", command=validar_contraseña_entre)

        def validar_contraseña_entre():
            """Función para validar la contraseña y proceder con la transferencia interna"""
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
                ventana.destroy()
                return

            # Proceder con la transferencia interna
            cuenta_origen = datos_validos['cuenta_origen']
            cuenta_destino = datos_validos['cuenta_destino']
            monto = datos_validos['monto']
            saldo_origen = datos_validos['saldo_origen']

            # Realizar transferencia
            nuevo_saldo_origen = saldo_origen - monto
            saldo_destino = float(cuenta_destino['saldo'].replace('$', '').replace('.', '').replace(',', ''))
            nuevo_saldo_destino = saldo_destino + monto

            # Actualizar saldos
            cuenta_origen['saldo'] = f"${nuevo_saldo_origen:,.0f}".replace(',', '.')
            cuenta_destino['saldo'] = f"${nuevo_saldo_destino:,.0f}".replace(',', '.')

            # Actualizar treeview
            self.actualizar_treeview()

            # Guardar cambios en cuentas.json
            self.guardar_cuentas()

            messagebox.showinfo("Éxito", f"Transferencia de ${monto:,.0f} realizada exitosamente entre tus cuentas.")
            ventana.destroy()


        # Botón para confirmar
        boton_confirmar = ttk.Button(ventana, text="Confirmar Transferencia", command=confirmar_transferencia_entre)
        boton_confirmar.pack(pady=20)

        # Botón para cancelar
        boton_cancelar = ttk.Button(ventana, text="Cancelar", command=ventana.destroy)  # <-- ASIGNADO A VARIABLE
        boton_cancelar.pack(pady=5)

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