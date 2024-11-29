import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Dirección y puerto
direccion = "localhost"
puerto = 9999

def ejecutar():
    def iniciar_servidor():
        def servidor():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as mySocket:
                try:
                    mySocket.bind((direccion, puerto))
                    output.insert(tk.END, f"Servidor UDP iniciado en {direccion}:{puerto}\n")
                    
                    while True:
                        msg, client_addr = mySocket.recvfrom(1024)
                        output.insert(tk.END, f"Mensaje recibido del cliente {client_addr}: {msg.decode()}\n")
                        
                        msg_out = f"Mensaje recibido: {msg.decode()}, gracias."
                        mySocket.sendto(msg_out.encode(), client_addr)
                        output.insert(tk.END, f"Enviado acuse de recibo al cliente {client_addr}\n")
                        break
                except Exception as e:
                    output.insert(tk.END, f"Error en el servidor: {e}\n")

        threading.Thread(target=servidor, daemon=True).start()

    def iniciar_cliente():
        def cliente():
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as mySocket:
                try:
                    msg = "Hola, soy un cliente UDP creado por el equipo 4."
                    output.insert(tk.END, f"Enviando mensaje al servidor: {msg}\n")
                    mySocket.sendto(msg.encode(), (direccion, puerto))
                    
                    msg_in, server_addr = mySocket.recvfrom(1024)
                    output.insert(tk.END, f"Acuse de recibo del servidor {server_addr}: {msg_in.decode()}\n")
                except Exception as e:
                    output.insert(tk.END, f"Error en el cliente: {e}\n")

        threading.Thread(target=cliente, daemon=True).start()

    # Crear ventana con Tkinter
    root = tk.Tk()
    root.title("Cliente/Servidor UDP")

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