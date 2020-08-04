import socket
import threading
import sys


class Servidor:
    # Criamos um atributo que representa a conexão socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Criando uma lista para guardar as conexões abertas
    conexoes = []
    # Construtor
    def __init__(self):
        # listen em todas as interfaces de rede 8080
        self.sock.bind(('0.0.0.0',8080))
        # E a aceitar conexões
        self.sock.listen(1)
    # função que vai rodar para sempre em thread
    def handler( self, conexao, endereco):
        while True:
            dados = conexao.recv(1024)
            # para cada uma das conexões ativas vamos enviar a mensagem guardada na varivavel de dados
            for conexao in self.conexoes:
                conexao.send(dados)
            #caso nao receba dados nenhum ela remove da lista e fecha conexao
            if not dados:
                print("{}:{} se desconectou".format(endereco[0],endereco[1]))
                self.conexoes.remove(conexao)
                conexao.close()
                break
            
    def run(self):
        while True:
            # aceita conexao e desestrutura a conexao e endereco
            conexao, endereco = self.sock.accept()
            # Cria thread para o metodo Handler
            threadConexao = threading.Thread(target=self.handler, args=(conexao, endereco))
            # Fala que a thread é um daemon
            threadConexao.daemon = True
            # A thread será executada 
            threadConexao.start()
            self.conexoes.append(conexao)
            print("{}:{} se conectou!".format(endereco[0], endereco[1]))
            
class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __init__(self, enderecoServidor):
        # quando o cliente for inicializado vamos estabelecer conexao com o servidor
        self.sock.connect((enderecoServidor, 8080))
        # criamos uma thread para permitir ficar manddando mensagem para o servidor
        threadInput = threading.Thread(target=self.sendMsg)
        # Daemon é quand estamos dizendo que é um processo em background
        threadInput.daemon = True
        threadInput.start()
        while True:
            dados = self.sock.recv(1024)
            print("{}".format(dados))
    
    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""),"utf-8"))


# Estamops verificando se ele recebeu algum argumento de IP e ocupa posição 1
# Caso seja receba ele irá se conectar ao servidor,  caso contrario e ele se conectará 
if len(sys.argv)> 1 :
    cliente = Client(sys.argv[1])
else:
    server = Servidor()
    server.run()

