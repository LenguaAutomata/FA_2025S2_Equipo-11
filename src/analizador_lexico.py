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
        self.palabras_reservadas = {
            'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION',
            'POTENCIA', 'RAIZ', 'INVERSO', 'MOD',
            'OPERACION', 'NUMERO'
        }
        
        self.estado_inicial = 0
        
        self.tabla_transiciones = {
            0: {'<': 4, '>': 5, '=': 7, 'LETRA': 1, 'DIGITO': 2, '/': 6, 'ESPACIO': 0, 'OTRO': -2},
            1: {'LETRA': 1, 'DIGITO': 1, 'OTRO': -1},
            2: {'DIGITO': 2, '.': 3, 'OTRO': -1},
            3: {'DIGITO': 8, 'OTRO': -2},
            4: {'OTRO': -1},
            5: {'OTRO': -1},
            6: {'OTRO': -1},
            7: {'OTRO': -1},
            8: {'DIGITO': 8, 'OTRO': -1}
        }
        
        self.estados_aceptacion = {
            1: 'PALABRA_RESERVADA',
            2: 'NUMERO_ENTERO',
            8: 'NUMERO_DECIMAL',
            4: 'SIMBOLO_APERTURA',
            5: 'SIMBOLO_CIERRE',
            6: 'SIMBOLO_CIERRE_COMPLETO',
            7: 'IGUAL'
        }
    
    def es_letra(self, char):
        return char.isalpha() or char == '_'
    
    def es_digito(self, char):
        return char.isdigit()
    
    def es_espacio(self, char):
        return char in ' \t\n'
    
    def obtener_tipo_caracter(self, char):
        if self.es_letra(char):
            return 'LETRA'
        elif self.es_digito(char):
            return 'DIGITO'
        elif char in '<>=/':
            return char
        elif char == '.':
            return '.'
        elif self.es_espacio(char):
            return 'ESPACIO'
        else:
            return 'OTRO'
    
    def analizar(self, codigo):
        tokens = []
        errores = []
        
        linea = 1
        columna = 1
        i = 0
        n = len(codigo)
        
        while i < n:
            char = codigo[i]
            
            if char == '\n':
                linea += 1
                columna = 1
                i += 1
                continue
            
            if char in ' \t':
                columna += 1
                i += 1
                continue
            
            lexema = ""
            estado_actual = self.estado_inicial
            inicio_columna = columna
            token_completado = False
            
            while i < n and not token_completado:
                char = codigo[i]
                tipo_char = self.obtener_tipo_caracter(char)
                
                if tipo_char in self.tabla_transiciones[estado_actual]:
                    nuevo_estado = self.tabla_transiciones[estado_actual][tipo_char]
                elif 'OTRO' in self.tabla_transiciones[estado_actual]:
                    nuevo_estado = self.tabla_transiciones[estado_actual]['OTRO']
                else:
                    break
                
                if nuevo_estado == -1:
                    token_completado = True
                elif nuevo_estado == -2:
                    errores.append(ErrorLexico(lexema + char, linea, inicio_columna, "Formato invalido"))
                    token_completado = True
                    i += 1
                    columna += 1
                else:
                    estado_actual = nuevo_estado
                    lexema += char
                    i += 1
                    columna += 1
                
                if (i < n and codigo[i] in ' \t\n' and nuevo_estado not in [-1, -2]):
                    token_completado = True
            
            if (lexema and estado_actual in self.estados_aceptacion and
                not any(error.lexema == lexema for error in errores)):
                
                tipo_token = self.estados_aceptacion[estado_actual]
                
                if tipo_token == 'PALABRA_RESERVADA':
                    lexema_upper = lexema.upper()
                    if lexema_upper in self.palabras_reservadas:
                        tokens.append(Token('PALABRA_RESERVADA', lexema_upper, linea, inicio_columna))
                    else:
                        tokens.append(Token('IDENTIFICADOR', lexema, linea, inicio_columna))
                else:
                    tokens.append(Token(tipo_token, lexema, linea, inicio_columna))
                    
            elif lexema and not token_completado:
                errores.append(ErrorLexico(lexema, linea, inicio_columna, "Secuencia no valida"))
            
            if not lexema and i < n:
                if char not in ' \t\n':
                    errores.append(ErrorLexico(char, linea, columna, f"Caracter no reconocido"))
                i += 1
                columna += 1
        
        return tokens, errores