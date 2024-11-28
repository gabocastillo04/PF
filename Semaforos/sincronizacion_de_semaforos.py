# sincronizacion_de_semaforos.py
import tkinter as tk
import threading
import time
import random

# Creamos un semáforo con un valor máximo de 2 (la impresora puede atender dos procesos a la vez)
semaforo_impresora = threading.Semaphore(2)

# Función para simular el envío del documento desde cada equipo
def enviar_documento(equipo_id, texto_area):
    paginas = random.randint(1, 10)  # Número aleatorio de páginas (1 a 10)
    texto_area.insert(tk.END, f"Equipo {equipo_id} tiene un documento de {paginas} páginas.\n")
    texto_area.yview(tk.END)  # Desplazamos el texto al final
    
    # Intentamos acceder a la impresora
    with semaforo_impresora:
        texto_area.insert(tk.END, f"Equipo {equipo_id} está enviando el documento a la impresora.\n")
        texto_area.yview(tk.END)
        time.sleep(paginas)  # Simulamos el tiempo de procesamiento basado en el número de páginas
        texto_area.insert(tk.END, f"Equipo {equipo_id} ha terminado de imprimir.\n")
        texto_area.yview(tk.END)

# Función para crear y manejar los hilos de impresión
def iniciar_impresion(texto_area):
    equipos = 6
    threads = []
    
    # Crear un hilo por cada equipo
    for equipo_id in range(1, equipos + 1):
        t = threading.Thread(target=enviar_documento, args=(equipo_id, texto_area))
        threads.append(t)
        t.start()
    
    # Esperamos a que todos los hilos terminen
    for t in threads:
        t.join()

# Función para ejecutar la simulación de impresión en un hilo separado
def ejecutar():
    # Crear la ventana principal de Tkinter
    ventana = tk.Tk()
    ventana.title("Simulación de Impresora")

    # Crear un área de texto para mostrar el estado de la impresora
    texto_area = tk.Text(ventana, height=15, width=60)
    texto_area.pack(padx=10, pady=10)

    # Crear un botón para comenzar la simulación
    # El botón lanzará el hilo que realizará la simulación
    boton_comenzar = tk.Button(ventana, text="Comenzar Simulación", command=lambda: threading.Thread(target=iniciar_impresion, args=(texto_area,), daemon=True).start())
    boton_comenzar.pack(pady=10)

    # Ejecutar el bucle principal de la interfaz
    ventana.mainloop()
