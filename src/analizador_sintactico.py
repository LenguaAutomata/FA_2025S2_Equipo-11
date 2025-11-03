class NodoArbol:
    """Clase para representar nodos del árbol de operaciones"""
    def __init__(self, tipo, valor=None):
        self.tipo = tipo  # 'OPERACION' o 'NUMERO'
        self.valor = valor  # Tipo de operación o valor numérico
        self.hijos = []  # Nodos hijos
        self.resultado = None  # Resultado de la operación
    
    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
    
    def __str__(self):
        return f"{self.tipo}({self.valor})"

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion_actual = 0
        self.operaciones = []
    
    def token_actual(self):
        if self.posicion_actual < len(self.tokens):
            return self.tokens[self.posicion_actual]
        return None
    
    def avanzar(self):
        if self.posicion_actual < len(self.tokens):
            self.posicion_actual += 1
        return self.token_actual()
    
    def coincidir(self, tipo_esperado, valor_esperado=None):
        token = self.token_actual()
        if token and token.tipo == tipo_esperado:
            if valor_esperado is None or token.valor == valor_esperado:
                resultado = token
                self.avanzar()
                return resultado
        return None
    
    def parsear(self):
        """Método principal para parsear todas las operaciones"""
        self.operaciones = []
        
        while self.posicion_actual < len(self.tokens):
            # Buscar inicio de operación
            if (self.token_actual() and 
                self.token_actual().tipo == 'SIMBOLO_APERTURA' and
                self.posicion_actual + 1 < len(self.tokens) and
                self.tokens[self.posicion_actual + 1].tipo == 'PALABRA_RESERVADA' and
                self.tokens[self.posicion_actual + 1].valor == 'OPERACION'):
                
                operacion = self.parsear_operacion()
                if operacion:
                    self.operaciones.append(operacion)
                else:
                    self.avanzar()
            else:
                self.avanzar()
        
        return self.operaciones
    
    def parsear_operacion(self):
        """Parsear una operación individual: <Operacion= TIPO> ... </Operacion>"""
        inicio_pos = self.posicion_actual
        
        # Verificar estructura: <Operacion= TIPO>
        if not (self.coincidir('SIMBOLO_APERTURA') and 
                self.coincidir('PALABRA_RESERVADA', 'OPERACION') and 
                self.coincidir('IGUAL')):
            self.posicion_actual = inicio_pos
            return None
        
        # Obtener tipo de operación
        token_operacion = self.coincidir('PALABRA_RESERVADA')
        if not token_operacion:
            self.posicion_actual = inicio_pos
            return None
        
        if not self.coincidir('SIMBOLO_CIERRE'):
            self.posicion_actual = inicio_pos
            return None
        
        # Crear nodo de operación
        nodo_operacion = NodoArbol('OPERACION', token_operacion.valor)
        
        # Parsear contenido (números u operaciones anidadas)
        while self.posicion_actual < len(self.tokens):
            # Verificar si es el cierre de la operación actual
            if (self.token_actual() and 
                self.token_actual().tipo == 'SIMBOLO_APERTURA' and
                self.posicion_actual + 1 < len(self.tokens) and
                self.tokens[self.posicion_actual + 1].tipo == 'SIMBOLO_CIERRE_COMPLETO' and
                self.posicion_actual + 2 < len(self.tokens) and
                self.tokens[self.posicion_actual + 2].valor == 'OPERACION'):
                
                # Consumir </Operacion>
                self.avanzar()  # <
                self.avanzar()  # /
                self.avanzar()  # OPERACION
                if self.token_actual() and self.token_actual().tipo == 'SIMBOLO_CIERRE':
                    self.avanzar()  # >
                break
            
            # Verificar si es una operación anidada
            if (self.token_actual() and 
                self.token_actual().tipo == 'SIMBOLO_APERTURA' and
                self.posicion_actual + 1 < len(self.tokens) and
                self.tokens[self.posicion_actual + 1].tipo == 'PALABRA_RESERVADA' and
                self.tokens[self.posicion_actual + 1].valor == 'OPERACION'):
                
                # Parsear operación anidada
                operacion_anidada = self.parsear_operacion()
                if operacion_anidada:
                    nodo_operacion.agregar_hijo(operacion_anidada)
                    continue
                else:
                    self.avanzar()
                    continue
            
            # Parsear número
            numero = self.parsear_numero()
            if numero:
                nodo_operacion.agregar_hijo(numero)
            else:
                self.avanzar()
        
        return nodo_operacion
    
    def parsear_numero(self):
        """Parsear un número: <Numero> VALOR </Numero>"""
        inicio_pos = self.posicion_actual
        
        # Verificar estructura: <Numero>
        if not (self.coincidir('SIMBOLO_APERTURA') and 
                self.coincidir('PALABRA_RESERVADA', 'NUMERO') and 
                self.coincidir('SIMBOLO_CIERRE')):
            self.posicion_actual = inicio_pos
            return None
        
        # Obtener valor numérico
        token_numero = self.token_actual()
        if not token_numero or (token_numero.tipo != 'NUMERO_ENTERO' and token_numero.tipo != 'NUMERO_DECIMAL'):
            self.posicion_actual = inicio_pos
            return None
        
        valor = token_numero.valor
        self.avanzar()  # Consumir el token del número
        
        # Verificar cierre: </Numero>
        if not (self.coincidir('SIMBOLO_APERTURA') and 
                self.coincidir('SIMBOLO_CIERRE_COMPLETO') and 
                self.coincidir('PALABRA_RESERVADA', 'NUMERO') and 
                self.coincidir('SIMBOLO_CIERRE')):
            self.posicion_actual = inicio_pos
            return None
        
        return NodoArbol('NUMERO', float(valor))

class EjecutorOperaciones:
    """Clase para ejecutar las operaciones y calcular resultados"""
    
    @staticmethod
    def ejecutar(nodo):
        """Ejecutar recursivamente un nodo del árbol"""
        if nodo.tipo == 'NUMERO':
            return float(nodo.valor)
        
        if nodo.tipo == 'OPERACION':
            # Ejecutar hijos primero (recursivamente)
            resultados_hijos = [EjecutorOperaciones.ejecutar(hijo) for hijo in nodo.hijos]
            
            if not resultados_hijos:
                return 0
            
            # Aplicar operación
            if nodo.valor == 'SUMA':
                resultado = sum(resultados_hijos)
            elif nodo.valor == 'RESTA':
                resultado = resultados_hijos[0]
                for num in resultados_hijos[1:]:
                    resultado -= num
            elif nodo.valor == 'MULTIPLICACION':
                resultado = 1
                for num in resultados_hijos:
                    resultado *= num
            elif nodo.valor == 'DIVISION':
                if len(resultados_hijos) < 2:
                    raise ValueError("División requiere al menos 2 operandos")
                resultado = resultados_hijos[0]
                for num in resultados_hijos[1:]:
                    if num == 0:
                        raise ValueError("División por cero")
                    resultado /= num
            elif nodo.valor == 'POTENCIA':
                if len(resultados_hijos) != 2:
                    raise ValueError("Potencia requiere exactamente 2 operandos")
                resultado = resultados_hijos[0] ** resultados_hijos[1]
            elif nodo.valor == 'RAIZ':
                if len(resultados_hijos) != 2:
                    raise ValueError("Raíz requiere exactamente 2 operandos")
                resultado = resultados_hijos[1] ** (1 / resultados_hijos[0])
            elif nodo.valor == 'INVERSO':
                if len(resultados_hijos) != 1:
                    raise ValueError("Inverso requiere exactamente 1 operando")
                if resultados_hijos[0] == 0:
                    raise ValueError("Inverso de cero no está definido")
                resultado = 1 / resultados_hijos[0]
            elif nodo.valor == 'MOD':
                if len(resultados_hijos) != 2:
                    raise ValueError("MOD requiere exactamente 2 operandos")
                if resultados_hijos[1] == 0:
                    raise ValueError("MOD por cero no está definido")
                resultado = resultados_hijos[0] % resultados_hijos[1]
            else:
                raise ValueError(f"Operación no soportada: {nodo.valor}")
            
            nodo.resultado = resultado
            return resultado
        
        return 0

    @staticmethod
    def generar_expresion_matematica(nodo):
        """Generar expresión matemática legible para mostrar en resultados"""
        if nodo.tipo == 'NUMERO':
            return str(nodo.valor)
        
        if nodo.tipo == 'OPERACION':
            expresiones_hijos = [EjecutorOperaciones.generar_expresion_matematica(hijo) for hijo in nodo.hijos]
            
            if nodo.valor == 'SUMA':
                if len(expresiones_hijos) > 1:
                    return "(" + " + ".join(expresiones_hijos) + ")"
                else:
                    return expresiones_hijos[0]
            elif nodo.valor == 'RESTA':
                if len(expresiones_hijos) > 1:
                    return "(" + " - ".join(expresiones_hijos) + ")"
                else:
                    return expresiones_hijos[0]
            elif nodo.valor == 'MULTIPLICACION':
                if len(expresiones_hijos) > 1:
                    return "(" + " * ".join(expresiones_hijos) + ")"
                else:
                    return expresiones_hijos[0]
            elif nodo.valor == 'DIVISION':
                if len(expresiones_hijos) > 1:
                    return "(" + " / ".join(expresiones_hijos) + ")"
                else:
                    return expresiones_hijos[0]
            elif nodo.valor == 'POTENCIA':
                if len(expresiones_hijos) == 2:
                    return f"({expresiones_hijos[0]} ^ {expresiones_hijos[1]})"
                else:
                    return f"potencia{tuple(expresiones_hijos)}"
            elif nodo.valor == 'RAIZ':
                if len(expresiones_hijos) == 2:
                    return f"raiz({expresiones_hijos[0]}, {expresiones_hijos[1]})"
                else:
                    return f"raiz{tuple(expresiones_hijos)}"
            elif nodo.valor == 'INVERSO':
                if len(expresiones_hijos) == 1:
                    return f"inverso({expresiones_hijos[0]})"
                else:
                    return f"inverso{tuple(expresiones_hijos)}"
            elif nodo.valor == 'MOD':
                if len(expresiones_hijos) == 2:
                    return f"({expresiones_hijos[0]} % {expresiones_hijos[1]})"
                else:
                    return f"mod{tuple(expresiones_hijos)}"
            else:
                return f"{nodo.valor}({', '.join(expresiones_hijos)})"
        
        return ""