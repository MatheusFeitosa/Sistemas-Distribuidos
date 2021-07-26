import socket

HOST = 'localhost'

PORTA = 5789

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORTA))

while(1):
	msg = input()
	sock.send(str.encode(msg))
	if(msg == "exit"):
		break
	msg = sock.recv(1024)
	print(str(msg, encoding = 'utf-8'))

sock.close()


