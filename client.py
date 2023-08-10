import socket
from json import loads
from utils import *

def keep_playing():
    while True:
        keep = input("Deseja continuar jogando sim ou nao? ")
        if keep == 'sim':
            return True
        if keep == 'nao':
            return False

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print("Conectado ao servidor")
    print("Aguardando outro jogador ...")
    
    server_msg = loads(client_socket.recv(SERVER_BUFFER).decode("utf-8"))
    player = server_msg['player']
    
    run_game = True
    while run_game:
        move = input("Jogue pedra, papel ou tesoura: ")
        client_socket.send(bytes(client_message(move=move), "utf-8"))
    
    # server_msg = loads(client_socket.recv(SERVER_BUFFER).decode("utf-8"))
    # server_msg = client_socket.recv(1024).decode()
        server_msg = loads(client_socket.recv(SERVER_BUFFER).decode("utf-8"))['winner']
        if server_msg == 'draw':
            print('Empate')
        elif server_msg == player:
            print('Voce venceu')
        else:
            print('Voce perdeu')
        
        move = ''
        if not keep_playing():
            move = 'sair'
            
        client_socket.send(bytes(client_message(move=move), "utf-8"))
        
        if loads(client_socket.recv(SERVER_BUFFER).decode("utf-8"))['status'] != 'run':
            run_game = False
    print("Jogo chegou ao fim")
    report = loads(client_socket.recv(REPORT_BUFFER).decode("utf-8"))
    draw = report['draw']
    if player == 'first':
        vitorias = report['p1']
        derrotas = report['p2']
    else:
        vitorias = report['p2']
        derrotas = report['p1']
    print(f'Numero de partidas jogadas: {vitorias + derrotas + draw}')
    print(f'Vitorias: {vitorias}')
    print(f'Derrotas: {derrotas}')
    print(f'Empates: {draw}')
    
    
    # screen = pygame.display.set_mode((WIDTH, HEIGTH))
    
    # rock_button = Button_Image(220, 500, rock_image, OPTION_HEIGTH, OPTION_WIDTH, screen)
    # paper_button = Button_Image(490, 500, paper_image, OPTION_HEIGTH, OPTION_WIDTH, screen)
    # scissor_button = Button_Image(760, 500, scissor_image, OPTION_HEIGTH, OPTION_WIDTH, screen)
    
    # run_screen = True
    # while run_screen:
        # choosed, move = draw_options(server_msg, screen, rock_button, paper_button, scissor_button)
        
        # if(choosed):
        #     client_socket.send(move.encode())
        
        #     winner = client_socket.recv(1024).decode()
        #     print(winner)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run_screen = False
                
    # pygame.quit()
    client_socket.close()

run_client()