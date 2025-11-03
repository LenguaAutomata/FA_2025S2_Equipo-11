import os
import subprocess
import tempfile

class GeneradorArbolGraphviz:
    """Clase para generar diagramas de árbol en SVG usando Graphviz"""
    
    @staticmethod
    def generar_arbol_svg(operaciones):
        """
        Generar diagramas de árbol para cada operación en SVG
        
        Args:
            operaciones: Lista de nodos de operaciones
        """
        archivos_generados = []
        
        for i, operacion in enumerate(operaciones):
            try:
                # Generar código DOT para esta operación
                dot_content = GeneradorArbolGraphviz._generar_dot(operacion, f"Operacion_{i+1}")
                
                # Crear archivo temporal para DOT
                with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False, encoding='utf-8') as dot_file:
                    dot_file.write(dot_content)
                    dot_path = dot_file.name
                
                # Nombre del archivo de salida
                output_file = f"arbol_operacion_{i+1}.svg"
                
                # Ejecutar Graphviz
                if GeneradorArbolGraphviz._ejecutar_graphviz(dot_path, output_file):
                    archivos_generados.append(output_file)
                
                # Limpiar archivo temporal
                os.unlink(dot_path)
                
            except Exception as e:
                print(f"Error generando arbol para operacion {i+1}: {e}")
        
        return archivos_generados
    
    @staticmethod
    def _generar_dot(nodo, nombre_operacion):
        """Generar código DOT para Graphviz"""
        dot_lines = [
            'digraph G {',
            '    rankdir=TB;',
            '    node [shape=box, style="filled,rounded", fontname="Arial", fontsize=12, penwidth=2];',
            '    edge [arrowhead=none, penwidth=2];',
            '    bgcolor="white";',
            '',
            f'    label="{nombre_operacion}";',
            '    labelloc=t;',
            '    fontsize=20;',
            '    fontname="Arial";',
            ''
        ]
        
        # Generar nodos y conexiones
        nodo_id = 0
        stack = [(nodo, f"nodo_{nodo_id}", None)]
        dot_lines.append(f'    nodo_{nodo_id} [label="{GeneradorArbolGraphviz._formatear_etiqueta(nodo)}", fillcolor="{GeneradorArbolGraphviz._obtener_color(nodo)}", color="{GeneradorArbolGraphviz._obtener_borde(nodo)}"];')
        nodo_id += 1
        
        while stack:
            current_node, current_id, parent_id = stack.pop(0)
            
            # Agregar conexión con el padre
            if parent_id is not None:
                dot_lines.append(f'    {parent_id} -> {current_id} [color="{GeneradorArbolGraphviz._obtener_color_linea(current_node)}"];')
            
            # Procesar hijos
            for hijo in current_node.hijos:
                hijo_id = f"nodo_{nodo_id}"
                dot_lines.append(f'    {hijo_id} [label="{GeneradorArbolGraphviz._formatear_etiqueta(hijo)}", fillcolor="{GeneradorArbolGraphviz._obtener_color(hijo)}", color="{GeneradorArbolGraphviz._obtener_borde(hijo)}"];')
                stack.append((hijo, hijo_id, current_id))
                nodo_id += 1
        
        dot_lines.append('}')
        return '\n'.join(dot_lines)
    
    @staticmethod
    def _formatear_etiqueta(nodo):
        """Formatear la etiqueta del nodo para Graphviz"""
        if nodo.tipo == 'NUMERO':
            return f"Numero\\n{nodo.valor}"
        else:
            resultado = f"{nodo.resultado:.2f}" if hasattr(nodo, 'resultado') and nodo.resultado is not None else "?"
            return f"{nodo.valor}\\n= {resultado}"
    
    @staticmethod
    def _obtener_color(nodo):
        """Obtener color del nodo segun su tipo"""
        if nodo.tipo == 'NUMERO':
            return "#e8f5e8"  # Verde claro
        elif nodo.valor in ['SUMA', 'RESTA']:
            return "#e3f2fd"  # Azul claro
        elif nodo.valor in ['MULTIPLICACION', 'DIVISION']:
            return "#fff3e0"  # Naranja claro
        elif nodo.valor in ['POTENCIA', 'RAIZ']:
            return "#f3e5f5"  # Purple claro
        else:
            return "#f5f5f5"  # Gris claro
    
    @staticmethod
    def _obtener_borde(nodo):
        """Obtener color del borde del nodo"""
        if nodo.tipo == 'NUMERO':
            return "#4caf50"  # Verde
        elif nodo.valor in ['SUMA', 'RESTA']:
            return "#2196f3"  # Azul
        elif nodo.valor in ['MULTIPLICACION', 'DIVISION']:
            return "#ff9800"  # Naranja
        elif nodo.valor in ['POTENCIA', 'RAIZ']:
            return "#9c27b0"  # Purple
        else:
            return "#9e9e9e"  # Gris
    
    @staticmethod
    def _obtener_color_linea(nodo):
        """Obtener color de la linea de conexion"""
        if nodo.tipo == 'NUMERO':
            return "#4caf50"
        elif nodo.valor in ['SUMA', 'RESTA']:
            return "#2196f3"
        elif nodo.valor in ['MULTIPLICACION', 'DIVISION']:
            return "#ff9800"
        elif nodo.valor in ['POTENCIA', 'RAIZ']:
            return "#9c27b0"
        else:
            return "#9e9e9e"
    
    @staticmethod
    def _ejecutar_graphviz(dot_path, output_file):
        """Ejecutar Graphviz para generar el diagrama SVG"""
        try:
            # Verificar si Graphviz esta instalado
            try:
                subprocess.run(['dot', '-V'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Graphviz no esta instalado. Instalalo desde: https://graphviz.org/download/")
                return False
            
            # Ejecutar dot para generar SVG
            subprocess.run(['dot', '-Tsvg', dot_path, '-o', output_file], check=True)
            
            print(f"Diagrama SVG generado: {output_file}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando Graphviz: {e}")
            return False