import numpy as np
import matplotlib.pyplot as plt
from funkcje.metody import przeliczenie, okno_wykl, tichonow, WGM, nextpow2, zakres, znajdz, tran_widm, parametry
from funkcje.wyodrebnienie import wyodrebnienie
plt.rc('font', size=16)

'''
Skrypt do tworzenia wykresów charakterystyk z pliku z pomiarami
Parametry:
zapis - y/n - tworzenie grafik do zapisu/ wyswietlanie wykresów
parametry toru pomiarowego
zakres czestotliwosci
parametry wykresów

Wyświetlanie i zapis jednoczesnie generuje słabej jakosci wykresy
'''

zapis = 'y' #zapis - 'y' / wyswietlanie - 'n'

# scieżka
nazwa_pliku='D:/Odczyt_LabVIEW/pomiary_009'
dane=np.loadtxt(nazwa_pliku+'.lvm')

# parametry wykresow
if zapis == 'y':
    font1 = 30
    font2 = 40
    linia = 3
    dpii = 300
else:
    font1 = 12
    font2 = 16
    linia = 2
    dpii = 100

#zakres czest.
fzero = 0 #[Hz]
fmin = 10 #[Hz]
fmax = 80 #[Hz]

#parametry układu pom
Vmax = 5 #[V]
S_ham = 0.23
S_acc = 10.2
W_ham = 100
W_acc = 10
H_pr =int(2000) #[Hz]
L = int(2)# [s] długość pomiaru
prog = 2.5 # próg wyodrębnienia pomiaru
ticks = range(fmin,fmax,4)

# obliczenia -------------V-------------------
dl_syg = int(L*H_pr)
delay = int(dl_syg*0.01)
czas = np.arange(0, L, 1 / H_pr)


[kanal_1, kanal_2, kanal_3] = wyodrebnienie(dane, delay, prog, dl_syg, Vmax)


kanal_1 = przeliczenie(kanal_1,S_ham, W_ham)
kanal_2 = przeliczenie(kanal_2,S_acc,W_acc)
kanal_3 = przeliczenie(kanal_3,S_acc,W_acc)

kanal_1 = okno_wykl(kanal_1 ,L, H_pr)
kanal_1 = tichonow(kanal_1 ,L, H_pr)
kanal_2 = okno_wykl(kanal_2, L, H_pr)
kanal_3 = okno_wykl(kanal_3, L, H_pr)


nfft=3**(nextpow2(dl_syg))

#wyznaczenie widmowej gestosci mocy

[S11, S12, S13, S22, S33, freq] = WGM(kanal_1, kanal_2, kanal_3, H_pr, nfft, typ ='fft')
w = freq * 2.0 * np.pi
[i_min, i_max] = zakres(fmin, fmax, freq)
freq=freq[i_min:i_max]
w=w[i_min:i_max]



plt.figure(figsize=(19.2, 10.8), dpi=dpii)
plt.plot(freq, np.abs(S11[i_min:i_max]), linewidth=linia)
plt.xticks(ticks)
plt.title('Gęstość widmowa mocy własna', fontsize=font2)
plt.xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
plt.ylabel(r'$S_{xx} [\frac{N^2}{Hz}]$', fontsize=font1, labelpad=2)
plt.tick_params(axis='both', which='major', labelsize=font1, pad=3)
plt.grid()
if zapis == 'y':
    plt.savefig(fname='S11.png', dpi=dpii)
else:
    plt.show()


plt.figure(figsize=(19.2, 10.8), dpi=dpii)
plt.plot(freq, np.abs(S12[i_min:i_max]), linewidth=linia)
plt.xticks(ticks)
plt.title('Gęstość widmowa mocy wzajemna', fontsize=font2)
plt.xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
plt.ylabel(r'$S_{xy} [\frac{\frac{N m}{s^2} }{Hz}]$', fontsize=font1)
plt.tick_params(axis='both', which='major', labelsize=font1, pad=3)
plt.grid()
if zapis == 'y':
    plt.savefig(fname='S12.png', dpi=dpii)
else:
    plt.show()

kanal_est = int(input('Podaj dla ktorego kanalu chcesz wyznaczyc odpowiedz (2 lub 3): '))
V = np.zeros(np.shape(freq), dtype='complex')
A = np.copy(V)
FRF = np.copy(V)

if kanal_est == 2:
    FRF = S12[i_min:i_max] / S11[i_min:i_max]
    Cxy = np.abs(S12[i_min:i_max]**2 / (S11[i_min:i_max] * S22[i_min:i_max]))
    V = FRF / (1j * w)
    A = V / (1j * w)
elif kanal_est == 3:
    FRF = S13[i_min:i_max] / S11[i_min:i_max]
    Cxy = np.abs(S13[i_min:i_max] ** 2 / (S11[i_min:i_max] * S33[i_min:i_max]))
    V = FRF / (1j * w)
    A = V / (1j * w)


plt.figure(figsize=(19.2, 10.8), dpi=dpii)
plt.plot(freq, np.abs(FRF), linewidth=linia, label = r'$|I|$')
plt.plot(freq, FRF.imag, 'r--', linewidth=linia, label = r'$Im(I)$')
plt.xticks(ticks)
plt.title('Charakterystyka częstotliwościowa w postaci inertancji', fontsize=font2)
plt.xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
plt.ylabel(r'Inertancja $[\frac{m}{Ns^2}]$', fontsize=font1)
plt.tick_params(axis='both', which='major', labelsize=font1, pad=3)
plt.legend(fontsize=font1)
plt.grid()
if zapis == 'y':
    plt.savefig(fname='inertancja.png', dpi=300)
else:
    plt.show()


plt.figure(figsize=(19.2, 10.8), dpi=dpii)
plt.plot(freq, np.abs(A), linewidth=linia, label = r'$|A|$')
plt.plot(freq, A.imag, 'r--', linewidth=linia, label = r'$Im(A)$')
plt.xticks(ticks)
plt.title('Charakterystyka częstotliwościowa w postaci\n podatności dynamicznej', fontsize=font2)
plt.xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
plt.ylabel(r'Podatność dynamiczna $[\frac{m}{N}]$', fontsize=font1)
plt.tick_params(axis='both', which='major', labelsize=font1, pad=3)
plt.ticklabel_format(axis='y', scilimits=(-3,3), useMathText=True)
plt.legend(fontsize=font1)
plt.grid()
if zapis == 'y':
    plt.savefig(fname='podatnosc.png', dpi=300)
else:
    plt.show()


plt.figure(figsize=(19.2, 10.8), dpi=dpii)
plt.plot(freq, np.abs(V), linewidth=linia, label = r'$|V|$')
plt.plot(freq, V.imag, 'r--', linewidth=linia, label = r'$Im(V)$')
plt.xticks(ticks)
plt.title('Charakterystyka częstotliwościowa w postaci mobilności', fontsize=font2)
plt.xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
plt.ylabel(r'Mobilność $[\frac{m}{Ns}]$', fontsize=font1)
plt.tick_params(axis='both', which='major', labelsize=font1, pad=3)
plt.ticklabel_format(axis='y', style='sci')
plt.legend(fontsize=font1)
plt.grid()
if zapis == 'y':
    plt.savefig(fname='mobilnosc.png', dpi=300)
else:
    plt.show()
