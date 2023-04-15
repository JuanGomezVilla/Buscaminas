# Importa la librería 'random' para jugar con números aleatorios
import random

# AJUSTES
ajustes = {
    "dimensionX": 6, # Cantidad de casillas en el eje X
    "dimensionY": 6, # Cantidad de casillas en el eje Y
    "bombas": 4, # Cantidad de bombas en la solución
    "notacionFacil": True, # Utilizar notación fácil (1-dimensión)
    "mostrarIntentos": False, # Para mostrar los intentos
    "mostrarSolucion": True, # Para mostrar la solución (modo desarrollo)
    "relleno": "x", # Valor de relleno
    "bomba": "*" # Valor de una bomba
}


# Función para definir un tablero, que lo acabará devolviendo
def definirTablero(ancho, alto, relleno):
    # Se puede escribir 'return [[relleno]*ancho]*alto', pero daría errores de repetición, por lo que no se utiliza
    # Creación de una lista para guardar listas de forma anidada
    nestedArray = []
    
    # Añadirá tantas filas como se indique en el alto
    for i in range(alto):
        # Va añadiendo filas nuevas con un relleno determinado, tantas como el ancho
        nestedArray.append([relleno] * ancho)
        
    # Devuelve la lista anidada
    return nestedArray


# Función para dibujar listas anidadas. No devuelve datos, realiza una acción
def dibujarNestedArray(lista):
    # Para cada fila de la lista
    for fila in lista:
        # Para cada columna de una fila
        for columna in fila:
            # Escribe todos los valores de la columna separados por un espacio
            print(columna, end=" ")
        # Aplica un salto de línea
        print()

# Función para leer números enteros y evitar valores erróneos por parte del usuario
def leerInt(mensaje):
    # Repetir por siempre (True es lo mismo que 1)
    while 1:
        # Intentar una acción que puede desencadenarse con un error
        try:
            # Pedir datos al usuario con un mensaje y devolver lo que el usuario ha escrito si es correcto 
            return int(input(mensaje))
        except:
            # Muestra un error
            print("Valor incorrecto. Inténtalo de nuevo...")
            # Vuelve a intentarlo
            continue


# Función que se iniciará (porque se llama) cuando finalicen las comprobaciones de ajustes
def iniciarPartida():
    # Define un tablero y una solución, con un relleno de 'x' y un valor de 0 (False, no hay bombas todavía)
    tablero = definirTablero(ajustes["dimensionX"], ajustes["dimensionY"], ajustes["relleno"])
    solucion = definirTablero(ajustes["dimensionX"], ajustes["dimensionY"], 0)
    
    # Inicia los intentos a 0
    intentos = 0
    
    # Rellena con tantas bombas como se indica en los ajustes
    for bomba in range(0, ajustes["bombas"]):
        # Ubicación de una bomba nueva por defecto
        xBomba = 0
        yBomba = 0
        
        # Evita repetir bombas, si la bomba ya existe vuelve a buscar de nuevo dicha bomba
        while 1:
            # Genera un número aleatorio entre 0 y las dimensiones
            xBomba = random.choice(range(0, ajustes["dimensionX"]))
            yBomba = random.choice(range(0, ajustes["dimensionY"]))
            
            # Si la bomba no existe, finaliza el bucle 'while' pero continúa en el bucle 'for'
            if solucion[yBomba][xBomba] != 1:
                break
        
        # Guarda la bomba nueva
        solucion[yBomba][xBomba] = 1
    
    # Muestra la solución si se activa desde los ajustes
    if ajustes["mostrarSolucion"]:
        dibujarNestedArray(solucion)
    
    # Ejecutar hasta que el usuario encuentre una bomba o gane
    while 1:
        # Si el usuario decide mostrar el número de intentos, estos se muestran
        if ajustes["mostrarIntentos"]:
            print("Intentos:", intentos)
        
        # Se dibuja el tablero
        dibujarNestedArray(tablero)
        
        # Coordenadas por defecto del usuario que luego recibirán un valor
        x = 0
        y = 0
        
        while 1:
            # El usuario escribe unas coordenadas
            x = leerInt("Coordenada X: ") - ajustes["notacionFacil"]
            y = leerInt("Coordenada Y: ") - ajustes["notacionFacil"]
            
            # Se verifica que tanto X como Y están en el rango, y en ese caso, termina el bucle de verificación
            # También verifica que X o Y no están repetidos
            if x not in range(0, ajustes["dimensionX"]):
                print("Coordenada X fuera de rango...")
            elif y not in range(0, ajustes["dimensionY"]):
                print("Coordenada Y fuera de rango...")
            elif tablero[y][x] != ajustes["relleno"]:
                print("Esa coordenada ya está marcada...")
            else:
                break # pass
            
   
        # Verificar si el usuario ha seleccionado una bomba, si se cumple, termina el bucle general
        if solucion[y][x]:
            # Dibuja todas las bombas
            # Para cada fila de la solución
            for i in range(len(solucion)):
                # Para cada columna de una fila
                for j in range(len(solucion[i])):
                    # Si existe una bomba, esta se imprime en el tablero
                    if solucion[i][j]:
                        tablero[i][j] = ajustes["bomba"]
            print("\n¡Bomba!")
            break
        
        # Buscar bombas
        cantidad = 0
        
        # Para todas las ubicaciones alrededor de la casilla seleccionada
        for fila in range(y-1, y+2):
            for columna in range(x-1, x+2):
                # Se evita el error de 'index out of bound' si, por ejemplo un valor fuera 0
                try:
                    # Si es un número negativo, puede buscar desde el final de la lista (-1), por lo que se evita
                    if fila >= 0 and columna >= 0:
                        # Si hay una bomba (1) suma 1
                        cantidad += solucion[fila][columna]
                except:
                    # Pasa del error
                    pass
        
        # Fija en el tablero la cantidad de bombas alrededor
        tablero[y][x] = cantidad
        
        # Suma 1 a los intentos
        intentos += 1
        
        # Si los intentos es igual al número de casillas menos las bombas es que ha ganado
        if intentos == ((ajustes["dimensionX"] * ajustes["dimensionY"]) - ajustes["bombas"]):
            print("\n¡Has ganado!")
            break
        
        # Aplica un saldo de línea
        print()
    
    # Como parte final, imprime el tablero
    dibujarNestedArray(tablero)
    print("\nFin del programa")

# COMPROBACIONES DE LOS AJUSTES (1º tipo, 2º rango)
# Se comprueba si los tipos son válidos, evitando que las configuraciones sean erróneas
if type(ajustes["dimensionX"]) is not int:
    print("El tipo de la dimensión en el eje X es erróneo...")
elif type(ajustes["dimensionY"]) is not int:
    print("El tipo de la dimensión en el eje Y es erróneo...")
elif type(ajustes["bombas"]) is not int:
    print("El tipo de valor de bombas es erróneo, deber ser un entero...")
elif type(ajustes["notacionFacil"]) is not bool:
    print("El tipo de la notación fácil es erróneo, deber ser booleano...")
elif type(ajustes["mostrarIntentos"]) is not bool:
    print("El tipo de mostrar intentos es erróneo, deber ser booleano...")
elif type(ajustes["mostrarSolucion"]) is not bool:
    print("El tipo de mostrar solución es erróneo, deber ser booleano...")
elif type(ajustes["relleno"]) is not str:
    print("El tipo del relleno es erróneo, debe ser una letra (str)...")
elif type(ajustes["bomba"]) is not str:
    print("El tipo de la bomba es erróneo, debe ser una letra (str)...")
    
# Se comprueba que los rangos no sean erróneos
elif ajustes["dimensionX"] <= 1 or ajustes["dimensionY"] <= 1 :
    print("Una de las dimensiones es errónea, tiene que ser mayor de 1...")

# Número de bombas correcto
elif ajustes["bombas"] >= (ajustes["dimensionX"] * ajustes["dimensionY"]):
    print("Cantidad de bombas fuera de rango...")

# Los ajustes booleanos no se verifican porque solo están en el rango de booleanos y habría pasado la condición anterior
# Se verifica el valor del relleno
elif len(ajustes["relleno"]) != 1:
    print("Solo puede haber una letra de relleno...")
# Se verifica el icono de la bomba
elif len(ajustes["bomba"]) != 1:
    print("Solo puede haber una letra de bomba...")
else:
    # Inicia la partida
    iniciarPartida()