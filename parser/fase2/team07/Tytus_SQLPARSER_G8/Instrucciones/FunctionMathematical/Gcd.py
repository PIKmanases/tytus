import math
from Instrucciones.TablaSimbolos.Instruccion import Instruccion
from Instrucciones.TablaSimbolos.Tipo import Tipo_Dato, Tipo
from Instrucciones.Excepcion import Excepcion
from Instrucciones.TablaSimbolos.Simbolo3D import Simbolo3d

# Esta función unicamente acepta enteros.
class Gcd(Instruccion):
    def __init__(self, opIzq, opDer, strGram, linea, columna, strSent):
        Instruccion.__init__(self,Tipo("",Tipo_Dato.NUMERIC),linea,columna,strGram,strSent)
        self.opIzq = opIzq
        self.opDer = opDer

    def ejecutar(self, tabla, arbol):
        super().ejecutar(tabla,arbol)
        # Si existe algún error en el operador izquierdo, retorno el error.
        resultadoIzq = self.opIzq.ejecutar(tabla, arbol)
        if isinstance(resultadoIzq, Excepcion):
            return resultadoIzq
        # Si existe algún error en el operador derecho, retorno el error.
        resultadoDer = self.opDer.ejecutar(tabla, arbol)
        if isinstance(resultadoDer, Excepcion):
            return resultadoDer
        if self.opIzq.tipo.tipo == Tipo_Dato.INTEGER and self.opDer.tipo.tipo == Tipo_Dato.INTEGER:
            if resultadoDer < 0 or resultadoIzq < 0:
                error = Excepcion('42883',"Semántico","La función GCD únicamente acepta valores númericos positivos",self.linea,self.columna)
                arbol.excepciones.append(error)
                arbol.consola.append(error.toString())
                return error

            self.tipo = Tipo("",Tipo_Dato.INTEGER)
            return math.gcd(resultadoIzq, resultadoDer)
        else:
            error = Excepcion('42883',"Semántico","No existe la función gcd("+self.opIzq.tipo.toString()+", "+self.opDer.tipo.toString()+")",self.linea,self.columna)
            arbol.excepciones.append(error)
            arbol.consola.append(error.toString())
            return error

    def traducir(self, tabla, arbol, cadenaTraducida):
        resultado = self.ejecutar(tabla, arbol)
        if isinstance(resultado,Excepcion):
            return resultado        
        codigo = ""
        temporal = arbol.generaTemporal()
        codigo += "\t" + temporal + " = " + str(resultado) + "\n"
        nuevo = Simbolo3d(self.tipo, temporal, codigo, None, None)
        return nuevo
