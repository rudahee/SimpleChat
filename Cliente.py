import socket
import threading


class ClaseCliente():
	def __init__(self):
		self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.cliente.connect(('localhost', 1337))

		self.nick = input("Selecciona tu nombre de usuario: ")

		mensajeRecibido = threading.Thread(target=self.RecibirMensajes)
		mensajeRecibido.daemon = True
		mensajeRecibido.start()

		while True:
			mensaje = input()
			if mensaje != "salir":
				self.EnviarMensajes(mensaje)
			else:
				self.cliente.close()


	def RecibirMensajes(self):
		while True:
			try:
				mensaje = self.cliente.recv(2048)
				print(mensaje.decode())
			except:
				pass

	def EnviarMensajes(self, mensaje):
		mensaje = self.nick + "- " + mensaje 

		self.cliente.send(bytes(mensaje.encode()))


start = ClaseCliente()
		