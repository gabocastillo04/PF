import threading
import time
import tkinter as tk

def ejecutar():  # Función principal
    def Hilo_02(nombre, apellido, label):  # función con parámetros
        # Simula el trabajo en el hilo secundario
        label.config(text="Hilos con argumentos en Python " + nombre + apellido)
        time.sleep(9)  # Se espera 9 segundos antes de seguir
        label.config(text="Hilos con Python desde el hilo secundario")

    # Crear la ventana principal de Tkinter
    ventana = tk.Tk()
    ventana.title("Programa de Hilos con Tkinter")

    # Crear una etiqueta para mostrar el progreso
    label = tk.Label(ventana, text="Esperando para ejecutar...")
    label.pack(pady=20)

    # Crear un botón que inicia el hilo cuando se hace clic
    boton = tk.Button(ventana, text="Iniciar Hilo", command=lambda: threading.Thread(target=Hilo_02, args=("Fab ", "Meneses Avila ", label), daemon=True).start())
    boton.pack(pady=20)

# Iniciar el loop de la interfaz gráfica
    ventana.mainloop()
