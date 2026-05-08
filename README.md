# Pescaria CG

Jogo arcade 2D de pesca desenvolvido em Python com renderização manual pixel a pixel, implementando os principais algoritmos clássicos de Computação Gráfica do zero — sem uso de primitivas gráficas de bibliotecas externas.

---

## Descrição do Jogo

O jogador controla um barco de pesca com um pescador a bordo. O objetivo é capturar o maior número de peixes possível dentro do tempo limite de **1 minuto e 30 segundos**.

Há dois tipos de peixe:
- **Peixe normal** — vale 10 pontos, se move horizontalmente pelo fundo do oceano
- **Peixe lendário** — vale 100 pontos, oscila com animação senoidal e tem textura de escamas

Ao fim do tempo, a pontuação final é exibida em uma tela de resultados.

---

## Controles

| Tecla | Ação |
|---|---|
| `←` / `→` | Mover o barco |
| `↑` / `↓` | Subir / descer o anzol |
| `Z` (segurar) | Ativar zoom |
| `ESC` | Voltar ao menu |
| `ESPAÇO` / `ENTER` | Confirmar na tela de fim de jogo |

No menu principal, é possível navegar com o mouse ou pressionar `1`, `2`, `3`.

---

## Instalação e Execução

### Requisitos

- Python 3.10 ou superior
- pygame-ce (Community Edition — compatível com Python 3.13+)

### Instalação

```bash
pip install pygame-ce
```

> **Atenção:** use `pygame-ce` e **não** `pygame`. O pygame-ce é a Community Edition com suporte ao Python mais atual (3.12+). Os dois não podem estar instalados ao mesmo tempo — se tiver o pygame instalado, remova antes:
> ```bash
> pip uninstall pygame
> pip install pygame-ce
> ```

### Executar

```bash
python main.py
```

---

## Estrutura do Projeto

```
pescaria-cg/
├── core/
│   ├── canvas.py        # Gerenciamento da superfície e set_pixel
│   ├── rasterizer.py    # Bresenham, Ponto Médio (círculo/elipse), Flood Fill
│   ├── scanline.py      # Scanline, gradiente por vértice, mapeamento de textura
│   ├── transforms.py    # Matrizes homogêneas 3x3 (translação, escala, rotação)
│   ├── clipping.py      # Algoritmo de Cohen-Sutherland
│   └── constants.py     # Modelos geométricos dos peixes e textura procedural
├── game/
│   ├── entities.py      # Entidades: Barco, Pescador, VaraDePesca, PeixeNormal, PeixeLendario
│   └── simulation.py    # Loop de jogo, colisões, HUD, viewport e minimap
├── menu.py              # Tela de abertura com todos os algoritmos de rasterização
├── main.py              # Ponto de entrada, máquina de estados
├── requirements.txt     # Dependências
└── README.md
```

---

## Funcionalidades Implementadas

### a) Set Pixel

Toda renderização parte da função `canvas.set_pixel(x, y, color)`, que escreve diretamente na superfície via `surface.set_at()` do pygame — a única função de biblioteca utilizada para exibição.

### b) Primitivas de Rasterização

Implementadas em `core/rasterizer.py` e utilizadas em `menu.py` na tela de abertura:

- **Reta — Bresenham:** usado nas linhas do HUD, corpo do barco, vara de pesca, anzol e separador da água
- **Circunferência — Ponto Médio:** usado para desenhar o sol na tela de abertura
- **Elipse — Ponto Médio:** usado para desenhar os pés do pescador na tela de abertura

### c) Preenchimento de Regiões

- **Flood Fill iterativo (pilha):** preenche o sol, o casco do barco e os sapatos do pescador na tela de abertura (`menu.py`)
- **Scanline:** preenche todos os polígonos dos peixes durante o jogo (`core/scanline.py`)

### d) Transformações Geométricas

Implementadas em `core/transforms.py` com matrizes homogêneas 3x3:

- **Translação:** movimentação de todos os peixes no mundo
- **Escala:** dimensionamento dos peixes e zoom da câmera (Window-to-Viewport)
- **Rotação:** peixe lendário oscila com `sin(tempo) * 20°` a cada frame
- **Composição:** multiplicação de matrizes para encadear transformações (translação × flip × escala)

### e) Animação 2D

- Peixe lendário oscila verticalmente e rotaciona com função senoidal
- Peixes normais se movem horizontalmente e reaparecem do outro lado da tela
- Zoom da câmera animado com interpolação linear (lerp)
- Direção do barco suavizada por lerp frame a frame

### f) Janela e Viewport

- `get_world_to_screen()` implementa a transformação Window → Viewport com suporte a zoom (translação + escala)
- **Viewport secundária (minimap):** exibida no canto superior direito, centra no anzol e amplifica a região com zoom 1.5×
- Zoom ativado com a tecla `Z`, com transição suavizada

### g) Recorte — Cohen-Sutherland

Implementado em `core/clipping.py`. Utilizado no minimap para validar se cada pixel de origem está dentro dos limites da tela antes de copiá-lo para a viewport secundária, evitando acesso fora dos limites.

### h) Mapeamento de Textura

O peixe lendário é renderizado com mapeamento UV sobre uma textura procedural de escamas (padrão xadrez dourado/marrom gerado em `core/constants.py`). A interpolação de coordenadas UV é feita scanline a scanline em `Scanline.fill_textured_polygon_procedural()`.

### i) Input

- **Teclado:** movimentação do barco, anzol, zoom e navegação de menus
- **Mouse:** clique nas opções do menu principal (com cursor customizado em forma de anzol desenhado com set_pixel)

### j) Gradiente por Vértice (adicional da Scanline)

O fundo do oceano é renderizado com `Scanline.fill_gradient_polygon()`, interpolando a cor de azul médio (`60, 120, 200`) na superfície até azul profundo (`5, 15, 45`) no fundo, com cor definida por vértice.

---

## Tecnologias

- Python 3.10+
- pygame-ce (apenas para janela, eventos e `set_at` / `get_at`)
- Matemática vetorial e álgebra linear implementadas manualmente

---

## Vídeo de Demonstração

> *(inserir link)*
