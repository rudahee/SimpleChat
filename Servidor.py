import socket
import threading


class ClaseServidor(): 

	def __init__(self):
		# Configuramos el tipo de conexion y nos ponemos a escuchar 
		self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.servidor.bind(('localhost', 1337))
		self.servidor.listen()
		self.servidor.setblocking(False)

		aceptarConex = threading.Thread(target=self.AceptarConexiones)
		aceptarConex.daemon = True
		aceptarConex.start()

		manejoMensajes = threading.Thread(target=self.ManejarMensajesEntrantes)
		manejoMensajes.daemon = True
		manejoMensajes.start()

		try:
			while True:
				Mensaje = input(" =>  ")
				if Mensaje == "salir":
					self.servidor.close()
					break
		except:
			self.servidor.close()

	def MandarMensajes(self, mensaje, emisor):
		for receptor in self.listaConexiones:
			try:
				if emisor != receptor:
					receptor.send(mensaje)
			except:
				self.listaConexiones.remove(cliente)

	def AceptarConexiones(self):

		self.listaConexiones = []

		while True:
			try:
				clienteConexion, clienteIP = self.servidor.accept()
				clienteConexion.setblocking(False)
				self.listaConexiones.append(clienteConexion)
				print("se ha conectado el cliente: ", clienteIP[0])
			except:
				pass

	def ManejarMensajesEntrantes(self):
		while True:
			if len(self.listaConexiones) != 0:
				for cliente in self.listaConexiones:
					try:
						mensaje = cliente.recv(2048)
						self.MandarMensajes(mensaje, cliente)
					except:
						pass

start = ClaseServidor()