import random
import math
ciudades = [
    (0, 0), (2, 6), (5, 3), (6, 7),
    (8, 2), (1, 4), (7, 5), (3, 1)
]

def distancia(a, b):
    return math.dist(ciudades[a], ciudades[b])
def distancia_ruta(ruta):
    total = 0
    for i in range(len(ruta)):
        total += distancia(ruta[i], ruta[(i + 1) % len(ruta)])
    return total
def vecino_cercano():
    pendientes = list(range(1, len(ciudades)))
    ruta = [0]

    while pendientes:
        actual = ruta[-1]
        siguiente = min(
            pendientes,
            key=lambda ciudad: distancia(actual, ciudad)
        )
        ruta.append(siguiente)
        pendientes.remove(siguiente)

    return ruta
def dos_opt(ruta):
    ruta = ruta.copy()
    mejoras = 0

    while True:
        mejorada = False

        for i in range(len(ruta) - 1):
            for j in range(i + 2, len(ruta)):
                if i == 0 and j == len(ruta) - 1:
                    continue

                nueva = (
                    ruta[:i + 1]
                    + ruta[i + 1:j + 1][::-1]
                    + ruta[j + 1:]
                )

                if distancia_ruta(nueva) < distancia_ruta(ruta) - 1e-9:
                    ruta = nueva
                    mejoras += 1
                    mejorada = True
                    break

            if mejorada:
                break

        if not mejorada:
            break

    return ruta, mejoras

random.seed(42)
ruta_aleatoria = list(range(len(ciudades)))
random.shuffle(ruta_aleatoria)
ruta_cercana = vecino_cercano()

for nombre, ruta in [
    ("Aleatoria", ruta_aleatoria),
    ("Nearest Neighbour", ruta_cercana)
]:
    inicial = distancia_ruta(ruta)
    final, mejoras = dos_opt(ruta)

    print(f"\nRuta: {nombre}")
    print(f"Distancia inicial: {inicial:.2f}")
    print(f"Distancia final: {distancia_ruta(final):.2f}")
    print(f"Mejoras realizadas: {mejoras}")
    print(f"Ruta final: {final}")
