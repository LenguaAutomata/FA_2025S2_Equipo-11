import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import sys

# Ajustar las importaciones según la estructura de carpetas
try:
    from analizador_lexico import AnalizadorLexico, Token, ErrorLexico
    from analizador_sintactico import AnalizadorSintactico, EjecutorOperaciones, NodoArbol
    from generador_arbol_graphviz import GeneradorArbolGraphviz
except ImportError:
    # Si estamos en la carpeta src, importar directamente
    from .analizador_lexico import AnalizadorLexico, Token, ErrorLexico
    from .analizador_sintactico import AnalizadorSintactico, EjecutorOperaciones, NodoArbol
    from .generador_arbol_graphviz import GeneradorArbolGraphviz

class AnalizadorAritmeticoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Operaciones Aritmeticas")
        self.root.geometry("800x600")
        
        self.analizador = AnalizadorLexico()
        self.archivo_actual = None
        self.base_dir = self.obtener_directorio_base()
        
        self.crear_interfaz()
    
    def obtener_directorio_base(self):
        """Obtener el directorio base del proyecto (Proyecto1)"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Si estamos en src, subir un nivel
        if os.path.basename(current_dir) == 'src':
            return os.path.dirname(current_dir)
        return current_dir
    
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
        
        self.cargar_ejemplo_complejo()
    
    def cargar_ejemplo_complejo(self):
        ejemplo = """
<Operacion= SUMA>
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
</Operacion>

<Operacion= SUMA>
<Numero> 5.4 </Numero>
<Operacion= MULTIPLICACION>
<Numero> 7.8 </Numero>
<Numero> 4.3 </Numero>
</Operacion>
</Operacion>

<Operacion= RESTA>
<Numero> 100 </Numero>
<Operacion= DIVISION>
<Numero> 50 </Numero>
<Numero> 2 </Numero>
</Operacion>
<Operacion= SUMA>
<Numero> 10 </Numero>
<Numero> 5 </Numero>
</Operacion>
</Operacion>

<Operacion= POTENCIA>
<Numero> 2 </Numero>
<Numero> 8 </Numero>
</Operacion>

<Operacion= RAIZ>
<Numero> 2 </Numero>
<Numero> 16 </Numero>
</Operacion>"""
        
        self.area_texto.insert(1.0, ejemplo)
    
    def abrir_archivo(self):
        # Buscar archivos en la carpeta ejemplos
        ejemplos_dir = os.path.join(self.base_dir, "ejemplos")
        if not os.path.exists(ejemplos_dir):
            ejemplos_dir = self.base_dir
            
        tipos_archivo = [("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        archivo = filedialog.askopenfilename(
            title="Abrir archivo", 
            initialdir=ejemplos_dir,
            filetypes=tipos_archivo
        )
        
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
                messagebox.showinfo("Exito", f"Archivo guardado como: {os.path.basename(archivo)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
    
    def analizar_codigo(self):
        contenido = self.area_texto.get(1.0, tk.END).strip()
        
        if not contenido:
            messagebox.showwarning("Advertencia", "El area de texto esta vacia")
            return
        
        try:
            # 1. Analisis Lexico
            tokens, errores = self.analizador.analizar(contenido)
            
            info_analisis = f"Analisis Lexico Completado:\n\nTokens reconocidos: {len(tokens)}\nErrores lexicos: {len(errores)}"
            
            if not errores:
                # 2. Analisis Sintactico
                analizador_sintactico = AnalizadorSintactico(tokens)
                operaciones = analizador_sintactico.parsear()
                
                info_analisis += f"\nOperaciones encontradas: {len(operaciones)}"
                
                if operaciones:
                    # 3. Ejecutar Operaciones
                    resultados = []
                    for i, operacion in enumerate(operaciones):
                        try:
                            resultado = EjecutorOperaciones.ejecutar(operacion)
                            expresion = EjecutorOperaciones.generar_expresion_matematica(operacion)
                            resultados.append({
                                'operacion': operacion,
                                'expresion': expresion,
                                'resultado': resultado,
                                'indice': i + 1
                            })
                        except Exception as e:
                            resultados.append({
                                'operacion': operacion,
                                'expresion': "ERROR",
                                'resultado': f"Error: {str(e)}",
                                'indice': i + 1
                            })
                    
                    # 4. Generar Archivos en el directorio base
                    self.crear_archivo_resultados(resultados)
                    self.crear_archivo_errores(errores)
                    
                    # 5. Generar diagramas de arbol SVG en el directorio base
                    archivos_svg = GeneradorArbolGraphviz.generar_arbol_svg(operaciones)
                    
                    info_analisis += f"\n\nDiagramas SVG generados: {len(archivos_svg)}"
                    info_analisis += f"\n\nArchivos generados:\n- Resultados.html\n- Errores.html\n- arbol_operacion_X.svg"
                    
                    # Mostrar resultados en consola tambien si se quiere
                    print("\n=== RESULTADOS DE OPERACIONES ===")
                    for resultado in resultados:
                        print(f"Operacion {resultado['indice']}: {resultado['expresion']} = {resultado['resultado']}")
                        
                else:
                    info_analisis += "\n\nNo se encontraron operaciones validas"
                    self.crear_archivo_errores(errores)
            else:
                self.crear_archivo_errores(errores)
                info_analisis += f"\n\nNo se ejecutaron operaciones debido a errores lexicos"
            
            messagebox.showinfo("Analisis Completado", info_analisis)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el analisis: {str(e)}")
    
    def crear_archivo_resultados(self, resultados):
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Resultados de Operaciones</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #2E86AB; color: white; }
        .resultado { font-weight: bold; color: #2E86AB; }
        .header { text-align: center; color: #2E86AB; }
        .error { color: #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">Resultados de Operaciones Aritmeticas</h1>
        <table>
            <tr>
                <th>No</th>
                <th>Operacion</th>
                <th>Expresion</th>
                <th>Resultado</th>
            </tr>"""
        
        for resultado in resultados:
            clase_resultado = "error" if "Error" in str(resultado['resultado']) else "resultado"
            html_content += f"""
            <tr>
                <td>{resultado['indice']}</td>
                <td>{resultado['operacion'].valor}</td>
                <td>{resultado['expresion']}</td>
                <td class="{clase_resultado}">{resultado['resultado']}</td>
            </tr>"""
        
        html_content += """
        </table>
    </div>
</body>
</html>"""
        
        output_path = os.path.join(self.base_dir, "Resultados.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def crear_archivo_errores(self, errores):
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Errores Lexicos</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f44336; color: white; }
        .header { text-align: center; color: #f44336; }
        .sin-errores { text-align: center; color: #4CAF50; font-size: 18px; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">REPORTE DE ERRORES LEXICOS</h1>"""
        
        if not errores:
            html_content += '<div class="sin-errores">No se encontraron errores lexicos</div>'
        else:
            html_content += """
        <table>
            <tr>
                <th>No</th>
                <th>Lexema</th>
                <th>Descripcion</th>
                <th>Linea</th>
                <th>Columna</th>
            </tr>"""
            
            for i, error in enumerate(errores, 1):
                html_content += f"""
            <tr>
                <td>{i}</td>
                <td><strong>{error.lexema}</strong></td>
                <td>{error.descripcion}</td>
                <td>{error.linea}</td>
                <td>{error.columna}</td>
            </tr>"""
            
            html_content += """
        </table>"""
        
        html_content += """
    </div>
</body>
</html>"""
        
        output_path = os.path.join(self.base_dir, "Errores.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def abrir_pdf(self, archivo_pdf):
        """Abrir un archivo PDF con el programa predeterminado"""
        try:
            if os.path.exists(archivo_pdf):
                if sys.platform == "win32":
                    os.startfile(archivo_pdf)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", archivo_pdf])
                else:  # Linux
                    subprocess.run(["xdg-open", archivo_pdf])
            else:
                messagebox.showerror("Error", f"El archivo PDF no se encuentra:\n{archivo_pdf}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el PDF: {str(e)}")
    
    def mostrar_manual_usuario(self):
        """Mostrar manual de usuario desde Documentos/"""
        archivo_manual = os.path.join(self.base_dir, "Documentos", "Manual de Usuario - Analizador de Operaciones Aritméticas - FA_2025S2_Equipo-11.pdf")
        if os.path.exists(archivo_manual):
            self.abrir_pdf(archivo_manual)
        else:
            messagebox.showinfo("Manual de Usuario", "Manual de Usuario:\n\n1. Escribe o carga codigo en el area de texto\n2. Haz clic en 'Analizar' para procesar\n3. Revisa los archivos generados:\n   - Resultados.html: Resultados numericos\n   - Errores.html: Reporte de errores\n   - arbol_operacion_X.svg: Diagramas de arbol")
    
    def mostrar_manual_tecnico(self):
        """Mostrar manual tecnico desde Documentos/"""
        archivo_manual = os.path.join(self.base_dir, "Documentos", "Manual Técnico - Analizador de Operaciones Aritméticas - FA_2025S2_Equipo-11.pdf")
        if os.path.exists(archivo_manual):
            self.abrir_pdf(archivo_manual)
        else:
            messagebox.showinfo("Manual Tecnico", "Manual Tecnico:\n\n- Desarrollado en Python\n- Analizador Lexico: Tabla de transiciones\n- Analizador Sintactico: Arbol de operaciones\n- Interfaz: Tkinter\n- Salidas: HTML y SVG")
    
    def mostrar_ayuda(self):
        messagebox.showinfo("Ayuda", "Desarrollado por:\n\n- Mario Miguel Arevalo Perez\n- Walter Francisco Melendez Aguilar\n- Para el curso de Lenguajes Formales y Automatas\n- 2025")

def main():
    root = tk.Tk()
    app = AnalizadorAritmeticoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()