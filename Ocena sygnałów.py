import matplotlib.pyplot as plt
import numpy as np
from funkcje.wyodrebnienie import wyodrebnienie

'''
Skrypt wyswietlający kolejne sygnaly wymuszenia i odpowiedzi
'''

nazwa_pliku='D:\Odczyt_LabVIEW\pomiary_0'

#zakres czest.
fzero = 0 #[Hz]
fmin = 10 #[Hz]
fmax = 100 #[Hz]

#parametry układu pom
Vmax = 5 #[V]
S_ham = 0.23
S_acc = 10.2
W_ham = 100
W_acc = 10
H_pr =int( 2000 ) #[Hz]
L = int ( 2 )# [s] długość pomiaru
prog = 2.25 # próg wyodrębnienia pomiaru
t = np.linspace(0, 2, 4000)

dl_syg = int(L*H_pr)
delay = int(dl_syg*0.01)
czas = np.arange(0, L, 1 / H_pr)

minamp=np.ones(np.shape(czas))*-5
maxamp=np.ones(np.shape(czas))*5
bin=[]
for j in range(1,73,1): # nastawy plikow 001 do 072
    if j < 10:
        filename=nazwa_pliku + '0' + str(j) + '.lvm'
    elif j >= 10:
        filename=nazwa_pliku + str(j) + '.lvm'
    dane = np.loadtxt(filename)
    [kanal_1, kanal_2, kanal_3] = wyodrebnienie(dane, delay, prog, dl_syg, Vmax)
    print(filename)
    [x, y] = np.shape(kanal_1)
    for i in range(y):
        plt.figure(1)
        plt.subplot(3, 1, 1)
        plt.plot(t, kanal_1[:, i])
        plt.plot(t, maxamp)
        plt.plot(t, minamp)
        plt.xlabel('czas [s]')
        plt.ylabel('amp wym')
        plt.grid()

        plt.subplot(3, 1, 2)
        plt.plot(t, kanal_2[:, i])
        plt.plot(t, maxamp)
        plt.plot(t, minamp)
        plt.xlabel('czas [s]')
        plt.ylabel('amp x')
        plt.grid()

        plt.subplot(3, 1, 3)
        plt.plot(t, kanal_3[:, i])
        plt.plot(t, maxamp)
        plt.plot(t, minamp)
        plt.xlabel('czas [s]')
        plt.ylabel('amp y')
        plt.grid()

        plt.subplots_adjust(hspace=0.5)
        plt.show()
    bin.append(y)

print(min(bin))
print(max(bin))
print(np.mean(bin))