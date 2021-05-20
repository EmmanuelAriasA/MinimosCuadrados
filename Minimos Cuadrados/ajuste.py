import numpy as np
import matplotlib.pyplot as plt

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

def graficar(puntos, coefs):
    """
    puntos: Arreglo con las coordenadas de los puntos.
    coefs:  Coeficientes del polinomio a graficar.
    """
    # Título de la gráfica
    titulo = f"{round(coefs[-1],3)}x^{len(coefs)-1} "

    for i in reversed(range(2, len(coefs)-1)):
        if coefs[i] < 0:
            titulo += f"{round(coefs[i], 3)}x^{i} "
        else:
            titulo += f"+ {round(coefs[i], 3)}x^{i} "

    if coefs[1] < 0:
        titulo += f"{round(coefs[1], 3)}x "
    else:
        titulo += f"+ {round(coefs[1], 3)}x "

    if coefs[0] < 0:
        titulo += f"{round(coefs[0], 3)}x "
    else:
        titulo += f"+ {round(coefs[0], 3)}x "

    plt.title(titulo)

    # Etiquetas
    plt.xlabel("x")
    plt.ylabel("y")

    # Graficar puntos
    plt.plot(*puntos.T, "ro") # Circulos rojos

    # Graficar polinomio
    x = np.linspace(-puntos[-1,0], puntos[-1,0]*2, puntos.shape[0]*3)
    y = [np.polyval(coefs[::-1], i) for i in x]
    plt.plot(x, y)

    plt.show()

def obtener_coeficientes(filas, puntos, grado):
    """
    filas:  Número de puntos leídos.
    puntos: Matriz con las coordenadas de cada punto.
    grado:  Grado del polinomio.

    Salida:
    Un arreglo con los coeficientes del polinomio.
    """
    sums_x = np.zeros(2*grado + 1, dtype=float)
    sums_x[0] = filas # N

    # Σxi, Σ(xi)^2, ..., Σ(xi)^2n
    for i in range(1, 2*grado + 1):
        sumx = np.sum(np.power(puntos[:,0],i), axis=0)
        sums_x[i] = sumx

    sums_xy = np.zeros(grado + 1, dtype=float)
    sums_xy[0] = np.sum(puntos[:,1], axis=0) # Σyi

    # Σxiyi, Σ(xi)^2yi, ..., Σ(xi)^nyi
    for i in range(1, grado + 1):
        temp_xy = np.copy(puntos)
        temp_xy[:,0] = np.power(temp_xy[:,0], i).transpose()
        sums_xy[i] = np.sum(np.prod(temp_xy, axis=1))

    matriz = np.zeros((grado+1,grado+1), dtype=float)

    for i in range(grado+1):
        for j in range(grado+1):
            matriz[i][j] = sums_x[i+j]

    return np.linalg.solve(matriz, sums_xy.transpose())


def menu(filas):
    """
    filas: Número de puntos leídos.

    Salida:
    El grado del polinomio que desea el usuario.
    """
    print("Grados de polinomio disponibles: ")
    for i in range(1, filas):
        print(i)

    return int(input("Introduce el grado del polinomio que deseas ajustar: "))
    

def main():
    # Creamos la matriz de puntos x,y
    puntos = np.loadtxt("puntos.csv", dtype=float, delimiter=",")
    filas, _ = puntos.shape
    cont = 0
    
    copia_puntos = np.copy(puntos)

    grado = menu(filas)
    coefs = obtener_coeficientes(filas, copia_puntos, grado)
    graficar(puntos, coefs)

main()

