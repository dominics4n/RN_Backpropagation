from math import exp
from random import seed
from random import random
import csv

seed("LindaLindaLinda")

class Neuronas:
    pesos = []
    error = 0
    salida = 0

def MinMax(categorias):
    MinVal = []
    MaxMinVal = []
    for categoria in categorias:
        minimo = min(categoria)
        maximo = max(categoria)
        MinVal.append(minimo)
        MaxMinVal.append(maximo - minimo)
    return [MinVal, MaxMinVal]

def Normalizar(categorias, min, max_min):
    Normalizados = []
    for i in range(len(categorias[0])):
        datos = []
        for j in range(len(categorias)):
            datos.append((categorias[j][i]-min[j])/max_min[j])
        Normalizados.append(datos)
    return Normalizados

def Crear_Red(parametros, num_N_ini, num_N_mid, num_N_fin):
    red = []
    for C_W in [[num_N_ini, parametros], [num_N_mid, num_N_ini], [num_N_fin, num_N_mid]]:
        Capa = []
        for n in range(C_W[0]):
            Capa.append(Neuronas())
            datos = []
            for w in range(C_W[1]):
                datos.append(random())
            Capa[n].pesos = datos
        red.append(Capa)
    return red
            
def Activar_Neurona(Entradas, Neurona):
    S = 0
    for x in range(len(Entradas)):
        S = S + Entradas[x] * Neurona.pesos[x]
    return 1.0 / (1.0 + exp(-S))

def Propagar_Entradas(Red_N, Soli_B):
    entradas = Soli_B
    for capas in Red_N:
        Salidas = []
        for neurona in capas:
            fun_act = Activar_Neurona(entradas, neurona)
            Salidas.append(fun_act)
            neurona.salida = fun_act
        entradas = Salidas
    return Salidas

def Propagar_Errores(Red_N, Resultado):
    for i in reversed(range(len(Red_N))):
        capa = Red_N[i]
        error_base = []
        if i != len(Red_N) - 1:
            for j in range(len(capa)):
                error = 0
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
                neurona.pesos[j] = neurona.pesos[j] - B * neurona.error * inputs[j]
            Nuevos_Inputs.append(neurona.salida)
        inputs = Nuevos_Inputs

def Entrena(Red_N, Set_Entrenamiento, B, n_rondas, resultados):
    kys = 0
    for ronda in range(n_rondas):
        sum_error = 0
        num_error = 0
        for row in Set_Entrenamiento:
            output = Propagar_Entradas(Red_N, row)
            sum_error += abs(resultados[kys]-output[0])
            if abs(resultados[kys]-output[0]) > 0.1:
                num_error += 1
            Propagar_Errores(Red_N, resultados[kys])
            Actualizar_Pesos(Red_N, row, B)
        print('>Ronda %d: Errores=%d, Sumatoria de errores=%.3f' % (ronda, num_error, sum_error))
    kys = kys + 1

def Predecir(Red_N):
    Edad, Ingreso Mensual,Calificacion,Modalidad Escolar,Dependientes,Recurses,Nivel economico,Becas Adicionales = []
    int(input("Ingresa " + xyString + ": "))
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
    Prediccion = Propagar_Entradas(Red_N, Solicitud)
    print(Prediccion)

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

Red = Crear_Red(n_inputs, 1, 1, n_outputs)
Entrena(Red, dataset, 0.5, 20, outputs)
Predecir(Red)