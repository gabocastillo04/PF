import tkinter as tk
from tkinter import PhotoImage
import random
import threading
import time
from PIL import Image, ImageTk  # Para redimensionar la imagen de fondo

symbols = ["🌼", "🍄", "🌟"]

class MarioRuletaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ruleta Mario")
        self.root.geometry("800x600")  # Tamaño inicial de la ventana

        # Configurar evento para redimensionar el fondo dinámicamente
        self.root.bind("<Configure>", self.resize_background)

        # Fondo inicial
        try:
            self.original_background = Image.open("ruta/a/tu/imagen.jpg")  # Cambia por la ruta de tu imagen
            self.resized_background = self.original_background.resize((800, 600))  # Ajuste inicial del tamaño
            self.background = ImageTk.PhotoImage(self.resized_background)
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
            self.background = None

        self.label_background = tk.Label(root, image=self.background)
        self.label_background.place(x=0, y=0, relwidth=1, relheight=1)

        # Variables para el estado del juego
        self.result = [''] * 3
        self.hilado_flags = [True] * 3
        self.threads = []
        self.score = 0

        # Elementos de la interfaz
        self.label_title = tk.Label(root, text="Ruleta Mario", font=("Arial", 20, "bold"), bg="#ffffff")
        self.label_title.pack(pady=10)

        self.label_result = tk.Label(root, text="Giros: --- --- ---", font=("Arial", 16), bg="#ffffff")
        self.label_result.pack(pady=10)

        self.label_score = tk.Label(root, text="Puntaje: 0", font=("Arial", 16), bg="#ffffff")
        self.label_score.pack(pady=10)

        self.button_spin = tk.Button(root, text="Girar", command=self.start_spin, font=("Arial", 14), bg="#4CAF50", fg="white", width=15)
        self.button_spin.pack(pady=10)

        self.button_play_again = tk.Button(root, text="Volver a jugar", command=self.reset_game, font=("Arial", 14), bg="#2196F3", fg="white", width=15)
        self.button_play_again.pack(pady=10)
        self.button_play_again.config(state=tk.DISABLED)

        self.button_stop = tk.Button(root, text="Detener", command=self.stop_spin, font=("Arial", 14), bg="#f44336", fg="white", width=15)
        self.button_stop.pack(pady=10)
        self.button_stop.config(state=tk.DISABLED)

        # Eventos para detener los giros
        self.root.bind("<Return>", self.stop_spin_event)

    def resize_background(self, event):
        """Redimensiona el fondo dinámicamente según el tamaño de la ventana."""
        if self.background:
            new_width = event.width
            new_height = event.height
            resized_background = self.original_background.resize((new_width, new_height))  # Eliminado ANTIALIAS
            self.background = ImageTk.PhotoImage(resized_background)
            self.label_background.config(image=self.background)

    def pantalla_giro(self, index):
        """Función para simular el giro de un tambor."""
        while self.hilado_flags[index]:
            self.result[index] = random.choice(symbols)
            self.update_result_label()
            time.sleep(0.1)  # Velocidad del giro (puedes ajustar este valor)

    def start_spin(self):
        """Inicia los giros de los tambores."""
        self.button_spin.config(state=tk.DISABLED)
        self.button_stop.config(state=tk.NORMAL)
        self.result = [''] * 3
        self.hilado_flags = [True] * 3
        self.threads = []

        for i in range(3):
            thread = threading.Thread(target=self.pantalla_giro, args=(i,))
            self.threads.append(thread)
            thread.start()

        self.label_result.config(text="Gira presionando Enter para detener cada tambor.")

    def stop_spin_event(self, event):
        """Detiene un tambor al presionar Enter."""
        for i in range(3):
            if self.hilado_flags[i]:
                self.hilado_flags[i] = False
                self.threads[i].join()
                if i == 2:  # Último tambor detenido
                    self.check_result()
                return

    def stop_spin(self):
        """Detiene un tambor al presionar el botón Detener."""
        for i in range(3):
            if self.hilado_flags[i]:
                self.hilado_flags[i] = False
                self.threads[i].join()
                if i == 2:  # Último tambor detenido
                    self.check_result()
                    self.button_stop.config(state=tk.DISABLED)
                return

    def update_result_label(self):
        """Actualiza la etiqueta con los resultados actuales."""
        self.label_result.config(text=f"Giros: {' '.join(self.result)}")

    def check_result(self):
        """Calcula el puntaje y muestra el resultado."""
        score_gain = self.calcula_score(self.result)
        self.score += score_gain
        if score_gain > 0:
            self.label_score.config(text=f"¡Ganaste {score_gain} puntos! Total: {self.score}")
        else:
            self.label_score.config(text=f"No ganaste esta vez. Puntaje total: {self.score}")
        self.button_play_again.config(state=tk.NORMAL)

    def calcula_score(self, result):
        """Calcula el puntaje basado en el resultado."""
        if result[0] == result[1] == result[2]:
            if result[0] == "🌟":
                return 5
            elif result[0] == "🌼":
                return 3
            elif result[0] == "🍄":
                return 2
        return 0

    def reset_game(self):
        """Reinicia el juego, pero mantiene el puntaje."""
        self.result = [''] * 3
        self.hilado_flags = [True] * 3
        self.label_result.config(text="Giros: --- --- ---")
        self.button_spin.config(state=tk.NORMAL)
        self.button_play_again.config(state=tk.DISABLED)
        self.button_stop.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = MarioRuletaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()