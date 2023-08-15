import socket
from json import loads
from utils import *

# funcao que checa se o player quer continuar jogando
def keep_playing():
    while True:
        keep = input("Deseja continuar jogando sim ou nao? ")
        if keep == 'sim':
            return True
        if keep == 'nao':
            return False
        print('ERRO: entrada invalida')

# funcao que roda o cliente
def run_client():
    # define os parametros do socket 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # conecta o cliente no servidor
    client_socket.connect((IP, PORT))
    print("Conectado ao servidor")
    print("Aguardando outro jogador ...")
    
    # recebe a mensagem que o jogo comecou
    server_msg = loads(client_socket.recv(SERVER_BUFFER).decode("utf-8"))
    # recebe a info se e o player 1 ou o player 2
    player = server_msg['player']
    
    run_game = True
    while run_game:
        #recebe o movimento do jogador e envia pro servidor
        move = input("Jogue pedra, papel ou tesoura: ")
        # valida movimento
        while move not in ['pedra', 'papel', 'tesoura']:
            print('ERRO: entrada invalida')
            move = input("Jogue pedra, papel ou tesoura: ")
        client_socket.send(bytes(client_message(move=move), "utf-8"))
    
        # recebe o vencedor do servidor e depois avisa o jogador quem ganhou
        server_msg = loads(client_socket.recv(SERVER_BUFFER).decode("utf-8"))['winner']
        if server_msg == 'draw':
            print('Empate')
        elif server_msg == player:
            print('Voce venceu')
        else:
            print('Voce perdeu')
        
        # checa se o jogador quer continuar jogando e envia pro servidor
        move = ''
        if not keep_playing():
            move = 'sair'
        client_socket.send(bytes(client_message(move=move), "utf-8"))
        
        # rece mensagem do servidor se continua o jogo ou para
        if loads(client_socket.recv(SERVER_BUFFER).decode("utf-8"))['status'] != 'run':
            run_game = False
    print("Jogo chegou ao fim")
    # recebe relatorio do servidor e printa
    report = loads(client_socket.recv(REPORT_BUFFER).decode("utf-8"))
    draw = report['draw']
    time = report['time']
    if player == 'first':
        vitorias = report['p1']
        derrotas = report['p2']
    else:
        vitorias = report['p2']
        derrotas = report['p1']
    print(f'Tempo de jogo: {time:.2f}(segundos)')
    print(f'Numero de partidas jogadas: {vitorias + derrotas + draw}')
    print(f'Vitorias: {vitorias}')
    print(f'Derrotas: {derrotas}')
    print(f'Empates: {draw}')
    
    # fecha o socket
    client_socket.close()

# roda o cliente
run_client()