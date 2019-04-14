import numpy as np

'''Skrypt zawieracjy metody wywolywane w programie do estymacji parametrow modalnych'''


def nextpow2(i):
    '''
    Metoda zwracajaca wykladnik kolejnej potegi 2
    wiekszej od podanej liczby

    i - liczba wejsciowa
    p - wykladnik
    '''

    n = 1
    p = 0
    while n < i:
        n *= 2
        p += 1
    return p


def przeliczenie(dane, S, W):
    '''
    Skrypt przeliczajacy sygnal z mV na wartosci fizyczne

    dane - macierz do przemnożenia
    S - czułość elementu pomiarowego
    W - wzmocnienie kanału
    '''

    a = 1000 / W / S
    dane = dane * a
    return dane


def okno_wykl(dane, L, H_pr):
    '''
    Przemnożenie sygnalu poprzez odpowiednie okno wykładcznie

    dane - macierz do przemnozenia
    L - dlugosc sygnalu w sekundach
    H_pr - czestotliwosc probkowania
    '''

    tal = 0.25 * L
    e = np.arange(0, L, 1/H_pr)
    e = np.exp(-1 / tal * e)
    [x, y] = np.shape(dane)

    for ys in range(y-1):
        dane[:, ys] = dane[:, ys] * e

    return dane


def tichonow(dane, L, H_pr):
    '''
    Przemnożenie sygnalu poprzez odpowiednie okno wykładcznie

     dane - macierz do przemnozenia
     L - dlugosc sygnalu w sekundach
     H_pr - czestotliwosc probkowania
     '''

    n = float(15)
    alfa = 1 / 30 * L * H_pr
    e = np.arange(0, L, 1 / H_pr)
    e2 = np.copy(e)

    for i in range(len(e)):
        e2[i] = 1 - (i**n) / (i**n + alfa**n)

    [x, y] = np.shape(dane)
    for ys in range(y - 1):
        dane[:, ys] = dane[:, ys] * e2

    return dane


def znajdz(f, freq):
    '''Funkcja znajduje pierwszy indeks o wiekszej wartosci od zadanej - freq w wektorze - f'''

    for freqs in range(len(freq)):
        if freq[freqs] >= f:
            i = freqs
            break
    return i


def zakres(fmin, fmax, freq):
    ''''
    Fukncja ogranicza wektor czestotliwosci freq do zakresu <fmin, fmax>
    zwraca indeksy odpowiedajace fmin, fmax
    '''

    if fmin < freq[0]:
        i_min = 0
    elif fmin >= freq[0]:
        for freqs in range(len(freq)):
            if freq[freqs] >= fmin:
                i_min = freqs
                break

    if fmax > freq[-1]:
        i_max = len(freq) - 1
    elif fmax <= freq[-1]:
        for freqs in range(len(freq)):
            if freq[freqs] >= fmax:
                i_max = freqs
                break
    return i_min, i_max


def WGM(kanal_1, kanal_2, kanal_3, H_pr, nfft, typ):
    '''
    Funkcja wyznaczajaca widmowa gestosc mocy sygnalow
    :param kanal_1: kanal wymuszenia
    :param kanal_2: kanal odpowiedzi x
    :param kanal_3: kanal odpowiedzi y
    :param H_pr: czestotliwosc probkowania
    :param nfft: liczba n punktowej FFT - potega 2
    :param typ: typ wyznaczania ( aktualnie tylko FFT)
    :return: Sij - Widmowe gestosci mocy wlasne (i=j) / wzajemne (i/=j)
    '''

    [x, y] = np.shape(kanal_1)
    dlugosc = int(np.floor((nfft + 1) / 2))
    freq = np.arange(0, dlugosc) * H_pr / nfft

    if typ == 'fft':
        R11 = np.zeros((2 * x -1, y ))
        R12 = np.copy(R11)
        R13 = np.copy(R11)
        R22 = np.copy(R11)
        R33 = np.copy(R11)

        for i in range(y -1):
            R11[:, i] = np.correlate(kanal_1[:, i], kanal_1[:, i], "full") / (len(kanal_1))
            R12[:, i] = np.correlate(kanal_2[:, i], kanal_1[:, i], "full") / (len(kanal_1))
            R13[:, i] = np.correlate(kanal_3[:, i], kanal_1[:, i], "full") / (len(kanal_1))
            R22[:, i] = np.correlate(kanal_2[:, i], kanal_2[:, i], "full") / (len(kanal_1))
            R33[:, i] = np.correlate(kanal_3[:, i], kanal_3[:, i], "full") / (len(kanal_1))

        Sxx = np.fft.fft(R11, axis=0, n=nfft)
        Sxy1 = np.fft.fft(R12, axis=0, n=nfft)
        Sxy2 = np.fft.fft(R13, axis=0, n=nfft)
        Syy1 = np.fft.fft(R22, axis=0, n=nfft)
        Syy2 = np.fft.fft(R33, axis=0, n=nfft)

        S11 = np.average(Sxx, axis=1) / H_pr * 2
        S12 = np.average(Sxy1, axis=1) / H_pr * 2
        S13 = np.average(Sxy2, axis=1) / H_pr * 2
        S22 = np.average(Syy1, axis=1) / H_pr * 2
        S33 = np.average(Syy2, axis=1) / H_pr * 2

        S11 = S11[0: dlugosc]
        S12 = S12[0: dlugosc]
        S13 = S13[0: dlugosc]
        S22 = S22[0: dlugosc]
        S33 = S33[0: dlugosc]

    return S11, S12, S13, S22, S33, freq


def tran_widm(pole, resi, w):
    '''Funkcja obliczajaca transmitancje widmowa na podstawie
    pole - bieguny uzyskane z RFP
    resi - reszty biegunow z RFP
    w - wektor czestosci
    '''

    H = np.zeros((len(w), len(pole)), dtype=complex)
    [r, y] = np.shape(H)
    for ys in range(y):
        for rs in range(r):
            H[rs, ys] = resi[ys] / (1.0j * w[rs] - pole[ys]) + np.conj(resi[ys]) / (1.0j * w[rs] - np.conj(pole[ys]))

    Hs = np.sum(H, axis=1)

    return Hs, H


def parametry(resi, pole, tau, amplitudy):
    '''Funkcja obliczajaca parametry na podstawie
    resi - reszty
    pole - bieguny
    tau - tlumienie okna wykl.
    amplitudy - wartosci amplitud dla rozwazanych biegunow
    Zwraca macierz o kolumnach:
     Lp. sigma sigma_kor w_t�. f_t�. w_nie_t�. f_nie_t�. ksi ksi_kor Re[R] Im[R] Amplituda
    '''
    para = np.zeros((len(pole), 12))

    for n in range(len(pole)):
        para[n, 0] = n + 1.0
        para[n, 1] = pole[n].real
        if tau != 0:
            para[n, 2] = para[n, 1] + 1 / tau
        elif tau == 0:
            para[n, 2] = para[n, 1]
        para[n, 3] = pole[n].imag
        para[n, 4] = para[n, 3] / (2 * np.pi)
        para[n, 5] = np.abs(pole[n])
        para[n, 6] = para[n, 5] / (2 * np.pi)
        para[n, 7] = - para[n, 1] / para[n, 5]
        if tau != 0:
            para[n, 8] = para[n, 7] - 1 / (tau * para[n, 5])
        elif tau == 0:
            para[n, 8] = para[n, 7]
        para[n, 9] = resi[n].real
        para[n, 10] = resi[n].imag
        para[n, 11] = amplitudy[n]
    lista = []
    for n in range(len(resi)):
        if para[n, 1] > 0:
            lista.append(n)

    para = np.delete(para, lista, axis=0)
    [x, y] = np.shape(para)
    for n in range(x):
        para[n, 0] = n + 1.0

    return para
