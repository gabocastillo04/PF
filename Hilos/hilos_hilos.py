import threading
import tkinter as tk

# Función que se ejecutará en el hilo
def Primer_Hilo(label):
    # Actualizar el texto en el widget de la etiqueta
    label.config(text="Mi Primer Programa con Hilos en Python")

# Función principal para ejecutar este módulo
def ejecutar():
    # Crear la ventana principal de tkinter
    root = tk.Tk()
    root.title("Hilos-Hilos")

    # Crear y empaquetar una etiqueta en la ventana
    label = tk.Label(root, text="Esperando ejecución del hilo...")
    label.pack(pady=20)

    # Crear y empezar el hilo
    thread = threading.Thread(target=Primer_Hilo, args=(label,))
    thread.start()

    # Iniciar el bucle principal de tkinter
    root.mainloop()
