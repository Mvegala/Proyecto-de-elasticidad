# -*- coding: utf-8 -*-
from __future__ import print_function

import numpy as np
import pandas as pd

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

#-----------------------------------------------------



def cargaPorGamma(gamma, N):
    rx = []
    for i in statesE:
        rx.append((i, Rx(i, N, gamma)))
    return rx


if __name__ == '__main__':
    #s_value = Vx(V, dfA, 's')
    
    #gamma ->parametro perteneciente a la carga total que llega al sistema
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
   
   
    print("obtención de las visitas: A")
    print(V(dfA))
    print("obtención de las visitas: B")
    print(V(dfB))
    print("obtención de las cargas")
    print(hx)
    print("obtención de las utilidades")
    print(ux)
    print("obtención de los tiempos de respuesta")
    print(rx)
    print()
    print()
    print()
    print()
    print()
    print()
    print()
    for g in range(0, 100, 10):
        print(g)
        print(cargaPorGamma(g, 5))


