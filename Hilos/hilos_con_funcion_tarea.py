import tkinter as tk
import threading
import time

def ejecutar():
    def Tarea_Tiempo(Tarea, text_widget):
        inicio = time.time()
        text_widget.insert(tk.END, f"Inicio de la tarea {Tarea}\n")
        time.sleep(2)
        duracion = time.time() - inicio
        text_widget.insert(tk.END, f"Fin de la tarea {Tarea} Duracion: {duracion:.2f}\n")

    def iniciar_tareas(text_widget):
        def run_tasks():
            hilo1 = threading.Thread(target=Tarea_Tiempo, args=("Tarea 1", text_widget))
            hilo2 = threading.Thread(target=Tarea_Tiempo, args=("Tarea 2", text_widget))

            hilo1.start()
            hilo2.start()

            hilo1.join()
            hilo2.join()

            text_widget.insert(tk.END, "Fin del programa\n")

        threading.Thread(target=run_tasks).start()

    def main():
        root = tk.Tk()
        root.title("Ejemplo de Hilos con Tkinter")

        text_widget = tk.Text(root, height=10, width=50)
        text_widget.pack(pady=20)

        btn_iniciar = tk.Button(root, text="Iniciar Tareas", command=lambda: iniciar_tareas(text_widget))
        btn_iniciar.pack(pady=20)

        root.mainloop()

if __name__ == "__main__":
    ejecutar()
