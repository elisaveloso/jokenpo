import socket
from threading import Thread
from utils import *

clients = []

rooms = []
    
def check_winner(move1, move2):
    if move1 == move2:
        return "Empate"
    
    if move1 == "pedra" and move2 == "tesoura":
        return "Player 1 ganhou"
    
    if move1 == "papel" and move2 == "pedra":
        return "Player 1 ganhou"
    
    if move1 == "tesoura" and move2 == "papel":
        return "Player 1 ganhou"
    
    return "Player 2 ganhou"
    
def game_start(player1, player2):
    player1.send('run'.encode())
    player2.send('run'.encode())
    while True:
        move1 = player1.recv(1024).decode()
        move2 = player2.recv(1024).decode()     
        
        print(move1)
        print(move2)
        
        # player1.send(move2.encode())
        # player2.send(move1.encode())
        
        # result = check_winner(move1, move2)
        # player1.send(result.encode())
        # player2.send(result.encode())
        
        # stay1 = player1.recv(1024).decode()
        # stay2 = player2.recv(1024).decode()
        
        # if stay1 == 'nao' or stay2 == 'nao':
        #     break
    
    
def handle_clients():
    if len(clients) >= 2:
        player1 = clients.pop(0)
        player2 = clients.pop(0)
        
        room = Thread(target=game_start, args=(player1, player2,))
        room.start()
        
        rooms.append(room)
    
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet connection and TCP socket
    server_socket.bind((IP, PORT)) # Bind to local host
    server_socket.listen() # Wait for connection...
    print(f"Server online on {IP}:{PORT}")
    
    while True:
        client_socket, client_adress = server_socket.accept() # Aceppt client connection
        print(f'Novo cliente de {client_adress}')  
        client_socket.send("Conectado ao servidor, aguardando outro player ...".encode()) # inform the client the connection
        clients.append(client_socket)
        handle_clients()


if __name__ == "__main__":
    run_server()