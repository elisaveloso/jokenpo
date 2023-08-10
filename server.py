import socket
from json import loads
from threading import Thread
from utils import *

clients = []

rooms = []

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
    
    keep_playing = True
    while keep_playing:
        move1 = loads(player1.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        move2 = loads(player2.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        
        winner = check_winner(move1, move2)
        report.win_count(winner)
        
        player1.send(bytes(server_message(player="first", status="run", winner=winner), "utf-8"))
        player2.send(bytes(server_message(player="second", status="run", winner=winner), "utf-8"))
        
        keep1 = loads(player1.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        keep2 = loads(player2.recv(CLIENT_BUFFER).decode("utf-8"))['move']
        
        status = 'run'
        if keep1 == 'sair' or keep2 == 'sair':
            keep_playing = False
            status = 'exit'
            
        player1.send(bytes(server_message(player="first", status=status, winner=winner), "utf-8"))
        player2.send(bytes(server_message(player="second", status=status, winner=winner), "utf-8"))
    
    player1.send(bytes(report_message(p1=report.get_p1(), p2=report.get_p2(), draw=report.get_draw()), "utf-8"))
    player2.send(bytes(report_message(p1=report.get_p1(), p2=report.get_p2(), draw=report.get_draw()), "utf-8"))
    print("Jogo chegou ao fim") 

def create_room():
    while len(clients) >= 2:
        player1 = clients.pop(0)
        player2 = clients.pop(0)
        
        thread_room = Thread(target=game_start, args=(player1, player2,))
        room = [player1, player2, thread_room]
        thread_room.start()
        
        rooms.append(room)

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Server online on {IP}:{PORT}")
    
    while True:
        client_socket, client_adress = server_socket.accept()
        print(f'Novo cliente de {client_adress}')
        clients.append(client_socket)
        create_room()

run_server()