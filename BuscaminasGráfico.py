# Importa todo de la librería de Tkinter, y de la misma un fragmento para mensajes emergentes y entrada de texto
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

# Librería para números aleatorios
import random

# AJUSTES, ALGUNOS LOS PUEDE CONFIGURAR EL USUARIO, EN LA FUNCIÓN DE EDICIÓN SE VERIFICAN VALORES VÁLIDOS
ajustes = {
    "celdasX": 10, # Cantidad de celdas en el eje X
    "celdasY": 10, # Cantidad de celdas en el eje Y
    "anchoCelda": 30, # Ancho de una celda
    "altoCelda": 30, # Alto de una celda
    "bombas": 0, # Cantidad de bombas, no modificar, valor que se actualiza solo tras la carga de una partida
    "titulo": "Buscaminas", # Título de la ventana
    "banderaCaracter": "", # Caracter de una bandera
    "bombaCaracter": "*", # Caracter de una bomba
    "maximoBombas": 0, # Número máximo de bombas (nBombas = int((celdasX * celdasY) / 6)), se actualiza solo, no modificar
    "dificultad": 10 # 1 -> Imposible (no escribir), 10 -> sencillo
}

# MÉTODO PARA CAMBIAR LAS DIMENSIONES
def cambiarDimensiones():
    try:
        # El usuario es preguntado por los datos nuevos
        celdas = simpledialog.askstring(title="Cambiar dimensión", prompt="ancho x alto:").split("x")
        
        # Se intenta realizar una conversión de string a enteros
        celdasX = int(celdas[0])
        celdasY = int(celdas[1])
        
        # Se verifica que el valor aportado es válido
        if celdasX in range(3, 11) and celdasY in range(3, 11):
            # En ese caso, le pasa los datos a otro método para que actualice las dimensiones
            actualizarDimensiones(celdasX, celdasY)
    except:
        # Pasa del error
        pass

# Actualiza las dimensiones con unos valores aportados
def actualizarDimensiones(cantidadX, cantidadY):    
    # Oculta todos los botones
    # En el eje Y
    for i in range(ajustes["celdasY"]):
        # En el eje X
        for j in range(ajustes["celdasX"]):
            # Los oculta, pero no los destruye
            tablero[i][j].place_forget()
    
    # Actualiza la información
    ajustes["celdasX"] = cantidadX
    ajustes["celdasY"] = cantidadY
    
    # Muestra aquellos botones que si existen
    for i in range(ajustes["celdasY"]):
        for j in range(ajustes["celdasX"]):
            tablero[i][j].place(
                x = j * ajustes["anchoCelda"],
                y = i * ajustes["altoCelda"] + 30, # +30 por el margen superior de los datos
                width = ajustes["anchoCelda"],
                height = ajustes["altoCelda"]
            )
    
    # Repite la partida de nuevo (actualizar)
    repetir()

# FUNCIÓN PARA MOSTRAR MENSAJES EMERGENTES CON TÍTULO Y CONTENIDO
def mostrarMensajeEmergente(mensaje, titulo):
    # Se indica el icono de 'question' para que la ventana no emita sonido cuando aparezca
    messagebox.showinfo(message=mensaje, title=titulo, icon="question")

# FUNCIÓN PARA CAMBIAR EL NÚMERO DE BOMBAS
def cambiarCantidadBombas():
    # Pregunta al usuario por un dato
    bombas = simpledialog.askstring(title="Cambiar cantidad de bombas", prompt="Bombas:")
    # En caso de error, salta el proceso
    try:
        # Convierte el dato a entero (inicialmente estaba en string)
        bombas = int(bombas)
        
        # Evita que el número sea muy pequeño o excesivamente grande
        if bombas <= 1 or bombas > ajustes["maximoBombas"]:
            mostrarMensajeEmergente(f"No puedes crear más de {ajustes['maximoBombas']} y menos de 1", "Error cambiando el número de bombas")
        else:
            # Si todo es correcto, actualiza el número de bombas de los ajustes y repite la partida
            ajustes["bombas"] = bombas
            repetir()
    except: # ValueError -> contenido del error
        # Muestra un mensaje de error
        # mostrarMensajeEmergente("Escribe un número válido", "Error cambiando el número de bombas")
        pass # Es posible que el usuario pulse el botón 'Cancelar', por eso se comenta la línea anterior

# FUNCIÓN PARA CAMBIAR EL CARACTER DE UNA BOMBA
def cambiarCaracterBomba():
    # En caso de errores por datos no admitidos por el programa
    try:
        # El usuario escribe un dato
        caracter = simpledialog.askstring(title="Cambiar caracter de de una bomba", prompt="Nuevo caracter:")
        # Si el dato no es de un solo caracter
        if len(caracter) != 1:
            # Muestra un mensaje de error
            mostrarMensajeEmergente("Dato inválido", "Error cambiando el dato")
        else:
            # Cambia el caracter actual de los ajustes por el nuevo
            ajustes["bombaCaracter"] = caracter
    except:
        # Pasa del error, puede desencadenarse por un texto excesivamente largo, y tal vez el programa no lo soporta
        pass

# FUNCIÓN PARA ESTABLECER UN NÚMERO APROPIADO DE BOMBAS
def setNumeroApropiadoBombas():
    # Indica que modificará la variable global banderas
    global banderas
    
    # Realiza un cálculo para obtener un número máximo de bombas
    ajustes["maximoBombas"] = int((ajustes["celdasY"] * ajustes["celdasX"]) / ajustes["dificultad"])
    
    # Establece el número de bombas según el máximo indicado
    ajustes["bombas"] = ajustes["maximoBombas"]
    
    # Actualiza el valor global
    banderas = ajustes["bombas"]
    
    # Actualiza el texto
    textoBanderas.config(text=f"Banderas: {banderas}")

# FUNCIÓN PARA REPETIR EL JUEGO
def repetir():
    # Declara las variables de uso global para que sean accesibles
    global tablero, finalJuego, solucion, intentos
    
    # Define un nuevo tablero, menciona que el final del juego está a 0, las banderas a los ajustes actuales y los intentos a 0
    solucion = definirTablero(ajustes["celdasX"], ajustes["celdasY"], 0)
    finalJuego = False
    setNumeroApropiadoBombas()
    intentos = 0
    
    # Resetea cada uno de los botones
    # Bucle para el eje Y
    for i in range(ajustes["celdasY"]):
        # Bucle para el eje X
        for j in range(ajustes["celdasX"]):
            # Guarda el botón del tablero en una variable auxiliar
            boton = tablero[i][j]
            # Lo habilita, esté o no deshabilitado
            boton["state"] = "normal"
            # Resetea a las configuraciones iniciales
            boton.config(bg="SystemButtonFace", text="", fg="white", disabledforeground="white")

# CREACIÓN Y CONFIGURACIONES DE LA VENTANA
# Crea una nueva ventana
ventana = Tk()

# La ventana creada tiene un tamaño de las celdas de cada eje por el ancho de la misma
ventana.config(
    width = ajustes["celdasX"] * ajustes["anchoCelda"],
    height = ajustes["celdasY"] * ajustes["altoCelda"] + 30 + 20 # +30 para el texto, y +20 para la barra de menú
)
# Fija el título de la ventana y evita que se pueda cambiar el tamaño con el ratón
ventana.title(ajustes["titulo"])
ventana.resizable(0, 0)
# Centra la ventana
ventana.eval("tk::PlaceWindow . center")

# Crea una barra en la parte superior de la ventana
barraMenu = Menu(ventana)

# OPCIÓN DE JUEGO (tearoff -> no muestra una línea con guiones)
juegoOpcion = Menu(barraMenu, tearoff=0)
# Subopciones (repetir la partida o cerrar la ventana)
juegoOpcion.add_command(label="Repetir", command=repetir)
juegoOpcion.add_command(label="Cambiar dimensiones", command=cambiarDimensiones)
juegoOpcion.add_separator() # Añade una línea de separación
juegoOpcion.add_command(label="Cerrar", command=ventana.destroy)

# OPCIÓN DE AJUSTES
ajustesOpcion = Menu(barraMenu, tearoff=0)
# Subopciones (cambiar la cantidad de bombas o el caracter)
ajustesOpcion.add_command(label="Cantidad de bombas", command=cambiarCantidadBombas)
ajustesOpcion.add_command(label="Caracter de una bomba", command=cambiarCaracterBomba)

# OPCIÓN DE AYUDA
ayudaOpcion = Menu(barraMenu, tearoff=0)
# Subopciones (información de como jugar, del programa, y la versión)
ayudaOpcion.add_command(label="Cómo jugar", command=lambda: mostrarMensajeEmergente("Desactiva todas las minas, pulsando en las casillas, que cada una guarda el número de bombas alrededor","Cómo jugar"))
ayudaOpcion.add_command(label="Información", command=lambda: mostrarMensajeEmergente("Práctica de Python - 2022 - JuanGV", "Información"))
ayudaOpcion.add_command(label="Versión", command=lambda: mostrarMensajeEmergente("Versión 1.0.0.0", "Versión"))

# Añade a la barra del menú las opciones principales
barraMenu.add_cascade(label="Juego", menu=juegoOpcion)
barraMenu.add_cascade(label="Ajustes", menu=ajustesOpcion)
barraMenu.add_cascade(label="Ayuda", menu=ayudaOpcion)

# Configura en la ventana que el menú sea 'barraMenu'
ventana.config(menu=barraMenu)

# Texto con el número de banderas
textoBanderas = Label(ventana, text=f"Banderas: {ajustes['bombas']}")
textoBanderas.place(x=0, y=0) # Ubica el texto en el inicio de la ventana
textoBanderas.config(font=("Arial", 14)) # Configura la fuente

# Botón para repetir la partida
botonRepetir = Button(text="Repetir", command=repetir)
botonRepetir.place(x=120, y=2) # Ubicación

# VARIABLES GLOBALES
solucion = tablero = intentos = banderas = finalJuego = None

# MÉTODO PARA FINALIZAR EL JUEGO
def finalizarJuego(mensaje):
    # Declara la variable 'finalJuego' como global para evitar que se cree una propia de la función
    global finalJuego
    
    # Como el juego ha finalizado, se activa
    finalJuego = 1
    
    # Aparece una ventana emergente por pantalla con un mensaje (de victoria o de fallo)
    mostrarMensajeEmergente(mensaje, "Fin del juego")

# MÉTODO PARA VERIFICAR SI EL BOTÓN QUE SE PASA POR PARÁMETRO ESTÁ VACÍO
def isBotonVacio(boton):
    # Si está vacío, es verde y no tiene contenido
    return boton.cget("bg") == "green" and boton.cget("text") == ""

# MÉTODO PARA DEFINIR UN TABLERO (LISTA ANIDADA)
def definirTablero(ancho, alto, relleno):
    # Crea la lista
    nestedArray = []
    
    # Se ejecutará tantas veces como veces en alto
    for i in range(alto):
        # Añade por línea un relleno tantas veces según el valor del ancho
        nestedArray.append([relleno] * ancho)
        
    # Devuelve el tablero creado
    return nestedArray

# FUNCIÓN PARA COMPROBAR SI EL JUEGO HA TERMINADO CON VICTORIA
def comprobarVictoria():
    # Se puede ganar si hay 0 huecos vacíos o si hay 0 banderas y están en la ubicación correcta
    huecosVacios = 0
    banderasCorrectas = 0
    
    # Para cada fila
    for i in range(ajustes["celdasY"]):
        # Para cada columna
        for j in range(ajustes["celdasX"]):
            # Guarda el botón
            boton = tablero[i][j]
            
            # Si está en rojo, es porque es una bandera (si es una mina no se verifica la victoria)
            # Por lo tanto, es una bandera, y si está en la solución
            if boton.cget("bg") == "red" and solucion[i][j]:
                # Suma 1 al número de banderas correctas
                banderasCorrectas += 1
            
            # Si el botón no es verde, puede ser una bandera o un hueco vacío
            if boton.cget("bg") != "green":
                # Suma 1 a los huecos vacíos
                huecosVacios += 1
    
    # Si los huecos vacíos equivalen al número de bombas o las banderas correctas a las bombas de los ajustes
    # Y el final de juego está a FALSE
    if (huecosVacios == ajustes["bombas"] or banderasCorrectas == ajustes["bombas"]) and finalJuego == False:
        # Imprime las bombas y finaliza el juego con un mensaje de victoria
        imprimirBombas()
        finalizarJuego("¡Victoria!")

# FUNCIÓN DE CLICK NORMAL DEL USUARIO SOBRE EL BOTÓN (POR COORDENADAS)
def deshabilitar(x, y):
    
    # Menciona que los intentos y las banderas son globales
    global intentos, banderas
    
    # Creación de bombas para evitar que el usuario pulse una por primera vez sin querer
    if intentos == 0:
        generarBombas(x, y)
    
    # Guarda el botón con el que se va a manejar
    boton = tablero[y][x]
    
    # Si las coordenadas son una bomba, el usuario habría pulsado una bomba
    if solucion[y][x]:
        # Imprime las bombas en el tablero y comunica al jugador que ha fallado
        imprimirBombas()
        finalizarJuego("¡Fallaste!")
    else:
        # El botón se configura a verde, es deshabilitado y deja el número de bombas como texto del botón
        boton.config(bg="green")
        boton["state"] = DISABLED
        boton.config(text=getBombasAlrededor(x, y))
        
        # Aumenta los intentos en 1
        intentos += 1
    
        # En caso de que el botón esté vacío (0 bombas alrededor), habrá que rellenar las casillas que están a su alrededor
        if isBotonVacio(boton):
            # Bucle en el eje Y
            for i in range(y-1, y+2):
                # Bucle en el eje X
                for j in range(x-1, x+2):
                    # Evita el error de un valor fuera de rango
                    try:
                        # Para evitar volver a otro lado del código, si los números no son negativos continúa
                        if i >= 0 and j >= 0:
                            # Guarda el botón en una variable auxiliar
                            boton = tablero[i][j]
                            
                            # Si el botón es una bandera (color rojo)
                            if boton.cget("bg") == "red":
                                # Lo resetea por uno normal
                                boton.config(bg="green", text=getBombasAlrededor(j, i))
                                boton["state"] = "normal"
                                # Devuelve la bandera y actualiza el texto
                                banderas += 1
                                textoBanderas.config(text=f"Banderas: {banderas}")
                            
                            # Si el botón no está en DISABLED, puede ser pulsado por el programa
                            # De este modo, se buscan todas las casillas con 0 bombas a su alrededor
                            # Se evita que el usuario tenga que hacer esta tarea
                            
                            # i y j tienen que estar en el rango del número de celdas
                            if i < ajustes["celdasY"] and j < ajustes["celdasX"]:
                                boton.invoke()
                    except:
                        # Pasa de largo al darse un error de fuera de rango y continúa en el bucle
                        pass
    
        # Al final del método se comprueba si se ha ganado
        # Si se hace con una tabulación menos, y el usuario encuentra una bomba, habría una gran cantidad de errores
        # En conclusión, este método solo se ejecuta si el usuario no pulsa una casilla que tenga una bomba
        comprobarVictoria()

# MÉTODO PARA INICIAR LAS VARIABLES GLOBALES
def iniciarVariables():
    # Declara las variables como alcance global y las inicia
    global solucion, tablero, intentos, banderas, finalJuego
    
    # Genera una solución vacía y un tablero (donde guardar los botones sin necesidad de append)
    solucion = definirTablero(ajustes["celdasX"], ajustes["celdasY"], 0)
    tablero = definirTablero(ajustes["celdasX"], ajustes["celdasY"], 0)
    
    # Deja los intentos a 0, el número de banderas según el número de bombas
    intentos = 0
    banderas = ajustes["bombas"]
    
    # El juego en teoría no ha acabado, por lo tanto, está a 0 (False)
    finalJuego = 0

# MÉTODO PARA OBTENER EL NÚMERO DE BOMBAS ALREDEDOR DE UNA CASILLA
def getBombasAlrededor(x, y):
    # El número de bombas inicial es 0
    cantidad = 0
    
    # Bucle para recorrer los alrededores de la casilla (primero por fila)
    for fila in range(y-1, y+2):
        # Posteriormente por columna
        for columna in range(x-1, x+2):
            # Evita el error de fuera de rango
            try:
                # Si la fila y la columna no son números negativos
                if fila >= 0 and columna >= 0:
                    # Aumenta la cantidad dependiendo de si existe bomba o no
                    # Existe -> 1, No existe -> 0
                    cantidad += solucion[fila][columna]
            except:
                # Pasa y continúa evitando el error
                pass
    
    # Si la cantidad es 0, fija la cantidad a un valor vacío (para no escribir 0)
    if cantidad == 0:
        cantidad = ""
    
    # Devuelve la cantidad obtenida
    return cantidad

# MÉTODO PARA GENERAR BOMBAS CON UNAS COORDENADAS INICIALES (despúes de la primera solución)
def generarBombas(x, y):
    # Rellena con tantas bombas como se indica en los ajustes
    for bomba in range(0, ajustes["bombas"]):
        # Coordenadas iniciales por defecto de la bomba
        xBomba = 0
        yBomba = 0
        
        # Se ejecutará hasta que desde dentro del bucle exista una condición que lo termine
        while 1:
            # Obtiene un número al azar dentro del rango del número de celdas
            xBomba = random.choice(range(0, ajustes["celdasX"]))
            yBomba = random.choice(range(0, ajustes["celdasY"]))
            
            # Si las nuevas coordenadas no están en otra bomba o donde el usuario ha pulsado, termina el bucle
            if solucion[yBomba][xBomba] != 1 and xBomba != x and yBomba != y:
                break
        
        # Después del bucle, se añade la bomba a la lista 'solución'
        solucion[yBomba][xBomba] = 1

# MÉTODO PARA IMPRIMIR LAS BOMBAS EN EL TABLERO
def imprimirBombas():
    # Bucle para las coordenadas en el eje Y
    for i in range(ajustes["celdasY"]):
        # Bucle para las coordenadas en el eje X
        for j in range(ajustes["celdasX"]):
            # Se guarda el botón en una variable temporal
            boton = tablero[i][j]
            
            # Si en ese botón había una bomba, configura el botón
            if solucion[i][j]:
                # Fondo de color rojo, asterisco, y color de letra negro
                boton.config(bg="red", text=ajustes["bombaCaracter"], disabledforeground="black")
            # Si el botón es una bandera, indica que está en un lugar equivocado
            elif boton.cget("bg") == "red":
                boton.config(text="X", disabledforeground="black")
            
            # Deshabilita este botón
            boton["state"] = DISABLED
            # Tras finalizar el bucle todos los botones habrán quedado deshabilitados, para evitar ediciones

# MÉTODO QUE RECIBE LAS COORDENADAS DE LA CASILLA DONDE EL USUARIO HA PULSADO CON EL BOTÓN DERECHO DEL RATÓN
def botonDerecho(y, x):
    # Se menciona que dichas variables son globales y no pertenecen a la función
    global banderas, finalJuego
    
    # Se guarda el botón que va a ser manejado
    boton = tablero[y][x]
    
    # Si el botón no es uno verde y el juego no ha acabado
    if boton.cget("bg") != "green" and finalJuego != True:
        # Si está deshabilitado
        if boton["state"] == "disabled":
            # Lo resetea a la configuración inicial
            boton["state"] = "normal"
            boton.config(bg="SystemButtonFace", text="")
            # Devuelve la bandera retirada
            banderas += 1
        else:
            # Si las banderas no son 0, puede seguir añadiendo estas
            if banderas != 0:
                # Deshabilita el botón, lo indica en color rojo y añade el caracter de la bandera de los ajustes
                boton["state"] = DISABLED
                tablero[y][x].config(bg="red", text=ajustes["banderaCaracter"])
                banderas -= 1 # Retira una bandera
        
        # Actualiza el texto de las banderas
        textoBanderas.config(text=f"Banderas: {banderas}")
    
    # Comprueba si el usuario ha ganado
    comprobarVictoria()

# Inicia las variables de uso global
iniciarVariables()
setNumeroApropiadoBombas()

# Crea un tablero fijo al principio de la partida
# Bucle para el eje Y
for i in range(ajustes["celdasY"]):
    # Bucle para el eje X
    for j in range(ajustes["celdasX"]):
        # Guarda un botón con una función de deshabilitar para cuando se realice un click (pasando las coordenadas únicas)
        tablero[i][j] = Button(disabledforeground="white", command= lambda i=i, j=j:deshabilitar(j, i))
        # Ubica el botón en el tablero
        tablero[i][j].place(
            x = j * ajustes["anchoCelda"],
            y = i * ajustes["altoCelda"] + 30, # +30 por el margen superior de los datos
            width = ajustes["anchoCelda"],
            height = ajustes["altoCelda"]
        )
        # Configura la fuente del botón
        tablero[i][j].config(font=("Consolas", 20, "bold"))
        # Acción para cuando se realice click derecho del ratón
        tablero[i][j].bind("<Button-2>", lambda event, y=i, x=j: botonDerecho(y, x))
        tablero[i][j].bind("<Button-3>", lambda event, y=i, x=j: botonDerecho(y, x))

# Bucle de ejecución de la ventana
ventana.mainloop()
