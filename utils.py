from json import dumps
import time

# classe que representa o relatorio do jogo
class Report():
    def __init__(self):
        self.p1 = 0
        self.p2 = 0
        self.draw = 0
        self.start = 0.0
        self.end = 0.0
        
    def win_count(self, winner):
        if winner == 'first':
            self.p1 = self.p1 + 1
        elif winner == 'second':
            self.p2 = self.p2 + 1
        elif winner == 'draw':
            self.draw = self.draw + 1
            
    def time_start(self):
        self.start = time.time()
        
    def time_end(self):
        self.end = time.time()
    
    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2
    
    def get_draw(self):
        return self.draw
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end

# IP e Porta do servidor
IP = 'localhost'
PORT = 8888

# tamanho das mensagens enviadas entre servidor e cliente
SERVER_BUFFER = 60
CLIENT_BUFFER = 20
REPORT_BUFFER = 60

# funcoes que criam um json para trocar mensagem
def server_message(player='first', status='wait', winner=''):
    return dumps({
        'player': player,
        'status': status,
        'winner': winner,
    })
    
def client_message(move=''):
    return dumps({
        'move': move,
    })
    
def report_message(p1 = 0, p2 = 0, draw = 0, time = 0.0):
    return dumps({
        'p1': p1,
        'p2': p2,
        'draw': draw,
        'time': time,
    })
    
if __name__ == '__main__':
    print("Server message size: ", len(bytes(server_message(player='second', status='wait'), "utf-8")))
    print("Client message size: ", len(bytes(client_message(move='scissor'), "utf-8")))
    print("Report message size: ", len(bytes(report_message(p1=0, p2=0, draw=0, time=0.0), "utf-8")))