import socket
from utilsGame import *
import sys

rock = Button_Image(220, 500, rock_image, OPTION_HEIGTH, OPTION_WIDTH)
paper = Button_Image(490, 500, paper_image, OPTION_HEIGTH, OPTION_WIDTH)
scissor = Button_Image(760, 500, scissor_image, OPTION_HEIGTH, OPTION_WIDTH)

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Internet connection and TCP socket
    client_socket.connect((IP, PORT)) # Connect to host
    
    message = client_socket.recv(1024).decode() # Receive a massage from host
    print(message)
    
    run = True
    while run:
        if message != 'run':
            txt = font.render("Aguarde o outro jogador: ", False, WHITE)
            screen.blit(txt, (540, 50))
        else:
            if rock.draw():
                print("pedra")
                client_socket.send("pedra".encode())
            if paper.draw():
                print("papel")
                client_socket.send("papel".encode())
            if scissor.draw():
                print("tesoura")
                client_socket.send("tesoura".encode())
        
        pygame.display.flip() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    
    pygame.quit()
    
    # run = client_socket.recv(1024).decode()

    # running = True
    # while running == True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.quit:
    #             running = False
    
    # running_game = True
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             sys.exit(0)
    #     pygame.display.update()
    # print("saiu")
    
    
    
    # while run == 'run':
    #     move = input('Jogue pedra, papel, tesoura: ').strip().lower()
    #     client_socket.send(move.encode())
        
    #     message = client_socket.recv(1024).decode()
    #     print("O outro jogador jogou: ", message)
        
    #     result = client_socket.recv(1024).decode()
    #     print(result,)
        
    #     stay = input('Deseja continuar sim ou nao: ').strip().lower()
    #     client_socket.send(stay.encode())
    #     if stay == 'nao':
    #         break
        
    client_socket.close()
    
if __name__ == "__main__":
    run_client()