import socket
import threading

# Dicionário de jogadas válidas
valid_moves = ['pedra', 'papel', 'tesoura']

# Dicionário de regras do jogo
game_rules = {
    'pedra': 'tesoura',
    'papel': 'pedra',
    'tesoura': 'papel'
}

# Classe que representa o jogo
class Game:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.moves = {}
        self.wins = {1: 0, 2: 0}
        self.playing = True

    def add_player(self, player_socket):
        if self.player1 is None:
            self.player1 = player_socket
            return 1
        elif self.player2 is None:
            self.player2 = player_socket
            return 2
        else:
            return None

    def receive_move(self, player_num, move):
        self.moves[player_num] = move
        if player_num == 1:
            opponent_num = 2
        else:
            opponent_num = 1

        if opponent_num in self.moves:
            self.check_winner(player_num, opponent_num)

    def check_winner(self, player1_num, player2_num):
        move1 = self.moves[player1_num]
        move2 = self.moves[player2_num]
        result = ''

        if move1 == move2:
            result = 'Empate!'
        elif game_rules[move1] == move2:
            result = f'Jogador {player1_num} venceu!'
            self.wins[player1_num] += 1
        else:
            result = f'Jogador {player2_num} venceu!'
            self.wins[player2_num] += 1

        self.player1.send(result.encode())
        self.player2.send(result.encode())

        self.moves = {}

        self.check_continue()

    def check_continue(self):
        response1 = self.player1.recv(1024).decode().strip().lower()
        response2 = self.player2.recv(1024).decode().strip().lower()

        if response1 == 'não' or response2 == 'não':
            self.playing = False
        else:
            self.player1.send('continuar'.encode())
            self.player2.send('continuar'.encode())

    def send_report(self):
        report = f"Relatório de jogo:\nTempo de jogo: {self.wins[1] + self.wins[2]}\nJogador 1: {self.wins[1]} vitórias\nJogador 2: {self.wins[2]} vitórias"
        self.player1.send(report.encode())
        self.player2.send(report.encode())

        self.player1.close()
        self.player2.close()


# Função para lidar com cada cliente individualmente
def handle_client(client_socket, game):
    player_num = game.add_player(client_socket)

    if player_num is None:
        client_socket.send("Jogo em andamento. Tente novamente mais tarde.".encode())
        client_socket.close()
    else:
        client_socket.send(f"Você é o Jogador {player_num}".encode())

        while game.playing:
            move = client_socket.recv(1024).decode().strip().lower()
            game.receive_move(player_num, move)

        game.send_report()


# Função principal do servidor
def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = 'localhost'
    port = 8888

    server_socket.bind((host, port))
    server_socket.listen(2)

    print(f"Servidor ouvindo em {host}:{port}")

    game = Game()

    while True:
        client_socket, address = server_socket.accept()
        print(f"Nova conexão de {address[0]}:{address[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, game))
        client_thread.start()


# Executa o servidor
run_server()
