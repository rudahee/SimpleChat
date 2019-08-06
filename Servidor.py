import socket
import threading

class ClaseServidor(): 

	def __init__(self):

		# Configuramos el tipo de conexion y nos ponemos a escuchar 
		self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.servidor.bind(('0.0.0.0', 1337))
		self.servidor.listen()
		self.servidor.setblocking(False) # No bloqueamos la conexion (Genera una excepcion si no puede mandar o recibir datos).

		# Ponemos un thread a aceptar las conexiones.
		aceptarConex = threading.Thread(target=self.AceptarConexiones)
		aceptarConex.daemon = True
		aceptarConex.start()

		# Ponemos un thread a leer y reenviar los mensajes entrantes.
		manejoMensajes = threading.Thread(target=self.ManejarMensajesEntrantes)
		manejoMensajes.daemon = True
		manejoMensajes.start()


		# Bucle que mantiene vivo el servidor.
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
				# Si la persona que envia el mensaje no es el que lo recibe, envia el mensaje.
				if emisor != receptor:
					receptor.send(mensaje)
			except:
				# Entramos en la excepcion si no se puede enviar el mensaje a alguien, y lo quitamos de la lista de clientes.
				self.listaConexiones.remove(cliente)


	def AceptarConexiones(self):

		self.listaConexiones = [] # Lista para guardar las conexiones

		while True: # Bucle que mantiene escuchando 
			try:
				clienteConexion, clienteIP = self.servidor.accept() # Empezamos a aceptar conexiones 
				clienteConexion.setblocking(False)
				self.listaConexiones.append(clienteConexion) # Agregamos el objeto cliente a nuestra lista.
				print("se ha conectado el cliente: ", clienteIP[0])
			except:
				pass # Esto es para el setblocking, si se puede aceptar, da una excepcion.


	def ManejarMensajesEntrantes(self):

		while True: # Bucle que mantiene vivo el manejo de mensajes.
			if len(self.listaConexiones) != 0: 
				for cliente in self.listaConexiones: 
					try:
						mensaje = cliente.recv(2048) # Recibimos un mensaje.
						self.MandarMensajes(mensaje, cliente) # Lo mandamos a enviar.
					except:
						pass # Esto es para el setblocking, si no recibe un mensaje, da una excepcion.

# --------------------------------------------------------------#

start = ClaseServidor()