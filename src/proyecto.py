import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from analizador_lexico import AnalizadorLexico, Token, ErrorLexico

class AnalizadorAritmeticoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Operaciones Aritmeticas")
        self.root.geometry("800x600")
        
        self.analizador = AnalizadorLexico()
        self.archivo_actual = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        frame_botones_superiores = ttk.Frame(main_frame)
        frame_botones_superiores.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.btn_abrir = ttk.Button(frame_botones_superiores, text="Abrir", command=self.abrir_archivo)
        self.btn_abrir.grid(row=0, column=0, padx=(0, 5))
        
        self.btn_guardar = ttk.Button(frame_botones_superiores, text="Guardar", command=self.guardar_archivo)
        self.btn_guardar.grid(row=0, column=1, padx=5)
        
        self.btn_guardar_como = ttk.Button(frame_botones_superiores, text="Guardar Como", command=self.guardar_como_archivo)
        self.btn_guardar_como.grid(row=0, column=2, padx=5)
        
        self.btn_analizar = ttk.Button(frame_botones_superiores, text="Analizar", command=self.analizar_codigo)
        self.btn_analizar.grid(row=0, column=3, padx=5)
        
        frame_botones_inferiores = ttk.Frame(main_frame)
        frame_botones_inferiores.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.btn_manual_usuario = ttk.Button(frame_botones_inferiores, text="Manual de Usuario", command=self.mostrar_manual_usuario)
        self.btn_manual_usuario.grid(row=0, column=0, padx=(0, 5))
        
        self.btn_manual_tecnico = ttk.Button(frame_botones_inferiores, text="Manual Tecnico", command=self.mostrar_manual_tecnico)
        self.btn_manual_tecnico.grid(row=0, column=1, padx=5)
        
        self.btn_ayuda = ttk.Button(frame_botones_inferiores, text="Ayuda", command=self.mostrar_ayuda)
        self.btn_ayuda.grid(row=0, column=2, padx=5)
        
        lbl_area_texto = ttk.Label(main_frame, text="Area de Texto:")
        lbl_area_texto.grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(0, 5))
        
        self.area_texto = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=80, height=30)
        self.area_texto.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        self.cargar_ejemplo_inicial()
    
    def cargar_ejemplo_inicial(self):
        ejemplo = """<Operacion= SUMA>
<Numero> 4.5 </Numero>
<Numero> 5.32 </Numero>
</Operacion>

<Operacion= RESTA>
<Numero> 84 </Numero>
<Numero> 33.7 </Numero>
</Operacion>

<Operacion= MULTIPLICACION>
<Numero> 5 </Numero>
<Numero> 7 </Numero>
</Operacion>"""
        
        self.area_texto.insert(1.0, ejemplo)
    
    def abrir_archivo(self):
        tipos_archivo = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        archivo = filedialog.askopenfilename(title="Abrir archivo", filetypes=tipos_archivo)
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                self.area_texto.delete(1.0, tk.END)
                self.area_texto.insert(1.0, contenido)
                self.archivo_actual = archivo
                
                messagebox.showinfo("Exito", f"Archivo cargado: {os.path.basename(archivo)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")
    
    def guardar_archivo(self):
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
        tipos_archivo = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        archivo = filedialog.asksaveasfilename(title="Guardar archivo como", defaultextension=".txt", filetypes=tipos_archivo)
        
        if archivo:
            try:
                contenido = self.area_texto.get(1.0, tk.END)
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                self.archivo_actual = archivo
                messagebox.showinfo("Exito", f"Archivo guardado como: {os.path.basename(archivo)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
    
    def analizar_codigo(self):
        contenido = self.area_texto.get(1.0, tk.END).strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "El area de texto esta vacia")
            return
        
        try:
            tokens, errores = self.analizador.analizar(contenido)
            
            info_analisis = f"Analisis Lexico Completado:\n\nTokens reconocidos: {len(tokens)}\nErrores encontrados: {len(errores)}"
            
            if not errores:
                self.crear_archivo_resultados(tokens)
                self.crear_archivo_errores(errores)
                info_analisis += f"\n\nArchivos generados:\n- Resultados.html\n- Errores.html"
            else:
                self.crear_archivo_errores(errores)
                info_analisis += f"\n\nNo se ejecutaron operaciones debido a errores lexicos"
            
            messagebox.showinfo("Analisis Completado", info_analisis)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el analisis: {str(e)}")
    
    def crear_archivo_resultados(self, tokens):
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Resultados de Operaciones</title>
</head>
<body>
    <h1>Resultados de Operaciones Aritmeticas</h1>
    <table border="1">
        <tr>
            <th>No</th>
            <th>Tipo</th>
            <th>Valor</th>
            <th>Linea</th>
            <th>Columna</th>
        </tr>"""
        
        for i, token in enumerate(tokens, 1):
            html_content += f"""
        <tr>
            <td>{i}</td>
            <td>{token.tipo}</td>
            <td>{token.valor}</td>
            <td>{token.linea}</td>
            <td>{token.columna}</td>
        </tr>"""
        
        html_content += """
    </table>
</body>
</html>"""
        
        with open("Resultados.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def crear_archivo_errores(self, errores):
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Errores Lexicos</title>
</head>
<body>
    <h1>REPORTE DE ERRORES</h1>"""
        
        if not errores:
            html_content += "<p>No se encontraron errores lexicos</p>"
        else:
            html_content += """
    <table border="1">
        <tr>
            <th>No</th>
            <th>Lexico</th>
            <th>Descripcion</th>
            <th>Linea</th>
            <th>Columna</th>
        </tr>"""
            
            for i, error in enumerate(errores, 1):
                html_content += f"""
        <tr>
            <td>{i}</td>
            <td>{error.lexema}</td>
            <td>{error.descripcion}</td>
            <td>{error.linea}</td>
            <td>{error.columna}</td>
        </tr>"""
            
            html_content += """
    </table>"""
        
        html_content += """
</body>
</html>"""
        
        with open("Errores.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def mostrar_manual_usuario(self):
        messagebox.showinfo("Manual de Usuario", "No implementado")
    
    def mostrar_manual_tecnico(self):
        messagebox.showinfo("Manual Tecnico", "No implementado")
    
    def mostrar_ayuda(self):
        messagebox.showinfo("Ayuda", "No implementado")

def main():
    root = tk.Tk()
    app = AnalizadorAritmeticoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()