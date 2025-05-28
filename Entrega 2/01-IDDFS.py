# Estrutura do grafo das ruínas
grafo_ruinas = {
    "Entrada": ["Sala A"],
    "Sala A": ["Sala B", "Sala C"],
    "Sala B": ["Sala D"],
    "Sala C": ["Sala E"],
    "Sala D": ["Sala F"],
    "Sala E": ["Sala G"],
    "Sala G": ["Sala H"],
    "Sala H": ["Sala Final"],
    "Sala F": [],
    "Sala Final": []
}

# Busca limitada em profundidade
def dls(grafo, atual, destino, limite, caminho):
    caminho.append(atual)
    if atual == destino:
        return True
    if limite <= 0:
        caminho.pop()
        return False
    for vizinho in grafo.get(atual, []):
        if dls(grafo, vizinho, destino, limite - 1, caminho):
            return True
    caminho.pop()
    return False

# Busca Iterativa
def iddfs(grafo, inicio, destino):
    profundidade = 0
    while True:
        caminho = []
        if dls(grafo, inicio, destino, profundidade, caminho):
            return caminho, profundidade
        profundidade += 1

# Executando o algoritmo
caminho, profundidade = iddfs(grafo_ruinas, "Entrada", "Sala Final")
print("Caminho encontrado:", caminho)
print("Profundidade necessária:", profundidade)
