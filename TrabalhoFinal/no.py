#imports
import socket
import select
import sys
import subprocess
import os
import time

hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)

entradas = []
conexoes = {}
estado = []
#Finger table
inicio = []
sucessor = {}
ate = {}
porta = {}
meuid = []

tabelaHash = {}
ocupado = []
conteudo = []

def iniciaServidor(HOST, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((HOST, int(PORT)))

    sock.listen(50)

    sock.setblocking(False)
    
    entradas.append(sock)

    return sock

def aceitaConexao(sock):

    clisock, endr = sock.accept()

    conexoes[clisock] = endr

    return clisock, endr


def atendeRequisicoes(clisock, endr):

    data = clisock.recv(1024)
    dataD = str(data, encoding = 'utf-8')        
    if (dataD == "oi"):
        clisock.send(str.encode(sys.argv[1]))

    if (dataD == "Ativar"):
        estado[0] = 1
        clisock.send(str.encode(str(estado[0])))
    
    if (dataD == "Desativar"):
        estado[0] = 0
        clisock.send(str.encode(str(estado[0])))

    if (dataD == "Atualizar"):
        clisock.send(str.encode('Estou ativo'))
        time.sleep(1)
        msg = clisock.recv(1024)
        no = str(msg, encoding = 'utf-8')
        inicio.append(int(no))
        clisock.send(str.encode(no))
        time.sleep(1)
        msg = clisock.recv(1024)
        suc = str(msg, encoding = 'utf-8')
        sucessor[int(no)] = int(suc)
        clisock.send(str.encode(suc))
        time.sleep(1)
        msg = clisock.recv(1024)
        at = str(msg, encoding = 'utf-8')
        ate[int(no)] = int(at)
        clisock.send(str.encode(at))
        time.sleep(1)
        msg = clisock.recv(1024)
        port = str(msg, encoding = 'utf-8')
        porta[int(no)] = int(port)
        clisock.send(str.encode(port))

    if (dataD == "Buscar"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            mensagem = str(msg, encoding = 'utf-8')
            chavehash = hash(mensagem)
            aux = 1
            try:
                no = tabelaHash[chavehash]
            except:
                clisock.send(str.encode('Mensagem não encontrada'))
                aux = 0
            if(aux == 1):
               saida =  buscarinformacao(no)
               clisock.send(str.encode(str(saida)))

        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()

    if (dataD == "Remover"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            mensagem = str(msg, encoding = 'utf-8')
            clisock.send(str.encode(str(hash(mensagem))))
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()


    if (dataD == "Adicionar"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            mensagem = str(msg, encoding = 'utf-8')
            partes = mensagem.split(' ', 1)
            funcionou = acharDisponivel(partes[1], meuid[0])
            if (funcionou != -1):
                atualizarTabelaHash(hash(partes[0]), funcionou, meuid[0])
                clisock.send(str.encode('Salvo com sucesso'))
            else:
                clisock.send(str.encode('Ocorreu um erro'))
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()
   

    if (dataD == "BuscarInformacao"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            no = str(msg, encoding = 'utf-8')
            saida = buscarinformacao(no)
            clisock.send(str.encode(str(saida)))
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()



    if (dataD == "AdicionarHash"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            comeco = str(msg, encoding = 'utf-8')
            clisock.send(str.encode('Continue'))
            time.sleep(1)
            msg = clisock.recv(1024)
            no = str(msg, encoding = 'utf-8')
            clisock.send(str.encode('Continue'))
            time.sleep(1)
            msg = clisock.recv(1024)
            hashchave = str(msg, encoding = 'utf-8')
            clisock.send(str.encode('Obrigado'))

            atualizarTabelaHash( hashchave, no,comeco)
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()


    if (dataD == "AdicionarNo"):
        if(estado[0] == 0):
            clisock.send(str.encode('Estou inativo'))
        else:
            clisock.send(str.encode('Estou ativo'))
            time.sleep(1)
            msg = clisock.recv(1024)
            comeco = str(msg, encoding = 'utf-8')
            if(ocupado[0] == 0):
                clisock.send(str.encode('Continue'))
            else:
                if(int(comeco)==int(inicio[0])):
                    clisock.send(str.encode('Falhou'))
                else:
                    clisock.send(str.encode('Continue'))
            time.sleep(1)
            msg = clisock.recv(1024)
            valor = str(msg, encoding = 'utf-8')
            if(ocupado[0] == 0):
                ocupado[0] = 1
                conteudo.append(valor)
                clisock.send(str.encode('Funcionou'))
            else:
                resultado = acharDisponivel(valor, comeco)
                if(resultado == 1):
                    clisock.send(str.encode(str(meuid[0])))
                else:
                    clisock.send(str.encode('Falhou'))
        del conexoes[clisock]
        entradas.remove(clisock)
        clisock.close()


    if dataD == "exit":
        return 1
    return 0

def acharDisponivel(valor, comeco):
    sockVizinho = socket.socket()
    sockVizinho.connect(('localhost', int(porta[int(inicio[0])])))
    sockVizinho.send(str.encode('AdicionarNo'))
    time.sleep(1)
    msg = sockVizinho.recv(1024)
    status = str(msg, encoding = 'utf-8')
    if (status == 'Estou ativo'):
        sockVizinho.send(str.encode(str(comeco)))
        time.sleep(1)
        msg = clisock.recv(1024)
        feedback = str(msg, encoding = 'utf-8')
        if(feedback == 'Continue'):
            sockVizinho.send(str.encode(str(valor)))
            time.sleep(1)
            msg = clisock.recv(1024)
            resultado = str(msg, encoding = 'utf-8')
            if(resultado != 'Falhou'):
                sockVizinho.close()
                return resultado
            else:
                sockVizinho.close()
                return -1
        else:
            sockVizinho.close()
            return -1
    else:
        sockVizinho.close()
        return -1

def atualizarTabelaHash( hashchave, no,comeco):
    tabelaHash[int(no)] = str(hashchave)
    sockVizinho = socket.socket()
    sockVizinho.connect(('localhost', int(porta[int(inicio[0])])))
    sockVizinho.send(str.encode('AdicionarHash'))
    time.sleep(1)
    msg = clisock.recv(1024)
    if (status == 'Estou ativo'):
        sockVizinho.send(str.encode(str(comeco)))
        time.sleep(1)
        msg = clisock.recv(1024)
        feedback = str(msg, encoding = 'utf-8')
        sockVizinho.send(str.encode(str(no)))
        time.sleep(1)
        msg = clisock.recv(1024)
        feedback2 = str(msg, encoding = 'utf-8')
        sockVizinho.send(str.encode(str(hashchave)))
        time.sleep(1)
        msg = clisock.recv(1024)
        feedback3 = str(msg, encoding = 'utf-8')
        sockVizinho.close()


def buscarinformacao(no):
    ultimo = 0
    if(int(meuid[0]) == int(no):
        return conteudo[0]
    for i in inicio:
        if(int(sucessor(int(i)))==int(no)):
            sockVizinho = socket.socket()
            sockVizinho.connect(('localhost', int(porta[int(i)])))
            sockVizinho.send(str.encode('BuscarInformacao'))
            time.sleep(1)
            msg = clisock.recv(1024)
            status = str(msg, encoding = 'utf-8')
            if (status == 'Estou ativo'):
                sockVizinho.send(str.encode(str(no)))
                time.sleep(1)
                msg = clisock.recv(1024)
                saida = str(msg, encoding = 'utf-8')
                sockVizinho.close()
                return saida
            else:
                return "Error"
        else:
            if((int(no) >= int(i) and no<=ate[int(i)]) or (int(i) >= ate[int(i)] and (int(no) >= int(i) or int(no <= ate[int(i)])))):
                sockVizinho = socket.socket()
                sockVizinho.connect(('localhost', int(porta[int(i)])))
                sockVizinho.send(str.encode('BuscarInformacao'))
                time.sleep(1)
                msg = clisock.recv(1024)
                status = str(msg, encoding = 'utf-8')
                if (status == 'Estou ativo'):
                    sockVizinho.send(str.encode(str(no)))
                    time.sleep(1)
                    msg = clisock.recv(1024)
                    saida = str(msg, encoding = 'utf-8')
                    sockVizinho.close()
                    return saida
                return "Error"
        ultimo = int(i)
    sockVizinho = socket.socket()
    sockVizinho.connect(('localhost', int(porta[int(i)])))
    sockVizinho.send(str.encode('BuscarInformacao'))
    time.sleep(1)
    msg = clisock.recv(1024)
    status = str(msg, encoding = 'utf-8')
        if (status == 'Estou ativo'):
            sockVizinho.send(str.encode(str(no)))
            time.sleep(1)
            msg = clisock.recv(1024)
            saida = str(msg, encoding = 'utf-8')
            sockVizinho.close()
            return saida
        else:
            return "Error"



def main():
    meuid.append(int(sys.argv[1]))
    PORT = int(sys.argv[2])
    tamanho = int(sys.argv[3])
    estado.append(0)
    sock = iniciaServidor('',PORT)
    while True:
        leitura, escrita, excecao = select.select(entradas, [], [])
        for pronto in leitura:
            if(pronto == sock):
                clisock, endr = aceitaConexao(sock)
                clisock.setblocking(False)
                entradas.append(clisock)
            else:
                saida = atendeRequisicoes(pronto, conexoes[pronto])
                if(saida == 1):
                    sock.close()
                    sys.exit()

main()
