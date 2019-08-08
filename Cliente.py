import socket
import threading

class ClaseCliente():

	def __init__(self):

		# Configuramos el tipo de conexion y nos conectamos al servidor.
		self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.cliente.connect(('vps717213.ovh.net', 1337))

		self.nick = input("Selecciona tu nombre de usuario: ")

		# Ponemos un thread a recibir los mensajes.
		mensajeRecibido = threading.Thread(target=self.RecibirMensajes)
		mensajeRecibido.daemon = True
		mensajeRecibido.start()

		# Bucle que mantiene vivo el bucle y ademas nos permite enviar mensajes.
		while True:
			mensaje = input()
			try:
				if mensaje != "salir":
					self.EnviarMensajes(mensaje)
				else:
					self.cliente.close()
			except:
				self.cliente.close()


	def RecibirMensajes(self):

		while True: # Bucle que mantiene viva la recepcion de mensajes.
			try:
				mensaje = self.cliente.recv(2048)
				print(mensaje.decode()) # Por defecto el encode es "utf-8".
			except:
				pass


	def EnviarMensajes(self, mensaje):

		mensaje = self.nick + "- " + mensaje # Agregamos el nick al mensaje. 
		self.cliente.send(bytes(mensaje.encode())) # Enviamos el mensaje codificado al servidor. Por defecto, en "utf-8".

# --------------------------------------------------------------#


start = ClaseCliente()
		
