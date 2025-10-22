import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os

class AnalizadorAritmeticoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Operaciones Aritmeticas")
        self.root.geometry("800x600")
        
        # Variable para almacenar la ruta del archivo actual
        self.archivo_actual = None
        
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
        self.btn_abrir = ttk.Button(frame_botones_superiores, text="Abrir", command=self.abrir_archivo)
        self.btn_abrir.grid(row=0, column=0, padx=(0, 5))
        
        self.btn_guardar = ttk.Button(frame_botones_superiores, text="Guardar", command=self.guardar_archivo)
        self.btn_guardar.grid(row=0, column=1, padx=5)
        
        self.btn_guardar_como = ttk.Button(frame_botones_superiores, text="Guardar Como", command=self.guardar_como_archivo)
        self.btn_guardar_como.grid(row=0, column=2, padx=5)
        
        self.btn_analizar = ttk.Button(frame_botones_superiores, text="Analizar", command=self.analizar_codigo)
        self.btn_analizar.grid(row=0, column=3, padx=5)
        
        # Frame para botones inferiores
        frame_botones_inferiores = ttk.Frame(main_frame)
        frame_botones_inferiores.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Botones inferiores
        self.btn_manual_usuario = ttk.Button(frame_botones_inferiores, text="Manual de Usuario", command=self.mostrar_manual_usuario)
        self.btn_manual_usuario.grid(row=0, column=0, padx=(0, 5))
        
        self.btn_manual_tecnico = ttk.Button(frame_botones_inferiores, text="Manual Tecnico", command=self.mostrar_manual_tecnico)
        self.btn_manual_tecnico.grid(row=0, column=1, padx=5)
        
        self.btn_ayuda = ttk.Button(frame_botones_inferiores, text="Ayuda", command=self.mostrar_ayuda)
        self.btn_ayuda.grid(row=0, column=2, padx=5)
        
        # Etiqueta para el area de texto
        lbl_area_texto = ttk.Label(main_frame, text="Area de Texto:")
        lbl_area_texto.grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        
        # Area de texto con scroll
        self.area_texto = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=30)
        self.area_texto.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Configurar tags sintaxis 
        self.configurar_sintaxis()
    
    def configurar_sintaxis(self):
        """Configurar colores para sintaxis basica"""
        self.area_texto.tag_configure("operacion", foreground="blue")
        self.area_texto.tag_configure("numero", foreground="green")
        self.area_texto.tag_configure("etiqueta", foreground="purple")
    
    def abrir_archivo(self):
        """Abrir un archivo para edicion"""
        tipos_archivo = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        archivo = filedialog.askopenfilename(
            title="Abrir archivo",
            filetypes=tipos_archivo
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                self.area_texto.delete(1.0, tk.END)
                self.area_texto.insert(1.0, contenido)
                self.archivo_actual = archivo
                self.resaltar_sintaxis()
                
                messagebox.showinfo("Exito", f"Archivo '{os.path.basename(archivo)}' cargado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")
    
    def guardar_archivo(self):
        """Guardar el archivo actual"""
        if self.archivo_actual:
            try:
                contenido = self.area_texto.get(1.0, tk.END)
                with open(self.archivo_actual, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                messagebox.showinfo("Exito", "Archivo guardado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
        else:
            self.guardar_como_archivo()
    
    def guardar_como_archivo(self):
        """Guardar el archivo con un nombre diferente"""
        tipos_archivo = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        archivo = filedialog.asksaveasfilename(
            title="Guardar archivo como",
            defaultextension=".txt",
            filetypes=tipos_archivo
        )
        
        if archivo:
            try:
                contenido = self.area_texto.get(1.0, tk.END)
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                self.archivo_actual = archivo
                messagebox.showinfo("Exito", f"Archivo guardado como '{os.path.basename(archivo)}'")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
    
    def analizar_codigo(self):
        """Analizar el codigo del area de texto"""
        contenido = self.area_texto.get(1.0, tk.END).strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "El area de texto esta vacia")
            return
        
        try:
            # Guardar contenido temporalmente para analisis
            archivo_temporal = "temp_analisis.txt"
            with open(archivo_temporal, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            # analizador lexico
            self.ejecutar_analizador(contenido)
            
            messagebox.showinfo("Analisis Completado", 
                               "El analisis se ha completado correctamente.\n"
                               "Archivos generados:\n"
                               "- Resultados.html\n"
                               "- Errores.html\n"
                               "- Diagrama_operaciones.png")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el analisis: {str(e)}")
    
    def ejecutar_analizador(self, contenido):
        """Ejecutar el analizador lexico"""
        print("Ejecutando analizador lexico...")
        print("Contenido a analizar:")
        print(contenido)
        
       
        # ejemplo
        self.crear_archivo_resultados()
        self.crear_archivo_errores()
    
    def crear_archivo_resultados(self):
        """Crear archivo HTML de resultados """
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resultados de Operaciones</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                .operacion { background-color: #f8f9fa; padding: 10px; margin: 10px 0; border-left: 4px solid #3498db; }
            </style>
        </head>
        <body>
            <h1>Resultados de Operaciones Aritmeticas</h1>
            <div class="operacion">
                <h3>Operacion SUMA 1</h3>
                <p>4.5 + 5.32 = 9.82</p>
            </div>
            <div class="operacion">
                <h3>Operacion RESTA 1</h3>
                <p>84 - 33.7 = 50.3</p>
            </div>
        </body>
        </html>
        """
        
        with open("Resultados.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def crear_archivo_errores(self):
        """Crear archivo HTML de errores """
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte de Errores Lexicos</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #e74c3c; }
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
            </style>
        </head>
        <body>
            <h1>REPORTE DE ERRORES</h1>
            <table>
                <tr>
                    <th>No</th>
                    <th>Lexico</th>
                    <th>Tipo</th>
                    <th>Linea</th>
                    <th>Columna</th>
                </tr>
                <tr>
                    <td>1</td>
                    <td>SUMAA</td>
                    <td>Error Lexico</td>
                    <td>15</td>
                    <td>10</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        with open("Errores.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def mostrar_manual_usuario(self):
        """Mostrar manual de usuario"""
        messagebox.showinfo("Manual de Usuario", 
                           "Manual de Usuario\n\n"
                           "mostrara el manual de usuario en formato PDF.\n"
                           "Por implementar: Integracion con lector PDF.")
    
    def mostrar_manual_tecnico(self):
        """Mostrar manual tecnico"""
        messagebox.showinfo("Manual Tecnico", 
                           "Manual Tecnico\n\n"
                           "mostrara el manual tecnico en formato PDF.\n"
                           "Por implementar: Integracion con lector PDF.")
    
    def mostrar_ayuda(self):
        """Mostrar informacion de desarrolladores"""
        messagebox.showinfo("Ayuda - Desarrolladores",
                           "Analizador de Operaciones Aritmeticas\n\n"
                           "Desarrollado por:\n"
                           "- Walter\n"
                           "- Mario\n\n"
                           "Lenguajes Formales y Automatas\n"
                           "Seccion 02 - 2025S2")
    
    def resaltar_sintaxis(self):
        """Resaltar """
        pass

def main():
    root = tk.Tk()
    app = AnalizadorAritmeticoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()