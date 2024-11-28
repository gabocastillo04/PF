import threading
import time
import random
import tkinter as tk

NUMERO_SILLAS = 3

class Barberia:
    def __init__(self, text_widget):
        self.sillas_sala_espera = NUMERO_SILLAS  
        self.sillas_sem = threading.Semaphore(NUMERO_SILLAS)  
        self.barbero_dormido = threading.Semaphore(0)  
        self.silla_barbero = threading.Lock()  
        self.corte_realizado = threading.Semaphore(0)  
        self.text_widget = text_widget  # Recibe el widget de texto para mostrar mensajes
        self.clientes_atendidos = 0  # Número de clientes atendidos

    def actualizar_mensaje(self, mensaje):
        # Usamos el after() para actualizar el widget de texto en el hilo principal
        self.text_widget.after(0, self._insertar_mensaje, mensaje)

    def _insertar_mensaje(self, mensaje):
        self.text_widget.insert(tk.END, mensaje + "\n")
        self.text_widget.yview(tk.END)  # Para que el texto se desplace hacia abajo automáticamente

    def cortar_pelo(self, cliente_id):
        mensaje = f"El barbero está cortando el pelo del cliente {cliente_id}."
        self.actualizar_mensaje(mensaje)
        time.sleep(random.uniform(1, 3))  # Simula el tiempo que toma cortar el pelo
        mensaje = f"El barbero ha terminado de cortar el pelo del cliente {cliente_id}."
        self.actualizar_mensaje(mensaje)

def cliente(barberia, cliente_id):
    mensaje = f"El cliente {cliente_id} ha llegado."
    barberia.actualizar_mensaje(mensaje)
    
    if barberia.sillas_sem.acquire(blocking=False): 
        mensaje = f"El cliente {cliente_id} está esperando en la sala de espera."
        barberia.actualizar_mensaje(mensaje)
        
        with barberia.silla_barbero:
            barberia.sillas_sem.release()  
            mensaje = f"El cliente {cliente_id} está siendo atendido."
            barberia.actualizar_mensaje(mensaje)
            barberia.barbero_dormido.release()  
            barberia.corte_realizado.acquire()  
            mensaje = f"El cliente {cliente_id} se va con el pelo cortado."
            barberia.actualizar_mensaje(mensaje)
    else:
        mensaje = f"El cliente {cliente_id} se va porque la sala de espera está llena."
        barberia.actualizar_mensaje(mensaje)

def barbero(barberia):
    while True:
        mensaje = "El barbero está durmiendo."
        barberia.actualizar_mensaje(mensaje)
        barberia.barbero_dormido.acquire()  # El barbero espera a que un cliente llegue
        mensaje = "El barbero ha sido despertado."
        barberia.actualizar_mensaje(mensaje)

        cliente_id = random.randint(1, 100)
        barberia.cortar_pelo(cliente_id)
        barberia.corte_realizado.release()  # Indica que el corte ha sido realizado

        barberia.clientes_atendidos += 1
        if barberia.clientes_atendidos >= 10:
            break  # Termina el barbero después de atender 10 clientes

def ejecutar():
    # Crear una ventana para la barbería
    ventana_barberia = tk.Tk()
    ventana_barberia.title("Barbero Dormilón")

    # Crear un área de texto para mostrar los mensajes
    text_widget = tk.Text(ventana_barberia, height=20, width=80, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10)

    # Botón para iniciar la barbería
    tk.Button(ventana_barberia, text="Iniciar Barbería", command=lambda: iniciar_barberia(text_widget), width=20, height=2).pack(pady=5)

    ventana_barberia.mainloop()

def iniciar_barberia(text_widget):
    # Crear una instancia de la barbería con la caja de texto para los mensajes
    barberia = Barberia(text_widget)
    
    # Iniciar el hilo del barbero
    hilo_barbero = threading.Thread(target=barbero, args=(barberia,))
    hilo_barbero.daemon = True  # Esto permite que el hilo termine cuando la aplicación principal termine
    hilo_barbero.start()

    # Crear los hilos de los clientes y programarlos en el hilo principal usando after()
    def crear_cliente(cliente_id):
        # Creamos y ejecutamos el hilo de cada cliente
        hilo_cliente = threading.Thread(target=cliente, args=(barberia, cliente_id))
        hilo_cliente.daemon = True
        hilo_cliente.start()

        # Programamos la creación del siguiente cliente
        if cliente_id < 10:  # Creamos hasta 10 clientes
            text_widget.after(random.randint(2000, 5000), crear_cliente, cliente_id + 1)

    # Iniciar el primer cliente
    crear_cliente(1)
