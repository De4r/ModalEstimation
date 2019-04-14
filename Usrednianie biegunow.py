import numpy as np

'''
Skrypt uśredniający wyznaczone parametry modalne uzyskane w eksperymentalnej analizy modalnej
'''


liczba_iteracji = 36  # liczba wezlow pomiarowych

# tworzenie macierzy oraz indeksowanie wierszow
postacie = np.zeros((200, 10))
[wiersze, kolumny] = np.shape(postacie)
for j in range(wiersze):
    postacie[j, 0] = j + 1

ilosc = 0  # parametr okreslajacy ilosc aktualnie istniejacych potaci drgan
f_tol = 0.3  # parametr tolerancji zakresu czestotliwosci postaci drgan
f_max = 80  # maskymalna czestotliwosc rozpatrywana w eksperymencie
sigma_max = 20  # maksymalny wspolczynnik tlumienia (odrzucanie biegunow nie rzeczywsitych)
licznik_min = 5  # minimalna ilosc wystapien potaci drgan

for xy in ('x', 'y'):
    for i in range(liczba_iteracji):
        plik = f'parametry/wyniki{i + 1}{xy}.txt'
        temp = np.loadtxt(fname=plik)
        [rows, cols] = np.shape(temp)
        if i == 0 and xy == 'x':
            for j in range(rows):
                if temp[j, 4] <= f_max and np.abs(temp[j, 2]) <= sigma_max:
                    for jj in range(8):
                        postacie[j, jj+1] = temp[j, jj+1]
                    postacie[j, 9] += 1
            ilosc = rows  # aktualizacja licznika istniejacych postaci drgan w macierzy

        else:
            for j in range(rows):
                if temp[j, 4] <= f_max and np.abs(temp[j, 2]) <= sigma_max:
                    check = 0  # licznik w celu sprawdzenia czy aktualnie rozpatrywana postac istnieje
                    for jj in range(ilosc):
                        if postacie[jj, 4] / postacie[jj, 9] - f_tol <= temp[j, 4] and postacie[jj, 4] / postacie[jj, 9]  + f_tol >= temp[j, 4]:
                            for jjj in range(8):
                                postacie[jj, jjj + 1] += temp[j, jjj + 1]
                            postacie[jj, 9] += 1
                            break
                        else:
                            check += 1  # inkrementacja jeśli nie istnieje dana czestosc drgan
                    if check == ilosc:  # dodanie nowej postaci drgan jesli nie istnieje odpowiednik
                        for jjj in range(8):
                            postacie[ilosc, jjj + 1] = temp[j, jjj + 1]
                        postacie[ilosc, 9] += 1
                        ilosc += 1  # inkrementacja ilosc istniejacych czestosci


postacie[:, 7:9] = postacie[:, 7:9] * 100  # przeliczenie bezwym. wspol. tlum. na procenty

[wier, kolu] = np.shape(postacie)
for wiersz in range(wier - 1, ilosc - 1, -1):  # usuniecie pustych wierszy macierzy
    if postacie[wiersz, 9] == 0:
        postacie = np.delete(postacie, wiersz, 0)

[wier, kolu] = np.shape(postacie)
for i in range(wier):  # usrednianie wyznaczonych parametrow ( sum(i)/ilosc )
    for j in range(8):
        postacie[i, j+1] = postacie[i, j+1] / postacie[i, 9]

[wier, kolu] = np.shape(postacie)
for wiersz in range(wier - 1, -1, -1):  # usuniecie postaci drgan o dodatnim wspolczynniku tlumienia
    if np.abs(postacie[wiersz, 2]) >= sigma_max:
        postacie = np.delete(postacie, wiersz, 0)

[wier, kolu] = np.shape(postacie)
for wiersz in range(wier - 1, -1, -1):  # usuniecie postaci dragn o liczniku wystapien < licznik_min
    if np.abs(postacie[wiersz, 9]) < licznik_min:
        postacie = np.delete(postacie, wiersz, 0)

postacie = postacie[postacie[:, 9].argsort()]  # sortowanie po liczniku wystapien

# zapis parametrow do pliku
naglowek = "Lp. sigma sigma_kor w_tł. f_tł. w_nie_tł. f_nie_tł. ksi ksi_kor licznik"
np.savetxt("Postacie drgan.txt", postacie, fmt="%.8f", header=naglowek)
