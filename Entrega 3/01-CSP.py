import random

# --- 1. Definição dos Domínios ---
DOMINIO_NUCLEOS = ['Fogo do Dragão', 'Sussurro Fantasma', 'Vontade de Ferro', 'Véu Sombrio', 'Coração de Jade']
DOMINIO_ABORDAGENS = ['Furtividade', 'Combate', 'Hacking', 'Diplomacia']

# --- 2. Função de Aptidão (Fitness Function) ---
# Esta função avalia quão boa é uma solução (cromossomo)
# Quanto maior a aptidão, melhor a solução. Penalidades são subtraídas de um valor base.
def calcular_aptidao(cromossomo):
    # Desempacota o cromossomo para facilitar a leitura
    nucleo_f1, nucleo_f2, nucleo_f3, abordagem_f1, abordagem_f2, abordagem_f3 = cromossomo

    aptidao = 1000  # Pontuação base máxima

    # --- Restrições de Núcleo e Abordagem por Fortaleza ---

    # Fortaleza 1 (Templo dos Sussurros)
    if abordagem_f1 == 'Furtividade':
        if nucleo_f1 != 'Sussurro Fantasma':
            aptidao -= 100  # Penalidade alta por não ter o núcleo ideal para furtividade
    elif abordagem_f1 == 'Combate':
        if nucleo_f1 != 'Fogo do Dragão':
            aptidao -= 100  # Penalidade alta por não ter o núcleo ideal para combate
    else: # Outras abordagens para F1 têm penalidade base
        aptidao -= 50
    
    # Penalidade geral por desalinhamento para F1 se não for um dos casos ideais
    if (abordagem_f1 == 'Furtividade' and nucleo_f1 != 'Sussurro Fantasma') or \
       (abordagem_f1 == 'Combate' and nucleo_f1 != 'Fogo do Dragão'):
        pass # Já penalizado acima
    elif (abordagem_f1 == 'Hacking' and nucleo_f1 == 'Vontade de Ferro') or \
         (abordagem_f1 == 'Diplomacia' and nucleo_f1 == 'Coração de Jade'):
        aptidao -= 20 # Pequena penalidade por usar abordagem não ideal para F1 mas com núcleo sinérgico
    else:
        aptidao -= 30 # Penalidade por desalinhamento geral

    # Fortaleza 2 (Ciber-Pagode)
    if abordagem_f2 == 'Hacking':
        if nucleo_f2 != 'Vontade de Ferro':
            aptidao -= 100
    elif abordagem_f2 == 'Furtividade':
        if nucleo_f2 != 'Véu Sombrio':
            aptidao -= 100
    else: # Outras abordagens para F2 têm penalidade base
        aptidao -= 50

    # Penalidade geral por desalinhamento para F2
    if (abordagem_f2 == 'Hacking' and nucleo_f2 != 'Vontade de Ferro') or \
       (abordagem_f2 == 'Furtividade' and nucleo_f2 != 'Véu Sombrio'):
        pass
    elif (abordagem_f2 == 'Combate' and nucleo_f2 == 'Fogo do Dragão'):
        aptidao -= 20
    else:
        aptidao -= 30

    # Fortaleza 3 (Distrito do Mercado Flutuante)
    if abordagem_f3 == 'Diplomacia':
        if nucleo_f3 != 'Coração de Jade':
            aptidao -= 100
    elif abordagem_f3 == 'Combate':
        if nucleo_f3 != 'Fogo do Dragão':
            aptidao -= 100
    else: # Outras abordagens para F3 têm penalidade base
        aptidao -= 50

    # Penalidade geral por desalinhamento para F3
    if (abordagem_f3 == 'Diplomacia' and nucleo_f3 != 'Coração de Jade') or \
       (abordagem_f3 == 'Combate' and nucleo_f3 != 'Fogo do Dragão'):
        pass
    elif (abordagem_f3 == 'Furtividade' and nucleo_f3 == 'Sussurro Fantasma'):
        aptidao -= 20
    else:
        aptidao -= 30

    # --- Restrição de Inventário Limitado de Núcleos ---
    # Todos os núcleos devem ser diferentes
    nucleos_usados = [nucleo_f1, nucleo_f2, nucleo_f3]
    if len(set(nucleos_usados)) < 3: # Se houver repetição, o tamanho do set será menor que 3
        aptidao -= 200 # Penalidade muito alta por violar esta restrição crítica

    # --- Restrição de Sinergia/Conflito de Abordagens ---
    # Combate em fortalezas adjacentes
    if abordagem_f1 == 'Combate' and abordagem_f2 == 'Combate':
        aptidao -= 150 # Penalidade alta por aumentar o alerta
    if abordagem_f2 == 'Combate' and abordagem_f3 == 'Combate':
        aptidao -= 150 # Penalidade alta por aumentar o alerta

    # Diplomacia só é eficaz na Fortaleza 3
    if abordagem_f1 == 'Diplomacia' or abordagem_f2 == 'Diplomacia':
        aptidao -= 75 # Penalidade por usar diplomacia onde não é eficaz

    # Garante que a aptidão não seja negativa
    return max(0, aptidao)

# --- 3. Funções do Algoritmo Genético ---

# Cria um cromossomo aleatório
def criar_cromossomo_aleatorio():
    # 3 núcleos e 3 abordagens
    nucleos = random.sample(DOMINIO_NUCLEOS, 3) # Garante que os 3 núcleos são únicos desde o início
    abordagens = [random.choice(DOMINIO_ABORDAGENS) for _ in range(3)]
    return nucleos + abordagens

# Inicializa a população
def inicializar_populacao(tamanho_populacao):
    return [criar_cromossomo_aleatorio() for _ in range(tamanho_populacao)]

# Seleção por Torneio
def selecao_torneio(populacao, aptidoes, tamanho_torneio=3):
    selecionados = []
    for _ in range(2): # Seleciona 2 pais
        melhor_candidato = None
        melhor_aptidao = -1
        for _ in range(tamanho_torneio):
            indice_aleatorio = random.randrange(len(populacao))
            candidato = populacao[indice_aleatorio]
            aptidao_candidato = aptidoes[indice_aleatorio]
            if aptidao_candidato > melhor_aptidao:
                melhor_aptidao = aptidao_candidato
                melhor_candidato = candidato
        selecionados.append(melhor_candidato)
    return selecionados[0], selecionados[1]

# Crossover (Cruzamento de um ponto)
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1) - 1) # Ponto de corte entre 1 e 5
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2

# Mutação
def mutacao(cromossomo, taxa_mutacao=0.1):
    for i in range(len(cromossomo)):
        if random.random() < taxa_mutacao:
            if i < 3: # É um gene de núcleo
                # Garante que a mutação ainda resulte em núcleos únicos no cromossomo
                # Isso é um pouco mais complexo, para simplificar, vamos re-sortear se houver duplicata
                # Uma abordagem mais robusta seria um operador de mutação específico para permutações
                novo_nucleo = random.choice(DOMINIO_NUCLEOS)
                temp_cromossomo = list(cromossomo)
                temp_cromossomo[i] = novo_nucleo
                if len(set(temp_cromossomo[:3])) == 3: # Verifica se ainda são únicos
                    cromossomo[i] = novo_nucleo
                else: # Se a mutação causou duplicata, tenta outro ou não muta
                    pass # Não muta ou tenta de novo, para este exemplo, vamos simplificar
            else: # É um gene de abordagem
                cromossomo[i] = random.choice(DOMINIO_ABORDAGENS)
    return cromossomo

# --- 4. Loop Principal do Algoritmo Genético ---
def algoritmo_genetico(tamanho_populacao=50, num_geracoes=1000, taxa_mutacao=0.1):
    populacao = inicializar_populacao(tamanho_populacao)
    melhor_solucao = None
    melhor_aptidao = -1

    for geracao in range(num_geracoes):
        aptidoes = [calcular_aptidao(c) for c in populacao]

        # Encontra a melhor solução na geração atual
        idx_melhor_atual = aptidoes.index(max(aptidoes))
        solucao_atual = populacao[idx_melhor_atual]
        aptidao_atual = aptidoes[idx_melhor_atual]

        if aptidao_atual > melhor_aptidao:
            melhor_aptidao = aptidao_atual
            melhor_solucao = solucao_atual
            # print(f"Geração {geracao}: Nova melhor aptidão = {melhor_aptidao}, Solução = {melhor_solucao}")

        # Critério de parada: se encontrar uma solução perfeita
        if melhor_aptidao == 1000:
            print(f"\nSolução perfeita encontrada na Geração {geracao}!")
            break

        nova_populacao = []
        # Elitismo: manter o melhor indivíduo da geração anterior
        nova_populacao.append(list(melhor_solucao)) # Adiciona uma cópia para não modificar o original

        # Preenche o resto da nova população
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = selecao_torneio(populacao, aptidoes)
            filho1, filho2 = crossover(list(pai1), list(pai2)) # Passa cópias para crossover

            mutacao(filho1, taxa_mutacao)
            mutacao(filho2, taxa_mutacao)

            # Garante que os núcleos dos filhos continuem únicos após crossover/mutação
            # Esta é uma correção importante para o problema de núcleos únicos
            if len(set(filho1[:3])) != 3:
                # Se houver duplicatas, tenta gerar novos núcleos aleatórios e únicos
                filho1[:3] = random.sample(DOMINIO_NUCLEOS, 3)
            if len(set(filho2[:3])) != 3:
                filho2[:3] = random.sample(DOMINIO_NUCLEOS, 3)

            nova_populacao.append(filho1)
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)

        populacao = nova_populacao

    return melhor_solucao, melhor_aptidao

# --- Execução do Algoritmo ---
print("Iniciando simulação do Algoritmo Genético para Infiltração Cyberpunk...\n")
solucao_final, aptidao_final = algoritmo_genetico(tamanho_populacao=100, num_geracoes=2000, taxa_mutacao=0.15)

print("\n--- Resultado Final ---")
if solucao_final:
    print(f"Melhor Solução Encontrada (Aptidão: {aptidao_final}):")
    print(f"  Fortaleza 1 (Templo dos Sussurros):")
    print(f"    Núcleo: {solucao_final[0]}")
    print(f"    Abordagem: {solucao_final[3]}")
    print(f"  Fortaleza 2 (Ciber-Pagode):")
    print(f"    Núcleo: {solucao_final[1]}")
    print(f"    Abordagem: {solucao_final[4]}")
    print(f"  Fortaleza 3 (Distrito do Mercado Flutuante):")
    print(f"    Núcleo: {solucao_final[2]}")
    print(f"    Abordagem: {solucao_final[5]}")