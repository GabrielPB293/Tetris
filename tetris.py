import random
import os
import time
from colorama import init, Fore, Style

init(autoreset=True)

LARGURA = 10
ALTURA = 20

# Cada peça é representada como uma matriz (lista de listas) de 0 e 1
PECAS = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1],
          [1, 1]],
    "T": [[0, 1, 0],
          [1, 1, 1]],
    "S": [[0, 1, 1],
          [1, 1, 0]],
    "Z": [[1, 1, 0],
          [0, 1, 1]],
    "J": [[1, 0, 0],
          [1, 1, 1]],
    "L": [[0, 0, 1],
          [1, 1, 1]],
}

CORES = {
    "I": Fore.CYAN,
    "O": Fore.YELLOW,
    "T": Fore.MAGENTA,
    "S": Fore.GREEN,
    "Z": Fore.RED,
    "J": Fore.BLUE,
    "L": Fore.WHITE,
}

ARQUIVO_RANKING = "ranking_tetris.txt"

# Variáveis globais do jogo
tabuleiro = []
peca = []
tipo = ""
pos_x = 0
pos_y = 0
pontos = 0
nome = ""


def cria_tabuleiro():
    global tabuleiro
    # o tabuleiro é uma matriz (lista de listas) com ALTURA linhas e LARGURA colunas
    tabuleiro = [[" " for _ in range(LARGURA)] for _ in range(ALTURA)]


def nova_peca():
    global peca, tipo, pos_x, pos_y
    tipo = random.choice(list(PECAS.keys()))
    peca = [linha[:] for linha in PECAS[tipo]]  # copia a matriz da peça sorteada
    pos_x = LARGURA // 2 - len(peca[0]) // 2
    pos_y = 0


def gira_peca(forma):
    # gira a matriz da peça em 90 graus
    return [list(linha) for linha in zip(*forma[::-1])]


def pode_mover(forma, x, y):
    for i in range(len(forma)):
        for j in range(len(forma[i])):
            if forma[i][j] == 1:
                nx = x + j
                ny = y + i
                if nx < 0 or nx >= LARGURA or ny >= ALTURA:
                    return False
                if ny >= 0 and tabuleiro[ny][nx] != " ":
                    return False
    return True


def fixa_peca():
    for i in range(len(peca)):
        for j in range(len(peca[i])):
            if peca[i][j] == 1 and pos_y + i >= 0:
                tabuleiro[pos_y + i][pos_x + j] = tipo


def limpa_linhas():
    global tabuleiro, pontos
    linhas_completas = 0
    nova_matriz = []

    for linha in tabuleiro:
        if " " in linha:
            nova_matriz.append(linha)
        else:
            linhas_completas += 1

    for _ in range(linhas_completas):
        nova_matriz.insert(0, [" " for _ in range(LARGURA)])

    tabuleiro = nova_matriz
    pontos += linhas_completas * 100


def mostra_tabuleiro():
    os.system("cls")

    # copia o tabuleiro e sobrepõe a peça atual, só para exibição
    tela = [linha[:] for linha in tabuleiro]
    for i in range(len(peca)):
        for j in range(len(peca[i])):
            if peca[i][j] == 1:
                y = pos_y + i
                x = pos_x + j
                if 0 <= y < ALTURA and 0 <= x < LARGURA:
                    tela[y][x] = tipo

    print("=" * 30)
    print("      ***** TETRIS *****")
    print("=" * 30)
    print(f"Jogador: {nome}     Pontos: {pontos}")
    print("+" + "--" * LARGURA + "+")
    for linha in tela:
        print("|", end="")
        for c in linha:
            if c == " ":
                print("  ", end="")
            else:
                print(f"{CORES.get(c, '')}[]{Style.RESET_ALL}", end="")
        print("|")
    print("+" + "--" * LARGURA + "+")


def salva_pontuacao():
    with open(ARQUIVO_RANKING, "a") as arq:
        arq.write(f"{nome};{pontos}\n")


def mostra_ranking():
    os.system("cls")
    print("=" * 30)
    print("      RANKING - TETRIS")
    print("=" * 30)

    if not os.path.isfile(ARQUIVO_RANKING):
        print("Ainda não há pontuações registradas.")
    else:
        with open(ARQUIVO_RANKING, "r") as arq:
            linhas = arq.readlines()

        lista = []
        for linha in linhas:
            partes = linha.strip().split(";")
            lista.append((partes[0], int(partes[1])))

        lista.sort(key=lambda item: item[1], reverse=True)

        for posicao in range(len(lista[:10])):
            jogador, pts = lista[posicao]
            print(f"{posicao + 1}º - {jogador:<15} {pts} pontos")

    input("\nPressione Enter para voltar ao menu...")


def jogar():
    global pos_x, pos_y, peca, nome, pontos

    nome = input("Informe seu nome: ")
    pontos = 0
    cria_tabuleiro()
    nova_peca()

    fim = False
    while not fim:
        mostra_tabuleiro()
        comando = input("Comando (a=esquerda d=direita w=girar espaço=queda enter=descer): ").lower()

        if comando == "a" and pode_mover(peca, pos_x - 1, pos_y):
            pos_x -= 1
        elif comando == "d" and pode_mover(peca, pos_x + 1, pos_y):
            pos_x += 1
        elif comando == "w":
            girada = gira_peca(peca)
            if pode_mover(girada, pos_x, pos_y):
                peca = girada
        elif comando == " ":
            while pode_mover(peca, pos_x, pos_y + 1):
                pos_y += 1

        # gravidade: a peça desce 1 linha a cada jogada
        if pode_mover(peca, pos_x, pos_y + 1):
            pos_y += 1
        else:
            fixa_peca()
            limpa_linhas()
            nova_peca()
            if not pode_mover(peca, pos_x, pos_y):
                fim = True  # não coube mais peça: fim de jogo

    mostra_tabuleiro()
    print("\nFim de jogo! O tabuleiro encheu 😵")
    print(f"Pontuação final: {pontos}")
    salva_pontuacao()
    input("Pressione Enter para voltar ao menu...")


def menu():
    while True:
        os.system("cls")
        print("=" * 30)
        print("      ***** TETRIS *****")
        print("=" * 30)
        print("1 - Jogar")
        print("2 - Ver Ranking")
        print("3 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            jogar()
        elif opcao == "2":
            mostra_ranking()
        elif opcao == "3":
            break
        else:
            print("Opção inválida")
            input("Pressione Enter...")


menu()
