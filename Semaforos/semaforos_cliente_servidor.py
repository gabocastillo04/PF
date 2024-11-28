# semaforos_cliente_servidor.py

import socket
import threading
from threading import Semaphore
import tkinter as tk

# Configuración del servidor
HOST = '127.0.0.1'
PORT = 65432
MAX_CLIENTES_SIMULTANEOS = 3

semaforo = Semaphore(MAX_CLIENTES_SIMULTANEOS)

def actualizar_mensaje(mensaje, text_widget):
    text_widget.insert(tk.END, mensaje + "\n")  # Insertar mensaje en la caja de texto
    text_widget.yview(tk.END)  # Desplazar la vista hacia abajo para ver el último mensaje

def manejar_cliente(conexion, direccion, text_widget):
    with semaforo:
        mensaje = conexion.recv(1024).decode('utf-8')
        respuesta = "Mensaje recibido y confirmado"
        
        # Actualizar la caja de texto con los mensajes
        actualizar_mensaje(f"Cliente ({direccion}): {mensaje}", text_widget)
        conexion.sendall(respuesta.encode('utf-8'))
        actualizar_mensaje(f"Servidor: {respuesta}", text_widget)

        conexion.close()

def iniciar_servidor(text_widget):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((HOST, PORT))
        servidor.listen(5)
        actualizar_mensaje(f"Servidor escuchando en {HOST}:{PORT}", text_widget)

        while True:
            conexion, direccion = servidor.accept()
            # Iniciar un hilo para manejar el cliente
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion, text_widget))
            hilo_cliente.start()

def iniciar_cliente(text_widget):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((HOST, PORT))
        mensaje = "Hola, servidor"
        cliente.sendall(mensaje.encode('utf-8'))

        # Esperar la respuesta del servidor
        respuesta = cliente.recv(1024).decode('utf-8')
        
        # Actualizar la caja de texto con los mensajes
        actualizar_mensaje(f"Cliente: {mensaje}", text_widget)
        actualizar_mensaje(f"Servidor: {respuesta}", text_widget)

def ejecutar():
    def iniciar_servidor_en_hilo():
        # Crear un hilo para el servidor
        servidor_thread = threading.Thread(target=iniciar_servidor, args=(text_widget,))
        servidor_thread.daemon = True
        servidor_thread.start()

    def iniciar_cliente_en_hilo():
        # Crear un hilo para el cliente
        cliente_thread = threading.Thread(target=iniciar_cliente, args=(text_widget,))
        cliente_thread.daemon = True
        cliente_thread.start()

    # Crear una ventana de Tkinter para los botones y la caja de texto
    ventana_semaforo = tk.Tk()
    ventana_semaforo.title("Semáforos Cliente/Servidor")

    # Crear un área de texto para mostrar los mensajes
    text_widget = tk.Text(ventana_semaforo, height=20, width=80, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10)

    # Crear los botones para iniciar el servidor y el cliente
    tk.Button(ventana_semaforo, text="Iniciar Servidor", command=iniciar_servidor_en_hilo, width=20, height=2).pack(pady=5)
    tk.Button(ventana_semaforo, text="Iniciar Cliente", command=iniciar_cliente_en_hilo, width=20, height=2).pack(pady=5)

    ventana_semaforo.mainloop()
