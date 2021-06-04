import matplotlib
from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt

# Definimos un arreglo para almacenar los puntos
puntos = []
# Abrimos nuestro archivo txt donde guardamos nuestros puntos
with open("Puntos.txt", "r") as File:
    for lineas in File:
        # Usamos lineas.split() para separar cada linea usando el caracter de espacio en blanco
        # Guardamos todos nuestros datos almacenados en el archivo en una lista
        puntos.extend(lineas.split())
# Cerramos el archivo
File.close()

# Creamos tanto nuestros contadores y nusetras listas
CoordenadasX = []
CoordenadasY = []
cont = 0

# Extraemos las coordenadas de la lista de puntos
for i in range(len(puntos)):
    if i % 2 == 0:
        CoordenadasX.append(float(puntos[i]))
        cont += 1
    else:
        CoordenadasY.append(float(puntos[i]))

# Matriz nxn de la expresion 4 del PDF
def formarMatriz():
    # Obtenemos la cantidad de puntos
    N = len(CoordenadasX)
    # Armamos la matriz
    for i in range(filas):
        for j in range(filas):
            # La primera fila la formamos por separado
            if i == 0 and j == 0:
                matriz[i][j] = N
            elif i == 0:
                for k in range(len(CoordenadasX)):
                    matriz[i][j] += pow(CoordenadasX[k], j)
            # Las demas filas las formamos juntas
            else:
                for k in range(len(CoordenadasX)):
                    matriz[i][j] += pow(CoordenadasX[k], (i+j))

#Soluciones de la matriz 4 del PDF
def formarSoluciones():
    for i in range(len(soluciones)):
        for k in range(len(CoordenadasY)):
            soluciones[i] += pow(CoordenadasX[k], i)*CoordenadasY[k]

# Imprimir la matriz
def imprimirMatriz(matriz, filas):
    
    for i in range(filas):
        print("[", end=" ")
        for j in range(filas):
            # imprime el numero redondeado por 2 cifras
            print(round(matriz[i][j], 2), end="\t")
        print("| "+str(round(soluciones[i], 2))+"\t]")

# Ajuste por minimos cuadrados con el algoritmo dado por el libro Chapra
def minimosCuadrados():
    sumx = 0  # Suma de los valores conocidos de x
    sumy = 0  # Suma de los valores conocidos de y
    sumxy = 0  # Suma de los productos x*y
    sumx2 = 0  # Suma de los cuadrados de x
    n = len(CoordenadasX)  # Cantidad de datos conocidos de la variable x

    for i in range(len(CoordenadasX)):  # Se ejecutan cada una de las sumas
        sumx = sumx + CoordenadasX[i]
        sumy = sumy + CoordenadasY[i]
        sumxy = sumxy + CoordenadasX[i]*CoordenadasY[i]
        sumx2 = sumx2 + CoordenadasX[i]**2

    promx = sumx/n  # Promedio de x
    promy = sumy/n  # Promedio de y

    # Calcula la pendiente (a1) - Tomado de Chapra
    a1 = (n * sumxy - sumx*sumy)/(n * sumx2 - sumx**2)
    a0 = promy - a1*promx  # Calcula el intercepto (a0) - Tomado de Chapra

    return a1, a0


# Metodo para imprimir el polinomio
def imprimirPolinomio(x):
    polinomio = f"{round(x[-1],3)}x^{len(x)-1} "

    for i in reversed(range(2, len(x)-1)):
        if x[i] < 0:
            polinomio += f"{round(x[i], 3)}x^{i} "
        else:
            polinomio += f"+ {round(x[i], 3)}x^{i} "

    if x[1] < 0:
        polinomio += f"{round(x[1], 3)}x "
    else:
        polinomio += f"+ {round(x[1], 3)}x "

    if x[0] < 0:
        polinomio += f"{round(x[0], 3)} "
    else:
        polinomio += f"+ {round(x[0], 3)} "

    print("El polinomio al que pertenecen los puntos es: ")
    print(polinomio)


# -----------------------------------------MAIN----------------------------------------------------------
print("Grados disponibles de 0 a ", cont-1)
grado = int(input("Grado del polinomio que deseas ajustar: "))

# Polinomio de grado n, el sistema es (n+1)*(n+1)
filas = grado + 1

# Declaramos nuestra matriz vacia
matriz = []
# Declaramos nuestro vector de soluciones
soluciones = []
# Construimos nuestra matriz, introduciendo 0 en ella e introducimos 0 en el array
for i in range(filas):
    matriz.append([0]*filas)
    soluciones.append(0)

# Mandamos a llamar nuestros metodos
a1, a0 = minimosCuadrados()
formarMatriz()
formarSoluciones()
print("-----------------------------------------------------")
imprimirMatriz(matriz, filas)
print("-----------------------------------------------------")

# Imprimir resultados de los parametros de la regresion
print("a1: ", a1)
print("a0: ", a0)
t = np.poly1d([a1, a0])
# print(t)
print("y = " + str(a1) + "x + " + str(a0))  # y = a1x + a0
print("-----------------------------------------------------")

# Resolvemos el sistema de ecuaciones
x = np.linalg.solve(matriz, soluciones)
# Imprimimos el polinomio
imprimirPolinomio(x)
print("-----------------------------------------------------")

plt.scatter(CoordenadasX, CoordenadasY, alpha=1, color="purple")
# Grafica de la recta de regresion
plt.plot(x, a1*np.array(x) + a0, label=t)
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.grid()
plt.show()