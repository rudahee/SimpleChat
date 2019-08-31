import socket
import threading
import time
import tkinter as tk
from tkinter import ttk



class AppCliente:
	
	def __init__(self):

		# Inicializamos las funciones de red.
		# 	Configuramos el tipo de conexion y nos conectamos al servidor.

		self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.cliente.connect(('localhost', 1337))


		# Vamos a llamar la ventana emergente para obtener el nick.

		self.emergente = tk.Tk()
		self.emergente.title("Obtener nick")
		
		self.obNick = tk.StringVar()
		
		frame = tk.Frame(self.emergente)
		frame.grid(row=0, column=0, padx=5, pady=5)

		labelNick = tk.Label(frame, text="Inserte su nick y pulse en Listo!")
		labelNick.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")

		insertNick = tk.Entry(frame, width=30, textvariable=self.obNick)
		insertNick.grid(row=2, column=0, sticky="w", padx=5, pady=5)

		botonNick = tk.Button(frame, text="Listo!", command=self.obtenerNick)
		botonNick.grid(row=2, column=1, sticky="e", padx=5, pady=5)

		self.emergente.mainloop()
		

		# Ponemos un thread a recibir los mensajes.
		mensajeRecibido = threading.Thread(target=self.recibirMensajes)
		mensajeRecibido.daemon = True
		mensajeRecibido.start()


		# Inicializamos las funciones graficas de la ventana principal del chat.

		self.root = tk.Tk()
		self.root.title("ChatSocket - " + self.obNick)

		self.mensajeEnviar = tk.StringVar()


		frame = tk.Frame(self.root)
		frame.grid(row=0, column=0, padx=5, pady=5)


		self.chat = ttk.Treeview(
			frame,
			height=10,
			columns=("#1", "#2", "#3"),
			selectmode="none",
			show="headings"
			)
		self.chat.heading('#1', text='Hora', anchor=tk.CENTER)
		self.chat.heading("#2", text="Usuario", anchor=tk.CENTER)
		self.chat.heading("#3", text="Mensaje", anchor=tk.W)
		self.chat.column("#1", stretch=False, width=50)
		self.chat.column("#2", stretch=False, width=80)
		self.chat.column("#3", stretch=False, width=400)
		self.chat.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

		Scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.chat.yview)
		Scrollbar.grid(row=0, column=3, sticky="nse")
		self.chat.configure(yscrollcommand=Scrollbar.set)

		escribir_mensaje = tk.Entry(frame, width=87, textvariable=self.mensajeEnviar)
		escribir_mensaje.grid(row=1, column=0, sticky="w", padx=10, pady=10)
		escribir_mensaje.bind('<Return>', lambda event: self.enviarMensajes())

		enviar_mensaje = tk.Button(frame, text="Enviar", command=self.enviarMensajes)
		enviar_mensaje.grid(row=1, column=1, sticky="e", padx=10, pady=10)

		self.root.mainloop()

	def obtenerNick(self):

		self.obNick = self.obNick.get()
		self.emergente.destroy()

	def recibirMensajes(self):

		while True: # Bucle que mantiene viva la recepcion de mensajes.
			try:
				mensaje = self.cliente.recv(2048)
				mensaje = mensaje.decode() # Por defecto el encode es "utf-8".
				hora, usuario, mensj = mensaje.split("||")
				ultMSJ = self.chat.insert("", 'end', text="asdasd", values=(hora, usuario, mensj))
				self.chat.see(ultMSJ)
			except:
				print("pass")

	def enviarMensajes(self):
		msj = self.mensajeEnviar.get()
		msj = time.strftime("%H:%M:%S") + "||" + self.obNick + "||" + msj # Agregamos el nick al mensaje. 
		self.cliente.send(bytes(msj.encode())) # Enviamos el mensaje codificado al servidor. Por defecto, en "utf-8".
		self.mensajeEnviar.set("")

if __name__ == "__main__":	
	AppCliente()
