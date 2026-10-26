objetos = {
    "A": (10, 2),
    "B": (3, 7),
    "C": (5, 30),
    "D": (4, 28)
}
capacidad = 10
def mochila(objetos, criterio):
    if criterio == "peso":
        ordenados = sorted(
            objetos.items(),
            key=lambda x: x[1][0]
        )
    else:
        ordenados = sorted(
            objetos.items(),
            key=lambda x: x[1][1] / x[1][0],
            reverse=True
        )

    peso_total = 0
    valor_total = 0
    seleccionados = []

    for nombre, (peso, valor) in ordenados:
        if peso_total + peso <= capacidad:
            seleccionados.append(nombre)
            peso_total += peso
            valor_total += valor

    return seleccionados, peso_total, valor_total
# Método 1: menor peso primero
resultado_peso = mochila(objetos, "peso")
# Método 2: mayor valor/peso primero
resultado_ratio = mochila(objetos, "ratio")
print("Menor peso primero:")
print("Objetos:", resultado_peso[0])
print("Peso total:", resultado_peso[1])
print("Valor total:", resultado_peso[2])
print("\nMayor valor/peso primero:")
print("Objetos:", resultado_ratio[0])
print("Peso total:", resultado_ratio[1])
print("Valor total:", resultado_ratio[2])
