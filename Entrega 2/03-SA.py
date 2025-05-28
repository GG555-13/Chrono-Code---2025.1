import random
import math

# Esta função simula o "nível de atividade" ou "ameaça" do guardião
# com base em 5 parâmetros de controle. O objetivo é minimizar essa atividade.
# Parâmetros: [frequência1, amplitude1, pulso1, frequência2, amplitude2]
# Definimos um conjunto de "parâmetros ideais" que resultariam na atividade mínima (0).
IDEAL_PARAMS = [75.0, 0.7, 248.0, 1.0, 0.5] # Exemplo de parâmetros ideais para desativação

def dinosaur_activity(params):
    """
    Calcula o nível de atividade do dinossauro robô para um dado conjunto de parâmetros.
    Quanto menor o valor, mais "desativado" o dinossauro está.
    """
    if len(params) != 5:
        return float('inf') # Retorna infinito se o número de parâmetros estiver incorreto

    # Calcula a "distância" dos parâmetros atuais em relação aos parâmetros ideais.
    # Usamos a soma dos quadrados das diferenças para simular uma função de custo
    # com um mínimo claro.
    activity = 0.0
    for i in range(5):
        activity += (params[i] - IDEAL_PARAMS[i])**2

    # Adiciona um pequeno ruído para simular a imprevisibilidade do ambiente real
    # e tornar a otimização mais desafiadora.
    activity += random.uniform(0, 0.5)

    return activity

# --- 2. Implementação do Algoritmo Simulated Annealing ---

def simulated_annealing(
    cost_function,
    param_ranges,
    initial_temperature,
    cooling_rate,
    num_iterations
):
    """
    Executa o algoritmo de Simulated Annealing para encontrar uma solução quase ótima.

    Args:
        cost_function (callable): A função a ser minimizada (atividade do dinossauro).
        param_ranges (list of tuples): Uma lista de tuplas (min, max) para cada parâmetro.
        initial_temperature (float): A temperatura inicial para o recozimento.
        cooling_rate (float): A taxa de resfriamento (ex: 0.99 para resfriamento exponencial).
        num_iterations (int): O número máximo de iterações.

    Returns:
        tuple: A melhor solução (parâmetros) encontrada e o custo correspondente.
    """
    num_params = len(param_ranges)

    # 2.1. Inicialização
    # Gera uma solução inicial aleatória dentro dos limites dos parâmetros.
    current_solution = [random.uniform(r[0], r[1]) for r in param_ranges]
    current_cost = cost_function(current_solution)

    best_solution = list(current_solution) # Copia a lista
    best_cost = current_cost

    temperature = initial_temperature

    print(f"Início da Simulação:")
    print(f"  Solução inicial: {current_solution}")
    print(f"  Custo inicial (atividade): {current_cost:.4f}")
    print("-" * 40)

    # 2.2. Iteração (Loop Principal)
    for i in range(num_iterations):
        # 2.2.a. Geração de Vizinho (S novo)
        # Cria uma nova solução perturbando aleatoriamente um dos parâmetros.
        # A magnitude da perturbação diminui com a temperatura.
        new_solution = list(current_solution)
        param_to_perturb = random.randint(0, num_params - 1)
        
        # Calcula o desvio máximo permitido para a perturbação,
        # que diminui com a temperatura para refinar a busca.
        max_deviation = (param_ranges[param_to_perturb][1] - param_ranges[param_to_perturb][0]) * (temperature / initial_temperature) * 0.1 # 10% do range, ajustado pela temperatura
        
        # Adiciona um valor aleatório dentro do desvio máximo
        new_solution[param_to_perturb] += random.uniform(-max_deviation, max_deviation)

        # Garante que o novo parâmetro permaneça dentro de seus limites definidos.
        new_solution[param_to_perturb] = max(param_ranges[param_to_perturb][0], new_solution[param_to_perturb])
        new_solution[param_to_perturb] = min(param_ranges[param_to_perturb][1], new_solution[param_to_perturb])

        new_cost = cost_function(new_solution)

        # 2.2.b. Cálculo da Variação de Energia (Delta E)
        delta_e = new_cost - current_cost

        # 2.2.c. Decisão de Aceitação
        # Se a nova solução é melhor OU (se for pior, mas aceita probabilisticamente)
        if delta_e < 0 or random.random() < math.exp(-delta_e / temperature):
            current_solution = list(new_solution)
            current_cost = new_cost

            # Atualiza a melhor solução global encontrada até agora
            if current_cost < best_cost:
                best_solution = list(current_solution)
                best_cost = current_cost

        # 2.2.d. Resfriamento (Cooling Schedule)
        # Reduz a temperatura gradualmente.
        temperature *= cooling_rate

        # Imprime o progresso a cada X iterações
        if i % (num_iterations // 10) == 0:
            print(f"Iteração {i}/{num_iterations}: Temp={temperature:.2f}, Custo Atual={current_cost:.4f}, Melhor Custo={best_cost:.4f}")

    print("-" * 40)
    return best_solution, best_cost


if __name__ == "__main__":
    # Definindo os limites para cada um dos 5 parâmetros
    # [frequência1 (1-200), amplitude1 (0.1-1.0), pulso1 (10-500), frequência2 (1-200), amplitude2 (0.1-1.0)]
    parameter_ranges = [
        (1.0, 200.0),  # Frequência 1
        (0.1, 1.0),    # Amplitude 1
        (10.0, 500.0), # Pulso 1
        (1.0, 200.0),  # Frequência 2
        (0.1, 1.0)     # Amplitude 2
    ]

    # Parâmetros do Simulated Annealing
    initial_temp = 1000.0  # Temperatura inicial alta para exploração
    cooling_rate = 0.995   # Taxa de resfriamento (exponencial)
    iterations = 30000     # Número de iterações para a simulação

    # Executa o algoritmo
    final_params, final_activity = simulated_annealing(
        dinosaur_activity,
        parameter_ranges,
        initial_temp,
        cooling_rate,
        iterations
    )

    print("\n--- Resultado Final ---")
    print(f"Parâmetros ideais para desativação (aproximados): {IDEAL_PARAMS}")
    print(f"Melhores parâmetros encontrados: {final_params}")
    print(f"Atividade mínima alcançada (custo): {final_activity:.4f}")

    # Uma pequena verificação para ver o quão perto chegamos dos parâmetros ideais
    distance_to_ideal = sum([(final_params[i] - IDEAL_PARAMS[i])**2 for i in range(5)])**0.5
    print(f"Distância euclidiana para os parâmetros ideais: {distance_to_ideal:.4f}")

    if final_activity < 1.0: # Um limiar arbitrário para considerar "desativado"
        print("\nO Guardião foi desativado com sucesso!")
    else:
        print("\nO Guardião robô ainda está ativo. Tente mais iterações ou ajuste os parâmetros do SA.")