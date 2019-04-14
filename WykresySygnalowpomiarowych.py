import matplotlib.pyplot as plt
import numpy as np
from funkcje.metody import przeliczenie

'''
Skrypt do rysowania wykresów wymuszenia i odpowiedzi
'''

filename='D:\Odczyt_LabVIEW\pomiary_042.lvm' # sciezka do pliku

co = 'odp' # wykres 'odp' - odpowiedzi, 'wym' - wymuszenia

dane = np.loadtxt(filename)
#parametry układu pom
Vmax = 5 #[V]
S_ham = 0.23
S_acc = 10.2
W_ham = 100
W_acc = 10
H_pr =int( 2000 ) #[Hz]
L = int ( 2 )# [s] długość pomiaru
t = np.linspace(0, 2, 4000)

dl_syg = int(L*H_pr)
delay = int(dl_syg*0.01)
czas = np.arange(0, L, 1 / H_pr)

t=np.arange(0, len(dane) / H_pr, 1 / H_pr)

kanal_1 = przeliczenie(dane[:, 0],S_ham, W_ham)
kanal_2 = przeliczenie(dane[:, 1],S_acc,W_acc)
kanal_3 = przeliczenie(dane[:, 2],S_acc,W_acc)

if co == 'wym':
    plt.figure(1)
    plt.plot(t, kanal_1, linewidth=1)
    plt.xlabel(r'Czas [s]', fontsize=12)
    plt.ylabel(r'Amplituda [N] ', fontsize =12)
    plt.title('Przebieg czasowy sygnału wymuszenia', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=12, pad=6)
    plt.grid()
    #plt.show()
    plt.savefig('wymuszenie.png', format='png', dpi=300)
elif co == 'odp':
    plt.figure(1)
    plt.plot(t, kanal_2, linewidth=1)
    plt.xlabel(r'Czas [s]', fontsize=12)
    plt.ylabel(r'Amplituda $[\frac{m}{s^2}]$', fontsize =12)
    plt.title('Przebieg czasowy sygnału odpowiedzi', fontsize =16)
    plt.tick_params(axis='both', which='major', labelsize=12, pad=6)
    plt.grid()
    #plt.show()
    plt.savefig('odpowiedz.png', format='png', dpi=300)


