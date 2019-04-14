import numpy as np
from numpy import zeros


'''
Funkcja wyodrebniajaca pojedyncze sygnaly z pliku pomiarowego

Dane wejsciowe:
wyniki - mcaierz ze sygnalami, 1 kolumna - wymuszenie, pozostale odpowiedzi
delay - wartosc opoznienia, o ktora sygnal jest cofany
prog - prog wykrycia pomiaru na podstawie sygnalu wymuszenia
dl_syg - dlugosc sygnalu do wyodrebnienia
Vmax - maksymalne napiecie w celu usuniecia sygnalow przesterowanych

'''


def wyodrebnienie(wyniki, delay, prog, dl_syg, Vmax):

    k = 35  # wartosc w celu prealokacji pamieci

    wzb = zeros((dl_syg, k))
    odpy = np.copy(wzb)
    odpx = np.copy(wzb)
    i = 0
    kk = 0

    while i <= len(wyniki) - dl_syg - 1:

        if abs(wyniki[i, 0]) > prog:
            if max(abs(wyniki[i - delay:i + dl_syg - delay, 0])) < Vmax:
                if max(abs(wyniki[i - delay:i + dl_syg - delay, 1])) < Vmax:
                    if max(abs(wyniki[i - delay:i + dl_syg - delay, 2])) < Vmax:

                        wzb[0:dl_syg, kk] = np.copy(wyniki[i - delay:i + dl_syg - delay, 0])
                        odpx[0:dl_syg, kk] = np.copy(wyniki[i - delay:i + dl_syg - delay, 1])
                        odpy[0:dl_syg, kk] = np.copy(wyniki[i - delay:i + dl_syg - delay, 2])

                        kk += 1

            i += 1 + dl_syg - delay
        i += 1

    # informacja o ilosci poprawnych sygnalow - kk
    [x, y] = np.shape(wzb)
    print(f'wymiar macierzy wzb -{y}')
    print(f' akutalny licznik to - {kk}')

    # usuniecie pustych kolumn
    for ys in range(k - 1, kk - 1, -1):
        if max(wzb[:, ys]) <= 0:
            wzb = np.delete(wzb, ys, 1)
            odpx = np.delete(odpx, ys, 1)
            odpy = np.delete(odpy, ys, 1)

    return wzb, odpx, odpy



