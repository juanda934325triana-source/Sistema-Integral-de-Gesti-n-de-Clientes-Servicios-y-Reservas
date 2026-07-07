import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from models.gestor import SoftwareFJ
from exceptions.excepciones import *


class SistemaGestionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Empresarial")
        self.root.geometry("850x650")
        self.root.configure(bg='#f5f6fa')
        self.root.resizable(False, False)

        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')

        # Colores corporativos
        bg = '#f5f6fa'
        fg = '#2c3e50'
        accent = '#34495e'

        self.estilo.configure('TFrame', background=bg)
        self.estilo.configure('TLabel', background=bg, font=('Segoe UI', 9), foreground=fg)
        self.estilo.configure('TButton', font=('Segoe UI', 9), padding=6)
        self.estilo.map('TButton', background=[('active', '#d5dbe3')])
        self.estilo.configure('TEntry', font=('Segoe UI', 9))
        self.estilo.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        self.estilo.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))

        self.estilo.configure('Header.TLabel', font=('Segoe UI', 22, 'bold'), foreground='#2c3e50')
        self.estilo.configure('Sub.TLabel', font=('Segoe UI', 11), foreground='#5d6d7e')
        self.estilo.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2c3e50')

        self.sistema = SoftwareFJ()
        self._cargar_datos_ejemplo()
        self.menu_principal()

    def _cargar_datos_ejemplo(self):
        try:
            self.sistema.registrar_cliente("Ana García", "ana@email.com", "3001234567", "premium")
            self.sistema.registrar_cliente("Carlos López", "carlos@email.com", "3007654321", "regular")
            self.sistema.crear_sala("Sala A", "Sala de reuniones", 50, 10)
            self.sistema.crear_equipo("HP Laptop", "Laptop HP", 20, "laptop")
            self.sistema.crear_asesoria("Python", "Asesoria en Python", 80, "senior")
        except:
            pass

    def menu_principal(self):
        self._limpiar()

        ttk.Label(self.root, text="Sistema de Gestión Empresarial", style='Header.TLabel').pack(pady=(35, 2))
        ttk.Label(self.root, text="Módulo de Clientes · Servicios · Reservas", style='Sub.TLabel').pack(pady=(0, 35))

        frame = ttk.Frame(self.root)
        frame.pack(pady=5, padx=50, fill='both', expand=True)

        botones = [
            ("Clientes", "Registrar Cliente", self.form_cliente),
            ("Clientes", "Ver Clientes", self.ver_clientes),
            ("Servicios", "Crear Servicio", self.form_servicio),
            ("Servicios", "Ver Servicios", self.ver_servicios),
            ("Reservas", "Nueva Reserva", self.form_reserva),
            ("Reservas", "Confirmar Reserva", self.confirmar_reserva),
            ("Reservas", "Cancelar Reserva", self.cancelar_reserva),
            ("Reservas", "Finalizar Reserva", self.terminar_reserva),
            ("Reservas", "Ver Reservas", self.ver_reservas),
            ("Sistema", "Estadísticas", self.ver_estadisticas),
            ("Sistema", "Salir", self.root.quit)
        ]

        for i, (cat, text, comando) in enumerate(botones):
            btn = ttk.Button(frame, text=f"{cat} · {text}", command=comando, width=30)
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=12, pady=10, sticky='ew')

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def _limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _formulario(self, titulo, campos, accion):
        self._limpiar()
        ttk.Label(self.root, text=titulo, style='Title.TLabel').pack(pady=(25, 15))

        frame = ttk.Frame(self.root)
        frame.pack(pady=10, padx=50)

        entradas = {}
        for i, (label, key) in enumerate(campos):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entrada = ttk.Entry(frame, width=50)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            entradas[key] = entrada

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Guardar", command=lambda: accion(entradas), width=14).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Volver", command=self.menu_principal, width=14).pack(side='left', padx=10)

    def _tabla(self, titulo, columnas, datos):
        self._limpiar()
        ttk.Label(self.root, text=titulo, style='Title.TLabel').pack(pady=(25, 10))

        frame = ttk.Frame(self.root)
        frame.pack(fill='both', expand=True, padx=50, pady=5)

        tree = ttk.Treeview(frame, columns=columnas, show='headings', height=16)
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor='center')

        for fila in datos:
            tree.insert('', 'end', values=fila)

        scroll = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')

        ttk.Button(self.root, text="Volver", command=self.menu_principal).pack(pady=15)

    def form_cliente(self):
        self._formulario(
            "Registrar Cliente",
            [
                ("Nombre completo:", "nombre"),
                ("Correo electrónico:", "email"),
                ("Teléfono:", "telefono"),
                ("Tipo (regular/premium/empresarial):", "tipo")
            ],
            self._guardar_cliente
        )

    def _guardar_cliente(self, entradas):
        try:
            nombre = entradas['nombre'].get()
            email = entradas['email'].get()
            telefono = entradas['telefono'].get()
            tipo = entradas['tipo'].get() or "regular"
            cliente = self.sistema.registrar_cliente(nombre, email, telefono, tipo)
            messagebox.showinfo("Éxito", f"Cliente registrado. ID: {cliente.id}")
            self.menu_principal()
        except (DatosClienteMalos, ClienteYaExiste) as e:
            messagebox.showerror("Error", str(e))

    def ver_clientes(self):
        clientes = self.sistema.listar_clientes()
        if not clientes:
            messagebox.showinfo("Clientes", "No hay clientes registrados")
            return
        datos = [(c.id, c.nombre, c.email, c.tipo, "Activo" if c.activo else "Inactivo") for c in clientes]
        self._tabla("Lista de Clientes", ('ID', 'Nombre', 'Email', 'Tipo', 'Estado'), datos)

    def form_servicio(self):
        self._formulario(
            "Crear Servicio",
            [
                ("Tipo (sala/equipo/asesoria):", "tipo"),
                ("Nombre:", "nombre"),
                ("Descripción:", "descripcion"),
                ("Precio por hora:", "precio"),
                ("Aforo (solo para sala):", "aforo"),
                ("Tipo de equipo (para equipo):", "tipo_equipo"),
                ("Nivel (para asesoria):", "nivel")
            ],
            self._guardar_servicio
        )

    def _guardar_servicio(self, entradas):
        try:
            tipo = entradas['tipo'].get().lower()
            nombre = entradas['nombre'].get()
            descripcion = entradas['descripcion'].get()
            precio = float(entradas['precio'].get())

            if tipo == "sala":
                aforo = int(entradas['aforo'].get() or 10)
                servicio = self.sistema.crear_sala(nombre, descripcion, precio, aforo)
            elif tipo == "equipo":
                tipo_eq = entradas['tipo_equipo'].get() or "computadora"
                servicio = self.sistema.crear_equipo(nombre, descripcion, precio, tipo_eq)
            elif tipo == "asesoria":
                nivel = entradas['nivel'].get() or "senior"
                servicio = self.sistema.crear_asesoria(nombre, descripcion, precio, nivel)
            else:
                messagebox.showerror("Error", "Tipo inválido")
                return

            messagebox.showinfo("Éxito", f"Servicio creado. ID: {servicio.id}")
            self.menu_principal()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ver_servicios(self):
        servicios = self.sistema.listar_servicios()
        if not servicios:
            messagebox.showinfo("Servicios", "No hay servicios registrados")
            return
        datos = [(s.id, s.nombre, s.tipo(), f"${s.precio_base}", "Disponible" if s.disponible else "No disponible") for s in servicios]
        self._tabla("Lista de Servicios", ('ID', 'Nombre', 'Tipo', 'Precio/h', 'Estado'), datos)

    def form_reserva(self):
        self._formulario(
            "Nueva Reserva",
            [
                ("ID Cliente:", "id_cliente"),
                ("ID Servicio:", "id_servicio"),
                ("Fecha (YYYY-MM-DD HH:MM):", "fecha"),
                ("Horas:", "horas"),
                ("Personas (opcional):", "personas"),
                ("Extras (opcional, separados por coma):", "extras")
            ],
            self._guardar_reserva
        )

    def _guardar_reserva(self, entradas):
        try:
            id_cliente = int(entradas['id_cliente'].get())
            id_servicio = int(entradas['id_servicio'].get())
            fecha = datetime.strptime(entradas['fecha'].get(), "%Y-%m-%d %H:%M")
            horas = float(entradas['horas'].get())

            extras = {}
            if entradas['personas'].get():
                extras['personas'] = int(entradas['personas'].get())
            if entradas['extras'].get():
                extras['extras'] = [x.strip() for x in entradas['extras'].get().split(',')]

            reserva = self.sistema.crear_reserva(id_cliente, id_servicio, fecha, horas, **extras)
            messagebox.showinfo("Éxito", f"Reserva creada. ID: {reserva.numero}\nEstado: Pendiente")
            self.menu_principal()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def confirmar_reserva(self):
        try:
            num = simpledialog.askinteger("Confirmar", "ID de la reserva:")
            if num is None:
                return
            costo = self.sistema.confirmar_reserva(num)
            messagebox.showinfo("Confirmación", f"Reserva {num} confirmada.\nCosto: ${costo:.2f}")
        except (ReservaNoExiste, EstadoReservaRaro, ServicioOcupado) as e:
            messagebox.showerror("Error", str(e))

    def cancelar_reserva(self):
        try:
            num = simpledialog.askinteger("Cancelar", "ID de la reserva:")
            if num is None:
                return
            self.sistema.cancelar_reserva(num)
            messagebox.showinfo("Cancelación", f"Reserva {num} cancelada.")
        except (ReservaNoExiste, EstadoReservaRaro) as e:
            messagebox.showerror("Error", str(e))

    def terminar_reserva(self):
        try:
            num = simpledialog.askinteger("Finalizar", "ID de la reserva:")
            if num is None:
                return
            self.sistema.terminar_reserva(num)
            messagebox.showinfo("Finalizado", f"Reserva {num} finalizada.")
        except (ReservaNoExiste, EstadoReservaRaro) as e:
            messagebox.showerror("Error", str(e))

    def ver_reservas(self):
        reservas = self.sistema.listar_reservas()
        if not reservas:
            messagebox.showinfo("Reservas", "No hay reservas registradas")
            return
        datos = [(r.numero, r.cliente.nombre, r.servicio.nombre, r.estado, f"${r.costo:.2f}" if r.costo else "Pendiente") for r in reservas]
        self._tabla("Lista de Reservas", ('ID', 'Cliente', 'Servicio', 'Estado', 'Costo'), datos)

    def ver_estadisticas(self):
        stats = self.sistema.estadisticas()
        msg = (f"Clientes: {stats['total_clientes']}\n"
               f"Servicios: {stats['total_servicios']}\n"
               f"Reservas: {stats['total_reservas']}\n"
               f"Reservas activas: {stats['reservas_activas']}")
        messagebox.showinfo("Estadísticas del Sistema", msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaGestionGUI(root)
    root.mainloop()