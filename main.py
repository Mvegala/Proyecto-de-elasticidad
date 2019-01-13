# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
import pandas as pd
import time, random
import matplotlib.pyplot as plt

# ----------------------------------------------------
#matriz de probabilidado de transicion A
states = ["e", "h", "s", "v", "g", "c", "b", "x"]

A = [
    # "e",  "h",  "s",  "v",  "g",  "c",  "b",  "x"
    [0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00], #e
    [0.00, 0.00, 0.70, 0.00, 0.10, 0.00, 0.00, 0.20], #h
    [0.00, 0.00, 0.40, 0.20, 0.15, 0.00, 0.00, 0.25], #s
    [0.00, 0.00, 0.00, 0.00, 0.65, 0.00, 0.00, 0.35], #v
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.30, 0.60, 0.10], #g
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00], #c
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00], #b
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]  #x
]

dfA = pd.DataFrame(A, index=states, columns=states)

#matriz de probabilidado de transicion B
B = [
    # "e",  "h",  "s",  "v",  "g",  "c",  "b",  "x"
    [0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00], #e
    [0.00, 0.00, 0.70, 0.00, 0.10, 0.00, 0.00, 0.20], #h
    [0.00, 0.00, 0.45, 0.15, 0.10, 0.00, 0.00, 0.30], #s
    [0.00, 0.00, 0.00, 0.00, 0.40, 0.00, 0.00, 0.60], #v
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.30, 0.55, 0.15], #g
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00], #c
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00], #b
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]  #x
]

dfB = pd.DataFrame(B, index=states, columns=states)

#Matriz de Demandas
statesE = ["h", "s", "v", "g", "c", "b"]
statesD = ["WS-CPU", "WS-disk", "AS-CPU", "AS-disk", "DS-CPU", "DS-disk"]
Dem=[

    #  "h",   "s",   "v",  "g",   "c",   "b"
    [0.008, 0.009, 0.011, 0.060, 0.012, 0.015], #WS-CPU
    [0.030, 0.010, 0.010, 0.010, 0.010, 0.010], #WS-disk
    [0.000, 0.030, 0.035, 0.025, 0.045, 0.040], #AS-CPU
    [0.000, 0.008, 0.080, 0.009, 0.011, 0.012], #AS-disk
    [0.000, 0.010, 0.009, 0.015, 0.070, 0.045], #DS-CPU
    [0.000, 0.035, 0.018, 0.050, 0.080, 0.090]  #DS-disk
]

Dem=[# ESTA MATRIZ ES PARA IGNORAR LOS QUE NO SEAN [WS-CPU, WS-disk]
    #  "h",   "s",   "v",  "g",   "c",   "b"
    [0.008, 0.009, 0.011, 0.060, 0.012, 0.015], #WS-CPU
    [0.030, 0.010, 0.010, 0.010, 0.010, 0.010], #WS-disk
    [0.000, 0.000, 0.000, 0.000, 0.000, 0.000], #AS-CPU
    [0.000, 0.000, 0.000, 0.000, 0.000, 0.000], #AS-disk
    [0.000, 0.000, 0.000, 0.000, 0.000, 0.000], #DS-CPU
    [0.000, 0.000, 0.000, 0.000, 0.000, 0.000]  #DS-disk
]
dfD = pd.DataFrame(Dem, index=statesD, columns=statesE)
# dfD2 = pd.DataFrame(Dem2, index=statesD, columns=statesE)

# ----------------------------------------------------



def V(df):

    peh = Px(df,'e','h')
    phs = Px(df,'h','s')
    pss = Px(df,'s','s')
    psv = Px(df,'s','v')
    phg = Px(df,'h','g')
    psg = Px(df,'s','g')
    pvg = Px(df,'v','g')
    pgc = Px(df,'g','c')
    pgb = Px(df,'g','b')

    #sistema lineal de ecuaciones a resolver para la obtencion de las visitas
    Ve = 1 #Equation 8.3.1
    Vh = Ve * peh #Equation 8.3.2
    # Vs = Vh * phs + Vs * pss #Equation 8.3.3
    # Vs = (Vh * phs) / (1 - pss) #Equation 8.3.8(1)
    Vs = phs / (1 - pss) #Equation 8.3.8(2)
    Vv = Vs * psv #Equation 8.3.4
    Vg = Vh * phg + Vs * psg + Vv * pvg #Equation 8.3.5
    Vc = Vg * pgc #Equation 8.3.6
    Vb = Vg * pgb #Equation 8.3.7
    Vx = 1

    statesG = ["e", "h", "s", "v", "g", "c", "b", "x"]

    v_dataV = [Ve , Vh, Vs, Vv, Vg, Vc, Vb, Vx]
    V = pd.Series(v_dataV, index=statesG)

    return V

# ----------------------------------------------------



# ----------------------------------------------------
# Devuelve las probabilidades de visita de un estado a otro

def Px(M, state1, state2):
    px = M.at[state1, state2]
    return px

#-----------------------------------------------------

# devuelve los vecinos del estado pasado

# def neighbors(df, state):
#     neig = df[df[state] > 0]
#     return neig

#-----------------------------------------------------

# calcula la carga para cada visita
 #lambda->vector que almacena la tasa de llegada para cada clase de operacion
def lambdaF(gamma, fa, fb, state):
    visitA = V(dfA)
    visitB = V(dfB)
    lan = gamma * (fa * visitA[state] + fb * visitB[state])
    return lan

#-----------------------------------------------------

# Metodo para Calcular la Utilidad: Mide cuan util es la configuracion del momento
#CPU (i)
#h(r)
#N-> numero de servidores(puede variar)
#landa-> carga
#D->demanda

def Ux(i, N, gamma):
    ux = 0
    for es in statesE:
        dem = Px(dfD, i, es)
        landa = lambdaF(gamma, fa, fb, es)
        ux += landa * dem / N
    return ux

#-----------------------------------------------------
# Metodo para Calcular los tiempos de respuesta
#Tengo dudas de como hacerlo, ver con Ivan

def Rx(i, N, gamma):
    rx = 0
    for es in statesD:
        dem = Px(dfD, es, i)
        rx += dem / (1 - Ux(es, N, gamma))
    return rx

def RxN(i, Ns, gamma):
    rx = 0
    for es in statesD:
        dem = Px(dfD, es, i)
        rx += dem / (1 - Ux(es, Ns[i], gamma))
    return rx

#-----------------------------------------------------



def cargaPorGamma(gamma, N):
    rx = []
    for i in statesE:
        rx.append((i, Rx(i, N, gamma)))
    return rx

def cargaPorGammaAndNumComponentes(gamma, Ns):
    rx = []
    for i in statesE:
        rx.append((i, RxN(i, Ns, gamma)))
    return rx







def grafico(filas, columnas):
    import random
    # ysample = random.sample(range(-50, 50), 100)
    #
    # xdata = []
    # ydata = []

    plt.show()
    fig, axes = plt.subplots(filas, columnas, sharex='all', sharey='all')
    valores = []

    for i in range(filas):
        valores.append([])
        for j in range(columnas):
            valores[i].append({'x': [], 'y': [], 'nComp': 0})
            line, = axes[i, j].plot([], [], 'r-')

    # for a in range(100):
    #
    #     xdata.append(a)
    #     ydata.append(ysample[a])
    #     for i in range(2):
    #     #         for j in range(3):
    #     #             line, = axes[i, j].plot(xdata, ydata, 'r-')
    #     #             line.set_xdata(xdata)
    #     #             line.set_ydata(ydata)
    #     #     plt.draw()
    #     #     plt.pause(1e-17)
    #     #     time.sleep(0.1)

    # add this if you don't want the window to disappear at the end
    # plt.show()
    return fig, axes, valores





def actualizaGrafico(filas, columnas, axes, valores):
    for i in range(filas):
        for j in range(columnas):
            line, = axes[i, j].plot(valores[i][j]['x'], valores[i][j]['y'], 'r-')
            axes[i, j].set_title(f'C={valores[i][j]["nComp"]} g={valores[i][j]["gamma"]}')

            x = valores[i][j]['x']
            y = valores[i][j]['y']
            if len(x) > 12:
                x = [x[-10:]]
                y = [y[-10:]]

            line.set_xdata(x)
            line.set_ydata(y)
    plt.draw()
    plt.pause(1e-17)







def tRespMaxMin():
    fig, axes, valores = grafico(2, 3)
    N = 1
    g = 0
    maximo = 25
    minimo = 10
    iteracion = -1 #Iteración actual
    incGamma = 0.2
    contadorIguales = {}
    for el in statesE:
        contadorIguales[el] = 0
    while iteracion < 1000:
        incGamma = random.random() * 0.5


        iteracion += 1
        if iteracion > 100 and iteracion < 200:
            incGamma = -1 * incGamma
        if iteracion > 400 and iteracion < 600:
            incGamma = -1 * incGamma
        if iteracion > 900 and iteracion < 1000:
            incGamma = -1 * incGamma
        if g + incGamma < 0:
            incGamma = 0

        g += incGamma

        error = False
        # cargas = cargaPorGammaAndNumComponentes(g, Ns)
        cargas = cargaPorGamma(g, N)
        accion = {'mas': 0, 'menos': 0}
        for indElemento, a in enumerate(cargas):
            carga = round(a[1]*100, 2)
            if indElemento > 2:
                i = 1
                j = indElemento-3
            else:
                i = 0
                j = indElemento

            valores[i][j]['x'].append(iteracion)
            valores[i][j]['y'].append(carga)
            # valores[i][j]['nComp'] = Ns[a[0]]
            valores[i][j]['nComp'] = N
            valores[i][j]['gamma'] = str(round(g, 2)) + f' n={a[0]} K={carga}'
            # print(valores)


            # if carga > maximo or carga < 0:
            #     contadorIguales[a[0]] += 1
            #     if contadorIguales[a[0]] > 5:
            #         Ns[a[0]] += 1
            #         print(f'añado componente {a[0]}')
            #         contadorIguales[a[0]] = 0
            #     error = True
            # elif carga < minimo and Ns[a[0]] > 1:
            #     contadorIguales[a[0]] += 1
            #     if contadorIguales[a[0]] > 5:
            #         Ns[a[0]] -= 1
            #         print(f'resto componente {a[0]}')
            #         contadorIguales[a[0]] = 0
            #     error = True

            if carga > maximo or carga < 0:
                accion['mas'] += 1
            elif carga < minimo and N > 1:
                accion['menos'] += 1

        if accion['mas'] > 0:
            N += 1
            error = True
        if accion['menos'] == len(cargas):
            N -= 1
            error = True
        actualizaGrafico(2, 3, axes, valores)
        if error:
            g -= incGamma

    plt.show()










def tRespMedio():
    fig, axes, valores = grafico(2, 3)
    N = 1
    g = 0
    maximo = 25
    minimo = 10
    iteracion = -1  # Iteración actual
    incGamma = 0.2
    contadorIguales = {}
    for el in statesE:
        contadorIguales[el] = 0
    while iteracion < 1000:
        incGamma = random.random() * 0.5

        iteracion += 1
        if iteracion > 100 and iteracion < 200:
            incGamma = -1 * incGamma
        if iteracion > 400 and iteracion < 600:
            incGamma = -1 * incGamma
        if iteracion > 900 and iteracion < 1000:
            incGamma = -1 * incGamma
        if g + incGamma < 0:
            incGamma = 0

        g += incGamma

        error = False
        # cargas = cargaPorGammaAndNumComponentes(g, Ns)
        cargas = cargaPorGamma(g, N)
        accion = {'mas': 0, 'menos': 0}
        tResp = 0
        for indElemento, a in enumerate(cargas):
            carga = round(a[1] * 100, 2)
            if indElemento > 2:
                i = 1
                j = indElemento - 3
            else:
                i = 0
                j = indElemento

            valores[i][j]['x'].append(iteracion)
            valores[i][j]['y'].append(carga)
            # valores[i][j]['nComp'] = Ns[a[0]]
            valores[i][j]['nComp'] = N
            valores[i][j]['gamma'] = str(round(g, 2)) + f' n={a[0]} K={carga}'
            # print(valores)

            # if carga > maximo or carga < 0:
            #     contadorIguales[a[0]] += 1
            #     if contadorIguales[a[0]] > 5:
            #         Ns[a[0]] += 1
            #         print(f'añado componente {a[0]}')
            #         contadorIguales[a[0]] = 0
            #     error = True
            # elif carga < minimo and Ns[a[0]] > 1:
            #     contadorIguales[a[0]] += 1
            #     if contadorIguales[a[0]] > 5:
            #         Ns[a[0]] -= 1
            #         print(f'resto componente {a[0]}')
            #         contadorIguales[a[0]] = 0
            #     error = True

            tResp += carga

        if tResp / len(cargas) > maximo:
            N += 1
            error = True
        if tResp / len(cargas) < minimo and N > 1:
            N -= 1
            error = True

        actualizaGrafico(2, 3, axes, valores)
        if error:
            g -= incGamma

    plt.show()











if __name__ == '__main__':
    #s_value = Vx(V, dfA, 's')

    # fig, axes, valores = grafico(2, 3)
    # valores = [ [{'x': [0, 1, 2, 3], 'y': [0, 1, 2, 3], 'nComp': 1},   {'x': [0, 1, 2, 3], 'y': [-1, 5, 6, -2], 'nComp': 0},   {'x': [0, 1, 2, 3], 'y': [0, 0, 2, 0], 'nComp': 0}],
    #             [{'x': [0, 1, 2, 3], 'y': [4, 5, 7, 8], 'nComp': 0},   {'x': [0, 1, 2, 3], 'y': [9, 7, 5, 2], 'nComp': 2},   {'x': [0, 1, 2, 3], 'y': [-1, 1, -1, 1], 'nComp': 0}]]
    # print(valores[0][0]['x'])
    # print(valores[0][0]['y'])
    # print(valores[0][1]['x'])
    # print(valores[0][1]['y'])
    # print(valores[0][2]['x'])
    # print(valores[0][2]['y'])
    # actualizaGrafico(2, 3, axes, valores)
    # exit()


    #gamma -> parametro perteneciente a la carga total que llega al sistema
    gamma = 11
    
    #la fraccion de sesion del tipo A y B respectivamente
    fa = 0.25
    fb = 1 - fa

    N = 3
    
    #se guardan las carga para cada una de las visitas:
    hx=[]
    for e in states:
        hx.append(   (e, lambdaF(gamma, fa, fb, e))   )
    
    ux = []
    for i in statesD:
        ux.append(   (i, Ux(i, N, gamma))   )
        
    rx = []
    for i in statesE:
        rx.append(   (i, Rx(i, N, gamma))   )
   
   
    print("Obtención de las visitas: A")
    print(V(dfA))
    print("Obtención de las visitas: B")
    print(V(dfB))
    print("Obtención de las cargas")
    print(hx)
    print("Obtención de las utilidades")
    print(ux)
    print("Obtención de los tiempos de respuesta")
    print(rx)
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    # N = 1
    # Ns = {}
    # for el in statesE:
    #     Ns[el] = 1
    # g = 0
    # maximo = 80
    # minimo = 1


    # tRespMedio()
    tRespMaxMin()




