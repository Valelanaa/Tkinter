import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
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
# FUNCIÓN MODIFICAR EVIDENCIA
# ==================================================
def modificar_evidencia():

    seleccionado = grilla.selection()

    # Validar selección
    if not seleccionado:
        messagebox.showwarning(
            "Modificar",
            "Debe seleccionar un registro para modificar"
        )
        return

    # Obtener datos
    item = seleccionado[0]
    datos = grilla.item(item, "values")

    id_evidencia = datos[0]
    nombre_actual = datos[1]
    tipo_actual = datos[2]
    fecha_actual = datos[3]
    descripcion_actual = datos[4]
    archivo_actual = datos[5]

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

    combo_tipo_mod = ttk.Combobox(
        ventana_mod,
        values=["PDF", "Word", "Excel", "Imagen"],
        state="readonly",
        width=27
    )
    combo_tipo_mod.place(x=170, y=110)
    combo_tipo_mod.set(tipo_actual)

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
        nuevo_tipo = combo_tipo_mod.get().strip()
        nueva_fecha = fecha_var.get().strip()
        nueva_descripcion = text_desc_mod.get("1.0", tk.END).strip()
        nuevo_archivo = ruta_modificada.get().strip()

        if nuevo_nombre == "":
            messagebox.showwarning(
                "Validación",
                "Ingrese el nombre"
            )
            return

        if nuevo_tipo == "":
            messagebox.showwarning(
                "Validación",
                "Seleccione el tipo"
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar modificación",
            f"¿Desea modificar la evidencia:\n\n{nuevo_nombre}?"
        )

        if confirmar:
            grilla.item(
                item,
                values=(
                    id_evidencia,
                    nuevo_nombre,
                    nuevo_tipo,
                    nueva_fecha,
                    nueva_descripcion,
                    nuevo_archivo
                )
            )

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
    "• Subir Preguntas",
    subitem=True
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

# Título de sección
tk.Label(
    panel_contenido,
    text="Estudiantes — Evidencias / Bitácoras",
    bg=GRIS_FONDO, fg=AZUL_OSCURO,
    font=("Arial", 13, "bold"), anchor="w"
).pack(anchor="w", pady=(0, 6))

tk.Frame(panel_contenido, bg=GRIS_BORDE, height=1).pack(fill="x", pady=(0, 8))

# --------------------------------------------------
# FILA SUPERIOR: mitad izquierda (combo) | mitad derecha (formulario)
# --------------------------------------------------
fila_superior = tk.Frame(panel_contenido, bg=GRIS_FONDO)
fila_superior.pack(fill="x")
fila_superior.columnconfigure(0, weight=1)
fila_superior.columnconfigure(1, weight=1)

# ---- Columna izquierda: combo Evidencias/Bitácoras ----
panel_izq = tk.Frame(fila_superior, bg=GRIS_FONDO)
panel_izq.grid(row=0, column=0, sticky="nw", padx=(0, 12), pady=(0, 6))

tk.Label(
    panel_izq, text="Evidencias / Bitácoras",
    bg=GRIS_FONDO, fg=GRIS_TEXTO, font=("Arial", 9)
).pack(anchor="w")

combo_evidencias = ttk.Combobox(
    panel_izq, values=["Todos", "Bitácora", "Evidencia"],
    state="readonly", width=20
)
combo_evidencias.current(0)
combo_evidencias.pack(anchor="w", pady=(2, 0))

# ---- Columna derecha: formulario alineado ----
panel_der = tk.Frame(fila_superior, bg=GRIS_FONDO)
panel_der.grid(row=0, column=1, sticky="ne", padx=(20, 0), pady=(0, 6))

# Configuración de columnas
panel_der.columnconfigure(0, weight=0)
panel_der.columnconfigure(1, weight=1)

# ==================================================
# TIPO
# ==================================================
tk.Label(
    panel_der,
    text="Tipo:",
    bg=GRIS_FONDO,
    fg=GRIS_TEXTO,
    font=("Arial", 10, "bold")
).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=6)

combo_tipo = ttk.Combobox(
    panel_der,
    values=["PDF", "Word", "Excel", "Imagen"],
    state="readonly",
    width=30
)
combo_tipo.grid(row=0, column=1, sticky="w", pady=6)

# ==================================================
# NOMBRE EVIDENCIA
# ==================================================
tk.Label(
    panel_der,
    text="Nombre Evidencia:",
    bg=GRIS_FONDO,
    fg=GRIS_TEXTO,
    font=("Arial", 10, "bold")
).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=6)

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
entry_nombre.grid(row=1, column=1, sticky="w", pady=6)

# ==================================================
# DESCRIPCIÓN
# ==================================================
tk.Label(
    panel_der,
    text="Descripción:",
    bg=GRIS_FONDO,
    fg=GRIS_TEXTO,
    font=("Arial", 10, "bold")
).grid(row=2, column=0, sticky="nw", padx=(0, 10), pady=6)

frame_desc = tk.Frame(
    panel_der,
    bg=GRIS_BORDE,
    bd=1,
    relief="solid"
)
frame_desc.grid(row=2, column=1, sticky="w", pady=6)

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
# CAMPO FECHA (BLOQUEADO)
# ==================================================
tk.Label(
    panel_der,
    text="Fecha:",
    bg=GRIS_FONDO,
    fg=GRIS_TEXTO,
    font=("Arial", 10, "bold")
).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=6)

entry_fecha = tk.Entry(
    panel_der,
    font=("Arial", 10),
    bg="#E2E8F0",
    fg=NEGRO,
    width=32,
    state="readonly",
    readonlybackground="#E2E8F0"
)

entry_fecha.grid(row=3, column=1, sticky="w", pady=6)

# ==================================================
# FUNCIÓN CARGAR EVIDENCIA
# ==================================================
ruta_archivo = ""

def cargar_evidencia():

    global ruta_archivo

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

# ==================================================
# BOTÓN CARGAR EVIDENCIA
# ==================================================
btn_cargar = tk.Button(
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
)

btn_cargar.grid(
    row=4,
    column=1,
    sticky="e",
    pady=(10, 0)
)

# ==================================================
# BOTÓN CARGAR
# ==================================================
btn_cargar.grid(row=4, column=1, sticky="e", pady=(10, 0))


# ==================================================
# FUNCIÓN NUEVA EVIDENCIA
# ==================================================
def nueva_evidencia():

    # -----------------------------
    # LIMPIAR COMBOS
    # -----------------------------
    combo_tipo.set("")
    combo_evidencias.set("")

    # -----------------------------
    # LIMPIAR ENTRIES
    # -----------------------------
    entry_nombre.delete(0, tk.END)

    # -----------------------------
    # LIMPIAR TEXT
    # -----------------------------
    text_descripcion.delete("1.0", tk.END)

    # -----------------------------
    # FECHA ACTUAL DEL SISTEMA
    # -----------------------------
    fecha_sistema = datetime.now().strftime("%d/%m/%Y")

    entry_fecha.config(state="normal")
    entry_fecha.delete(0, tk.END)
    entry_fecha.insert(0, fecha_sistema)
    entry_fecha.config(state="readonly")

# --------------------------------------------------
# GRILLA / TABLA
# --------------------------------------------------
tk.Frame(panel_contenido, bg=GRIS_BORDE, height=1).pack(fill="x", pady=8)

columnas = ("id_evidencia", "nom_evidencia", "tipo", "fecha_carga", "descripcion", "archivo")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Grilla.Treeview",
    background=BLANCO, fieldbackground=BLANCO,
    foreground=NEGRO, rowheight=22,
    font=("Arial", 10)
)
style.configure(
    "Grilla.Treeview.Heading",
    background=AZUL_OSCURO, foreground=BLANCO,
    font=("Arial", 10, "bold"), relief="flat"
)
style.map("Grilla.Treeview", background=[("selected", AZUL_MEDIO)])

frame_tabla = tk.Frame(panel_contenido, bg=GRIS_BORDE, bd=1, relief="solid")
frame_tabla.pack(fill="both", expand=True)

scroll_tabla = tk.Scrollbar(frame_tabla)
scroll_tabla.pack(side="right", fill="y")

grilla = ttk.Treeview(
    frame_tabla,
    columns=columnas,
    show="headings",
    yscrollcommand=scroll_tabla.set,
    style="Grilla.Treeview",
    height=6
)
grilla.pack(fill="both", expand=True)
scroll_tabla.config(command=grilla.yview)

encabezados = {
    "id_evidencia":  ("Id",              50),
    "nom_evidencia": ("Nom. Evidencia",  130),
    "tipo":          ("Tipo",            70),
    "fecha_carga":   ("Fecha de Carga",  95),
    "descripcion":   ("Descripción",     160),
    "archivo":       ("Archivo",         80),
}

for col, (texto, ancho_col) in encabezados.items():
    grilla.heading(col, text=texto)
    grilla.column(col, width=ancho_col, minwidth=40, anchor="w")

# --------------------------------------------------
# BARRA DE ACCIONES
# --------------------------------------------------
tk.Frame(panel_contenido, bg=GRIS_BORDE, height=1).pack(fill="x", pady=(8, 6))

barra_acciones = tk.Frame(panel_contenido, bg=GRIS_FONDO)
barra_acciones.pack(fill="x")

# ==================================================
# FUNCIÓN ELIMINAR EVIDENCIA
# ==================================================
def eliminar_evidencia():

    # Obtener selección
    seleccionado = grilla.selection()

    # Validar si seleccionó algo
    if not seleccionado:
        messagebox.showwarning(
            "Eliminar",
            "Debe seleccionar un registro para eliminar"
        )
        return

    # Obtener datos del registro seleccionado
    item = seleccionado[0]
    datos = grilla.item(item, "values")

    id_evidencia = datos[0]
    nombre_evidencia = datos[1]

    # Confirmación
    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Está seguro de eliminar el registro?\n\n"
        f"ID: {id_evidencia}\n"
        f"Nombre: {nombre_evidencia}"
    )

    # Si acepta, eliminar
    if confirmar:
        grilla.delete(item)

        messagebox.showinfo(
            "Eliminado",
            "Registro eliminado correctamente"
        )

def accion_placeholder(nombre):
    messagebox.showinfo(nombre, f"Acción: {nombre}")
    
# ==================================================
# CONTADOR ID EVIDENCIA
# ==================================================
contador_id_evidencia = 1

# ==================================================
# FUNCIÓN ACEPTAR EVIDENCIA
# ==================================================
def aceptar_evidencia():

    global contador_id_evidencia
    global ruta_archivo

    # ------------------------------------------
    # DATOS DEL FORMULARIO
    # ------------------------------------------
    nombre_evidencia = entry_nombre.get().strip()

    tipo_evidencia = combo_tipo.get().strip()

    fecha_sistema = entry_fecha.get().strip()

    descripcion = text_descripcion.get(
        "1.0",
        tk.END
    ).strip()

    # ------------------------------------------
    # VALIDACIONES
    # ------------------------------------------
    if nombre_evidencia == "":
        messagebox.showwarning(
            "Validación",
            "Ingrese el nombre de la evidencia"
        )
        return

    if tipo_evidencia == "":
        messagebox.showwarning(
            "Validación",
            "Seleccione el tipo"
        )
        return

    if ruta_archivo == "":
        messagebox.showwarning(
            "Validación",
            "Debe cargar un archivo"
        )
        return

    # ------------------------------------------
    # INSERTAR EN LA GRILLA
    # ------------------------------------------
    grilla.insert(
        "",
        "end",
        values=(
            contador_id_evidencia,
            nombre_evidencia,
            tipo_evidencia,
            fecha_sistema,
            descripcion,
            ruta_archivo
        )
    )

    # ------------------------------------------
    # INCREMENTAR ID
    # ------------------------------------------
    contador_id_evidencia += 1

    # ------------------------------------------
    # MENSAJE
    # ------------------------------------------
    messagebox.showinfo(
        "Registro",
        "Evidencia registrada correctamente"
    )

botones_acciones = [

    (
        "Cancelar",
        GRIS_BORDE,
        NEGRO,
        lambda: accion_placeholder("Cancelar")
    ),

    (
        "Nueva Evidencia",
        AZUL_MEDIO,
        BLANCO,
        nueva_evidencia
    ),

    (
    "Modificar",
    AZUL_OSCURO,
    BLANCO,
    modificar_evidencia
    ),

    (
    "Eliminar",
    ROJO,
    BLANCO,
    eliminar_evidencia
    ),

    (
        "Aceptar",
        VERDE,
        BLANCO,
        aceptar_evidencia
    )

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
# ==================================================
ventana.mainloop()