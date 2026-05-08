def gerar_textura_procedural(size=64):
    """
    Gera uma matriz de cores simulando um padrão de escamas (xadrez/diamante).
    Retorna uma lista de listas com tuplas RGB.
    """
    textura = []
    for y in range(size):
        linha = []
        for x in range(size):
            # Cria um padrão quadriculado simples
            if (x // 8 + y // 8) % 2 == 0:
                linha.append((218, 165, 32))  # Dourado escuro
            else:
                linha.append((139, 69, 19))  # Marrom
        textura.append(linha)
    return textura


# Corpo do peixe com 8 vertices (formato mais realista) + UV
PEIXE_MODELO_UV = [
    ((35, 0),   (1.0, 0.5)),
    ((22, -13), (0.8, 0.1)),
    ((0, -17),  (0.5, 0.0)),
    ((-18, -11),(0.2, 0.1)),
    ((-24, 0),  (0.0, 0.5)),
    ((-18, 11), (0.2, 0.9)),
    ((0, 17),   (0.5, 1.0)),
    ((22, 13),  (0.8, 0.9)),
]

# Cauda bifurcada (dois triangulos) - começa no ponto esquerdo do corpo (-24, 0)
PEIXE_CAUDA = [
    [(-24, 0), (-44, -20), (-32, 0)],
    [(-24, 0), (-44,  20), (-32, 0)],
]

# Nadadeira dorsal - base sobre a borda do corpo
PEIXE_NADADEIRA = [(-5, -15), (15, -14), (5, -28)]

COR_MAR = (10, 30, 60)
