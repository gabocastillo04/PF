# sala_de_chat.py

import tkinter as tk
import socket
import threading

# Dirección del host y puerto
HOST = '127.0.0.1'
PORT = 65432

# Lista de clientes conectados
clientes = []

# Función para manejar la comunicación con cada cliente (servidor)
def manejar_cliente(cliente_socket, chat_text):
    while True:
        try:
            # Recibe el mensaje del cliente
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if mensaje:
                mostrar_mensaje(mensaje, chat_text)  # Pasamos chat_text como parámetro
                # Retransmite el mensaje a todos los clientes
                transmitir_mensaje(mensaje, cliente_socket)
            else:
                remover_cliente(cliente_socket)
                break
        except:
            remover_cliente(cliente_socket)
            break

# Función para retransmitir el mensaje a todos los clientes (servidor)
def transmitir_mensaje(mensaje, cliente_socket):
    for cliente in clientes:
        if cliente != cliente_socket:
            try:
                cliente.send(mensaje.encode('utf-8'))
            except:
                remover_cliente(cliente)

# Función para remover un cliente de la lista y cerrar su conexión (servidor)
def remover_cliente(cliente_socket):
    if cliente_socket in clientes:
        clientes.remove(cliente_socket)
        cliente_socket.close()

# Configuración y ejecución del servidor (servidor)
def iniciar_servidor(chat_text):
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((HOST, PORT))
    servidor_socket.listen(5)
    print(f"[Servidor iniciado] Esperando conexiones en {HOST}:{PORT}...")
    mostrar_mensaje("[Servidor iniciado] Esperando conexiones en 127.0.0.1:65432...", chat_text)
    
    while True:
        cliente_socket, cliente_direccion = servidor_socket.accept()
        print(f"[Nueva conexión] {cliente_direccion}")
        mostrar_mensaje(f"[Nueva conexión] {cliente_direccion}", chat_text)
        clientes.append(cliente_socket)
        threading.Thread(target=manejar_cliente, args=(cliente_socket, chat_text), daemon=True).start()

# Función para recibir mensajes del servidor (cliente)
def recibir_mensajes(cliente_socket, chat_text):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if mensaje:
                mostrar_mensaje(mensaje, chat_text)  # Pasamos chat_text como parámetro
            else:
                cliente_socket.close()
                break
        except:
            cliente_socket.close()
            break

# Función para mostrar el mensaje en la interfaz gráfica
def mostrar_mensaje(mensaje, chat_text):
    chat_text.config(state=tk.NORMAL)  # Habilitar el Text widget para insertar el mensaje
    chat_text.insert(tk.END, mensaje + "\n")
    chat_text.yview(tk.END)  # Desplazar hacia abajo para mostrar el nuevo mensaje
    chat_text.config(state=tk.DISABLED)  # Volver a deshabilitar para que no se edite

# Enviar mensaje desde la interfaz gráfica (cliente)
def enviar_mensaje(cliente_socket, mensaje_entry):
    mensaje = mensaje_entry.get()
    if mensaje:
        cliente_socket.send(mensaje.encode('utf-8'))
        mensaje_entry.delete(0, tk.END)

# Iniciar el servidor desde la interfaz gráfica
def iniciar_servidor_gui(chat_text):
    threading.Thread(target=iniciar_servidor, args=(chat_text,), daemon=True).start()

# Iniciar el cliente desde la interfaz gráfica
def iniciar_cliente_gui():
    global cliente_socket
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((HOST, PORT))
    
    # Inicia un hilo para recibir mensajes
    threading.Thread(target=recibir_mensajes, args=(cliente_socket, chat_text), daemon=True).start()
    
    mostrar_mensaje("[Conectado al servidor] Ya puedes empezar a chatear.", chat_text)

# Función para ejecutar la interfaz de la sala de chat
def ejecutar():
    global cliente_socket
    global chat_text
    global mensaje_entry
    
    # Configuración de la interfaz gráfica
    root = tk.Tk()
    root.title("Sala de Chat - Cliente/Servidor")
    
    # Crear un Frame para el chat
    frame_chat = tk.Frame(root)
    frame_chat.pack(pady=10)

    # Crear un Text widget para mostrar los mensajes del chat
    chat_text = tk.Text(frame_chat, width=50, height=20, wrap=tk.WORD, state=tk.DISABLED)
    chat_text.pack(side=tk.LEFT)

    # Crear una barra de desplazamiento
    scrollbar = tk.Scrollbar(frame_chat, command=chat_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configurar la barra de desplazamiento
    chat_text.config(yscrollcommand=scrollbar.set)

    # Crear un Entry widget para ingresar el mensaje
    mensaje_entry = tk.Entry(root, width=40)
    mensaje_entry.pack(pady=10)

    # Botón para enviar el mensaje
    enviar_button = tk.Button(root, text="Enviar", command=lambda: enviar_mensaje(cliente_socket, mensaje_entry))
    enviar_button.pack(pady=5)

    # Botones para iniciar servidor y cliente
    boton_servidor = tk.Button(root, text="Iniciar Servidor", command=lambda: iniciar_servidor_gui(chat_text))
    boton_servidor.pack(side=tk.LEFT, padx=10)

    boton_cliente = tk.Button(root, text="Conectar como Cliente", command=iniciar_cliente_gui)
    boton_cliente.pack(side=tk.RIGHT, padx=10)

    # Ejecutar la interfaz gráfica
    root.mainloop()
