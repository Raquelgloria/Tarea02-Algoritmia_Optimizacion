
import random
import math
import time
import matplotlib.pyplot as plt

ciudades = [
    (0, 0), (2, 6), (5, 3), (6, 7),
    (8, 2), (1, 4), (7, 5), (3, 1)
]


def distancia(a, b):
    return math.dist(ciudades[a], ciudades[b])


def distancia_ruta(ruta):
    total = 0

    for i in range(len(ruta)):
        total += distancia(
            ruta[i],
            ruta[(i + 1) % len(ruta)]
        )

    return total



def vecino_2opt(ruta, rng):
    nueva = ruta.copy()

    i, j = sorted(rng.sample(range(len(ruta)), 2))
    nueva[i:j + 1] = nueva[i:j + 1][::-1]

    return nueva



def recorido_simulado(
    ruta_inicial,
    esquema,
    iteraciones=3000,
    temperatura_inicial=10,
    temperatura_final=0.01
):
    rng = random.Random(42)

    actual = ruta_inicial.copy()
    costo_actual = distancia_ruta(actual)

    mejor = actual.copy()
    mejor_costo = costo_actual

    historial = []
    inicio = time.perf_counter()

    for t in range(iteraciones):

        progreso = t / (iteraciones - 1)

        if esquema == "lineal":
            temperatura = (
                temperatura_inicial
                + (temperatura_final - temperatura_inicial)
                * progreso
            )
        else:
            temperatura = (
                temperatura_inicial
                * (temperatura_final / temperatura_inicial)
                ** progreso
            )

        siguiente = vecino_2opt(actual, rng)
        costo_siguiente = distancia_ruta(siguiente)

        # En minimización, una diferencia positiva
        # significa que la nueva ruta es mejor.
        delta = costo_actual - costo_siguiente

        if delta > 0:
            aceptar = True
        else:
            probabilidad = math.exp(-max(0, -delta) / temperatura)
            aceptar = rng.random() < probabilidad

        if aceptar:
            actual = siguiente
            costo_actual = costo_siguiente

        if costo_actual < mejor_costo:
            mejor = actual.copy()
            mejor_costo = costo_actual

       
        historial.append(mejor_costo)

    tiempo = time.perf_counter() - inicio

    return mejor, mejor_costo, historial, tiempo



random.seed(42)
ruta_inicial = list(range(len(ciudades)))
random.shuffle(ruta_inicial)

resultados = {}

for esquema in ["lineal", "exponencial"]:
    ruta, costo, historial, tiempo = recorido_simulado(
        ruta_inicial,
        esquema
    )

    resultados[esquema] = {
        "ruta": ruta,
        "costo": costo,
        "historial": historial,
        "tiempo": tiempo
    }

    print(f"\nEnfriamiento {esquema}")
    print("Ruta inicial:", ruta_inicial)
    print("Mejor ruta:", ruta + [ruta[0]])
    print(f"Distancia final: {costo:.2f}")
    print(f"Tiempo de ejecución: {tiempo:.6f} segundos")


# GRÁFICA 1: Convergencia
plt.figure()

for esquema, resultado in resultados.items():
    plt.plot(
        resultado["historial"],
        label=f"Enfriamiento {esquema}"
    )

plt.xlabel("Iteraciones")
plt.ylabel("Mejor distancia encontrada")
plt.title("Convergencia del Recorido Simulado")
plt.legend()
plt.grid(True)
plt.show()


# GRÁFICA 2: Tiempo vs. calidad de la solución
plt.figure()

for esquema, resultado in resultados.items():
    plt.scatter(
        resultado["tiempo"],
        resultado["costo"],
        label=esquema
    )

    plt.annotate(
        esquema,
        (resultado["tiempo"], resultado["costo"])
    )

plt.xlabel("Tiempo de ejecución (segundos)")
plt.ylabel("Distancia final")
plt.title("Tiempo de ejecución vs. calidad")
plt.legend()
plt.grid(True)
plt.show()
