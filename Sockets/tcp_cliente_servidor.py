import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Dirección y puerto
direccion = "localhost"
puerto = 9999

def ejecutar():
    def iniciar_servidor():
        def servidor():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
                try:
                    mySocket.bind((direccion, puerto))
                    output.insert(tk.END, f"Servidor iniciado en {direccion}:{puerto}\n")
                    mySocket.listen(5)
                    output.insert(tk.END, "Esperando conexiones...\n")

                    client, client_addr = mySocket.accept()
                    output.insert(tk.END, f"Conexión establecida con {client_addr}\n")
                    
                    msg = client.recv(1024).decode()
                    output.insert(tk.END, f"Mensaje recibido del cliente: {msg}\n")
                    
                    msg_out = f"Mensaje recibido: {msg}. Gracias."
                    client.send(msg_out.encode())
                    output.insert(tk.END, f"Enviando acuse de recibo: {msg_out}\n")
                    
                    client.close()
                    output.insert(tk.END, "Conexión cerrada con el cliente.\n")
                except Exception as e:
                    output.insert(tk.END, f"Error en el servidor: {e}\n")

        threading.Thread(target=servidor, daemon=True).start()

    def iniciar_cliente():
        def cliente():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mySocket:
                try:
                    mySocket.connect((direccion, puerto))
                    output.insert(tk.END, f"Conexión establecida con el servidor en {direccion}:{puerto}\n")
                    
                    msg = "Hola, soy un cliente TCP creado por Equipo 4."
                    output.insert(tk.END, f"Enviando mensaje al servidor: {msg}\n")
                    mySocket.send(msg.encode())
                    
                    msg_in = mySocket.recv(1024).decode()
                    output.insert(tk.END, f"Acuse de recibo del servidor: {msg_in}\n")
                    
                    mySocket.close()
                    output.insert(tk.END, "Conexión cerrada con el servidor.\n")
                except Exception as e:
                    output.insert(tk.END, f"Error en el cliente: {e}\n")

        threading.Thread(target=cliente, daemon=True).start()

    # Crear ventana con Tkinter
    root = tk.Tk()
    root.title("Cliente/Servidor TCP")

    # Área de texto para logs
    output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    output.pack(pady=20)

    # Botón para iniciar el servidor
    server_button = tk.Button(root, text="Iniciar Servidor", command=iniciar_servidor)
    server_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Botón para iniciar el cliente
    client_button = tk.Button(root, text="Iniciar Cliente", command=iniciar_cliente)
    client_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()