#O cliente recebe uma mensagem de introdução, ele responde com nome do arquivo e a palavra que deseja encontrar no formato "arquivo palavra" e recebe a resposta, para finalizar ele fala exit
import socket


HOST = 'localhost'

PORTA = 5788

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORTA))

while(1):

	while(1):
		msg = input()
		if(msg == "exit" or len(msg.split()) == 2):
			break
	
	

	sock.send(str.encode(msg))
	
	if(msg == "exit"):
		break
		
	msg = sock.recv(1024)
	
	print(str(msg, encoding = 'utf-8'))

sock.close()


