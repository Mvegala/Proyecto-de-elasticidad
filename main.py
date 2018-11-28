from __future__ import print_function

import numpy as np
import pandas as pd

# ----------------------------------------------------

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
v_data = [23, 56, 11, 678, 6, 95, 111, 34]
V = pd.Series(v_data, index=states)


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
    peh = Px(dfA, 'e', 'h')
    phs = Px(dfA, 'h', 's')
    pss = Px(dfA, 's', 's')
    psv = Px(dfA, 's', 'v')
    phg = Px(dfA, 'h', 'g')
    psg = Px(dfA, 's', 'g')
    pvg = Px(dfA, 'v', 'g')
    pgc = Px(dfA, 'g', 'c')
    pgb = Px(dfA, 'g', 'b')

    # a = np.array([[Ve,peh], [Vh,phs,Vs,pss]])
    # b = np.array([Vh,Vs])
    # x = np.linalg.solve(a,b)

    Ve = 1
    Vh = Ve * peh
    # Vs = Vh * phs + Vs * pss
    Vs = (Vh * phs) / (1 - pss)
    Vv = Vs * psv
    Vg = Vh * phg + Vs * psg + Vv * pvg
    Vc = Vg * pgc
    Vb = Vg * pgb

    return (Ve, Vh, Vs, Vv, Vg, Vc, Vb)


# ----------------------------------------------------
# para matriz B
def VB(M):
    peh = Px(dfB, 'e', 'h')
    peh = Px(dfB, 'e', 'h')
    phs = Px(dfB, 'h', 's')
    pss = Px(dfB, 's', 's')
    psv = Px(dfB, 's', 'v')
    phg = Px(dfB, 'h', 'g')
    psg = Px(dfB, 's', 'g')
    pvg = Px(dfB, 'v', 'g')
    pgc = Px(dfB, 'g', 'c')
    pgb = Px(dfB, 'g', 'b')

    # a = np.array([[Ve,peh], [Vh,phs,Vs,pss]])
    # b = np.array([Vh,Vs])
    # x = np.linalg.solve(a,b)

    Ve = 1
    Vh = Ve * peh
    # Vs = Vh * phs + Vs * pss
    Vs = (Vh * phs) / (1 - pss)
    Vv = Vs * psv
    Vg = Vh * phg + Vs * psg + Vv * pvg
    Vc = Vg * pgc
    Vb = Vg * pgb

    # para matriz B

    return (Ve, Vh, Vs, Vv, Vg, Vc, Vb)


# ----------------------------------------------------
# get visit probabilities for given state global

def Px(M, state1, state2):
    px = M.at[state1, state2]
    return px


# -----------------------------------------------------
# get adyacent to me

def Ady(M, state):
    ad = dfA[dfA[state] > 0]
    return ad


# -----------------------------------------------------

if __name__ == '__main__':
    s_value = Vx(V, dfA, 's')

    print(VA(dfA))
    print(VB(dfB))

