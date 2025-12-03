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

        # Verificar si es gerente (hardcoded para demo)
        if nombre == "Gerente" and contraseña == "gerente123":
            self.controller.usuario_actual = nombre
            self.controller.tipo_usuario = "gerente"
            
            # Mostrar mensaje de éxito
            cadena_texto = f'Bienvenido Gerente: {nombre}'
            self.texto.config(text=cadena_texto)
            
            # Guardar datos del gerente (sin hash, en texto plano)
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
            # Es un cliente: verificar contra datos guardados
            clave_usuario = f"{nombre}_{contraseña}"  # Clave compuesta: nombre_contraseña
            stored_password = self.get_stored_password("cliente.json", nombre)
            if stored_password and stored_password == contraseña:
                self.controller.usuario_actual = clave_usuario  # Usar clave compuesta como identificador único
                self.controller.tipo_usuario = "cliente"
                
                # Mostrar mensaje de éxito
                cadena_texto = f'Bienvenido Cliente: {nombre}'
                self.texto.config(text=cadena_texto)
            else:
                # Si no existe, crear nuevo usuario cliente
                self.controller.usuario_actual = clave_usuario
                self.controller.tipo_usuario = "cliente"
                
                cadena_texto = f'Bienvenido Nuevo Cliente: {nombre}'
                self.texto.config(text=cadena_texto)
                
                # Guardar datos del cliente (sin hash, en texto plano)
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
        self.controller.mostrar_frame("NotebookFrame")
    
    def get_stored_password(self, filename, nombre):
        """Obtiene la contraseña almacenada para un usuario"""
        try:
            with open(filename, 'r') as f:
                data = js.load(f)
                for user in data:
                    if user['nombre'] == nombre:
                        return user.get('contraseña')
        except (FileNotFoundError, js.JSONDecodeError):
            return None
        return None


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
        # Cargar cuentas específicas del usuario (usando clave compuesta)
        self.cargar_cuentas_usuario(self.controller.usuario_actual)
        
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
        
        ttk.Button(pestana2, text="Crear cuenta").pack(pady=10)
        ttk.Button(pestana2, text="Transferencias").pack(pady=10)
        
        # Pestaña 3 - Ayuda
        pestana3 = ttk.Frame(self.notebook)
        self.notebook.add(pestana3, text="Ayuda")
        
        ttk.Label(pestana3, text="Centro de Ayuda - Modo Cliente", font=('Arial', 14, 'bold')).pack(pady=20)
        ttk.Label(pestana3, text=f"Bienvenido Cliente: {self.controller.usuario_actual.split('_')[0]}").pack(pady=10)  # Mostrar solo nombre
        ttk.Button(pestana3, text="Soporte al Cliente").pack(pady=10)
        ttk.Button(pestana3, text="Preguntas Frecuentes").pack(pady=10)

    def cargar_cuentas_usuario(self, usuario_clave):
        """Carga las cuentas específicas del usuario desde el archivo JSON usando clave compuesta"""
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos = js.load(archivo)
                self.cuentas_data = datos.get(usuario_clave, self.obtener_cuentas_predeterminadas())
        except (FileNotFoundError, js.JSONDecodeError):
            # Si el archivo no existe o está corrupto, usar predeterminadas
            self.cuentas_data = self.obtener_cuentas_predeterminadas()
            self.guardar_cuentas_usuario(usuario_clave)  # Crear el archivo con datos iniciales

    def guardar_cuentas_usuario(self, usuario_clave):
        """Guarda las cuentas del usuario en el archivo JSON usando clave compuesta"""
        try:
            with open("usuarios_cuentas.json", 'r') as archivo:
                datos = js.load(archivo)
        except (FileNotFoundError, js.JSONDecodeError):
            datos = {}
        
        # Actualizar las cuentas del usuario
        datos[usuario_clave] = self.cuentas_data
        
        with open("usuarios_cuentas.json", 'w') as archivo:
            js.dump(datos, archivo, indent=4)

    def obtener_cuentas_predeterminadas(self):
        """Devuelve las cuentas predeterminadas si el usuario no tiene datos guardados"""
        return [
            {"id": "1", "tipo": "Cuenta Vista", "numero": "252670021", "saldo": "$15.000"},
            {"id": "2", "tipo": "Cuenta de Ahorros", "numero": "252670022", "saldo": "$200.000"},
            {"id": "3", "tipo": "Cuenta Rut", "numero": "252670023", "saldo": "$30.000"},
            {"id": "4", "tipo": "Cuenta Corriente", "numero": "252670024", "saldo": "$50.000"}
        ]

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
            
            # Guardar los cambios en el archivo
            self.guardar_cuentas_usuario(self.controller.usuario_actual)
            
            messagebox.showinfo("Éxito", f"Se eliminaron {len(cuentas_seleccionadas)} cuenta(s) correctamente")

    def limpiar_checkbuttons(self):
        """Limpia los checkbuttons y variables"""
        for var in self.variables_cuentas:
            var.set(False)
    
    def cerrar_sesion(self):
        """Volver a la pantalla de login"""
        self.controller.usuario_actual = None
        self.controller.tipo_usuario = None
        self.controller.mostrar_frame("LoginFrame")


# Ejecutar la aplicación
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()