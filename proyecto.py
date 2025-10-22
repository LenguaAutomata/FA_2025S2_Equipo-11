import tkinter as tk
from tkinter import ttk

class AnalizadorAritmeticoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Operaciones Aritmeticas")
        self.root.geometry("800x600")
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Frame para botones superiores
        frame_botones_superiores = ttk.Frame(main_frame)
        frame_botones_superiores.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botones superiores
        self.btn_abrir = ttk.Button(frame_botones_superiores, text="Abrir", command=self.boton_sin_funcion)
        self.btn_abrir.grid(row=0, column=0, padx=(0, 5))
        
        self.btn_guardar = ttk.Button(frame_botones_superiores, text="Guardar", command=self.boton_sin_funcion)
        self.btn_guardar.grid(row=0, column=1, padx=5)
        
        self.btn_guardar_como = ttk.Button(frame_botones_superiores, text="Guardar Como", command=self.boton_sin_funcion)
        self.btn_guardar_como.grid(row=0, column=2, padx=5)
        
        self.btn_analizar = ttk.Button(frame_botones_superiores, text="Analizar", command=self.boton_sin_funcion)
        self.btn_analizar.grid(row=0, column=3, padx=5)
        
        # Frame para botones inferiores
        frame_botones_inferiores = ttk.Frame(main_frame)
        frame_botones_inferiores.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Botones inferiores
        self.btn_manual_usuario = ttk.Button(frame_botones_inferiores, text="Manual de Usuario", command=self.boton_sin_funcion)
        self.btn_manual_usuario.grid(row=0, column=0, padx=(0, 5))
        
        self.btn_manual_tecnico = ttk.Button(frame_botones_inferiores, text="Manual Técnico", command=self.boton_sin_funcion)
        self.btn_manual_tecnico.grid(row=0, column=1, padx=5)
        
        self.btn_ayuda = ttk.Button(frame_botones_inferiores, text="Ayuda", command=self.boton_sin_funcion)
        self.btn_ayuda.grid(row=0, column=2, padx=5)
        
        # Etiqueta para el área de texto
        lbl_area_texto = ttk.Label(main_frame, text="Área de Texto:")
        lbl_area_texto.grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        
        # Área de texto con scroll
        self.area_texto = tk.Text(main_frame, wrap=tk.WORD, width=80, height=30)
        self.area_texto.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Scrollbar para el área de texto
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.area_texto.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.area_texto.configure(yscrollcommand=scrollbar.set)
    
    def boton_sin_funcion(self):
        """Nada"""
        print("No hace nada")

def main():
    root = tk.Tk()
    app = AnalizadorAritmeticoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()