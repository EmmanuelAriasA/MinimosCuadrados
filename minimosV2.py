import matplotlib
from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt

# Metodo para imprimir polinomio
def imprimirPolinomio(coeficientes):

    polinomio = f"{round(coefs[-1],3)}x^{len(coefs)-1} "

    for i in reversed(range(2, len(coefs)-1)):
        if coefs[i] < 0:
            polinomio += f"{round(coefs[i], 3)}x^{i} "
        else:
            polinomio += f"+ {round(coefs[i], 3)}x^{i} "

    
    if coefs[1] < 0:
        polinomio += f"{round(coefs[1], 3)}x "
    else:
        polinomio += f"+ {round(coefs[1], 3)}x "

    if coefs[0] < 0:
        polinomio += f"{round(coefs[0], 3)}"
    else:
        polinomio += f"+ {round(coefs[0], 3)} "

    print("\n Polinomio: ")
    print(polinomio)


# Metodo para sacar el polinomio que se ajusta a los puntos
def obtener_coeficientes(filas, puntos, grado):
    sums_x = np.zeros(2*grado + 1, dtype=float)
    sums_x[0] = filas  # N

    # Σxi, Σ(xi)^2, ..., Σ(xi)^2n
    for i in range(1, 2*grado + 1):
        sumx = np.sum(np.power(puntos[:, 0], i), axis=0)
        sums_x[i] = sumx

    sums_xy = np.zeros(grado + 1, dtype=float)
    sums_xy[0] = np.sum(puntos[:, 1], axis=0)  # Σyi

    # Σxiyi, Σ(xi)^2yi, ..., Σ(xi)^nyi
    for i in range(1, grado + 1):
        temp_xy = np.copy(puntos)
        temp_xy[:, 0] = np.power(temp_xy[:, 0], i).transpose()
        sums_xy[i] = np.sum(np.prod(temp_xy, axis=1))

    matriz = np.zeros((grado+1, grado+1), dtype=float)

    for i in range(grado+1):
        for j in range(grado+1):
            matriz[i][j] = sums_x[i+j]

    return np.linalg.solve(matriz, sums_xy.transpose())


# Metodo para sacar la recta de regresion
def minCuadrados(x, y):

    sumx = 0  # Suma de los valores conocidos de x
    sumy = 0  # Suma de los valores conocidos de y
    sumxy = 0  # Suma de los productos x*y
    sumx2 = 0  # Suma de los cuadrados de x
    n = len(x)  # Cantidad de datos conocidos de la variable x

    for i in range(len(x)):  # Se ejecutan cada una de las sumas
        sumx = sumx + x[i]
        sumy = sumy + y[i]
        sumxy = sumxy + x[i]*y[i]
        sumx2 = sumx2 + x[i]**2

    promx = sumx/n  # Promedio de x
    promy = sumy/n  # Promedio de y

    # Calcula la pendiente (a1) - Tomado de Chapra
    a1 = (n * sumxy - sumx*sumy)/(n * sumx2 - sumx**2)
    a0 = promy - a1*promx  # Calcula el intercepto (a0) - Tomado de Chapra

    return a1, a0


def grdo(filas):
    print("Grados de polinomio disponibles: ")
    for i in range(1, filas):
        print(i)

    return int(input("Introduce el grado del polinomio que deseas ajustar: "))


#-------------------------------------------------------------------------------------------------
# Definimos un arreglo para almacenar los puntos
puntos = []
# Abrimos nuestro archivo txt donde guardamos nuestros puntos
with open("Coordenadas.txt", "r") as File:
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

# Ahora para poder utilizar la libreria numpy, debemos crear arreglos de tipo numpy
x = np.array(CoordenadasX)
y = np.array(CoordenadasY)

xy = np.array([x, y])
matrizXY = np.transpose(xy)
filas, _ = matrizXY.shape
pol = grdo(filas)

coefs = obtener_coeficientes(filas, matrizXY, pol)
print("-----------------------------------------------------")
imprimirPolinomio(coefs)

# Mandamos llamar nuestro metodo para obtener los valores del polinomio
a1, a0 = minCuadrados(x, y)

# Imprimir resultados de los parametros de la regresion
print("-----------------------------------------------------")
print("a1: ", a1)
print("a0: ", a0)
t = np.poly1d([a1, a0])
# print(t)
print("y = " + str(a1) + "x + " + str(a0))  # y = a1x + a0
print("-----------------------------------------------------")

plt.scatter(x, y, alpha=1, color="purple")
# Grafica de la recta de regresion
plt.plot(x, a1*np.array(x) + a0, label=t)
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.grid()
plt.show()
