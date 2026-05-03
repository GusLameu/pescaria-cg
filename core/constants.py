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


# Vértices ORIGINAIS centrados na origem (0,0) com coordenadas UV (0.0 a 1.0)
# Formato: [ ((x, y), (u, v)), ... ]
PEIXE_MODELO_UV = [
    ((50, 0),   (1.0, 0.5)),  # Nariz (Pega a direita da textura)
    ((0, -30),  (0.5, 0.0)),  # Topo (Pega o topo da textura)
    ((-50, 0),  (0.0, 0.5)),  # Cauda (Pega a esquerda da textura)
    ((0, 30),   (0.5, 1.0))   # Baixo (Pega embaixo da textura)
]

COR_MAR = (10, 30, 60)
