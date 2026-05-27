import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
import subprocess
import sys
from tkcalendar import Calendar #Para que al modificar la fecha salga un calendario
from PIL import Image, ImageTk #para la imagen del logo 

# ==================================================
# PALETA DE COLORES
# ==================================================
AZUL_OSCURO   = "#1E3A5F"
AZUL_MEDIO    = "#2E5F8A"
AZUL_CLARO    = "#D6E4F0"
BLANCO        = "#FFFFFF"
GRIS_FONDO    = "#F4F6F9"
GRIS_BORDE    = "#CBD5E0"
GRIS_TEXTO    = "#4A5568"
NEGRO         = "#1A202C"
ROJO          = "#C0392B"
VERDE         = "#1E6E3B"

# ==================================================
# CLASE EVIDENCIAS
# ==================================================
class Evidencias:

    # ----------------------------------------------
    # ARRAY DINÁMICO (LISTA)
    # ----------------------------------------------
    lista_evidencias = []

    # ----------------------------------------------
    # CONSTRUCTOR
    # ----------------------------------------------
    def __init__(self, id_evidencia, id_estudiante, nombre_estudiante, nombre_evidencia, fecha_carga, path_archivo, descripcion, calificacion=0, estado="No revisado", fecha_revision=""):
       
        self.id_evidencia = id_evidencia
        self.id_estudiante = id_estudiante
        self.nombre_estudiante = nombre_estudiante
        self.nombre_evidencia = nombre_evidencia
        self.fecha_carga = fecha_carga
        self.path_archivo = path_archivo
        self.descripcion = descripcion

        # ------------------------------------------
        # VALORES POR DEFECTO
        # ------------------------------------------
        self.calificacion = calificacion
        self.estado = estado
        self.fecha_revision = fecha_revision
        
    

    # ==================================================
    # MÉTODO INCLUIR EVIDENCIA
    # ==================================================
    @classmethod
    def incluir_evidencia(cls, evidencia):

        cls.lista_evidencias.append(evidencia)

    # ==================================================
    # MÉTODO ELIMINAR EVIDENCIA
    # ==================================================
    @classmethod
    def eliminar_evidencia(cls, id_evidencia):

        for evidencia in cls.lista_evidencias:

            if evidencia.id_evidencia == id_evidencia:

                cls.lista_evidencias.remove(evidencia)
                return True

        return False

    # ==================================================
    # MÉTODO MODIFICAR EVIDENCIA
    # ==================================================
    @classmethod
    def modificar_evidencia(
        cls,
        id_evidencia,
        nuevo_nombre,
        nueva_descripcion,
        nuevo_archivo
    ):

        for evidencia in cls.lista_evidencias:

            if evidencia.id_evidencia == id_evidencia:

                evidencia.nombre_evidencia = nuevo_nombre
                evidencia.descripcion = nueva_descripcion
                evidencia.path_archivo = nuevo_archivo

                return True

        return False

    # ==================================================
    # MÉTODO GUARDAR REGISTRO
    # ==================================================
    def guardar_registro(self):

        Evidencias.lista_evidencias.append(self)

# ==================================================
# ABRIR ARCHIVO EN EL SISTEMA
# ==================================================
def abrir_archivo_sistema(ruta):

    if not ruta or not os.path.exists(ruta):
        messagebox.showwarning(
            "Archivo",
            "El archivo no existe o la ruta está vacía"
        )
        return

    try:
        if sys.platform == "win32":
            os.startfile(ruta)
        elif sys.platform == "darwin":
            subprocess.run(["open", ruta], check=True)
        else:
            subprocess.run(["xdg-open", ruta], check=True)
    except OSError:
        messagebox.showerror(
            "Archivo",
            "No se pudo abrir el archivo"
        )

# ==================================================
# VENTANA PRINCIPAL
# ==================================================
ventana = tk.Tk()
ventana.title("Biblioteca UDI")

ancho = 900
alto  = 700
x = (ventana.winfo_screenwidth()  // 2) - (ancho // 2)
y = (ventana.winfo_screenheight() // 2) - (alto  // 2)
ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
ventana.configure(bg=GRIS_FONDO)
ventana.resizable(False, False)

# ==================================================
# BARRA SUPERIOR
# ==================================================
barra_superior = tk.Frame(ventana, bg=AZUL_OSCURO, height=90)
barra_superior.pack(fill="x")
barra_superior.pack_propagate(False)

# Logo + miga de pan (izquierda)
contenedor_izq = tk.Frame(barra_superior, bg=AZUL_OSCURO)
contenedor_izq.pack(side="left", padx=20, pady=10)

# ==========================================
# CARGAR LOGO 40x40
# ==========================================
imagen_logo = Image.open("auron.png") 
imagen_logo = imagen_logo.resize((100, 100))
logo = ImageTk.PhotoImage(imagen_logo)

label_logo = tk.Label(
    contenedor_izq,
    image=logo,
    bg=AZUL_OSCURO
)
label_logo.pack(anchor="w")

tk.Label(
    contenedor_izq,
    text="Inicio > Biblioteca > Gestión de Libros",
    bg=AZUL_OSCURO, fg=AZUL_CLARO, font=("Arial", 9)
).pack(anchor="w", pady=(3, 0))

# Título centrado
tk.Label(
    barra_superior,
    text="Sistema Biblioteca UDI",
    bg=AZUL_OSCURO, fg=BLANCO, font=("Arial", 22, "bold")
).place(relx=0.5, rely=0.38, anchor="center")

# Fecha (abajo derecha)
fecha_actual = datetime.now().strftime("%d/%m/%Y")
tk.Label(
    barra_superior,
    text=f"Fecha: {fecha_actual}",
    bg=AZUL_OSCURO, fg=BLANCO, font=("Arial", 10)
).place(relx=0.98, rely=0.82, anchor="se")

# ==================================================
# CUERPO  (menú lateral + contenido)
# ==================================================
cuerpo = tk.Frame(ventana, bg=GRIS_FONDO)
cuerpo.pack(fill="both", expand=True)

# --------------------------------------------------
# MENÚ LATERAL
# --------------------------------------------------
menu_lateral = tk.Frame(cuerpo, bg=AZUL_OSCURO, width=175)
menu_lateral.pack(side="left", fill="y")
menu_lateral.pack_propagate(False)

# ==================================================
# TÍTULO MENÚ
# ==================================================
tk.Label(
    menu_lateral,
    text="Menú",
    bg=AZUL_OSCURO,
    fg=AZUL_CLARO,
    font=("Arial", 10, "bold"),
    anchor="w",
    padx=12,
    pady=8
).pack(fill="x")


# ==================================================
# GRILLA Y ACTUALIZACIÓN
# ==================================================
grilla = None
contador_id_evidencia = 1


def actualizar_grilla():
    global grilla

    if grilla is None:
        return

    try:
        if not grilla.winfo_exists():
            grilla = None
            return
    except tk.TclError:
        grilla = None
        return

    for item in grilla.get_children():
        grilla.delete(item)

    for evidencia in Evidencias.lista_evidencias:
        grilla.insert(
            "",
            "end",
            values=(
                evidencia.id_evidencia,
                evidencia.id_estudiante,
                evidencia.nombre_estudiante,
                evidencia.nombre_evidencia,
                evidencia.fecha_carga,
                evidencia.descripcion,
                evidencia.path_archivo,
                evidencia.calificacion,
                evidencia.estado,
                evidencia.fecha_revision
            )
        )


# ==================================================
# FUNCIÓN MODIFICAR EVIDENCIA
# ==================================================
def modificar_evidencia():
    global grilla

    if grilla is None:
        messagebox.showwarning(
            "Modificar",
            "La grilla no está disponible"
        )
        return

    seleccionado = grilla.selection()

    # Validar selección
    if not seleccionado:
        messagebox.showwarning(
            "Modificar",
            "Debe seleccionar un registro para modificar"
        )
        return

    # Obtener datos desde el array dinámico
    item = seleccionado[0]
    datos = grilla.item(item, "values")
    id_evidencia = int(datos[0])

    evidencia_sel = None
    for evidencia in Evidencias.lista_evidencias:
        if evidencia.id_evidencia == id_evidencia:
            evidencia_sel = evidencia
            break

    if evidencia_sel is None:
        messagebox.showwarning(
            "Modificar",
            "No se encontró la evidencia seleccionada"
        )
        return

    nombre_actual = evidencia_sel.nombre_evidencia
    fecha_actual = evidencia_sel.fecha_carga
    descripcion_actual = evidencia_sel.descripcion
    archivo_actual = evidencia_sel.path_archivo

    # ==========================================
    # VENTANA EMERGENTE
    # ==========================================
    ventana_mod = tk.Toplevel(ventana)
    ventana_mod.title("Modificar Evidencia")
    ventana_mod.geometry("500x450")
    ventana_mod.configure(bg=GRIS_FONDO)
    ventana_mod.resizable(False, False)
    ventana_mod.grab_set()  # bloquea ventana principal

    # ==========================================
    # VARIABLES
    # ==========================================
    ruta_modificada = tk.StringVar(value=archivo_actual)

    # ==========================================
    # CAMPOS
    # ==========================================
    tk.Label(
        ventana_mod,
        text="ID Evidencia:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).place(x=30, y=30)

    entry_id = tk.Entry(
        ventana_mod,
        width=30,
        state="readonly",
        readonlybackground="#E2E8F0"
    )
    entry_id.place(x=170, y=30)
    entry_id.config(state="normal")
    entry_id.insert(0, id_evidencia)
    entry_id.config(state="readonly")

    # Nombre
    tk.Label(
        ventana_mod,
        text="Nombre:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).place(x=30, y=70)

    entry_nombre_mod = tk.Entry(ventana_mod, width=30)
    entry_nombre_mod.place(x=170, y=70)
    entry_nombre_mod.insert(0, nombre_actual)

    # Tipo
    tk.Label(
        ventana_mod,
        text="Tipo:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).place(x=30, y=110)


    # ==========================================
    # FECHA CON CALENDARIO
    # ==========================================
    tk.Label(
    ventana_mod,
    text="Fecha:",
    bg=GRIS_FONDO,
    fg=GRIS_TEXTO,
    font=("Arial", 10, "bold")
    ).place(x=30, y=150)

    # Variable de fecha
    fecha_var = tk.StringVar(value=fecha_actual)

    # Campo donde se muestra la fecha
    entry_fecha_mod = tk.Entry(
    ventana_mod,
    width=22,
    textvariable=fecha_var,
    state="readonly",
    readonlybackground="#E2E8F0"
    )
    entry_fecha_mod.place(x=170, y=150)

    # ==========================================
    # FUNCIÓN ABRIR CALENDARIO
    # ==========================================
    def abrir_calendario():

        ventana_cal = tk.Toplevel(ventana_mod)
        ventana_cal.title("Seleccionar fecha")
        ventana_cal.geometry("250x250")
        ventana_cal.grab_set()

        cal = Calendar(
            ventana_cal,
            selectmode="day",
            date_pattern="dd/mm/yyyy"
        )
        cal.pack(pady=10)

        def seleccionar_fecha():
            fecha_var.set(cal.get_date())
            ventana_cal.destroy()

        tk.Button(
            ventana_cal,
            text="Aceptar",
            bg=VERDE,
            fg=BLANCO,
            command=seleccionar_fecha
        ).pack(pady=10)

    # Botón calendario
    btn_fecha = tk.Button(
    ventana_mod,
    text="📅",
    width=3,
    bg=AZUL_MEDIO,
    fg=BLANCO,
    command=abrir_calendario
    )
    btn_fecha.place(x=390, y=147)

    # Descripción
    tk.Label(
        ventana_mod,
        text="Descripción:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).place(x=30, y=190)

    text_desc_mod = tk.Text(
        ventana_mod,
        width=28,
        height=4
    )
    text_desc_mod.place(x=170, y=190)
    text_desc_mod.insert("1.0", descripcion_actual)

    # Archivo
    tk.Label(
        ventana_mod,
        text="Archivo:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).place(x=30, y=290)

    entry_archivo_mod = tk.Entry(
        ventana_mod,
        width=23,
        textvariable=ruta_modificada
    )
    entry_archivo_mod.place(x=170, y=290)

    # ==========================================
    # CARGAR NUEVO ARCHIVO
    # ==========================================
    def cargar_archivo_mod():
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo"
        )

        if archivo:
            ruta_modificada.set(archivo)

    tk.Button(
        ventana_mod,
        text="...",
        width=3,
        command=cargar_archivo_mod
    ).place(x=390, y=287)

    # ==========================================
    # GUARDAR CAMBIOS
    # ==========================================
    def guardar_cambios():

        nuevo_nombre = entry_nombre_mod.get().strip()
        
        nueva_fecha = fecha_var.get().strip()
        nueva_descripcion = text_desc_mod.get("1.0", tk.END).strip()
        nuevo_archivo = ruta_modificada.get().strip()

        if nuevo_nombre == "":
            messagebox.showwarning(
                "Validación",
                "Ingrese el nombre"
            )
            return

        

        confirmar = messagebox.askyesno(
            "Confirmar modificación",
            f"¿Desea modificar la evidencia:\n\n{nuevo_nombre}?"
        )

        if confirmar:

        # ------------------------------------------
        # MODIFICAR EN EL ARRAY DINÁMICO
        # ------------------------------------------
            Evidencias.modificar_evidencia(
            int(id_evidencia),
            nuevo_nombre,
            nueva_descripcion,
            nuevo_archivo
        )

            # ------------------------------------------
        # ACTUALIZAR FECHA EN ARRAY
        # ------------------------------------------
        for evidencia in Evidencias.lista_evidencias:

            if evidencia.id_evidencia == int(id_evidencia):

                evidencia.fecha_carga = nueva_fecha

        # ------------------------------------------
        # ACTUALIZAR GRILLA
        # ------------------------------------------
        actualizar_grilla()

        messagebox.showinfo(
            "Modificado",
            "Registro actualizado correctamente"
        )

        ventana_mod.destroy()

    # ==========================================
    # BOTONES
    # ==========================================
    tk.Button(
        ventana_mod,
        text="Cancelar",
        bg=GRIS_BORDE,
        fg=NEGRO,
        width=12,
        command=ventana_mod.destroy
    ).place(x=120, y=370)

    tk.Button(
        ventana_mod,
        text="Aceptar",
        bg=VERDE,
        fg=BLANCO,
        width=12,
        command=guardar_cambios
    ).place(x=260, y=370)

# ==================================================
# FUNCIÓN ELIMINAR EVIDENCIA
# ==================================================
def eliminar_evidencia():
    global grilla

    if grilla is None:
        messagebox.showwarning(
            "Eliminar",
            "La grilla no está disponible"
        )
        return

    seleccionado = grilla.selection()

    if not seleccionado:
        messagebox.showwarning(
            "Eliminar",
            "Debe seleccionar un registro para eliminar"
        )
        return

    item = seleccionado[0]
    datos = grilla.item(item, "values")

    id_evidencia = datos[0]
    nombre_evidencia = datos[3]

    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Está seguro de eliminar el registro?\n\n"
        f"ID: {id_evidencia}\n"
        f"Evidencia: {nombre_evidencia}"
    )

    if confirmar:
        Evidencias.eliminar_evidencia(int(id_evidencia))
        actualizar_grilla()
        messagebox.showinfo(
            "Eliminado",
            "Registro eliminado correctamente"
        )

# ==================================================
# FUNCIÓN ITEMS
# ==================================================
def crear_item(parent, texto, subitem=False, comando=None):

    color = AZUL_CLARO if subitem else BLANCO
    tamaño = 10 if subitem else 11
    peso = "normal" if subitem else "bold"
    padx = 28 if subitem else 12

    item = tk.Label(
        parent,
        text=texto,
        bg=AZUL_OSCURO,
        fg=color,
        font=("Arial", tamaño, peso),
        anchor="w",
        padx=padx,
        pady=6,
        cursor="hand2"
    )

    item.pack(fill="x")

    def enter(e):
        item.config(bg=AZUL_MEDIO)

    def leave(e):
        item.config(bg=AZUL_OSCURO)

    item.bind("<Enter>", enter)
    item.bind("<Leave>", leave)

    if comando:
        item.bind("<Button-1>", lambda e: comando())

    return item

# ==================================================
# FUNCIÓN DESPLEGAR
# ==================================================
def toggle_submenu(frame):
    if frame.winfo_viewable():
        frame.pack_forget()
    else:
        frame.pack(fill="x")

# ==================================================
# ESTUDIANTES
# ==================================================
contenedor_estudiantes = tk.Frame(menu_lateral, bg=AZUL_OSCURO)
contenedor_estudiantes.pack(fill="x")

crear_item(
    contenedor_estudiantes,
    "▶ Estudiantes",
    comando=lambda: toggle_submenu(submenu_estudiantes)
)

submenu_estudiantes = tk.Frame(
    contenedor_estudiantes,
    bg=AZUL_OSCURO
)

crear_item(
    submenu_estudiantes,
    "• Gestión de Evidencias",
    subitem=True
)

# ==================================================
# TUTORES ACADÉMICOS
# ==================================================
contenedor_tutores = tk.Frame(menu_lateral, bg=AZUL_OSCURO)
contenedor_tutores.pack(fill="x")

crear_item(
    contenedor_tutores,
    "▶ Tutores Académicos",
    comando=lambda: toggle_submenu(submenu_tutores)
)

submenu_tutores = tk.Frame(
    contenedor_tutores,
    bg=AZUL_OSCURO
)

crear_item(
    submenu_tutores,
    "• Revisar Evidencias",
    subitem=True
)

crear_item(
    submenu_tutores,
    "• Informes",
    subitem=True
)

# ==================================================
# ASESORES PEDAGÓGICOS
# ==================================================
contenedor_asesores = tk.Frame(menu_lateral, bg=AZUL_OSCURO)
contenedor_asesores.pack(fill="x")

crear_item(
    contenedor_asesores,
    "▶ Asesores Pedagógicos",
    comando=lambda: toggle_submenu(submenu_asesores)
)

submenu_asesores = tk.Frame(
    contenedor_asesores,
    bg=AZUL_OSCURO
)

crear_item(
    submenu_asesores,
    "• Observaciones",
    subitem=True
)

# ==================================================
# ESPACIO FLEXIBLE
# ==================================================
tk.Frame(menu_lateral, bg=AZUL_OSCURO).pack(fill="both", expand=True)

# ==================================================
# BOTÓN SALIR
# ==================================================
def salir():
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        ventana.destroy()

btn_salir = tk.Button(
    menu_lateral,
    text="Salir",
    bg=ROJO,
    fg=BLANCO,
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    activebackground="#A93226",
    activeforeground=BLANCO,
    command=salir
)

btn_salir.pack(fill="x", padx=12, pady=12)
# --------------------------------------------------
# PANEL DE CONTENIDO PRINCIPAL
# --------------------------------------------------
panel_contenido = tk.Frame(cuerpo, bg=GRIS_FONDO)
panel_contenido.pack(side="left", fill="both", expand=True, padx=12, pady=10)

# ==================================================
# FUNCIÓN LIMPIAR PANEL
# ==================================================
def limpiar_panel():
    global grilla

    for widget in panel_contenido.winfo_children():
        widget.destroy()

    grilla = None

# ==================================================
# PANEL GESTIÓN EVIDENCIAS (ESTUDIANTES)
# ==================================================
def mostrar_panel_estudiantes():
    global grilla, contador_id_evidencia

    limpiar_panel()

    panel_estudiantes = tk.Frame(
        panel_contenido,
        bg=GRIS_FONDO
    )
    panel_estudiantes.pack(fill="both", expand=True)

    # --------------------------------------------------
    # FILA SUPERIOR: formulario alineado a la derecha
    # --------------------------------------------------
    fila_superior = tk.Frame(panel_estudiantes, bg=GRIS_FONDO)
    fila_superior.pack(fill="x")
    fila_superior.columnconfigure(0, weight=1)
    fila_superior.columnconfigure(1, weight=1)

    panel_der = tk.Frame(fila_superior, bg=GRIS_FONDO)
    panel_der.grid(row=0, column=1, sticky="ne", padx=(20, 0), pady=(0, 6))
    panel_der.columnconfigure(0, weight=0)
    panel_der.columnconfigure(1, weight=1)

    # ==================================================
    # ID ESTUDIANTE
    # ==================================================
    tk.Label(
        panel_der,
        text="ID Estudiante:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)

    entry_id_estudiante = tk.Entry(
        panel_der,
        font=("Arial", 10),
        width=32
    )
    entry_id_estudiante.grid(row=0, column=1, sticky="w", pady=6)

    # ==================================================
    # NOMBRE ESTUDIANTE
    # ==================================================
    tk.Label(
        panel_der,
        text="Nombre Estudiante:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)

    entry_nombre_estudiante = tk.Entry(
        panel_der,
        font=("Arial", 10),
        width=32
    )
    entry_nombre_estudiante.grid(row=1, column=1, sticky="w", pady=6)

    # ==================================================
    # NOMBRE EVIDENCIA
    # ==================================================
    tk.Label(
        panel_der,
        text="Nombre Evidencia:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=6)

    entry_nombre = tk.Entry(
        panel_der,
        font=("Arial", 10),
        bg=BLANCO,
        fg=NEGRO,
        relief="solid",
        highlightthickness=1,
        highlightbackground=GRIS_BORDE,
        highlightcolor=AZUL_MEDIO,
        width=32
    )
    entry_nombre.grid(row=2, column=1, sticky="w", pady=6)

    # ==================================================
    # DESCRIPCIÓN
    # ==================================================
    tk.Label(
        panel_der,
        text="Descripción:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).grid(row=3, column=0, sticky="nw", padx=(0, 10), pady=6)

    frame_desc = tk.Frame(
        panel_der,
        bg=GRIS_BORDE,
        bd=1,
        relief="solid"
    )
    frame_desc.grid(row=3, column=1, sticky="w", pady=6)

    text_descripcion = tk.Text(
        frame_desc,
        font=("Arial", 10),
        bg=BLANCO,
        fg=NEGRO,
        relief="flat",
        height=4,
        width=30,
        wrap="word"
    )
    text_descripcion.pack(padx=1, pady=1)

    # ==================================================
    # FECHA (BLOQUEADA)
    # ==================================================
    tk.Label(
        panel_der,
        text="Fecha:",
        bg=GRIS_FONDO,
        fg=GRIS_TEXTO,
        font=("Arial", 10, "bold")
    ).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=6)

    entry_fecha = tk.Entry(
        panel_der,
        font=("Arial", 10),
        bg="#E2E8F0",
        fg=NEGRO,
        width=32,
        state="readonly",
        readonlybackground="#E2E8F0"
    )
    entry_fecha.grid(row=4, column=1, sticky="w", pady=6)

    fecha_sistema = datetime.now().strftime("%d/%m/%Y")
    entry_fecha.config(state="normal")
    entry_fecha.insert(0, fecha_sistema)
    entry_fecha.config(state="readonly")

    # ==================================================
    # CARGAR ARCHIVO
    # ==================================================
    ruta_archivo = ""

    def cargar_evidencia():
        nonlocal ruta_archivo

        archivo = filedialog.askopenfilename(
            title="Seleccionar evidencia",
            filetypes=[
                ("Archivos PDF", "*.pdf"),
                ("Archivos Word", "*.docx"),
                ("Archivos Excel", "*.xlsx"),
                ("Todos los archivos", "*.*")
            ]
        )

        if archivo:
            ruta_archivo = archivo
            messagebox.showinfo(
                "Archivo seleccionado",
                f"Archivo cargado:\n\n{archivo}"
            )

    tk.Button(
        panel_der,
        text="📎 Cargar evidencia",
        bg=AZUL_MEDIO,
        fg=BLANCO,
        font=("Arial", 10),
        relief="flat",
        cursor="hand2",
        activebackground=AZUL_OSCURO,
        activeforeground=BLANCO,
        command=cargar_evidencia
    ).grid(row=5, column=1, sticky="e", pady=(10, 0))

    # --------------------------------------------------
    # GRILLA / TABLA
    # --------------------------------------------------
    tk.Frame(panel_estudiantes, bg=GRIS_BORDE, height=1).pack(fill="x", pady=8)

    columnas = (
        "id_evidencia",
        "id_estudiante",
        "nombre_estudiante",
        "nom_evidencia",
        "fecha_carga",
        "descripcion",
        "archivo",
        "calificacion",
        "estado",
        "fecha_revision"
    )

    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Grilla.Treeview",
        background=BLANCO,
        fieldbackground=BLANCO,
        foreground=NEGRO,
        rowheight=22,
        font=("Arial", 10)
    )
    style.configure(
        "Grilla.Treeview.Heading",
        background=AZUL_OSCURO,
        foreground=BLANCO,
        font=("Arial", 10, "bold"),
        relief="flat"
    )
    style.map("Grilla.Treeview", background=[("selected", AZUL_MEDIO)])

    frame_tabla = tk.Frame(
        panel_estudiantes,
        bg=GRIS_BORDE,
        bd=1,
        relief="solid"
    )
    frame_tabla.pack(fill="both", expand=True)

    scroll_vertical = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_vertical.pack(side="right", fill="y")

    scroll_horizontal = tk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_horizontal.pack(side="bottom", fill="x")

    grilla = ttk.Treeview(
        frame_tabla,
        columns=columnas,
        show="headings",
        yscrollcommand=scroll_vertical.set,
        xscrollcommand=scroll_horizontal.set,
        style="Grilla.Treeview",
        height=6
    )
    grilla.pack(fill="both", expand=True)
    scroll_vertical.config(command=grilla.yview)
    scroll_horizontal.config(command=grilla.xview)

    encabezados = {
        "id_evidencia": ("Id", 50),
        "id_estudiante": ("ID Estudiante", 120),
        "nombre_estudiante": ("Nombre Estudiante", 160),
        "nom_evidencia": ("Nom. Evidencia", 140),
        "fecha_carga": ("Fecha Carga", 100),
        "descripcion": ("Descripción", 180),
        "archivo": ("Archivo", 120),
        "calificacion": ("Calificación", 90),
        "estado": ("Estado", 100),
        "fecha_revision": ("Fecha Revisión", 110),
    }

    for col, (texto, ancho_col) in encabezados.items():
        grilla.heading(col, text=texto)
        grilla.column(col, width=ancho_col, minwidth=40, anchor="w")

    # ==================================================
    # NUEVA EVIDENCIA
    # ==================================================
    def nueva_evidencia_form():
        nonlocal ruta_archivo

        entry_id_estudiante.delete(0, tk.END)
        entry_nombre_estudiante.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        text_descripcion.delete("1.0", tk.END)
        ruta_archivo = ""

        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        entry_fecha.config(state="normal")
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, fecha_actual)
        entry_fecha.config(state="readonly")

    # ==================================================
    # ACEPTAR EVIDENCIA
    # ==================================================
    def aceptar_evidencia():
        nonlocal ruta_archivo
        global contador_id_evidencia

        nombre_evidencia = entry_nombre.get().strip()
        id_estudiante = entry_id_estudiante.get().strip()
        nombre_estudiante = entry_nombre_estudiante.get().strip()
        fecha_registro = entry_fecha.get().strip()
        descripcion = text_descripcion.get("1.0", tk.END).strip()

        if id_estudiante == "":
            messagebox.showwarning(
                "Validación",
                "Ingrese el ID del estudiante"
            )
            return

        if nombre_estudiante == "":
            messagebox.showwarning(
                "Validación",
                "Ingrese el nombre del estudiante"
            )
            return

        if nombre_evidencia == "":
            messagebox.showwarning(
                "Validación",
                "Ingrese el nombre de la evidencia"
            )
            return

        if ruta_archivo == "":
            messagebox.showwarning(
                "Validación",
                "Debe cargar un archivo"
            )
            return

        nueva_evidencia = Evidencias(
            contador_id_evidencia,
            id_estudiante,
            nombre_estudiante,
            nombre_evidencia,
            fecha_registro,
            ruta_archivo,
            descripcion
        )

        nueva_evidencia.guardar_registro()
        contador_id_evidencia += 1
        actualizar_grilla()

        messagebox.showinfo(
            "Registro",
            "Evidencia registrada correctamente"
        )

        nueva_evidencia_form()

    # --------------------------------------------------
    # BARRA DE ACCIONES
    # --------------------------------------------------
    tk.Frame(panel_estudiantes, bg=GRIS_BORDE, height=1).pack(fill="x", pady=(8, 6))

    barra_acciones = tk.Frame(panel_estudiantes, bg=GRIS_FONDO)
    barra_acciones.pack(fill="x")

    botones_acciones = [
        ("Cancelar", GRIS_BORDE, NEGRO, nueva_evidencia_form),
        ("Nueva Evidencia", AZUL_MEDIO, BLANCO, nueva_evidencia_form),
        ("Modificar", AZUL_OSCURO, BLANCO, modificar_evidencia),
        ("Eliminar", ROJO, BLANCO, eliminar_evidencia),
        ("Aceptar", VERDE, BLANCO, aceptar_evidencia),
    ]

    for texto, bg, fg, cmd in botones_acciones:
        tk.Button(
            barra_acciones,
            text=texto,
            bg=bg,
            fg=fg,
            font=("Arial", 10),
            relief="flat",
            padx=14,
            pady=5,
            cursor="hand2",
            activebackground=AZUL_OSCURO,
            activeforeground=BLANCO,
            command=cmd
        ).pack(side="left", padx=(0, 6))

    actualizar_grilla()

# ==================================================
# PANEL REVISAR EVIDENCIAS
# ==================================================
def revisar_evidencias():

    limpiar_panel()

    panel_revision = tk.Frame(
        panel_contenido,
        bg=GRIS_FONDO
    )
    panel_revision.pack(fill="both", expand=True)

    tk.Label(
        panel_revision,
        text="Revisión de Evidencias",
        bg=GRIS_FONDO,
        fg=AZUL_OSCURO,
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    columnas = (
        "id",
        "estudiante",
        "evidencia",
        "fecha",
        "estado",
        "nota"
    )

    frame_tabla = tk.Frame(
        panel_revision,
        bg=GRIS_BORDE,
        bd=1,
        relief="solid"
    )
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    frame_contenedor = tk.Frame(frame_tabla, bg=GRIS_BORDE)
    frame_contenedor.pack(fill="both", expand=True)

    tabla = ttk.Treeview(
        frame_contenedor,
        columns=columnas,
        show="headings",
        height=12
    )

    scroll_vertical = ttk.Scrollbar(
        frame_contenedor,
        orient="vertical",
        command=tabla.yview
    )
    scroll_horizontal = ttk.Scrollbar(
        frame_tabla,
        orient="horizontal",
        command=tabla.xview
    )
    tabla.configure(
        yscrollcommand=scroll_vertical.set,
        xscrollcommand=scroll_horizontal.set
    )

    tabla.pack(side="left", fill="both", expand=True)
    scroll_vertical.pack(side="right", fill="y")
    scroll_horizontal.pack(side="bottom", fill="x")

    encabezados = {
        "id": ("ID", 60),
        "estudiante": ("Estudiante", 180),
        "evidencia": ("Evidencia", 180),
        "fecha": ("Fecha", 100),
        "estado": ("Estado", 120),
        "nota": ("Nota", 80)
    }

    for col, (texto, ancho) in encabezados.items():
        tabla.heading(col, text=texto)
        tabla.column(col, width=ancho, stretch=False)

    def cargar_tabla_revision():

        for item in tabla.get_children():
            tabla.delete(item)

        for evidencia in Evidencias.lista_evidencias:
            tabla.insert(
                "",
                "end",
                values=(
                    evidencia.id_evidencia,
                    evidencia.nombre_estudiante,
                    evidencia.nombre_evidencia,
                    evidencia.fecha_carga,
                    evidencia.estado,
                    evidencia.calificacion
                )
            )

    cargar_tabla_revision()

    ventana_revision_abierta = {"widget": None}

    def crear_campo_bloqueado(parent, etiqueta, valor, y, ancho=40):

        tk.Label(
            parent,
            text=etiqueta,
            bg=GRIS_FONDO,
            fg=GRIS_TEXTO,
            font=("Arial", 10, "bold")
        ).place(x=30, y=y)

        entry = tk.Entry(
            parent,
            width=ancho,
            state="readonly",
            readonlybackground="#E2E8F0"
        )
        entry.place(x=180, y=y)
        entry.config(state="normal")
        entry.insert(0, valor)
        entry.config(state="readonly")

        return entry

    def abrir_ventana_revision(event=None):

        seleccionado = tabla.selection()

        if not seleccionado:
            return

        if (
            ventana_revision_abierta["widget"] is not None
            and ventana_revision_abierta["widget"].winfo_exists()
        ):
            return

        item = seleccionado[0]
        datos = tabla.item(item, "values")
        id_evidencia = int(datos[0])

        evidencia_sel = None
        for evidencia in Evidencias.lista_evidencias:
            if evidencia.id_evidencia == id_evidencia:
                evidencia_sel = evidencia
                break

        if evidencia_sel is None:
            messagebox.showwarning(
                "Revisión",
                "No se encontró la evidencia seleccionada"
            )
            return

        ventana_rev = tk.Toplevel(ventana)
        ventana_revision_abierta["widget"] = ventana_rev
        ventana_rev.title("Revisión de Evidencia")
        ventana_rev.geometry("560x520")
        ventana_rev.configure(bg=GRIS_FONDO)
        ventana_rev.resizable(False, False)
        ventana_rev.grab_set()

        def cerrar_ventana():
            ventana_revision_abierta["widget"] = None
            ventana_rev.destroy()

        ventana_rev.protocol("WM_DELETE_WINDOW", cerrar_ventana)

        crear_campo_bloqueado(
            ventana_rev,
            "Nombre estudiante:",
            evidencia_sel.nombre_estudiante,
            30
        )
        crear_campo_bloqueado(
            ventana_rev,
            "Id Estudiante:",
            evidencia_sel.id_estudiante,
            70
        )

        tk.Label(
            ventana_rev,
            text="Path archivo:",
            bg=GRIS_FONDO,
            fg=GRIS_TEXTO,
            font=("Arial", 10, "bold")
        ).place(x=30, y=110)

        entry_path = tk.Entry(
            ventana_rev,
            width=32,
            state="readonly",
            readonlybackground="#E2E8F0"
        )
        entry_path.place(x=180, y=110)
        entry_path.config(state="normal")
        entry_path.insert(0, evidencia_sel.path_archivo)
        entry_path.config(state="readonly")

        tk.Button(
            ventana_rev,
            text="Ver",
            bg=AZUL_MEDIO,
            fg=BLANCO,
            width=6,
            command=lambda: abrir_archivo_sistema(evidencia_sel.path_archivo)
        ).place(x=460, y=107)

        tk.Label(
            ventana_rev,
            text="Observaciones:",
            bg=GRIS_FONDO,
            fg=GRIS_TEXTO,
            font=("Arial", 10, "bold")
        ).place(x=30, y=150)

        text_observaciones = tk.Text(
            ventana_rev,
            width=40,
            height=5,
            bg="#E2E8F0",
            fg=NEGRO,
            relief="solid",
            highlightthickness=1,
            highlightbackground=GRIS_BORDE
        )
        text_observaciones.place(x=180, y=150)
        text_observaciones.insert("1.0", evidencia_sel.descripcion)
        text_observaciones.config(state="disabled")

        tk.Label(
            ventana_rev,
            text="Nota:",
            bg=GRIS_FONDO,
            fg=GRIS_TEXTO,
            font=("Arial", 10, "bold")
        ).place(x=30, y=250)

        def validar_nota(valor):

            if valor == "":
                return True

            try:
                if valor.count(".") > 1:
                    return False

                nota_parcial = float(valor)
                return 0 <= nota_parcial <= 5

            except ValueError:
                return False

        vcmd_nota = ventana_rev.register(validar_nota)

        entry_nota = tk.Entry(
            ventana_rev,
            width=10,
            validate="key",
            validatecommand=(vcmd_nota, "%P")
        )
        entry_nota.place(x=180, y=250)
        entry_nota.insert(0, str(evidencia_sel.calificacion))

        tk.Label(
            ventana_rev,
            text="Estado:",
            bg=GRIS_FONDO,
            fg=GRIS_TEXTO,
            font=("Arial", 10, "bold")
        ).place(x=30, y=290)

        combo_estado = ttk.Combobox(
            ventana_rev,
            values=["Revisado", "No revisado"],
            state="readonly",
            width=18
        )
        combo_estado.place(x=180, y=290)

        if evidencia_sel.estado in ["Revisado", "No revisado"]:
            combo_estado.set(evidencia_sel.estado)
        else:
            combo_estado.set("No revisado")

        def aceptar_revision():

            nota_texto = entry_nota.get().strip()
            estado = combo_estado.get().strip()

            if nota_texto == "":
                messagebox.showwarning(
                    "Validación",
                    "Ingrese la nota (0 a 5)"
                )
                return

            nota = float(nota_texto)
            if nota < 0 or nota > 5:
                messagebox.showwarning(
                    "Validación",
                    "La nota debe estar entre 0 y 5"
                )
                return

            if estado == "":
                messagebox.showwarning(
                    "Validación",
                    "Seleccione el estado"
                )
                return

            evidencia_sel.calificacion = nota
            evidencia_sel.estado = estado
            evidencia_sel.fecha_revision = datetime.now().strftime("%d/%m/%Y")

            actualizar_grilla()
            cargar_tabla_revision()

            messagebox.showinfo(
                "Revisión",
                "Evidencia revisada correctamente"
            )

            cerrar_ventana()

        tk.Button(
            ventana_rev,
            text="Cancelar",
            bg=GRIS_BORDE,
            fg=NEGRO,
            width=12,
            command=cerrar_ventana
        ).place(x=150, y=360)

        tk.Button(
            ventana_rev,
            text="Aceptar",
            bg=VERDE,
            fg=BLANCO,
            width=12,
            command=aceptar_revision
        ).place(x=290, y=360)

    tabla.bind("<<TreeviewSelect>>", abrir_ventana_revision)

# ==================================================
# MOSTRAR PANEL INICIAL
# ==================================================
mostrar_panel_estudiantes()

# ==================================================
# ACTUALIZAR MENÚ ESTUDIANTES
# ==================================================
submenu_estudiantes.destroy()

submenu_estudiantes = tk.Frame(
    contenedor_estudiantes,
    bg=AZUL_OSCURO
)

crear_item(
    submenu_estudiantes,
    "• Gestión de Evidencias",
    subitem=True,
    comando=mostrar_panel_estudiantes
)

# ==================================================
# ACTUALIZAR MENÚ TUTORES
# ==================================================
submenu_tutores.destroy()

submenu_tutores = tk.Frame(
    contenedor_tutores,
    bg=AZUL_OSCURO
)

crear_item(
    submenu_tutores,
    "• Revisar Evidencias",
    subitem=True,
    comando=revisar_evidencias
)

crear_item(
    submenu_tutores,
    "• Informes",
    subitem=True
)

ventana.mainloop()