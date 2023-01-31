#! usr/bin/python3
#CSC 346
#
#Author: Mason Mariani

import random	
import sys
import threading
import socket

def connect_to_server(server_addr, server_port):#
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server_addr, server_port))
	return sock

def connect_user(client_addr, client_port):#
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_sock.bind((client_addr, client_port))
	server_sock.listen(5)
	return server_sock

def recv_user(conn_sock):#
	allData = ""
	while True:
		data = conn_sock.recv(1028)
		if not data:
			break
		else:
			allData = allData + data.decode()
	return allData

def recv_server(sock):#
	allData = ""
	while True:
		data = sock.recv(1024)
		if not data:
			break
		else:
			allData = allData + data.decode()
	return allData

def send_user(conn_sock, recvData):#
	conn_sock.sendall(recvData.encode())

def send_server(sock, recvData):#
	sock.sendall(recvData.encode())

def handle_server(conn_sock, sock):#
	#recive all data from the server, then send it to the client
	try:
		print("Connection Established to Server")
		recvData = recv_server(sock)
		print("Data from server:", recvData)
		send_user(conn_sock, recvData)
	except:
		sock.close()
	else:
		sock.close()

def handle_client(conn_sock, sock):#
	#recive all data from client then send that to the server
	try:
		print("Connection Established to Client")
		recvData = recv_user(conn_sock)
		print("Data from user:", recvData)
		send_server(sock, recvData)
	except:
		conn_sock.close()
	else:
		conn_sock.close()

def parse_run(inputs):#
	#argv1 = client argv2 = server
	#normal case
	if len(inputs) == 3:
		client = inputs[1]
		client = client.split(':')
		client_addr = client[0]
		client_port = client[1]
		if client_addr == '':
			client_addr = "0.0.0.0"
		if client_port == '':
			new_rand = random.randint(1024, 65535)
			cilent_port = new_rand
			new_client_port = new_rand
			new_client_port = int(new_client_port)
		else:
			new_client_port = int(client_port)

		server = inputs[2].split(':')
		server_addr = server[0]
		server_port = int(server[1])

	#special case 
	if len(inputs) == 2:
		#get random 
		client_addr = "0.0.0.0"
		new_rand = random.randint(1024, 65535)
		new_client_port = new_rand
		new_client_port = int(new_client_port)

		server = inputs[1].split(':')
		server_addr = server[0]
		server_port = server[1]

	client_port = int(new_client_port)
	server_port = int(server_port)

	return client_addr, client_port, server_addr, server_port

def main():
	inputs = sys.argv
	client_addr, client_port, server_addr, server_port = parse_run(inputs)

	#connect user to this program
	#(act as host)
	server_sock = connect_user(client_addr, client_port)

	#connect this program to the server
	#(act as client)
	sock = connect_to_server(server_addr, server_port)

	#start threads for sending/reciving data from client/server
	while True:
		conn_sock, conn_addr = server_sock.accept()
		client_thread = threading.Thread(target=handle_client, args=(conn_sock, sock)).start()
		server_thread = threading.Thread(target=handle_server, args=(conn_sock, sock)).start()

if __name__ == '__main__':
	main()