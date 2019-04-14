import numpy as np
from funkcje.orthogonal import orthogonal
from scipy.signal import residue

'''
Wyznaczenie parametrow modalnych za pomoca metody RFP
skrypt używa skryptu: orthogonal.py

Dane wejsciowe:
rec - FRF otrzymana z sygnalu pomiarowego
omega - zakres czestosci dla FRF (rec)
N - liczba stopni swobody (postaci drgan) aproksymacji

Dane wyjsciowe:
alfa - FRF otrzymana podczas aproksymacji
Resi - wektor zawierajacy residua kolejnych postaci drgan
Pole - wektor zwieracjacy bieguny kolejnych postaci drgan

Skrypt utworzony na podstawie:
https://www.mathworks.com/matlabcentral/fileexchange/3805-rational-fraction-polynomial-method
'''


def RFP(rec, omega, N):

    x = np.shape(omega)
    if x == 1:
        omega = np.transpose(omega)

    x = np.shape(rec)
    if x == 1:
        rec = np.transpose(rec)
    # normalizacja danych
    nom_omega = np.max(omega)
    omega = omega / nom_omega

    m = 2 * N -1  # licznik
    n = 2 * N  # mianownik

    #  stworzenie wielomanów ortogonalnych
    [phimatrix, coeff_a] = orthogonal(rec, omega, 1, m)
    [thetamatrix, coeff_b] = orthogonal(rec, omega, 2, n)

    [x, y] = np.shape(phimatrix)
    Phi = phimatrix[:, 0:x]

    [x, y] = np.shape(thetamatrix)
    Theta = thetamatrix[:, 0:x]

    T = np.diag(rec) @ thetamatrix[:, 0: y - 1]

    W = rec * thetamatrix[:, y - 1]

    X = - 2.0 * np.real(np.conj(np.transpose(Phi)) @ T)
    G = 2.0 * np.real(np.conj(np.transpose(Phi)) @ W)
    [x, y] = np.shape(X)

    d = - 1.0 * np.linalg.inv(np.eye(x,y) - np.transpose(X) @ X) @ np.transpose(X) @ G

    C = G - X @ d
    D = np.append(d, 1.0)  #dodanie jedynki na koniec append?

    alfa = np.zeros(len(omega), dtype=complex)

    #  obliczenie aproksymowanej charakterystyki
    for i in range(len(omega)):
        numer = np.sum(np.transpose(C) * Phi[i, :])
        denom = np.sum(np.transpose(D) * Theta[i, :])
        alfa[i] = np.true_divide(numer, denom)

    A = coeff_a @ C
    A = np.transpose(A[::-1])  #  standaryzowane wspolczynniki licznika

    B = coeff_b @ D
    B = np.transpose((B[::-1]))  #  standaryzowane wspolczynniki mianownika

    [R, P, K] = residue(A, B)  # obliczenie reszt i biegunow

    #  odrzucenie biegunow lezacych w zakresie ujemnych czestosci
    x = int(len(R))
    ii=0
    Resi = np.zeros((int(x), 1), dtype=complex)
    Pole = np.copy(Resi)
    for i in range(int(x)):
        if P[i].imag >= 0:
            Resi[ii] = R[i]
            Pole[ii] = P[i]
            ii += 1
    for i in range(int(x) - 1, -1, -1):
        if np.abs(Pole[i]) == 0:
            Resi = np.delete(Resi, i)
            Pole = np.delete(Pole, i)

    #  denormalizacja danych
    Resi = Resi * nom_omega
    Pole = Pole * nom_omega

    return Resi, Pole, alfa
