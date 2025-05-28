import random

# --- Configurações do Problema ---
# A sequência alvo secreta que o algoritmo genético precisa encontrar.
# Em um cenário real, esta seria a combinação desconhecida do sistema de defesa do livro.
SEQUENCIA_ALVO_SECRETA = [2, 5, 1, 8, 3]
NUM_MODULOS = len(SEQUENCIA_ALVO_SECRETA)
VALOR_MIN_MODULO = 0
VALOR_MAX_MODULO = 9

# --- Parâmetros do Algoritmo Genético ---
TAMANHO_POPULACAO = 100
NUM_GERACOES = 500
TAXA_MUTACAO = 0.05  # 5% de chance de um gene (configuração do módulo) mutar
TAMANHO_TORNEIO = 5  # Número de indivíduos selecionados para o torneio de seleção de pais

# --- Classe para representar um Cromossomo (uma possível solução) ---
class Cromossomo:
    def __init__(self, genes=None):
        """
        Inicializa um cromossomo.
        Se 'genes' não for fornecido, gera genes aleatórios.
        Genes: Lista de inteiros representando as configurações dos módulos.
        """
        if genes is None:
            self.genes = [random.randint(VALOR_MIN_MODULO, VALOR_MAX_MODULO) for _ in range(NUM_MODULOS)]
        else:
            self.genes = genes
        self.aptidao = 0 # A aptidão será calculada posteriormente

    def __repr__(self):
        """Representação em string do cromossomo."""
        return f"Cromossomo({self.genes}, Aptidão: {self.aptidao:.2f})"

# --- Funções do Algoritmo Genético ---

def calcular_aptidao(cromossomo: Cromossomo) -> float:
    """
    Calcula a aptidão de um cromossomo.
    A aptidão é calculada com base no risco de alarme e no número de módulos corretos.
    Objetivo: Maximizar módulos corretos e minimizar o risco total de alarme.
    """
    risco_total_alarme = 0
    modulos_corretos = 0

    for i in range(NUM_MODULOS):
        # Calcula o risco para cada módulo como a diferença absoluta entre o valor
        # do gene do cromossomo e o valor alvo secreto.
        risco_total_alarme += abs(cromossomo.genes[i] - SEQUENCIA_ALVO_SECRETA[i])
        
        # Verifica se o módulo está configurado corretamente.
        if cromossomo.genes[i] == SEQUENCIA_ALVO_SECRETA[i]:
            modulos_corretos += 1
    
    # A aptidão é uma combinação que prioriza módulos corretos e penaliza o risco.
    # Multiplicamos 'modulos_corretos' por um peso maior para que a correção seja mais valorizada.
    # Se todos os módulos estiverem corretos, o risco_total_alarme será 0, e a aptidão será máxima.
    aptidao = (modulos_corretos * 100) - risco_total_alarme
    cromossomo.aptidao = aptidao
    return aptidao

def gerar_populacao_inicial(tamanho_populacao: int) -> list[Cromossomo]:
    """
    Gera uma população inicial de cromossomos aleatórios.
    """
    populacao = [Cromossomo() for _ in range(tamanho_populacao)]
    return populacao

def selecionar_pais(populacao: list[Cromossomo], tamanho_torneio: int) -> list[Cromossomo]:
    """
    Seleciona pais para a próxima geração usando seleção por torneio.
    Em cada torneio, um número 'tamanho_torneio' de indivíduos é escolhido aleatoriamente,
    e o indivíduo com a melhor aptidão entre eles é selecionado como pai.
    """
    pais = []
    for _ in range(len(populacao)):
        # Escolhe 'tamanho_torneio' indivíduos aleatoriamente da população.
        candidatos = random.sample(populacao, tamanho_torneio)
        
        # Encontra o melhor candidato (o mais apto) entre os selecionados.
        melhor_candidato = max(candidatos, key=lambda c: c.aptidao)
        pais.append(melhor_candidato)
    return pais

def cruzar(pai1: Cromossomo, pai2: Cromossomo) -> tuple[Cromossomo, Cromossomo]:
    """
    Realiza o cruzamento (crossover) de um ponto entre dois pais para gerar dois filhos.
    Um ponto de corte aleatório é escolhido, e os genes são trocados após esse ponto.
    """
    ponto_cruzamento = random.randint(1, NUM_MODULOS - 1) # Ponto de corte entre 1 e NUM_MODULOS-1
    
    # Cria os genes dos filhos combinando partes dos genes dos pais.
    genes_filho1 = pai1.genes[:ponto_cruzamento] + pai2.genes[ponto_cruzamento:]
    genes_filho2 = pai2.genes[:ponto_cruzamento] + pai1.genes[ponto_cruzamento:]
    
    return Cromossomo(genes_filho1), Cromossomo(genes_filho2)

def mutar(cromossomo: Cromossomo, taxa_mutacao: float) -> Cromossomo:
    """
    Aplica mutação a um cromossomo.
    Para cada gene, há uma chance 'taxa_mutacao' de seu valor ser alterado aleatoriamente.
    """
    for i in range(NUM_MODULOS):
        if random.random() < taxa_mutacao:
            # Altera o gene para um novo valor aleatório dentro do intervalo permitido.
            cromossomo.genes[i] = random.randint(VALOR_MIN_MODULO, VALOR_MAX_MODULO)
    return cromossomo

# --- Função Principal do Algoritmo Genético ---
def executar_algoritmo_genetico():
    """
    Executa o algoritmo genético para encontrar a sequência alvo.
    """
    print("Iniciando o Algoritmo Genético para desvendar o Livro de Oraculum...")
    print(f"Sequência alvo secreta (conhecida apenas pelo simulador): {SEQUENCIA_ALVO_SECRETA}")

    # 1. Geração da População Inicial
    populacao = gerar_populacao_inicial(TAMANHO_POPULACAO)

    for geracao in range(1, NUM_GERACOES + 1):
        # 2. Avaliação da Aptidão de cada Cromossomo na População
        for cromossomo in populacao:
            calcular_aptidao(cromossomo)

        # Encontra o melhor indivíduo da geração atual para monitoramento
        melhor_cromossomo_geracao = max(populacao, key=lambda c: c.aptidao)

        # Imprime o progresso a cada 50 gerações ou se uma solução ideal for encontrada
        if geracao % 50 == 0 or melhor_cromossomo_geracao.aptidao == (NUM_MODULOS * 100):
            print(f"\n--- Geração {geracao} ---")
            print(f"Melhor Cromossomo: {melhor_cromossomo_geracao.genes}")
            print(f"Aptidão: {melhor_cromossomo_geracao.aptidao:.2f}")
            
            # Verifica se a solução ideal foi encontrada (aptidão máxima possível)
            if melhor_cromossomo_geracao.aptidao == (NUM_MODULOS * 100):
                print("\n Solução ótima encontrada! O livro foi desvendado sem alarmes!")
                print(f"Sequência final aplicada pelo robô: {melhor_cromossomo_geracao.genes}")
                return melhor_cromossomo_geracao.genes

        # 3. Seleção de Pais para a Próxima Geração
        pais = selecionar_pais(populacao, TAMANHO_TORNEIO)

        # 4. Criação da Nova População (Cruzamento e Mutação)
        nova_populacao = []
        # Garante que a nova população tenha o mesmo tamanho, cruzando em pares.
        for i in range(0, TAMANHO_POPULACAO, 2):
            pai1 = pais[i]
            # Se o número de pais for ímpar, o último pai é cruzado com o primeiro.
            pai2 = pais[i+1] if i+1 < TAMANHO_POPULACAO else pais[0] 
            
            filho1, filho2 = cruzar(pai1, pai2)
            
            # Aplica mutação aos filhos
            nova_populacao.append(mutar(filho1, TAXA_MUTACAO))
            nova_populacao.append(mutar(filho2, TAXA_MUTACAO))
        
        # Atualiza a população para a próxima geração
        populacao = nova_populacao[:TAMANHO_POPULACAO] # Garante que o tamanho da população seja mantido

    # Se o loop terminar sem encontrar a solução ótima
    print("\nO algoritmo genético concluiu as gerações.")
    melhor_cromossomo_final = max(populacao, key=lambda c: c.aptidao)
    print(f"Melhor solução encontrada: {melhor_cromossomo_final.genes}")
    print(f"Aptidão final: {melhor_cromossomo_final.aptidao:.2f}")
    print("O robô aplicou a melhor sequência que conseguiu otimizar.")
    return melhor_cromossomo_final.genes

# --- Execução do Algoritmo ---
if __name__ == "__main__":
    solucao_encontrada = executar_algoritmo_genetico()
    print(f"\nSequência alvo real (para comparação): {SEQUENCIA_ALVO_SECRETA}")
    print(f"Sequência encontrada pelo robô: {solucao_encontrada}")
