import socket

# Função para iniciar o cliente
def start_client():
    host = 'localhost'
    port = 8888

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Conectado ao servidor.")

    while True:
        message = client_socket.recv(1024).decode()
        print(message)

        if "Jogador" in message:
            while True:
                move = input("Faça sua jogada (pedra, papel ou tesoura): ")
                client_socket.send(move.encode())
                response = client_socket.recv(1024).decode()
                print(response)

                if "Jogador" not in response:
                    break

            while True:
                continue_game = input("Deseja continuar jogando? (sim/não): ")
                client_socket.send(continue_game.encode())
                response = client_socket.recv(1024).decode()
                print(response)

                if response != 'continuar':
                    client_socket.close()
                    return


# Inicia o cliente
start_client()
