import socket
from json import loads
from threading import Thread
from utils import *

# vetor com os cliente que nao entraram em salas ainda
clients = []

# vetor com as salas que foram criadas
rooms = []

# funcao que retorna o vencedor
def check_winner(move1, move2):
    if move1 == move2:
        return 'draw'
    
    if move1 == 'pedra' and move2 == 'tesoura':
        return 'first'

    if move1 == 'papel' and move2 == 'pedra':
        return 'first'

    if move1 == 'tesoura' and move2 == 'papel':
        return 'first'

    return 'second'

def game_start(player1, player2):
    # avisa que o jogo comecou
    player1.send(bytes(server_message("first", "run"), "utf-8"))
    player2.send(bytes(server_message("second", "run"), "utf-8"))
    report = Report()
    # contabiliza o tempo do inicio do jogo
    report.time_start()
    
    keep_playing = True
    while keep_playing:
        #recebe as jogadas do servidor
        move1 = loads(player1.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        move2 = loads(player2.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        
        # checa o ganhador e contabiliza no relatorio
        winner = check_winner(move1, move2)
        report.win_count(winner)
        
        # envia o ganhador para os jogadores
        player1.send(bytes(server_message(player="first", status="run", winner=winner), "utf-8"))
        player2.send(bytes(server_message(player="second", status="run", winner=winner), "utf-8"))
        
        # recebe mensagem se o jogador quer continuar jogando
        keep1 = loads(player1.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        keep2 = loads(player2.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        
        # define se o jogo vai finalizar
        status = 'run'
        if keep1 == 'sair' or keep2 == 'sair':
            keep_playing = False
            status = 'exit'
            
        # envia mensagem se o jogo vai acabar ou continuar
        player1.send(bytes(server_message(player="first", status=status, winner=winner), "utf-8"))
        player2.send(bytes(server_message(player="second", status=status, winner=winner), "utf-8"))
    
    # contabiliza o fim de jogo
    report.time_end()
    # envia o relatorio para os jogadores
    player1.send(bytes(report_message(p1=report.get_p1(), p2=report.get_p2(), draw=report.get_draw(), time=report.get_end() - report.get_start()), "utf-8"))
    player2.send(bytes(report_message(p1=report.get_p1(), p2=report.get_p2(), draw=report.get_draw(), time=report.get_end() - report.get_start()), "utf-8"))
    
    # finaliza o socket do cliente
    for room in rooms:
        if player1 in room and player2 in room:
            p1 = room.pop(0)
            p2 = room.pop(0)
            p1.close()
            p2.close()
            break

def create_room():
    # enquato o vetor tiver dois ou mais clientes cria uma sala
    while len(clients) >= 2:
        # retira os clientes do vetor
        player1 = clients.pop(0)
        player2 = clients.pop(0)
        
        # cria uma sala(thread) onde os dois jogadores iram jogar o jogo
        thread_room = Thread(target=game_start, args=(player1, player2,))
        # cria uma sala e adiciona no vetor de salas
        room = [player1, player2, thread_room]
        thread_room.start()
        
        rooms.append(room)
    
#funcao que roda o servidor
def run_server():
    # define os parametros do socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # define o ip e a porta do servidor
    server_socket.bind((IP, PORT))
    # faz o servidor ouvir o client
    server_socket.listen()
    print(f"Server online on {IP}:{PORT}")
    
    while True:
        # aceita conexao do client
        client_socket, client_adress = server_socket.accept()
        print(f'Novo cliente de {client_adress}')
        # adiciona o cliente no vetor de cliente nao alocados em salas
        clients.append(client_socket)
        # cria uma sala
        create_room()

# comeca a rodar o servidor
run_server()