
from __future__ import print_function

import numpy as np
import pandas as pd

# ----------------------------------------------------
# - matriz de probabilidad o de transicion A
states = ["e", "h", "s", "v", "g", "c", "b", "x"]

A = [
    [0.00, 1.00, 0.0, 0.00, 0.00, 0.00, 0.00, 0.00],
    [0.00, 0.00, 0.70, 0.00, 0.10, 0.00, 0.00, 0.20],
    [0.00, 0.00, 0.40, 0.20, 0.15, 0.00, 0.00, 0.25],
    [0.00, 0.00, 0.00, 0.00, 0.65, 0.00, 0.00, 0.35],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.30, 0.60, 0.10],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
]

dfA = pd.DataFrame(A, index=states, columns=states)
# matriz de probabilidad o de transicion B
B = [
    [0.00, 1.00, 0.0, 0.00, 0.00, 0.00, 0.00, 0.00],
    [0.00, 0.00, 0.70, 0.00, 0.10, 0.00, 0.00, 0.20],
    [0.00, 0.00, 0.45, 0.21, 0.10, 0.00, 0.00, 0.30],
    [0.00, 0.00, 0.00, 0.00, 0.40, 0.00, 0.00, 0.60],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.30, 0.55, 0.15],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
]

dfB = pd.DataFrame(B, index=states, columns=states)


# visits data
# v_data = [23, 56, 11, 678, 6, 95, 111, 34]
# V = pd.Series(v_data, index=states)

# ----------------------------------------------------
# hay que modificarlo
def Vx(V, M, state):
    # get visits data
    vs = V.values

    # get visit probabilities for given state
    ps = M[state].values

    vx_value = np.dot(vs, ps)

    return vx_value

# ----------------------------------------------------

def VA(M):

    # para matriz A
    peh = Px(dfA ,'e' ,'h')
    phs = Px(dfA ,'h' ,'s')
    pss = Px(dfA ,'s' ,'s')
    psv = Px(dfA ,'s' ,'v')
    phg = Px(dfA ,'h' ,'g')
    psg = Px(dfA ,'s' ,'g')
    pvg = Px(dfA ,'v' ,'g')
    pgc = Px(dfA ,'g' ,'c')
    pgb = Px(dfA ,'g' ,'b')

    # a = np.array([[Ve,peh], [Vh,phs,Vs,pss]])
    # b = np.array([Vh,Vs])
    # x = np.linalg.solve(a,b)

    # sistema lineal de ecuaciones a resolver para la obtencion de las visitas
    Ve =1
    Vh = Ve * peh
    # Vs = Vh * phs + Vs * pss
    Vs = (Vh * phs) / (1 - pss)
    Vv = Vs * psv
    Vg = Vh * phg + Vs * psg + Vv * pvg
    Vc = Vg * pgc
    Vb = Vg * pgb

    statesG = ["e", "h", "s", "v", "g", "c", "b"]

    v_dataV = [Ve , Vh, Vs, Vv, Vg, Vc, Vb]
    V = pd.Series(v_dataV, index=statesG)

    return (V)

# ----------------------------------------------------
# para matriz B
def VB(M):
    peh = Px(dfB ,'e' ,'h')
    phs = Px(dfB ,'h' ,'s')
    pss = Px(dfB ,'s' ,'s')
    psv = Px(dfB ,'s' ,'v')
    phg = Px(dfB ,'h' ,'g')
    psg = Px(dfB ,'s' ,'g')
    pvg = Px(dfB ,'v' ,'g')
    pgc = Px(dfB ,'g' ,'c')
    pgb = Px(dfB ,'g' ,'b')

    # sistema lineal de ecuaciones a resolver para la obtencion de las visitas
    Ve =1
    Vh = Ve * peh
    # Vs = Vh * phs + Vs * pss
    Vs = (Vh * phs) / (1 - pss)
    Vv = Vs * psv
    Vg = Vh * phg + Vs * psg + Vv * pvg
    Vc = Vg * pgc
    Vb = Vg * pgb

    statesG = ["e", "h", "s", "v", "g", "c", "b"]

    v_dataV = [Ve , Vh, Vs, Vv, Vg, Vc, Vb]
    V = pd.Series(v_dataV, index=statesG)

    return (V)

# ----------------------------------------------------
# Devuelve las probabilidades de visita de un estado a otro

def Px(M ,state1 ,state2):
    px = M.at[state1, state2]
    return px


# -----------------------------------------------------

# calcula la carga para cada visita
# lambda->vector que almacena la tasa de llegada para cada clase de operacion
def lambdaF(gamma ,fa ,fb ,state):
    visitA = VA(dfA)
    visitB = VB(dfB)
    lan = gamma * (fa * visitA[state] + fb * visitB[state])
    return lan


# -----------------------------------------------------
# devuelve los vecinos del estado pasado

def neighbors(M ,state):
    neig = dfA[dfA[state] > 0]
    return neig


# -----------------------------------------------------

if __name__ == '__main__':

    # gamma ->parametro perteneciente a la carga total que llegaal sistema
    gamma = 1

    # la fraccion de sesion del tipo A y B respectivamente
    fa = 0.25
    fb = 0.75

    # se guardan las carga para cada una de las visitas:
    hx =[]
    for i in range(len(VA(dfA))):
        hx.append(lambdaF(gamma ,fa ,fb ,i))

    print("obtencion de las visitas a cada estado: A")
    print(VA(dfA))
    print("obtencion de las visitas a cada estado: B")
    print(VB(dfB))
    print("obtencion de las cargas")
    print(hx)


