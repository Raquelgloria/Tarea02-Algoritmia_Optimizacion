import random
import math
import time
import itertools
import matplotlib.pyplot as plt

def distancia(a, b):
    return math.dist(a, b)


def distancia_ruta(ruta, ciudades):
    total = 0

    for i in range(len(ruta)):
        total += distancia(
            ciudades[ruta[i]],
            ciudades[ruta[(i + 1) % len(ruta)]]
        )

    return total


# 1. Construye el árbol de expansión mínima usando Prim
def construir_mst(ciudades):
    n = len(ciudades)
    visitadas = {0}
    arbol = [[] for _ in range(n)]

    while len(visitadas) < n:
        mejor = None
        menor_distancia = float("inf")

        for u in visitadas:
            for v in range(n):
                if v not in visitadas:
                    d = distancia(ciudades[u], ciudades[v])

                    if d < menor_distancia:
                        menor_distancia = d
                        mejor = (u, v)

        u, v = mejor
        visitadas.add(v)
        arbol[u].append(v)
        arbol[v].append(u)

    return arbol


# Obtiene una ruta a partir del recorrido del MST
def ruta_mst(ciudades):
    arbol = construir_mst(ciudades)
    ruta = []
    visitadas = set()

    def dfs(u):
        visitadas.add(u)
        ruta.append(u)

        for v in arbol[u]:
            if v not in visitadas:
                dfs(v)

    dfs(0)
    return ruta


# 2. Mejora una ruta con 2-opt
def dos_opt(ruta, ciudades):
    ruta = ruta.copy()
    n = len(ruta)

    while True:
        mejorada = False

        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue

                nueva = (
                    ruta[:i + 1]
                    + ruta[i + 1:j + 1][::-1]
                    + ruta[j + 1:]
                )

                if distancia_ruta(nueva, ciudades) < (
                    distancia_ruta(ruta, ciudades) - 1e-9
                ):
                    ruta = nueva
                    mejorada = True
                    break

            if mejorada:
                break

        if not mejorada:
            break

    return ruta


def ruta_optima(ciudades):
    n = len(ciudades)
    mejor_costo = float("inf")

    
    for permutacion in itertools.permutations(range(1, n)):
        ruta = [0] + list(permutacion)
        costo = distancia_ruta(ruta, ciudades)

        if costo < mejor_costo:
            mejor_costo = costo

    return mejor_costo



def recocido_simulado(ruta_inicial, ciudades, semilla):
    rng = random.Random(semilla)
    actual = ruta_inicial.copy()
    costo_actual = distancia_ruta(actual, ciudades)

    mejor = actual.copy()
    mejor_costo = costo_actual

    iteraciones = 1000
    t_inicial = 100
    t_final = 0.01

    for t in range(iteraciones):
        progreso = t / (iteraciones - 1)

        temperatura = t_inicial * (
            t_final / t_inicial
        ) ** progreso

        i, j = sorted(rng.sample(range(len(actual)), 2))
        siguiente = actual.copy()
        siguiente[i:j + 1] = siguiente[i:j + 1][::-1]

        
        if i == 0 and j == len(actual) - 1:
            continue

        costo_siguiente = distancia_ruta(siguiente, ciudades)
        delta = costo_actual - costo_siguiente

        if delta > 0 or rng.random() < math.exp(delta / temperatura):
            actual = siguiente
            costo_actual = costo_siguiente

        if costo_actual < mejor_costo:
            mejor = actual.copy()
            mejor_costo = costo_actual

    return mejor



resultados = {
    "MST puro": [],
    "MST + 2-opt": [],
    "Búsqueda Local": [],
    "Recocido Simulado": []
}

razones_mst = []
razones_mst_opt = []
tiempo_inicio = time.perf_counter()

for instancia in range(100):
    rng = random.Random(1000 + instancia)

    
    ciudades = [
        (rng.uniform(0, 100), rng.uniform(0, 100))
        for _ in range(9)
    ]

    # Óptimo exacto
    optimo = ruta_optima(ciudades)

    # MST puro
    ruta = ruta_mst(ciudades)
    costo_mst = distancia_ruta(ruta, ciudades)

    # MST + 2-opt
    ruta_mejorada = dos_opt(ruta, ciudades)
    costo_mst_opt = distancia_ruta(ruta_mejorada, ciudades)

  
    ruta_aleatoria = list(range(9))
    rng.shuffle(ruta_aleatoria)

    ruta_local = dos_opt(ruta_aleatoria, ciudades)
    costo_local = distancia_ruta(ruta_local, ciudades)

    
    ruta_sa = recocido_simulado(
        ruta_aleatoria, ciudades, 5000 + instancia
    )
    costo_sa = distancia_ruta(ruta_sa, ciudades)

    resultados["MST puro"].append(costo_mst)
    resultados["MST + 2-opt"].append(costo_mst_opt)
    resultados["Búsqueda Local"].append(costo_local)
    resultados["Recocido Simulado"].append(costo_sa)

    razones_mst.append(costo_mst / optimo)
    razones_mst_opt.append(costo_mst_opt / optimo)

tiempo_total = time.perf_counter() - tiempo_inicio

print("Instancias evaluadas: 100")
print(f"Tiempo total: {tiempo_total:.2f} segundos")

print("\nPromedios de distancia:")
for metodo, costos in resultados.items():
    print(f"{metodo}: {sum(costos) / len(costos):.2f}")

print("\nRazón de aproximación:")
print(f"MST promedio: {sum(razones_mst) / 100:.4f}")
print(f"MST máxima: {max(razones_mst):.4f}")
print(f"MST + 2-opt promedio: {sum(razones_mst_opt) / 100:.4f}")
print(f"MST + 2-opt máxima: {max(razones_mst_opt):.4f}")


# Razón de aproximación
plt.figure(figsize=(9, 5))
plt.hist(razones_mst, bins=12, edgecolor="black")
plt.axvline(2, linestyle="--", label="Límite teórico = 2")
plt.xlabel("Costo MST / Costo óptimo")
plt.ylabel("Número de instancias")
plt.title("Razón de aproximación del MST en 100 instancias")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.show()


# Comparación de costos
plt.figure(figsize=(9, 5))
nombres = list(resultados.keys())
costos = [resultados[nombre] for nombre in nombres]

plt.boxplot(costos, tick_labels=nombres)
plt.ylabel("Distancia total")
plt.title("Comparación de métodos en 100 instancias")
plt.xticks(rotation=15)
plt.grid(axis="y", alpha=0.3)
plt.show()


# Razón MST antes y después de 2-opt
plt.figure(figsize=(9, 5))
plt.boxplot(
    [razones_mst, razones_mst_opt],
    tick_labels=["MST puro", "MST + 2-opt"]
)
plt.axhline(2, linestyle="--", label="Límite teórico = 2")
plt.ylabel("Costo obtenido / Costo óptimo")
plt.title("Efecto de aplicar 2-opt al MST")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.show()
