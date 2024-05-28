import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Cobrinha")

# Cores RGB
preto = (0, 0, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)

# Relógio do jogo
relogio = pygame.time.Clock()

# Carregar efeitos sonoros
comida_sfx = pygame.mixer.Sound("C://Users//sakur//Downloads//Eat-munch_-Sound-effect.wav")
perdeu_sfx = pygame.mixer.Sound("C://Users//sakur//Downloads//Lose-sound-effects.wav")

# Parâmetros da cobrinha
tamanho_quadrado = 20
velocidade_jogo = 15

# Pontuação do jogador
pontos = 0
fonte_pontos = pygame.font.SysFont(None, 30)


# Função para gerar comida
def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(
        tamanho_quadrado)
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y


# Função para desenhar a cobra na tela
def desenhar_cobra(cobra_lista):
    for pixel in cobra_lista:
        pygame.draw.rect(tela, verde, [pixel[0], pixel[1], tamanho_quadrado, tamanho_quadrado])


# Função para exibir mensagem na tela
def mensagem(texto, cor, tamanho, pos_x, pos_y):
    fonte = pygame.font.SysFont(None, tamanho)
    texto_tela = fonte.render(texto, True, cor)
    tela.blit(texto_tela, [pos_x, pos_y])


# Função principal para rodar o jogo
def rodar_jogo():
    global pontos
    fim_jogo = False
    jogo_encerrado = False

    cobra_x, cobra_y = largura / 2, altura / 2
    cobra_lista = [[cobra_x, cobra_y]]
    comprimento_cobra = 1
    velocidade_x, velocidade_y = 0, 0
    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        while jogo_encerrado:
            tela.fill(preto)
            mensagem("Você perdeu! Pontuação: " + str(pontos) + ". Pressione R para jogar novamente ou Q para sair.",
                     vermelho, 25, largura / 6, altura / 3)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        fim_jogo = True
                        jogo_encerrado = False
                    elif evento.key == pygame.K_r:
                        pontos = 0
                        rodar_jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    velocidade_x = 0
                    velocidade_y = -tamanho_quadrado
                elif evento.key == pygame.K_DOWN:
                    velocidade_x = 0
                    velocidade_y = tamanho_quadrado
                elif evento.key == pygame.K_LEFT:
                    velocidade_x = -tamanho_quadrado
                    velocidade_y = 0
                elif evento.key == pygame.K_RIGHT:
                    velocidade_x = tamanho_quadrado
                    velocidade_y = 0

        if cobra_x >= largura or cobra_x < 0 or cobra_y >= altura or cobra_y < 0:
            perdeu_sfx.play()  # Toca o som de perda
            jogo_encerrado = True

        cobra_x += velocidade_x
        cobra_y += velocidade_y

        tela.fill(preto)
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_quadrado, tamanho_quadrado])

        cobra_cabeca = [cobra_x, cobra_y]
        cobra_lista.append(cobra_cabeca)

        if len(cobra_lista) > comprimento_cobra:
            del cobra_lista[0]

        for segmento in cobra_lista[:-1]:
            if segmento == cobra_cabeca:
                jogo_encerrado = True
                perdeu_sfx.play()  # Toca o som de perda

        desenhar_cobra(cobra_lista)

        # Exibir pontos do jogador
        mensagem("Pontos: " + str(pontos), verde, 24, 10, 10)

        pygame.display.update()

        if cobra_x == comida_x and cobra_y == comida_y:
            comida_x, comida_y = gerar_comida()
            comida_sfx.play()  # Toca o som de comer
            pontos += 1
            comprimento_cobra += 1

        relogio.tick(velocidade_jogo)

    pygame.quit()


rodar_jogo()
