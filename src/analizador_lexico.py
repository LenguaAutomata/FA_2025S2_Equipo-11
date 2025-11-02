# analizador_lexico_final.py

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna
    
    def __str__(self):
        return f"Token({self.tipo}, '{self.valor}', línea {self.linea}, columna {self.columna})"

class ErrorLexico:
    def __init__(self, lexema, linea, columna, descripcion):
        self.lexema = lexema
        self.linea = linea
        self.columna = columna
        self.descripcion = descripcion
    
    def __str__(self):
        return f"Error Léxico: '{self.lexema}' en línea {self.linea}, columna {self.columna} - {self.descripcion}"

class AnalizadorLexico:
    def __init__(self):
        # Palabras reservadas del lenguaje específico
        self.palabras_reservadas = {
            'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION',
            'POTENCIA', 'RAIZ', 'INVERSO', 'MOD',
            'OPERACION', 'NUMERO'
        }
    
    def es_letra(self, char):
        return char.isalpha() or char == '_'
    
    def es_digito(self, char):
        return char.isdigit()
    
    def es_espacio(self, char):
        return char in ' \t\n'
    
    def analizar(self, codigo):
        """
        Analizador léxico SIMPLIFICADO que procesa el código carácter por carácter
        """
        tokens = []
        errores = []
        
        linea = 1
        columna = 1
        i = 0
        n = len(codigo)
        
        while i < n:
            char = codigo[i]
            
            # Manejo de saltos de línea
            if char == '\n':
                linea += 1
                columna = 1
                i += 1
                continue
            
            # Ignorar espacios y tabs
            if char in '\t':
                columna += 1
                i += 1
                continue
            
            if char in ' ':
                columna += 1
                i += 1
                continue
            
            
            inicio_columna = columna
            
            if char == '<':
                # Verificar si es '</' (símbolo de cierre completo)
                if i + 1 < n and codigo[i + 1] == '/':
                    tokens.append(Token('SIMBOLO_CIERRE_COMPLETO', '</', linea, inicio_columna))
                    i += 2
                    columna += 2
                else:
                    # Es '<' simple
                    tokens.append(Token('SIMBOLO_APERTURA', '<', linea, inicio_columna))
                    i += 1
                    columna += 1
                continue
            
            elif char == '>':
                tokens.append(Token('SIMBOLO_CIERRE', '>', linea, inicio_columna))
                i += 1
                columna += 1
                continue
            
            elif char == '=':
                tokens.append(Token('IGUAL', '=', linea, inicio_columna))
                i += 1
                columna += 1
                continue
            
            # PALABRAS Y IDENTIFICADORES
            elif self.es_letra(char):
                lexema = ""
                while i < n and (self.es_letra(codigo[i]) or self.es_digito(codigo[i])):
                    lexema += codigo[i]
                    i += 1
                    columna += 1
                
                # Verificar si es palabra reservada
                lexema_upper = lexema.upper()
                if lexema_upper in self.palabras_reservadas:
                    tokens.append(Token('PALABRA_RESERVADA', lexema_upper, linea, inicio_columna))
                else:
                    tokens.append(Token('IDENTIFICADOR', lexema, linea, inicio_columna))
                continue
            
            # NÚMEROS (enteros y decimales)
            elif self.es_digito(char):
                lexema = ""
                tiene_punto = False
                es_valido = True
                
                while i < n and (self.es_digito(codigo[i]) or codigo[i] == '.'):
                    if codigo[i] == '.':
                        if tiene_punto:  # Ya tenía un punto, error
                            es_valido = False
                        tiene_punto = True
                    
                    lexema += codigo[i]
                    i += 1
                    columna += 1
                
                if es_valido and tiene_punto:
                    # Verificar que tenga dígitos después del punto
                    if lexema.endswith('.'):
                        errores.append(ErrorLexico(lexema, linea, inicio_columna, "Número decimal incompleto"))
                    else:
                        tokens.append(Token('NUMERO_DECIMAL', lexema, linea, inicio_columna))
                elif es_valido:
                    tokens.append(Token('NUMERO_ENTERO', lexema, linea, inicio_columna))
                else:
                    errores.append(ErrorLexico(lexema, linea, inicio_columna, "Formato de número inválido"))
                continue
            
            # CARACTERES NO RECONOCIDOS
            else:
                if char not in ' \t\n':  # No reportar espacios
                    errores.append(ErrorLexico(
                        char, linea, columna,
                        f"Carácter '{char}' no reconocido"
                    ))
                i += 1
                columna += 1
        
        return tokens, errores