import tkinter as tk
from tkinter import font, Toplevel
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
import fitz  # pip install pymupdf
import os
import queue
import subprocess

# Importar módulos de las carpetas del proyecto
from Hilos import hilos_hilos, hilos_con_argumentos, hilos_con_funcion_tarea, hilos_sincronizados, mario_bros_ruleta
from Sockets import mensajes_cliente_servidor, tcp_cliente_servidor, udp_cliente_servidor, comunicacion_directa, comunicacion_indirecta, autenticacion_aguila
from Semaforos import condicion_de_carrera, sincronizacion_de_semaforos, semaforos_cliente_servidor, barbero_dormilon, sala_de_chat_local, sala_de_chat_ip
from Patrones import futuro_promesa, productor_consumidor, actores, reactor_y_proactor

# Ruta específica del archivo PDF
PDF_PATH = r"Documentacion/pdfproyectofinal.pdf"  # Asegúrate de que esta ruta sea válida

# Función para mostrar documentación en un visor PDF
def mostrar_documentacion():
    ventana_pdf = Toplevel(root)
    ventana_pdf.title("Documentación")
    ventana_pdf.geometry("650x600")

    # Crear marco para Canvas y scrollbars
    frame = tk.Frame(ventana_pdf)
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="white")
    scroll_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)

    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Marco interior para colocar imágenes
    inner_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    def load_pdf():
        try:
            doc = fitz.open(PDF_PATH)
            for page_number in range(len(doc)):
                page = doc.load_page(page_number)
                pix = page.get_pixmap()
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                photo = ImageTk.PhotoImage(image)

                label = tk.Label(inner_frame, image=photo, bg="white")
                label.image = photo  # Prevenir que Python borre la referencia
                label.pack()

            # Ajustar el scrollregion al contenido
            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        except Exception as e:
            tk.Label(inner_frame, text=f"Error al cargar el PDF:\n{e}", fg="red", bg="white").pack()

    load_pdf()

# Diccionario para mapear opciones a funciones
opciones_funciones = {
    "Hilos-Hilos": hilos_hilos.ejecutar if hasattr(hilos_hilos, 'ejecutar') else lambda: print("Función no encontrada"),
    "Hilos con argumentos": hilos_con_argumentos.ejecutar if hasattr(hilos_con_argumentos, 'ejecutar') else lambda: print("Función no encontrada"),
    "Hilos con función tarea": hilos_con_funcion_tarea.ejecutar if hasattr(hilos_con_funcion_tarea, 'ejecutar') else lambda: print("Función no encontrada"),
    "Hilos sincronizados": hilos_sincronizados.ejecutar if hasattr(hilos_sincronizados, 'ejecutar') else lambda: print("Función no encontrada"),
    "Mario Bros Ruleta": mario_bros_ruleta.main if hasattr(mario_bros_ruleta, 'main') else lambda: print("Función no encontrada"),
    "Mensajes Cliente/Servidor": mensajes_cliente_servidor.ejecutar if hasattr(mensajes_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "TCP Cliente/Servidor": tcp_cliente_servidor.ejecutar if hasattr(tcp_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "UDP Cliente/Servidor": udp_cliente_servidor.ejecutar if hasattr(udp_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Sincronización de semáforos": sincronizacion_de_semaforos.ejecutar if hasattr(sincronizacion_de_semaforos, 'ejecutar') else lambda: print("Función no encontrada"),
    "Barbero dormilón": barbero_dormilon.ejecutar if hasattr(barbero_dormilon, 'ejecutar') else lambda: print("Función no encontrada"),
    "Sala de chat": sala_de_chat_ip.ejecutar if hasattr(sala_de_chat_ip, 'ejecutar') else lambda: print("Función no encontrada"),
    "Futuro Promesa": futuro_promesa.ejecutar if hasattr(futuro_promesa, 'ejecutar') else lambda: print("Función no encontrada"),
    "Productor-Consumidor": productor_consumidor.ejecutar if hasattr(productor_consumidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Reactor y Proactor": reactor_y_proactor.ejecutar if hasattr(reactor_y_proactor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Comunicacion Directa": comunicacion_directa.ejecutar if hasattr(comunicacion_directa, 'ejecutar') else lambda: print("Función no encontrada"),
    "Comunicacion Indirecta": comunicacion_indirecta.ejecutar if hasattr(comunicacion_indirecta, 'ejecutar') else lambda: print("Función no encontrada"),
    "Autenticacion Aguila": autenticacion_aguila.ejecutar if hasattr(autenticacion_aguila, 'ejecutar') else lambda: print("Función no encontrada"),
    "Semaforos Cliente/Servidor": semaforos_cliente_servidor.ejecutar if hasattr(semaforos_cliente_servidor, 'ejecutar') else lambda: print("Función no encontrada"),
    "Sala de Chat Local": sala_de_chat_local.ejecutar if hasattr(sala_de_chat_local, 'ejecutar') else lambda: print("Función no encontrada"),
    "Condicion de Carrera": condicion_de_carrera.ejecutar if hasattr(condicion_de_carrera, 'ejecutar') else lambda: print("Función no encontrada"),
    "actores": actores.ejecutar if hasattr(actores, 'ejecutar') else lambda: print("Función no encontrada"),
}

# Función para mostrar submenús
def mostrar_submenu(titulo, opciones):
    for widget in root.winfo_children():
        if widget != menu_bar:
            widget.destroy()

    frame = tk.Frame(root, bg="#2c3e50")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    for opcion in opciones:
        tk.Button(frame, text=opcion, command=opciones_funciones.get(opcion, lambda: print("Función no encontrada")),
                  bg="#3498db", fg="white", font=("Helvetica", 12, "bold"), bd=0, padx=10, pady=10).pack(pady=10)

    # Centrar los botones
    frame.update_idletasks()
    frame_width = frame.winfo_width()
    for button in frame.winfo_children():
        button_width = button.winfo_reqwidth()
        button.pack_configure(padx=(frame_width - button_width) // 2)

# Crear la ventana principal
root = tk.Tk()
root.title("Programación Concurrente UPP SFTW_07_03")
root.geometry("800x600")
root.configure(bg="#34495e")
root.state('zoomed')  # Maximizar la ventana al iniciar

# Cargar la imagen de fondo
bg_image = Image.open("Imagenes/BG.png")
bg_photo = ImageTk.PhotoImage(bg_image)

# Crear un label para la imagen de fondo
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Crear el menú sobre la imagen de fondo
menu_bar = tk.Frame(root, bg="#2c3e50")
menu_bar.pack(side="top", fill="x")
menu_bar.lift()  # Asegurar que el menú siempre esté en la parte superior

# Opciones de submenú
hilos_opciones = ["Hilos-Hilos", "Hilos con argumentos", "Hilos con función tarea", "Hilos sincronizados", "Mario Bros Ruleta"]
sockets_opciones = ["Mensajes Cliente/Servidor", "TCP Cliente/Servidor", "UDP Cliente/Servidor", "Comunicacion Directa", "Comunicacion Indirecta", "Autenticacion Aguila"]
semaforos_opciones = ["Sincronización de semáforos", "Barbero dormilón", "Sala de chat", "Condicion de Carrera", "Semaforos Cliente/Servidor", "Sala de Chat Local"]
patrones_opciones = ["Futuro Promesa", "Productor-Consumidor", "Actores", "Reactor y Proactor"]

# Botones de menú principal
menu_font = font.Font(family="Helvetica", size=12, weight="bold")
boton_estilo = {"bg": "#3498db", "fg": "white", "font": menu_font, "bd": 0, "padx": 10, "pady": 10}

tk.Button(menu_bar, text="Hilos", command=lambda: mostrar_submenu("Hilos", hilos_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Sockets", command=lambda: mostrar_submenu("Sockets", sockets_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Semáforos", command=lambda: mostrar_submenu("Semáforos", semaforos_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Patrones", command=lambda: mostrar_submenu("Patrones", patrones_opciones), **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Documentación", command=mostrar_documentacion, **boton_estilo).pack(side="left", expand=True, fill="x")
tk.Button(menu_bar, text="Salir", command=root.quit, **boton_estilo).pack(side="left", expand=True, fill="x")

# Asegurar que el menú siempre esté en la parte superior
menu_bar.lift()

# Iniciar el loop de Tkinter
root.mainloop()