# Define a função principal de diagnóstico para o carro de corrida Star-Racer 3000.
def diagnosticar_carro(sintomas, estado_componentes):
    """
    Args:
        sintomas (list): Uma lista de strings com os sintomas observados pelo piloto
                         ou sensores do carro (ex: ['perda_potencia', 'cheiro_queimado']).
        estado_componentes (dict): Um dicionário onde as chaves são os nomes dos
                                   componentes do carro (ex: 'motor', 'pneus')
                                   e os valores são seus estados atuais (ex: 'ok', 'superaquecido').

    Returns:
        list: Uma lista de dicionários. Cada dicionário representa um diagnóstico
              e contém as chaves 'problema' (descrição do problema) e 'acao_sugerida'
              (ação recomendada para o reparo).
              Se nenhum problema for identificado pelas regras, retorna uma sugestão de inspeção.
    """
    diagnosticos = [] # Inicializa uma lista para armazenar todos os diagnósticos encontrados.

    # --- Regras de Diagnóstico Baseadas em Sintomas Combinados e Individuais ---

    # Regra 1: Perda de potência e fumaça do escapamento (indica problemas graves no motor/energia)
    if 'perda_potencia' in sintomas and 'fumaça_escapamento' in sintomas:
        diagnosticos.append({
            'problema': 'Motor com falha grave ou sistema de energia instável.',
            'acao_sugerida': 'Verificar velas, injeção e cabos do motor. Inspecionar regulador de voltagem.'
        })

    # Regra 2: Vibração anormal e direção puxando (sugere problemas em pneus/aerodinâmica)
    if 'vibracao_anormal' in sintomas and 'direcao_puxando' in sintomas:
        diagnosticos.append({
            'problema': 'Pneus ou aerodinâmica comprometidos.',
            'acao_sugerida': 'Checar balanceamento e alinhamento dos pneus. Inspecionar estado da asa traseira.'
        })

    # Regra 3: Cheiro queimado (sinal de superaquecimento ou curto-circuito)
    if 'cheiro_queimado' in sintomas:
        diagnosticos.append({
            'problema': 'Superaquecimento de motor, freios ou curto-circuito elétrico.',
            'acao_sugerida': 'Verificar nível de fluidos, temperatura do motor e fusíveis. Resfriar freios.'
        })

    # Regra 4: Instabilidade em curvas (relacionado a pneus ou aerodinâmica)
    if 'instabilidade_curva' in sintomas:
        diagnosticos.append({
            'problema': 'Pneus com pressão irregular ou danos aerodinâmicos.',
            'acao_sugerida': 'Verificar pressão dos pneus. Inspecionar defletores e spoilers.'
        })

    # Regra 5: Display do painel falhando (problemas no sistema elétrico/energia)
    if 'display_painel_falha' in sintomas:
        diagnosticos.append({
            'problema': 'Falha no sistema de energia ou conectividade do painel.',
            'acao_sugerida': 'Verificar fusíveis e conexões da bateria. Reiniciar sistema eletrônico.'
        })

    # Regra 6: Barulho metálico nos freios (indica desgaste de componentes do freio)
    if 'barulho_metalico_freios' in sintomas:
        diagnosticos.append({
            'problema': 'Desgaste das pastilhas de freio ou discos.',
            'acao_sugerida': 'Substituir pastilhas e verificar discos. Verificar vazamento de fluido.'
        })

    # Regra 7: Perda de potência (mas sem fumaça do escapamento, diagnóstico mais específico)
    if 'perda_potencia' in sintomas and 'fumaça_escapamento' not in sintomas:
        diagnosticos.append({
            'problema': 'Possível falha de ignição ou obstrução na entrada de ar.',
            'acao_sugerida': 'Verificar filtro de ar e sistema de ignição.'
        })

    # Regra 8: Fumaça do escapamento (mas sem perda de potência, outro diagnóstico específico)
    if 'fumaça_escapamento' in sintomas and 'perda_potencia' not in sintomas:
        diagnosticos.append({
            'problema': 'Vazamento de óleo ou problema na combustão.',
            'acao_sugerida': 'Verificar nível e vazamentos de óleo. Inspecionar bicos injetores.'
        })


    # Verifica se o motor está superaquecido
    if estado_componentes.get('motor') == 'superaquecido':
        diagnosticos.append({
            'problema': 'Motor superaquecido.',
            'acao_sugerida': 'Desligar o motor imediatamente. Verificar sistema de arrefecimento e nível de fluido.'
        })

    # Verifica se há pneu furado
    if estado_componentes.get('pneus') == 'furado':
        diagnosticos.append({
            'problema': 'Pneu furado.',
            'acao_sugerida': 'Substituir pneu danificado.'
        })

    # Verifica se o sistema de energia está sem energia
    if estado_componentes.get('sistema_energia') == 'sem_energia':
        diagnosticos.append({
            'problema': 'Sem energia no sistema principal.',
            'acao_sugerida': 'Verificar bateria e alternador. Chamar equipe de resgate.'
        })

    # Se, após todas as regras, nenhum diagnóstico específico foi adicionado, sugere uma inspeção geral.
    if not diagnosticos:
        diagnosticos.append({
            'problema': 'Nenhum problema aparente com base nos sintomas e regras fornecidas.',
            'acao_sugerida': 'Realizar uma inspeção de rotina completa.'
        })

    return diagnosticos

# Função auxiliar para executar e imprimir os resultados de cada cenário.
def executar_simulacao(cenario_nome, sintomas, estado_componentes):
    """
    Executa a simulação para um cenário específico de diagnóstico e imprime os resultados.

    Args:
        cenario_nome (str): Nome descritivo do cenário.
        sintomas (list): Lista de sintomas para o cenário.
        estado_componentes (dict): Dicionário com o estado dos componentes para o cenário.
    """
    print(f"\n--- Cenário: {cenario_nome} ---")
    # Exibe os sintomas observados; se não houver, mostra 'Nenhum'.
    print(f"Sintomas Observados: {', '.join(sintomas) if sintomas else 'Nenhum'}")
    # Exibe o estado atual dos componentes.
    print(f"Estado Atual dos Componentes: {estado_componentes}")

    resultados_diagnostico = diagnosticar_carro(sintomas, estado_componentes)

    print("\nResultados do Diagnóstico:")
    if resultados_diagnostico:
        # Itera sobre cada diagnóstico e o imprime formatado.
        for i, resultado in enumerate(resultados_diagnostico):
            print(f"  Diagnóstico {i+1}:")
            print(f"    Problema: {resultado['problema']}")
            print(f"    Ação Sugerida: {resultado['acao_sugerida']}")
    else:
        # Caso não haja diagnósticos específicos.
        print("  Nenhum diagnóstico específico encontrado.")
    print("-" * 40) 


# Cenário 1: Problemas no motor (perda de potência e fumaça)
sintomas_cenario1 = ['perda_potencia', 'fumaça_escapamento']
estado_componentes_cenario1 = {
    'motor': 'falha_ignicao',
    'pneus': 'ok',
    'sistema_energia': 'ok',
    'aerodinamica': 'ok',
    'sistema_freios': 'ok'
}

# Cenário 2: Problemas nos pneus e na aerodinâmica (vibração, direção puxando, instabilidade)
sintomas_cenario2 = ['vibracao_anormal', 'direcao_puxando', 'instabilidade_curva']
estado_componentes_cenario2 = {
    'motor': 'ok',
    'pneus': 'desgastado',
    'sistema_energia': 'ok',
    'aerodinamica': 'asa_danificada',
    'sistema_freios': 'ok'
}

# Cenário 3: Problema no painel e cheiro de queimado (curto-circuito no sistema de energia)
sintomas_cenario3 = ['display_painel_falha', 'cheiro_queimado']
estado_componentes_cenario3 = {
    'motor': 'ok',
    'pneus': 'ok',
    'sistema_energia': 'curto_circuito',
    'aerodinamica': 'ok',
    'sistema_freios': 'ok'
}

# Cenário 4: Nenhum sintoma grave (inspeção de rotina esperada)
sintomas_cenario4 = []
estado_componentes_cenario4 = {
    'motor': 'ok',
    'pneus': 'ok',
    'sistema_energia': 'ok',
    'aerodinamica': 'ok',
    'sistema_freios': 'ok'
}

# Cenário 5: Barulho de freio e motor superaquecido (diagnóstico por sintoma e estado)
sintomas_cenario5 = ['barulho_metalico_freios']
estado_componentes_cenario5 = {
    'motor': 'superaquecido', 
    'pneus': 'ok',
    'sistema_energia': 'ok',
    'aerodinamica': 'ok',
    'sistema_freios': 'desgaste_pastilhas'
}

# Cenário 6: Apenas perda de potência (sem fumaça)
sintomas_cenario6 = ['perda_potencia']
estado_componentes_cenario6 = {
    'motor': 'ok',
    'pneus': 'ok',
    'sistema_energia': 'ok',
    'aerodinamica': 'ok',
    'sistema_freios': 'ok'
}

# Cenário 7: Apenas fumaça do escapamento (sem perda de potência)
sintomas_cenario7 = ['fumaça_escapamento']
estado_componentes_cenario7 = {
    'motor': 'perda_oleo',
    'pneus': 'ok',
    'sistema_energia': 'ok',
    'aerodinamica': 'ok',
    'sistema_freios': 'ok'
}

# Cenário 8: Pneu furado (diagnóstico apenas pelo estado do componente)
sintomas_cenario8 = []
estado_componentes_cenario8 = {
    'motor': 'ok',
    'pneus': 'furado', 
    'sistema_energia': 'ok',
    'aerodinamica': 'ok',
    'sistema_freios': 'ok'
}

# Chama a função de simulação para cada cenário definido.
executar_simulacao("Motor com Problemas Graves", sintomas_cenario1, estado_componentes_cenario1)
executar_simulacao("Problemas de Estabilidade (Pneus/Aerodinâmica)", sintomas_cenario2, estado_componentes_cenario2)
executar_simulacao("Falha Elétrica e Aquecimento", sintomas_cenario3, estado_componentes_cenario3)
executar_simulacao("Carro Sem Sintomas Aparente", sintomas_cenario4, estado_componentes_cenario4)
executar_simulacao("Barulho nos Freios e Motor Quente", sintomas_cenario5, estado_componentes_cenario5)
executar_simulacao("Apenas Perda de Potência", sintomas_cenario6, estado_componentes_cenario6)
executar_simulacao("Apenas Fumaça do Escapamento", sintomas_cenario7, estado_componentes_cenario7)
executar_simulacao("Pneu Furado Detectado", sintomas_cenario8, estado_componentes_cenario8)
