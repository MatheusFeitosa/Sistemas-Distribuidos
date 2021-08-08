#O servidor usa um código auxiliar para contar o números de palavras, que esta comentado no arquivo codigo.py, ele envia uma mensagem inicial e sempre espera duas palavras no formato "arquivo palavra", confere quantas tem, se tiver e responde, no exit ele finaliza


import socket
import select
import sys

HOST = '' 
PORT = 5788

entradas = [sys.stdin]
conexoes = {}

def achaPalavra(nome_arquivo, palavra):
	contador = 0
	
	try:
		arquivo = open(nome_arquivo, "r")


		#Percorro por todas palavras do arquivo e se for igual a palavra que procuro somo um ao contador
		for linha in arquivo:
    			palavras = linha.split()
    			for i in palavras:
    				if(i.lower() == palavra.lower()):
    					contador += 1	

		arquivo.close()
		
		return str(contador)
	
	except:
		
		#Se der except é por que não foi encontrado o arquivo
		
		return "Documento nao encontrado"


# O código é igual ao seu
def iniciaServidor():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

	sock.bind((HOST, PORT))

	sock.listen(5) 

	sock.setblocking(False)

	entradas.append(sock)

	return sock

def aceitaConexao(sock):

	clisock, endr = sock.accept()

	conexoes[clisock] = endr 

	return clisock, endr


def atendeRequisicoes(clisock, endr):

	data = clisock.recv(1024) 
	#Como o cliente só consegue enviar 2 possiveis mensagens, ou 2 palavras ou uma palavra só sendo ela "exit", então confiro se ela é "exit, se for eu termino a conexão
	if str(data, encoding = 'utf-8') == "exit": 
		print(str(endr) + '-> encerrou')
		del conexoes[clisock] 
		entradas.remove(clisock) 
		clisock.close() 
		return 
	#Aqui eu separo a mensagem em 2 palavras, pois estou tratando na parte do cliente dele não poder passar mais de 2 palavras nem apenas 1 ou nenhuma.
	retorno = str(data, encoding = 'utf-8').split()
	data = achaPalavra(retorno[0], retorno[1])
	clisock.send(str.encode(data))


def main():
	sock = iniciaServidor()
	print("Pronto para receber conexoes...")
	while True:
		leitura, escrita, excecao = select.select(entradas, [], [])
		for pronto in leitura:
			if pronto == sock: 
				clisock, endr = aceitaConexao(sock)
				print ('Conectado com: ', endr)
				clisock.setblocking(False)
				entradas.append(clisock)
			elif pronto == sys.stdin:
				cmd = input()
				if cmd == 'fim':
					if not conexoes: 
						sock.close()
						sys.exit()
					else: print("ha conexoes ativas")
				elif cmd == 'hist': 
					print(str(conexoes.values()))
			else: 
				atendeRequisicoes(pronto, conexoes[pronto])

main()



