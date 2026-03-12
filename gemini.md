# Jogo de Botão com Visão Computacional

Este projeto é uma implementação de um jogo de futebol de botão inspirado no estilo do jogo mobile *Soccer Stars*, mas controlado inteiramente por gestos capturados pela câmera do computador.

## Objetivo
Criar uma experiência imersiva e retro onde o jogador utiliza movimentos das mãos para selecionar seus "botões" (jogadores) e dispará-los contra a bola.

## Controles
- **Seleção**: Posicione a ponta do dedo indicador sobre o jogador.
- **Mira e Força**: Faça um gesto de "pinça" (unir polegar e indicador) próximo ao jogador selecionado. Estique a mão (afaste o ponto da pinça do ponto inicial) para aumentar a força e definir a direção, similar ao movimento de puxar um elástico.

## Tecnologias
- **Python 3**: Linguagem base.
- **Pygame**: Motor gráfico e de física simples.
- **MediaPipe**: Biblioteca de visão computacional para rastreamento de mãos em tempo real.
- **OpenCV**: Captura e processamento de imagem da câmera.

## Estrutura Inicial
1. Campo retrô minimalista.
2. 1 Jogador (Botão).
3. 1 Bola.
4. Física de colisão e atrito.
