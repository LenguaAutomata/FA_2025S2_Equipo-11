import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from analizador_lexico import AnalizadorLexico, Token, ErrorLexico
from analizador_sintactico import AnalizadorSintactico, EjecutorOperaciones, NodoArbol

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
            # 1. Análisis Léxico
            tokens, errores = self.analizador.analizar(contenido)
            
            info_analisis = f"Analisis Léxico Completado:\n\nTokens reconocidos: {len(tokens)}\nErrores léxicos: {len(errores)}"
            
            if not errores:
                # 2. Análisis Sintáctico
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
                    
                    # 4. Generar Archivos
                    self.crear_archivo_resultados(resultados)
                    self.crear_diagrama_arbol_html(operaciones)
                    self.crear_archivo_errores(errores)
                    
                    info_analisis += f"\n\nArchivos generados:\n- Resultados.html\n- Errores.html\n- ArbolOperaciones.html"
                    
                    # Mostrar resultados en consola también
                    print("\n=== RESULTADOS DE OPERACIONES ===")
                    for resultado in resultados:
                        print(f"Operación {resultado['indice']}: {resultado['expresion']} = {resultado['resultado']}")
                        
                else:
                    info_analisis += "\n\nNo se encontraron operaciones válidas"
                    self.crear_archivo_errores(errores)
            else:
                self.crear_archivo_errores(errores)
                info_analisis += f"\n\nNo se ejecutaron operaciones debido a errores léxicos"
            
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
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">Resultados de Operaciones Aritméticas</h1>
        <table>
            <tr>
                <th>No</th>
                <th>Operación</th>
                <th>Expresión</th>
                <th>Resultado</th>
            </tr>"""
        
        for resultado in resultados:
            html_content += f"""
            <tr>
                <td>{resultado['indice']}</td>
                <td>{resultado['operacion'].valor}</td>
                <td>{resultado['expresion']}</td>
                <td class="resultado">{resultado['resultado']}</td>
            </tr>"""
        
        html_content += """
        </table>
    </div>
</body>
</html>"""
        
        with open("Resultados.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def crear_diagrama_arbol_html(self, operaciones):
        """Crear diagrama de árbol en formato HTML"""
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Diagrama de Árbol de Operaciones</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .nodo { margin: 10px 0; padding: 12px; border-radius: 5px; transition: all 0.3s; }
        .nodo:hover { transform: translateX(5px); }
        .operacion { background-color: #e3f2fd; border-left: 4px solid #2196F3; font-weight: bold; }
        .numero { background-color: #e8f5e8; border-left: 4px solid #4CAF50; }
        .resultado { color: #FF5722; font-weight: bold; }
        .header { text-align: center; color: #2E86AB; margin-bottom: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">Diagrama de Árbol de Operaciones</h1>"""
        
        for i, operacion in enumerate(operaciones):
            html_content += f"""
        <div class="operacion-seccion">
            <h2>Operación {i+1}: {operacion.valor}</h2>
            {EjecutorOperaciones.generar_html_arbol(operacion)}
        </div>"""
        
        html_content += """
    </div>
</body>
</html>"""
        
        with open("ArbolOperaciones.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def crear_archivo_errores(self, errores):
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Errores Léxicos</title>
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
        <h1 class="header">REPORTE DE ERRORES LÉXICOS</h1>"""
        
        if not errores:
            html_content += '<div class="sin-errores">✅ No se encontraron errores léxicos</div>'
        else:
            html_content += """
        <table>
            <tr>
                <th>No</th>
                <th>Lexema</th>
                <th>Descripción</th>
                <th>Línea</th>
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
        
        with open("Errores.html", "w", encoding="utf-8") as f:
            f.write(html_content)
    
    def mostrar_manual_usuario(self):
        messagebox.showinfo("Manual de Usuario", "Manual de Usuario:\n\n1. Escribe o carga código en el área de texto\n2. Haz clic en 'Analizar' para procesar\n3. Revisa los archivos generados: Resultados.html, Errores.html, ArbolOperaciones.html")
    
    def mostrar_manual_tecnico(self):
        messagebox.showinfo("Manual Tecnico", "Manual Técnico:\n\n- Desarrollado en Python 3.13\n- Analizador Léxico: Tabla de transiciones\n- Analizador Sintáctico: Árbol de operaciones\n- Interfaz: Tkinter\n- Salidas: HTML")
    
    def mostrar_ayuda(self):
        messagebox.showinfo("Ayuda", "Desarrollado por:\n\n- Tu nombre aquí\n- Para el curso de Lenguajes Formales y Autómatas\n- 2025")

def main():
    root = tk.Tk()
    app = AnalizadorAritmeticoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()