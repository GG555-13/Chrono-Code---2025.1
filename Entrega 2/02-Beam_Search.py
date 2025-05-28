import heapq

# Heurística simples baseada em uma lista de palavras "corretas"
valid_words = {"enter", "the", "path", "of", "knowledge", "now"}

# Candidatos por posição (simulando possíveis traduções por palavra)
candidates = [
    ["enter", "entering", "enters"],
    ["the", "this", "a"],
    ["path", "way", "road"],
    ["of", "from", "to"],
    ["knowledge", "wisdom", "tech"],
    ["now", "soon", "today"]
]

beam_width = 3

def heuristic_score(sentence):
    return sum(1 for word in sentence if word in valid_words)

def beam_search_translation(candidates, beam_width):
    beam = [([], 0)]  # (sentença até agora, score acumulado)
    
    for position in candidates:
        new_beam = []
        for prefix, _ in beam:
            for word in position:
                new_sentence = prefix + [word]
                score = heuristic_score(new_sentence)
                heapq.heappush(new_beam, (-score, new_sentence))
        
        # Seleciona os beam_width melhores
        beam = [heapq.heappop(new_beam)[::-1] for _ in range(min(beam_width, len(new_beam)))]
    
    # Retorna a melhor sentença
    best_sentence, best_score = max(beam, key=lambda x: x[1])
    return best_sentence, best_score

# Executa a busca
result_sentence, score = beam_search_translation(candidates, beam_width)

# Imprime o resultado
print("Resultado da tradução:")
print("Frase:", " ".join(result_sentence))
print("Pontuação heurística:", score)
