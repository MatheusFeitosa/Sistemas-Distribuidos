#O servidor usa um código auxiliar para contar o números de palavras, que esta comentado no arquivo codigo.py, ele envia uma mensagem inicial e sempre espera duas palavras no formato "arquivo palavra", confere quantas tem, se tiver e responde, no exit ele finaliza

import socket

def achaPalavra(nome_arquivo, palavra):
	contador = 0
	
	try:
		arquivo = open(nome_arquivo, "r")



		for linha in arquivo:
    			palavras = linha.split()
    			for i in palavras:
    				if(i.lower() == palavra.lower()):
    					contador += 1	

		arquivo.close()
		
		return str(contador)
	
	except:
		
		return "Documento nao encontrado"


HOST = 'localhost'

PORTA = 5789

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORTA))

msg = "Envie o nome do arquivo e a palavra que deseja contar"

while(1):
	sock.send(str.encode(msg))
	msg = sock.recv(1024)
	if(str(msg, encoding = 'utf-8') == "exit"):
		break
	retorno = str(msg, encoding = 'utf-8').split()
	
	msg = achaPalavra(retorno[0], retorno[1])

sock.close()


