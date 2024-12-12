from math import e, log
# формула Циалковского для одной ступени
def fuel_mass(M0, I, V):
    k = 13
    e_VI = e ** (V/I)
    return ((M0 * k * (e_VI - 1)) / (k + 1 - e_VI))

# Формула Циалковского для многоступенчатой ракеты
def get_V(ml1, ml2, ml3):
    # ml1, ml2, ml3 - массы ступеней, посчитанные ранее
    i1 = 4600
    i2 = 2650
    m0 = 5712
    m1 = 110460
    m2 = 4500
    return (i1 * log((m0 + ml1 + ml2 + ml3) / (m0 + m1 + ml2)) + i2 * log((m0 + ml2) / (m0 + m2)))
