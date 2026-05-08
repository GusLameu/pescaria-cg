
# Projeto de Computação Gráfica — Simulação 2D com Rasterização Manual - Pescaria CG

## Descrição Geral

Este projeto consiste em uma simulação gráfica 2D desenvolvida em Python utilizando a biblioteca PyGame, com foco na implementação manual dos principais algoritmos fundamentais de Computação Gráfica.

A aplicação renderiza uma cena interativa contendo um peixe modelado por polígonos e preenchido com textura procedural, utilizando algoritmos implementados do zero sem depender das primitivas gráficas prontas do PyGame.

O objetivo principal do projeto é demonstrar o funcionamento interno de técnicas clássicas de rasterização, preenchimento, transformações geométricas, clipping e mapeamento de textura.

---

# Funcionalidades Implementadas

## 1. Set Pixel

O projeto possui uma implementação própria da operação de escrita de pixels através da função:

```python
set_pixel(x, y, color)
```

Essa função é responsável por desenhar todos os elementos gráficos da aplicação.

Características:

* Controle manual de pixels
* Verificação de limites da tela
* Base para todos os algoritmos gráficos

---

# 2. Rasterização de Primitivas

## 2.1 Rasterização de Linhas

Foi implementado o algoritmo de Bresenham para desenho eficiente de retas.

Características:

* Uso apenas de aritmética inteira
* Alta eficiência
* Renderização pixel a pixel

---

## 2.2 Rasterização de Circunferências

Foi implementado o algoritmo do Ponto Médio para circunferências.

Características:

* Uso de simetria de 8 pontos
* Eficiência computacional
* Renderização suave

---

## 2.3 Rasterização de Elipses

Foi implementado o algoritmo do Ponto Médio para elipses.

Características:

* Divisão em duas regiões
* Simetria de 4 pontos
* Renderização precisa

---

# 3. Preenchimento de Regiões

## 3.1 Flood Fill

Foi implementado o algoritmo Flood Fill iterativo utilizando pilha.

Características:

* Conectividade-4
* Preenchimento recursivo iterativo
* Evita estouro de pilha da recursão tradicional

---

## 3.2 Scanline

Foi implementado o algoritmo Scanline para preenchimento de polígonos.

Características:

* Cálculo de interseções
* Preenchimento horizontal
* Renderização eficiente

---

# 4. Transformações Geométricas

O projeto utiliza matrizes homogêneas 3x3 para realizar transformações geométricas.

Transformações implementadas:

## 4.1 Translação

Movimentação de objetos no plano cartesiano.

---

## 4.2 Escala

Redimensionamento de objetos.

---

## 4.3 Rotação

Rotação de objetos utilizando seno e cosseno.

---

## 4.4 Multiplicação de Matrizes

Composição de transformações geométricas.

---

# 5. Animação 2D

A aplicação possui animação contínua em tempo real através do loop principal do PyGame.

Características:

* Atualização frame a frame
* Movimentação de objetos
* Aplicação dinâmica de transformações

---

# 6. Janela e Viewport

O sistema utiliza uma área de visualização para exibição dos objetos gráficos.

Características:

* Controle da área visível
* Organização espacial da cena
* Integração com clipping

---

# 7. Clipping — Cohen-Sutherland

Foi implementado o algoritmo de recorte de linhas de Cohen-Sutherland.

Características:

* Códigos de região binários
* Aceitação trivial
* Rejeição trivial
* Cálculo de interseções

O algoritmo garante que apenas as partes visíveis das linhas sejam renderizadas na tela.

---

# 8. Mapeamento de Textura

O peixe é preenchido utilizando mapeamento de textura procedural.

Características:

* Coordenadas UV
* Interpolação horizontal e vertical
* Textura procedural gerada manualmente
* Aplicação em polígonos

A textura utilizada simula escamas através de um padrão xadrez.

---

# 9. Input do Usuário

O projeto possui interação através de teclado e/ou mouse.

Características:

* Navegação em menus
* Controle da aplicação
* Interação em tempo real

---

# 10. Menus e Interface

O sistema possui menu gráfico interativo desenvolvido em PyGame.

Características:

* Navegação por teclado
* Interface visual personalizada
* Interações gráficas adicionais

---

# Estrutura do Projeto

## Arquivos Principais

### `canvas.py`

Responsável pela manipulação direta de pixels.

---

### `rasterizer.py`

Implementa os algoritmos de rasterização:

* Linha
* Circunferência
* Elipse
* Flood Fill

---

### `scanline.py`

Implementa:

* Scanline
* Gradiente
* Mapeamento de textura

---

### `transforms.py`

Implementa transformações geométricas utilizando matrizes.

---

### `clipping.py`

Implementa o algoritmo de Cohen-Sutherland.

---

### `constants.py`

Armazena:

* Modelos geométricos
* Texturas procedurais
* Constantes visuais

---

# Tecnologias Utilizadas

* Python
* PyGame
* Matemática vetorial
* Álgebra linear
* Rasterização manual

---

# Objetivos Acadêmicos

O projeto foi desenvolvido com o objetivo de aplicar na prática os principais conceitos da disciplina de Computação Gráfica.

Entre os conceitos abordados estão:

* Rasterização
* Transformações geométricas
* Clipping
* Preenchimento de polígonos
* Mapeamento de textura
* Manipulação de pixels
* Estruturas matemáticas para gráficos 2D

---

# Resultado Final

A aplicação demonstra de forma prática como motores gráficos 2D funcionam internamente, implementando manualmente algoritmos clássicos utilizados em computação gráfica.

O projeto combina:

* fundamentos matemáticos
* manipulação direta de pixels
* algoritmos clássicos
* renderização procedural
* interação em tempo real

resultando em uma simulação gráfica completa desenvolvida do zero.
