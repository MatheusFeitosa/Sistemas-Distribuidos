#O cliente recebe uma mensagem de introdução, ele responde com nome do arquivo e a palavra que deseja encontrar no formato "arquivo palavra" e recebe a resposta, para finalizar ele fala exit

import socket

HOST = ''

PORTA = 5789

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORTA))

sock.listen(1)

novoSock, endereco = sock.accept()

print("Conectando com: " + str(endereco))

while(1):
	msg = novoSock.recv(1024)
	
	print(str(msg, encoding = 'utf-8'))
	
	msg = input()
	
	

	novoSock.send(str.encode(msg))
	
	if(msg == "exit"):
		break
	
novoSock.close()
sock.close()

