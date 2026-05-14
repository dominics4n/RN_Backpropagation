from math import exp
from random import seed
from random import random
import csv

seed("LindaLindaLinda")

class Neuronas:
    pesos = []
    error = 0
    salida = 0

#Encuentra el valor minimo y maximo de cada categoria
def MinMax(categorias):
    MinVal = []
    MaxMinVal = []
    for categoria in categorias:
        minimo = min(categoria)
        maximo = max(categoria)
        MinVal.append(minimo)
        MaxMinVal.append(maximo - minimo)
    return [MinVal, MaxMinVal]

#Normalizacion de los datos para su uso en la Red Neuronal
def Normalizar(categorias, min, max_min):
    Normalizados = []
    for i in range(len(categorias[0])):
        datos = []
        for j in range(len(categorias)):
            datos.append((categorias[j][i]-min[j])/max_min[j])
        Normalizados.append(datos)
    return Normalizados

#Creacion de la Red NEuronal
def Crear_Red(parametros, num_N_ini, num_N_mid, num_N_fin):
    red = []
    #Por cada capa
    for C_W in [[num_N_ini, parametros], [num_N_mid, num_N_ini], [num_N_fin, num_N_mid]]:
        Capa = []
        for n in range(C_W[0]):
            #Crea una Neurona
            Capa.append(Neuronas())
            datos = []
            #Crea los pesos de la neurona
            for w in range(C_W[1]):
                datos.append(random())
            Capa[n].pesos = datos
        red.append(Capa)
    return red
            
def Activar_Neurona(Entradas, Neurona):
    S = 0
    #Producto Escalar
    for x in range(len(Entradas)):
        S = S + Entradas[x] * Neurona.pesos[x]
    #Funcion de Activacion
    return 1.0 / (1.0 + exp(-S))

def Propagar_Entradas(Red_N, Soli_B):
    entradas = Soli_B
    for capas in Red_N:
        Salidas = []
        for neurona in capas:
            fun_act = Activar_Neurona(entradas, neurona)
            Salidas.append(fun_act)
            neurona.salida = fun_act
        #Usamos las Salidas como entradas para la siguiente Capa
        entradas = Salidas
    return Salidas

def Propagar_Errores(Red_N, Resultado):
    #Comenzamos desde la ultima capa
    for i in reversed(range(len(Red_N))):
        capa = Red_N[i]
        error_base = []
        #Revisamos si nos encontramos en la ultima capa
        if i != len(Red_N) - 1:
            for j in range(len(capa)):
                error = 0
                #Sumamos los errores de la capa superior
                for neurona in Red_N[i + 1]:
                    error = error + (neurona.pesos[j] * neurona.error)
                error_base.append(error)
        else:
            for neurona in capa:
                error_base.append(neurona.salida - Resultado)
        for j in range(len(capa)):
            capa[j].error = error_base[j] * (capa[j].salida * (1 - capa[j].salida))

def Actualizar_Pesos(Red_N, Soli_Beca, B):
    inputs = Soli_Beca
    for i in range(len(Red_N)):
        Nuevos_Inputs = []
        for neurona in Red_N[i]:
            for j in range(len(inputs)):
                #Ley del cuadrado minimo
                neurona.pesos[j] = neurona.pesos[j] - B * neurona.error * inputs[j]
            Nuevos_Inputs.append(neurona.salida)
        inputs = Nuevos_Inputs

def Entrena(Red_N, Set_Entrenamiento, B, n_rondas, resultados, FrecuenciaPrint, NivelPrint):
    printcount = FrecuenciaPrint
    for ronda in range(n_rondas):
        sum_error = 0
        num_error = 0
        soli = 0
        kys = 0
        for row in Set_Entrenamiento:
            output = Propagar_Entradas(Red_N, row)
            if nivelprint == 2:
                if printcount == FrecuenciaPrint:
                    print("\tSolicitud "+str(soli)+".- Prediccion: "+str(output[0])+"  Esperado: " + str(resultados[kys]))
            soli += 1
            sum_error += abs(resultados[kys]-output[0])
            if abs(resultados[kys]-output[0]) > 0.1:
                num_error += 1
            Propagar_Errores(Red_N, resultados[kys])
            Actualizar_Pesos(Red_N, row, B)
            kys = kys + 1
        if NivelPrint != 0:
            if printcount == FrecuenciaPrint:
                print('>Ronda %d: Errores=%d, Sumatoria de errores=%.3f' % (ronda, num_error, sum_error))
                printcount = 0
            else:
                printcount += 1
    
def Predecir(Red_N, Solicitud):
    Prediccion = Propagar_Entradas(Red_N, Solicitud)
    print("La prediccion del sistema es: "+str(Prediccion[0]))
    if(Prediccion[0] > 0.5):
        print("La beca fue aceptada")
    else:
        print("La beca fue rechazada")

def Preguntas_Input():
    #Pregunta edad
    valido = False
    while not valido:
        try:
            Edad = float(input("Ingresa la edad del aspirante: "))
            if Edad < 1 or Edad > 99:
                print("Ingresa una edad valida")
            else:
                valido = True
        except ValueError:
            print("Ingresa una edad valida")
    #Pregunta Ingreso
    valido = False
    while not valido:
        try:
            Ingreso = float(input("Ingresa el ingreso mensual del aspirante: "))
            if Ingreso < 0:
                print("Ingresa un ingreso valido")
            else:
                valido = True
        except ValueError:
            print("Ingresa un ingreso valido")
    #Pregunta Calificacion
    valido = False
    while not valido:
        try:
            Calificacion = float(input("Ingresa el Promedio escolar del aspirante: "))
            if Calificacion < 0 or Calificacion > 10:
                print("Ingresa un promedio valido")
            else:
                valido = True
        except ValueError:
            print("Ingresa un promedio valido")
    #Pregunta Modalidad Escolar
    valido = False
    while not valido:
        try:
            Modalidad = float(input("Ingresa la Modalidad Escolar del aspirante\n\t1.- Presencial\n\t2.- A Distancia\n"))
            if Modalidad == 1 or Modalidad == 2:
                valido = True
            else:
                print("Ingresa una Modalidad Escolar valida")
        except ValueError:
            print("Ingresa una Modalidad Escolar valida")
    #Pregunta Dependientes
    valido = False
    while not valido:
        try:
            Dependientes = float(input("Ingresa el numero de Dependientes del aspirante: "))
            if Dependientes < 0 or Dependientes > 50:
                print("Ingresa un numero de Dependientes valido")
            else:
                valido = True
        except ValueError:
            print("Ingresa un numero de Dependientes valido")
    #Pregunta Recurses
    valido = False
    while not valido:
        try:
            Recurses = float(input("Ingresa el numero de Recurses que ha llevado el aspirante: "))
            if Recurses < 0 or Recurses > 50:
                print("Ingresa un numero de Recurses valido")
            else:
                valido = True
        except ValueError:
            print("Ingresa un numero de Recurses valido")
    #Pregunta Nivel SocioEconomico
    valido = False
    while not valido:
        try:
            lvleconomico = float(input("Ingresa el Nivel SocioEconomico del aspirante:\n\t1.- Clase Baja\n\t2.- Clase Media\n\t3.- Clase Alta\n"))
            if lvleconomico == 1 or lvleconomico == 2 or lvleconomico == 3:
                valido = True
            else:
                print("Ingresa un Nivel SocioEconomico valido")
        except ValueError:
            print("Ingresa un Nivel SocioEconomico valido")
    #Pregunta Becas Adicionales
    valido = False
    while not valido:
        try:
            BecasPlus = float(input("Ingresa el numero de Becas Adicionales con las que cuenta el aspirante: "))
            if BecasPlus < 0 or BecasPlus > 5:
                print("Ingresa un numero de Becas Adicionales valido")
            else:
                valido = True
        except ValueError:
            print("Ingresa un numero de Becas Adicionales valido")

    return [[Edad],[Ingreso],[Calificacion],[Modalidad],[Dependientes],[Recurses],[lvleconomico],[BecasPlus]]

# Open the CSV file for reading
dataset = []
outputs = []
Categorias = []
Campos = []
           
with open('becas.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    Campos = next(csvreader)
    for atributo in Campos:
        Categorias.append([])
    for fila in csvreader:
        id = 0
        for campo in fila:
            Categorias[id].append(float(campo))
            id += 1
    outputs = Categorias.pop()

minmax = MinMax(Categorias)
dataset = Normalizar(Categorias, minmax[0], minmax[1])
n_inputs = len(dataset[0])
n_outputs = 1
frecuenciaprint = 0
nivelprint = 1

Red = Crear_Red(n_inputs, 2, 3, n_outputs)
Entrena(Red, dataset, 0.5, 5000, outputs, frecuenciaprint, nivelprint)

prediciendo = True
while prediciendo:
    inputbase = Preguntas_Input()
    prediccion_Set = Normalizar(inputbase, minmax[0], minmax[1])
    Predecir(Red, prediccion_Set[0])
    valido = False
    while not valido:
        try:
            Repetir = int(input("Deseas predecir una nueva beca? \n\t0.- NO (Salir)\n\t1.- SI\n"))
            if Repetir !=0 and Repetir != 1:
                print("Ingresa una opcion valida")
            else:
                valido = True
                if Repetir == 0:
                    prediciendo = False
        except ValueError:
            print("Ingresa una opcion valid")