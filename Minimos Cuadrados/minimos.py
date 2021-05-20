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
        polinomio += f"{round(coefs[0], 3)}x "
    else:
        polinomio += f"+ {round(coefs[0], 3)}x "

    print("\n Polinomio: ")
    print(polinomio)


def obtener_coeficientes(filas, puntos, grado):
    """
    filas:  Número de puntos leídos.
    puntos: Matriz con las coordenadas de cada punto.
    grado:  Grado del polinomio.

    Salida:
    Un arreglo con los coeficientes del polinomio.
    """
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


def grdo(filas):
    print("Grados de polinomio disponibles: ")
    for i in range(1, filas):
        print(i)

    return int(input("Introduce el grado del polinomio que deseas ajustar: "))


# Abrimos nuestro archivo txt donde guardamos nuestros puntos
with open("CoordenadasX.txt", "r") as File:
    # Guardamos todos nuestros datos almacenados en el archivo en una lista
    FileContent = File.readlines()
# Si ya no utilizamos nuestro archivo, cerramos el acceso
File.close()


# Esto es ya que para leer el archivo, la mitad de los puntos son
# las x y la otra mitad son y
datos = (len(FileContent))/2
# Creamos tanto nuestros contadores y nusetras listas
contador = 0
CoordenadasX = []
CoordenadasY = []

# Los datos guardados en nuestra lista los almacenamos en nuestro arreglo
for fileLine in FileContent:
    contador += 1
    # Para que no se almacenen los tabuladores y los saltos de linea
    # Los cambiamos por caracteres vacios
    fileLine = fileLine.replace("\n", "")
    fileLine = fileLine.replace("\t", "")
    # Si nuestro contador llega a mas de la mitad de los datos
    # significa que llegamos a las y, y los guardamos en su respectivo arreglo
    if(contador > datos):
        CoordenadasY.append(float(fileLine))
    else:
        # Sino, lo guardamos en las x
        CoordenadasX.append(float(fileLine))

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

# Creamos nuestro arreglo de unos con el tamaño de alguno de nuestros arreglos
Unos = np.ones_like(x)

# Generamos nuestra matriz en base a nuestro arreglo de 1 y puntos en x
At = np.array([Unos, x])
# Y obtenemos su traspuesta
A = np.transpose(At)

# Basado en la formula para minimos cuadrados AtAX = AtY
# Hacemos la multiplicacion de matrices y resolvemos la igualdad
AtA = np.dot(At, A)
Aty = np.dot(At, y)
Res = np.linalg.solve(AtA, Aty)
# Imprimimos nuestro resultado
print("-----------------------------------------------------")
print("Primer valor: ", Res[1])
print("Segundo valor: ", Res[0])
print("y", "=", Res[1], "x", "+ ", Res[0])
print("-----------------------------------------------------")
plt.scatter(x, y, alpha=0.5, color="purple")
# Grafica de la recta de la regresion
plt.plot(x, Res[1]*np.array(x) + Res[0])
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.grid()
plt.show()

"""
#E imprimimos la grafica
plt.scatter(x, y, alpha=1, color="purple")
#plt.ylim([-10, 10])
#plt.xlim([-10, 10])
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.plot([-10, 10], [Res[0] + Res[1] * -10, Res[0] + Res[1] * 10], c="red")

plt.show()
"""
