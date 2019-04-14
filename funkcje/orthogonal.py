import numpy as np

'''
Tworzenie wielomianow ortogonalnych dla skryptu RFP

Dane wejsciowe:
rec - FRF otrzymana z sygnalu pomiarowego
omega - zakres czestosci dla FRF (rec)
phitheta - funkcja wagowa: 1 - macierz phi, 2 - macierz theta
kmax - stopien wielomianu

Dane wyjsciowe:
P - macierz wielomianow ortogonalnych obliczonych w punktach czestosci (omega)
coeff - macierz wspolczynnikow pozwalajaca na transformacje wielomianu orotogonalnego na standardowy wielomian

Skrypt utworzony na podstawie:
https://www.mathworks.com/matlabcentral/fileexchange/3805-rational-fraction-polynomial-method
'''


def orthogonal(rec, omega, phitheta, kmax):

    if phitheta == 1:
        q = np.ones(np.shape(omega))  # funkcja wagowa dla macierzy phi
    elif phitheta == 2:
        q = abs(rec)**2  # funkcja wagowa dla macierzy theta
    elif phitheta != 1 and phitheta != 2:
        print('Phitheta musi byc 1 or 2')

    R_minus1 = np.zeros(np.shape(omega))
    R_0 = 1 / np.sqrt(2 * np.sum(q) * np.ones(np.shape(omega)))
    R = np.transpose(np.vstack((R_minus1, R_0)))
    coeff = np.zeros((kmax + 1, kmax + 2))
    coeff[0, 1] = 1 / np.sqrt(2 * np.sum(q))

    # tworzenie wielomianow oraz macierzy transformacji
    for k in range(kmax):
        Vkm1 = 2.0 * np.sum(omega * R[:, k + 1] * R[:, k] * q)
        Sk = omega * R[:, k + 1] - Vkm1 * R[:, k]  # @
        Dk = np.sqrt(2.0 * np.sum((Sk ** 2) * q))

        R = np.column_stack((R, np.true_divide(Sk, Dk)))

        coeff[:, k + 2] = -1.0 * Vkm1 * coeff[:, k]
        coeff[1: k + 2, k + 2] = coeff[1: k + 2, k + 2] + coeff[0: k + 1, k + 1]
        coeff[:, k + 2] = coeff[:, k + 2] / Dk

    R = R[:, 1: kmax+2]
    coeff = coeff[:, 1:kmax + 2]

    jk = np.zeros((1, kmax + 1), dtype='complex')
    P = np.zeros(np.shape(R), dtype='complex')
    # zespolone wielomiany ortogonalne
    for k in range(kmax + 1):
        P[:, k] = R[:, k] * 1.0j**k
        jk[0, k] = 1.0j**k

    coeff = (np.conj(np.transpose(jk)) @ jk) * coeff  # zespolona macierz transformacji

    return P, coeff
