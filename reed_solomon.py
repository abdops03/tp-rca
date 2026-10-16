
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code du professeur : Reed-Solomon
"""

def somme(l1, l2, l3, r1, r2, r3):
    result1 = (l1 + r1) % 2
    result2 = (l2 + r2) % 2
    result3 = (l3 + r3) % 2
    return result1, result2, result3


def produit(l1, l2, l3, r1, r2, r3):
    result1 = (1-l1)*(1-l2)*l3*r1 + l1*(1-r1)*(1-r2)*r3 + (1-l1)*l2*(1-l3)*r2
    result1 += l2*(1-r1)*r2*(1-r3)
    result1 += (1-l1)*l2*l3*((1-r1)*r2*r3 + r1*(1-r2)*(1-r3) + r1*(1-r2)*r3)
    result1 += (1-r1)*r2*r3*((1-l1)*l2*l3 + l1*(1-l2)*(1-l3) + l1*(1-l2)*l3)
    result1 += l1*(1-l2)*(1-l3)*r1*(1-r3) + r1*(1-r2)*(1-r3)*l1*(1-l3)
    result1 += l1*(1-l2)*l3*r1*r3 + r1*(1-r2)*r3*l1*l3
    result1 += l1*l2*(1-l3)*r1*r2*r3 + r1*r2*(1-r3)*l1*l2*l3
    result1 = 1.0 * (result1 > 10**(-7))

    result2 = (1-l1)*(1-l2)*l3*r2 + (1-r1)*(1-r2)*r3*l2
    result2 += (1-l1)*l2*(1-l3)*((1-r1)*r2*r3 + r1*(1-r3))
    result2 += (1-r1)*r2*(1-r3)*((1-l1)*l2*l3 + l1*(1-l3))
    result2 += (1-l1)*l2*l3*r1*((1-r2)*(1-r3) + r2*r3)
    result2 += (1-r1)*r2*r3*l1*((1-l2)*(1-l3) + l2*l3)
    result2 += l1*(1-l2)*(1-l3)*r1*(1-r2) + r1*(1-r2)*(1-r3)*l1*(1-l2)
    result2 += l1*(1-l2)*l3*r1*((1-r2)*r3 + r2) + r1*(1-r2)*r3*l1*((1-l2)*l3 + l2)
    result2 += l1*l2*(1-l3)*r1*r2*(1-r3)
    result2 += l1*l2*l3*r1*r2*r3
    result2 = 1.0 * (result2 > 10**(-7))

    result3 = (1-l1)*(1-l2)*l3*r3 + (1-r1)*(1-r2)*r3*l3
    result3 += (1-l1)*l2*(1-l3)*r1 + (1-r1)*r2*(1-r3)*l1
    result3 += (1-l1)*l2*l3*((1-r1)*r2*r3 + r1*(1-r3))
    result3 += (1-r1)*r2*r3*((1-l1)*l2*l3 + l1*(1-l3))
    result3 += l1*(1-l2)*(1-l3)*r1*r2 + r1*(1-r2)*(1-r3)*l1*l2
    result3 += l1*(1-l2)*l3*r1*((1-r2)*r3 + r2*(1-r3))
    result3 += r1*(1-r2)*r3*l1*((1-l2)*l3 + l2*(1-l3))
    result3 += l1*l2*l3*r1*r2*r3
    result3 = 1.0 * (result3 > 10**(-7))

    return result1, result2, result3


def inverse(l1, l2, l3):
    result1 = (1-l1)*l2*(1-l3) + (1-l1)*l2*l3 + l1*(1-l2)*(1-l3) + l1*l2*l3
    result1 = 1.0 * (result1 > 10**(-7))

    result2 = (1-l1)*l2*l3 + l1*(1-l2)*(1-l3) + l1*(1-l2)*l3 + l1*l2*(1-l3)
    result2 = 1.0 * (result2 > 10**(-7))

    result3 = (1-l1)*(1-l2)*l3 + (1-l1)*l2*(1-l3) + l1*(1-l2)*(1-l3) + l1*l2*(1-l3)
    result3 = 1.0 * (result3 > 10**(-7))

    return result1, result2, result3


def redond(a2, a1, a0):
    b3 = somme(*produit(*a2, 0, 1, 1), *a1)
    b2 = somme(*a2, *a0)
    b1 = produit(*a2, 0, 1, 0)
    b0 = produit(*a2, 0, 1, 1)

    c3 = somme(*produit(*b3, 0, 1, 1), *b2)
    c2 = somme(*b1, *b3)
    c1 = somme(*produit(*b3, 0, 1, 0), *b0)
    c0 = produit(*b3, 0, 1, 1)

    r3 = somme(*produit(*c3, 0, 1, 1), *c2)
    r2 = somme(*c1, *c3)
    r1 = somme(*produit(*c3, 0, 1, 0), *c0)
    r0 = produit(*c3, 0, 1, 1)

    return list(r3), list(r2), list(r1), list(r0)


def syndromes(a2, a1, a0, r3, r2, r1, r0):
    S1 = produit(*a2, 1, 0, 1)
    S1 = somme(*S1, *produit(*a1, 1, 1, 1))
    S1 = somme(*S1, *produit(*a0, 1, 1, 0))
    S1 = somme(*S1, *produit(*r3, 0, 1, 1))
    S1 = somme(*S1, *produit(*r2, 1, 0, 0))
    S1 = somme(*S1, *produit(*r1, 0, 1, 0))
    S1 = somme(*S1, *r0)

    S2 = produit(*a2, 1, 1, 1)
    S2 = somme(*S2, *produit(*a1, 0, 1, 1))
    S2 = somme(*S2, *produit(*a0, 0, 1, 0))
    S2 = somme(*S2, *produit(*r3, 1, 0, 1))
    S2 = somme(*S2, *produit(*r2, 1, 1, 0))
    S2 = somme(*S2, *produit(*r1, 1, 0, 0))
    S2 = somme(*S2, *r0)

    S3 = produit(*a2, 1, 1, 0)
    S3 = somme(*S3, *produit(*a1, 0, 1, 0))
    S3 = somme(*S3, *produit(*a0, 1, 1, 1))
    S3 = somme(*S3, *produit(*r3, 1, 0, 0))
    S3 = somme(*S3, *produit(*r2, 1, 0, 1))
    S3 = somme(*S3, *produit(*r1, 0, 1, 1))
    S3 = somme(*S3, *r0)

    S4 = produit(*a2, 0, 1, 1)
    S4 = somme(*S4, *produit(*a1, 1, 0, 1))
    S4 = somme(*S4, *produit(*a0, 1, 0, 0))
    S4 = somme(*S4, *produit(*r3, 1, 1, 1))
    S4 = somme(*S4, *produit(*r2, 0, 1, 0))
    S4 = somme(*S4, *produit(*r1, 1, 1, 0))
    S4 = somme(*S4, *r0)

    return list(S1), list(S2), list(S3), list(S4)
