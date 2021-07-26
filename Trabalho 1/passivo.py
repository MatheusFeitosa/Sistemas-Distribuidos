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
	if(str(msg, encoding = 'utf-8') == "exit"):
		break
	print(str(msg, encoding = 'utf-8'))
	novoSock.send(msg)
	
novoSock.close()
sock.close()

