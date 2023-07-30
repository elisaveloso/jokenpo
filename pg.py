import pygame

# Inicialize o pygame
pygame.init()

# Defina as dimensões da tela
largura_tela = 800
altura_tela = 600

# Crie a tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Exemplo de Texto no Pygame")

# Defina as cores (opcional)
branco = (255, 255, 255)
preto = (0, 0, 0)

# Crie um objeto de fonte
fonte = pygame.font.SysFont(None, 48)  # Pode usar a fonte padrão ou escolher uma específica

# Crie um texto
texto = "Olá, Pygame!"

# Renderize o texto em uma superfície
superficie_texto = fonte.render(texto, True, branco)

# Defina a posição do texto na tela (centro neste exemplo)
pos_x = (largura_tela - superficie_texto.get_width()) // 2
pos_y = (altura_tela - superficie_texto.get_height()) // 2

# Defina o loop principal do jogo
jogo_funcionando = True
while jogo_funcionando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_funcionando = False

    # Preencha a tela com a cor de fundo (preto neste exemplo)
    tela.fill(preto)

    # Desenhe o texto na tela
    tela.blit(superficie_texto, (pos_x, pos_y))

    # Atualize a tela
    pygame.display.update()

# Encerre o pygame corretamente quando o loop do jogo terminar
pygame.quit()
