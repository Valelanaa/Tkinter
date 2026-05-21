import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# =========================
# VENTANA PRINCIPAL
# =========================
ventana = tk.Tk()
ventana.title("Biblioteca UDI")

ancho = 900
alto = 700

x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
y = (ventana.winfo_screenheight() // 2) - (alto // 2)

ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
ventana.configure(bg="white")

# =========================
# IMAGEN SUPERIOR DERECHA
# =========================
imagen_logo = tk.PhotoImage(file="udi.png")
imagen_logo = imagen_logo.subsample(3, 3)

label_logo = tk.Label(
    ventana,
    image=imagen_logo,
    bg="white"
)

label_logo.place(
    relx=1.0,
    y=10,
    x=-10,
    anchor="ne"
)

# =========================
# VARIABLES
# =========================
num1 = tk.StringVar()
num2 = tk.StringVar()
num3 = tk.StringVar()
num4 = tk.StringVar()
num5 = tk.StringVar()
num6 = tk.StringVar()

# =========================
# CLASE BIBLIOTECA
# =========================
class Biblioteca:

    # CONSTRUCTOR
    def __init__(self):

        # ARRAY DINAMICO
        self.datos_libros = []

    # =========================
    # METODO NUEVO
    # =========================
    def nuevo(
        self,
        cajas,
        focus_entry,
        funcion_guardar
    ):

        hay_datos = False

        for caja in cajas:

            if caja.get() != "":
                hay_datos = True

        if hay_datos:

            respuesta = messagebox.askyesno(
                "Guardar",
                "¿Desea guardar la información antes de limpiar?"
            )

            if respuesta:
                funcion_guardar()

        for caja in cajas:
            caja.set("")

        focus_entry.focus()

    # =========================
    # METODO GUARDAR
    # =========================
    def guardar(self, registro):

        self.datos_libros.append(registro)

    # =========================
    # METODO ELIMINAR
    # =========================
    def eliminar(self, indice):

        if 0 <= indice < len(self.datos_libros):

            self.datos_libros.pop(indice)

    # =========================
    # METODO EDITAR
    # =========================
    def editar(self, indice, nuevos_datos):

        if 0 <= indice < len(self.datos_libros):

            self.datos_libros[indice]["nombre"] = nuevos_datos["nombre"]

            self.datos_libros[indice]["editorial"] = nuevos_datos["editorial"]

            self.datos_libros[indice]["autor"] = nuevos_datos["autor"]

            self.datos_libros[indice]["copias"] = nuevos_datos["copias"]

# OBJETO DE LA CLASE
biblioteca = Biblioteca()

# FILA SELECCIONADA
fila_seleccionada = None

# =========================
# VALIDACIONES
# =========================
def validar_fecha(texto):

    if len(texto) > 10:
        return False

    for c in texto:
        if not (c.isdigit() or c == "/"):
            return False

    return True


def validar_id(texto):

    return len(texto) <= 10


def validar_texto_100(texto):

    return len(texto) <= 100


def validar_copias(texto):

    if texto == "":
        return True

    return texto.isdigit() and len(texto) <= 3


validacionFecha = ventana.register(validar_fecha)
validacionId = ventana.register(validar_id)
validacionTexto100 = ventana.register(validar_texto_100)
validacionCopias = ventana.register(validar_copias)

# =========================
# FECHA
# =========================
filaFecha = tk.Frame(ventana, bg="white")
filaFecha.pack(pady=2, anchor="w", padx=10)

etiquetaFecha = tk.Label(
    filaFecha,
    text="Fecha de ingreso:",
    font=("Arial", 11),
    bg="white",
    width=18,
    anchor="w"
)
etiquetaFecha.pack(side="left")

fecha_actual = datetime.now().strftime("%d/%m/%Y")
num1.set(fecha_actual)

textoFecha = tk.Entry(
    filaFecha,
    font=("Arial", 11),
    bg="lightyellow",
    textvariable=num1,
    state="readonly",
    width=40
)
textoFecha.pack(side="left")

# =========================
# ID
# =========================
filaId = tk.Frame(ventana, bg="white")
filaId.pack(pady=2, anchor="w", padx=10)

etiquetaId = tk.Label(
    filaId,
    text="ID del libro:",
    font=("Arial", 11),
    bg="white",
    width=18,
    anchor="w"
)
etiquetaId.pack(side="left")

textoId = tk.Entry(
    filaId,
    font=("Arial", 11),
    bg="lightyellow",
    textvariable=num2,
    validate="key",
    validatecommand=(validacionId, "%P"),
    width=40
)
textoId.pack(side="left")

# =========================
# NOMBRE
# =========================
filaNombre = tk.Frame(ventana, bg="white")
filaNombre.pack(pady=2, anchor="w", padx=10)

etiquetaNombre = tk.Label(
    filaNombre,
    text="Nombre del libro:",
    font=("Arial", 11),
    bg="white",
    width=18,
    anchor="w"
)
etiquetaNombre.pack(side="left")

textoNombre = tk.Entry(
    filaNombre,
    font=("Arial", 11),
    bg="lightyellow",
    textvariable=num3,
    validate="key",
    validatecommand=(validacionTexto100, "%P"),
    width=40
)
textoNombre.pack(side="left")

# =========================
# EDITORIAL
# =========================
filaEditorial = tk.Frame(ventana, bg="white")
filaEditorial.pack(pady=2, anchor="w", padx=10)

etiquetaEditorial = tk.Label(
    filaEditorial,
    text="Editorial:",
    font=("Arial", 11),
    bg="white",
    width=18,
    anchor="w"
)
etiquetaEditorial.pack(side="left")

textoEditorial = tk.Entry(
    filaEditorial,
    font=("Arial", 11),
    bg="lightyellow",
    textvariable=num4,
    validate="key",
    validatecommand=(validacionTexto100, "%P"),
    width=40
)
textoEditorial.pack(side="left")

# =========================
# AUTOR
# =========================
filaAutor = tk.Frame(ventana, bg="white")
filaAutor.pack(pady=2, anchor="w", padx=10)

etiquetaAutor = tk.Label(
    filaAutor,
    text="Autor:",
    font=("Arial", 11),
    bg="white",
    width=18,
    anchor="w"
)
etiquetaAutor.pack(side="left")

textoAutor = tk.Entry(
    filaAutor,
    font=("Arial", 11),
    bg="lightyellow",
    textvariable=num5,
    validate="key",
    validatecommand=(validacionTexto100, "%P"),
    width=40
)
textoAutor.pack(side="left")

# =========================
# COPIAS
# =========================
filaCopias = tk.Frame(ventana, bg="white")
filaCopias.pack(pady=2, anchor="w", padx=10)

etiquetaCopias = tk.Label(
    filaCopias,
    text="Numero de copias:",
    font=("Arial", 11),
    bg="white",
    width=18,
    anchor="w"
)
etiquetaCopias.pack(side="left")

textoCopias = tk.Entry(
    filaCopias,
    font=("Arial", 11),
    bg="lightyellow",
    textvariable=num6,
    validate="key",
    validatecommand=(validacionCopias, "%P"),
    width=40
)
textoCopias.pack(side="left")

# =========================
# TABLA
# =========================
ANCHOS_COL = (120, 100, 220, 180, 180, 80)

TEXTO_COL = (
    "Fecha ingreso",
    "ID Libro",
    "Nombre del libro",
    "Editorial",
    "Autor",
    "Copias",
)

FUENTE_CELDA = ("Arial", 10)

contador_filas_tabla = []

# =========================
# SELECCIONAR FILA
# =========================
def seleccionar_fila(fila):

    global fila_seleccionada

    fila_seleccionada = fila

    for i, widgets in enumerate(contador_filas_tabla):

        color = "#ededed" if i % 2 else "white"

        for w in widgets:
            w.config(bg=color)

    indice = fila - 1

    if 0 <= indice < len(contador_filas_tabla):

        for w in contador_filas_tabla[indice]:
            w.config(bg="lightblue")

# =========================
# INSERTAR FILA
# =========================
def insertar_fila_registro(valores):

    n = len(contador_filas_tabla)

    bg = "#ededed" if n % 2 else "white"

    r = n + 1

    fila_widgets = []

    for col, val in enumerate(valores):

        ancla = "center" if col in (0, 1, 5) else "w"

        lbl = tk.Label(
            inner_tabla,
            text=str(val),
            font=FUENTE_CELDA,
            bg=bg,
            fg="black",
            relief=tk.SOLID,
            borderwidth=1,
            anchor=ancla,
            padx=2,
            pady=0,
            width=int(ANCHOS_COL[col] / 10),
            wraplength=ANCHOS_COL[col]
        )

        lbl.grid(
            row=r,
            column=col,
            sticky="news"
        )

        lbl.bind(
            "<Button-1>",
            lambda e, fila=r: seleccionar_fila(fila)
        )

        fila_widgets.append(lbl)

    contador_filas_tabla.append(fila_widgets)

    canvas_tabla.update_idletasks()

    canvas_tabla.configure(
        scrollregion=canvas_tabla.bbox("all")
    )


# =========================
# BLOQUEAR CAMPOS
# =========================
def bloquear_campos():

    textoId.config(state="readonly")
    textoNombre.config(state="readonly")
    textoEditorial.config(state="readonly")
    textoAutor.config(state="readonly")
    textoCopias.config(state="readonly")


# =========================
# HABILITAR CAMPOS
# =========================
def habilitar_campos():

    textoId.config(state="normal")
    textoNombre.config(state="normal")
    textoEditorial.config(state="normal")
    textoAutor.config(state="normal")
    textoCopias.config(state="normal")
    
# =========================
# NUEVO
# =========================
def nuevo_registro():

    if (
        num2.get() != "" or
        num3.get() != "" or
        num4.get() != "" or
        num5.get() != "" or
        num6.get() != ""
    ):

        respuesta = messagebox.askyesno(
            "Guardar",
            "¿Desea guardar la información antes de limpiar?"
        )

        if respuesta:
            guardar_datos()


    # HABILITAR CAMPOS
    habilitar_campos()
    
    num2.set("")
    num3.set("")
    num4.set("")
    num5.set("")
    num6.set("")

    textoId.focus()

# =========================
# GUARDAR
# =========================
def guardar_datos():

    if (
        num2.get() == "" or
        num3.get() == "" or
        num4.get() == "" or
        num5.get() == "" or
        num6.get() == ""
    ):

        messagebox.showwarning(
            "Campos vacíos",
            "Debe completar todos los campos"
        )

        return

    respuesta = messagebox.askyesno(
        "Guardar",
        "¿Desea guardar el registro?"
    )

    if respuesta:

        biblioteca.guardar(
            {
                "fecha": num1.get(),
                "id": num2.get(),
                "nombre": num3.get(),
                "editorial": num4.get(),
                "autor": num5.get(),
                "copias": num6.get()
            }
        )

        insertar_fila_registro(
            (
                num1.get(),
                num2.get(),
                num3.get(),
                num4.get(),
                num5.get(),
                num6.get()
            )
        )

        messagebox.showinfo(
            "Guardado",
            "Registro guardado correctamente"
        )
                # BLOQUEAR CAMPOS
        bloquear_campos()

# =========================
# ELIMINAR REGISTRO
# =========================
def eliminar_registro():

    global fila_seleccionada

    if fila_seleccionada is None:

        messagebox.showwarning(
            "Eliminar",
            "Debe seleccionar un registro"
        )

        return

    respuesta = messagebox.askyesno(
        "Eliminar",
        "¿Desea eliminar el registro seleccionado?"
    )

    if respuesta:

        indice = fila_seleccionada - 1

        biblioteca.eliminar(indice)

        if 0 <= indice < len(contador_filas_tabla):

            for widget in contador_filas_tabla[indice]:
                widget.destroy()

            contador_filas_tabla.pop(indice)

        for i, fila in enumerate(contador_filas_tabla):

            nueva_fila = i + 1

            for col, widget in enumerate(fila):

                widget.grid(
                    row=nueva_fila,
                    column=col,
                    sticky="nsew"
                )

                widget.bind(
                    "<Button-1>",
                    lambda e, fila=nueva_fila:
                    seleccionar_fila(fila)
                )

        fila_seleccionada = None
        
# =========================
# EDITAR REGISTRO
# =========================
def editar_registro():

    global fila_seleccionada

    if fila_seleccionada is None:

        messagebox.showwarning(
            "Editar",
            "Debe seleccionar un registro"
        )

        return

    indice = fila_seleccionada - 1

    if 0 <= indice < len(biblioteca.datos_libros):

        registro = biblioteca.datos_libros[indice]

        # CARGAR DATOS EN LOS ENTRY
        num1.set(registro["fecha"])
        num2.set(registro["id"])
        num3.set(registro["nombre"])
        num4.set(registro["editorial"])
        num5.set(registro["autor"])
        num6.set(registro["copias"])

        # HABILITAR CAMPOS
        textoNombre.config(state="normal")
        textoEditorial.config(state="normal")
        textoAutor.config(state="normal")
        textoCopias.config(state="normal")

        # BLOQUEAR FECHA E ID
        textoFecha.config(state="readonly")
        textoId.config(state="readonly")

        # CAMBIAR BOTON GUARDAR A ACTUALIZAR
        botonGuardar.config(
            text="Actualizar",
            command=actualizar_registro
        )
        
# =========================
# ACTUALIZAR REGISTRO
# =========================
def actualizar_registro():

    global fila_seleccionada

    if fila_seleccionada is None:
        return

    indice = fila_seleccionada - 1

    respuesta = messagebox.askyesno(
        "Actualizar",
        "¿Desea actualizar el registro?"
    )

    if respuesta:

        # ACTUALIZAR ARRAY
        biblioteca.editar(indice, {
            "nombre": num3.get(),
            "editorial": num4.get(),
            "autor": num5.get(),
            "copias": num6.get()
        })

        fila = contador_filas_tabla[indice]

        # ACTUALIZAR TABLA
        fila[2].config(text=num3.get())
        fila[3].config(text=num4.get())
        fila[4].config(text=num5.get())
        fila[5].config(text=num6.get())

        messagebox.showinfo(
            "Actualizado",
            "Registro actualizado correctamente"
        )

        # BLOQUEAR CAMPOS
        bloquear_campos()

        # RESTAURAR BOTON GUARDAR
        botonGuardar.config(
            text="Guardar",
            command=guardar_datos
        )

        textoId.focus()
        
    
        


# =========================
# BOTONES
# =========================
filaBotones = tk.Frame(ventana, bg="white")
filaBotones.pack(pady=10)

botonNuevo = tk.Button(
    filaBotones,
    text="Nuevo",
    font=("Arial", 10, "bold"),
    bg="khaki",
    width=12,
    command=nuevo_registro
)
botonNuevo.pack(side="left", padx=5)

botonEditar = tk.Button(
    filaBotones,
    text="Editar",
    font=("Arial", 10, "bold"),
    bg="lightblue",
    width=12,
    command=editar_registro
)

botonEditar.pack(side="left", padx=5)

botonGuardar = tk.Button(
    filaBotones,
    text="Guardar",
    font=("Arial", 10, "bold"),
    bg="lightgreen",
    width=12,
    command=guardar_datos
)
botonGuardar.pack(side="left", padx=5)

botonBorrar = tk.Button(
    filaBotones,
    text="Eliminar",
    font=("Arial", 10, "bold"),
    bg="tomato",
    width=12,
    command=eliminar_registro
)
botonBorrar.pack(side="left", padx=5)



# =========================
# TABLA VISUAL
# =========================
frameTabla = tk.Frame(
    ventana,
    bg="white",
    relief=tk.SOLID,
    borderwidth=1
)

frameTabla.pack(
    pady=4,
    anchor="w",
    padx=10,
    fill="x"
)

canvas_tabla = tk.Canvas(
    frameTabla,
    bg="white",
    highlightthickness=0,
    height=200,
)

scroll_tabla = tk.Scrollbar(
    frameTabla,
    orient=tk.VERTICAL,
    command=canvas_tabla.yview,
)
scroll_horizontal = tk.Scrollbar(
    frameTabla,
    orient=tk.HORIZONTAL,
    command=canvas_tabla.xview
)

canvas_tabla.configure(
    yscrollcommand=scroll_tabla.set,
    xscrollcommand=scroll_horizontal.set
)

inner_tabla = tk.Frame(
    canvas_tabla,
    bg="white"
)

for c, ancho in enumerate(ANCHOS_COL):

    inner_tabla.grid_columnconfigure(
        c,
        minsize=ancho,
        weight=0
    )

for col, titulo in enumerate(TEXTO_COL):

    tk.Label(
        inner_tabla,
        text=titulo,
        font=("Arial", 10, "bold"),
        bg="white",
        fg="black",
        relief=tk.SOLID,
        borderwidth=1,
        anchor="center",
        padx=2,
        pady=0,
    ).grid(
        row=0,
        column=col,
        sticky="nsew"
    )

window_inner_id = canvas_tabla.create_window(
    (0, 0),
    window=inner_tabla,
    anchor="nw"
)

def _actualizar_scroll_tabla(_event=None):

    canvas_tabla.configure(
        scrollregion=canvas_tabla.bbox("all")
    )

    canvas_tabla.itemconfig(
        window_inner_id,
        width=sum(ANCHOS_COL) + 20
    )

inner_tabla.bind(
    "<Configure>",
    _actualizar_scroll_tabla
)

canvas_tabla.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scroll_tabla.grid(
    row=0,
    column=1,
    sticky="ns"
)
scroll_horizontal.grid(
    row=1,
    column=0,
    sticky="ew"
)

frameTabla.rowconfigure(0, weight=1)
frameTabla.columnconfigure(0, weight=1)

_actualizar_scroll_tabla()



# =========================
# CANCELAR
# =========================
def cancelar_datos():

    if (
        num2.get() != "" or
        num3.get() != "" or
        num4.get() != "" or
        num5.get() != "" or
        num6.get() != ""
    ):

        respuesta = messagebox.askyesno(
            "Cancelar",
            "¿Desea eliminar toda la información de los cuadros de texto?"
        )

        if respuesta:

            num2.set("")
            num3.set("")
            num4.set("")
            num5.set("")
            num6.set("")

            textoId.focus()

    else:
        textoId.focus()


# =========================
# MOSTRAR DATOS
# =========================
def mostrar_datos():

    respuesta = messagebox.askyesno(
        "Mostrar Datos",
        "¿Desea limpiar la grilla y volver a cargar los datos del Array Dinámico?"
    )

    if respuesta:

        # LIMPIAR CAMPOS DE TEXTO
        num2.set("")
        num3.set("")
        num4.set("")
        num5.set("")
        num6.set("")

        # ELIMINAR FILAS VISUALES DE LA GRILLA
        for fila in contador_filas_tabla:

            for widget in fila:
                widget.destroy()

        contador_filas_tabla.clear()

        # VOLVER A MOSTRAR DATOS DEL ARRAY DINAMICO
        for libro in biblioteca.datos_libros:

            insertar_fila_registro(
                (
                    libro["fecha"],
                    libro["id"],
                    libro["nombre"],
                    libro["editorial"],
                    libro["autor"],
                    libro["copias"]
                )
            )

        textoId.focus()

# =========================
# SALIR
# =========================
def salir_programa():

    respuesta = messagebox.askyesno(
        "Salir",
        "¿Desea salir del programa?"
    )

    if respuesta:

        # LIMPIAR ARRAY
        biblioteca.datos_libros.clear()

        # LIMPIAR TABLA
        for fila in contador_filas_tabla:

            for widget in fila:
                widget.destroy()

        contador_filas_tabla.clear()

        ventana.destroy()

    else:
        textoId.focus()


# =========================
# BOTONES INFERIORES
# =========================
filaBotonesInferiores = tk.Frame(
    ventana,
    bg="white"
)

filaBotonesInferiores.pack(
    pady=10
)

# BOTON CANCELAR
botonCancelar = tk.Button(
    filaBotonesInferiores,
    text="Cancelar",
    font=("Arial", 10, "bold"),
    bg="orange",
    fg="black",
    width=15,
    command=cancelar_datos
)

botonCancelar.pack(
    side="left",
    padx=10
)

# BOTON MOSTRAR DATOS
botonMostrarDatos = tk.Button(
    filaBotonesInferiores,
    text="Mostrar Datos",
    font=("Arial", 10, "bold"),
    bg="gold",
    fg="black",
    width=15,
    command=mostrar_datos
)

botonMostrarDatos.pack(
    side="left",
    padx=10
)

# BOTON SALIR
botonSalir = tk.Button(
    filaBotonesInferiores,
    text="Salir",
    font=("Arial", 10, "bold"),
    bg="red",
    fg="white",
    width=15,
    command=salir_programa
)

botonSalir.pack(
    side="left",
    padx=10
)

textoId.focus()

# =========================
# ENTER PARA CAMBIAR DE CAMPO
# =========================
def pasar_siguiente(event, siguiente):

    siguiente.focus()

# FECHA -> ID
textoFecha.bind(
    "<Return>",
    lambda event: pasar_siguiente(event, textoId)
)

# ID -> NOMBRE
textoId.bind(
    "<Return>",
    lambda event: pasar_siguiente(event, textoNombre)
)

# NOMBRE -> EDITORIAL
textoNombre.bind(
    "<Return>",
    lambda event: pasar_siguiente(event, textoEditorial)
)

# EDITORIAL -> AUTOR
textoEditorial.bind(
    "<Return>",
    lambda event: pasar_siguiente(event, textoAutor)
)

# AUTOR -> COPIAS
textoAutor.bind(
    "<Return>",
    lambda event: pasar_siguiente(event, textoCopias)
)

# COPIAS -> BOTON GUARDAR
textoCopias.bind(
    "<Return>",
    lambda event: botonGuardar.focus()
)

habilitar_campos()

ventana.mainloop()