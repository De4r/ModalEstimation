import numpy as np

# skrypt pomocniczny - statystyka jakosci sygnałów

statystyka = np.zeros((5, 1))
ilosc = 0
mniej_niz_095 = []
for xy in ('x', 'y'):
    for i in range(36):
        plik = f'jakosc/wyniki{i + 1}{xy}_jakosc.txt'
        with open(plik, 'r') as file:
            temp = file.readlines()
        temp = temp[6::]

        for counter, splits in enumerate(temp):
            kosz = float(splits.split(': ', 1)[1])
            statystyka[counter] += kosz
            if counter == 1:
                if kosz < 0.90:
                    mniej_niz_095.append(f'{i+1}{xy}')
        ilosc += 1

print(statystyka)
print(ilosc)
print(mniej_niz_095)

print(statystyka / ilosc)
