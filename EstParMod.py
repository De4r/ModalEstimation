import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
from funkcje.metody import przeliczenie, okno_wykl, tichonow, WGM, nextpow2, zakres, znajdz, tran_widm, parametry
from funkcje.wyodrebnienie import wyodrebnienie
from funkcje.RFP import RFP
plt.rc('font', size=16)

zapis = 'y' #zapis - 'y' / wyswietlanie - 'n'


# parametry wykresow
if zapis == 'y':
    font1 = 30
    font2 = 40
    linia = 3
    linia2 = 1.75
    dpii = 300
else:
    font1 = 12
    font2 = 16
    linia = 2
    linia2 = 1.75
    dpii = 100

nazwa_pliku='D:/Odczyt_LabVIEW/pomiary_009'

dane=np.loadtxt(nazwa_pliku+'.lvm')

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
H_pr =int( 2000 ) #[Hz]
L = int ( 2 )# [s] długość pomiaru
prog = 2.5 # próg wyodrębnienia pomiaru
ticks = range(fmin,fmax,2)

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
print(f'nfft to : {nfft}')

#wyznaczenie widmowej gestosci mocy

[S11, S12, S13, S22, S33, freq] = WGM(kanal_1, kanal_2, kanal_3, H_pr, nfft, typ ='fft')
w = freq * 2.0 * np.pi
[i_min, i_max] = zakres(fmin, fmax, freq)
freq=freq[i_min:i_max]
w=w[i_min:i_max]

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


plt.figure(1)
plt.subplot(3,1,1)
plt.plot(freq, np.abs(FRF), label = '|I|')
plt.plot(freq, FRF.imag, label = 'Im(I)')
plt.xticks(ticks)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Interancja [m/s^2/N')
plt.legend()
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(freq, np.abs(V), label = '|V|')
plt.plot(freq, V.imag, label = 'Im(V)')
plt.xticks(ticks)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Interancja [m/s/N')
plt.legend()
plt.grid()

plt.subplot(3, 1, 3)
plt.plot(freq, np.abs(A), label = '|A|')
plt.plot(freq, A.imag, label = 'Im(A)')
plt.xticks(ticks)
plt.xlabel('Częstotliwość [Hz]')
plt.ylabel('Interancja [m/N')
plt.legend()
plt.grid()

plt.subplots_adjust(hspace=0.5)
plt.show()


#estymacja przedziałami
koniec = 'n'
while koniec != 'y':

    f2 = plt.figure(figsize=(19.2, 10.8), dpi=dpii)
    a2 = f2.add_subplot(111)
    a2.plot(freq, np.abs(FRF), linewidth=linia)
    a2.set_title('Charakterystyka widmowa w postaci inertancji', fontsize=font2)
    a2.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=font1)
    a2.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
    ax1 = f2.axes[0]
    ax1.set_xlim(min(freq), max(freq))
    ax1.set_ylim(0, np.amax(np.abs(FRF)) + 0.1 * np.amax(np.abs(FRF)))
    ax1.tick_params(axis='both', which='major', labelsize=font1)
    ax1c = ax1.twinx()
    ax1c.fill_between(freq, 1, Cxy, facecolor='#0079a3', alpha=0.8)
    ax1c.tick_params(axis='both', which='major', labelsize=font1)
    ax1c.set_ylabel('Koherencja', fontsize=font1)
    ax1c.set_ylim(0, 1)
    a2.grid()
    if zapis == 'y':
        plt.savefig('Iner+koherencja.png', dpi=dpii)
    else:
        plt.show()
    plt.clf()

    podzial = input('Podaj czestotliowsci dzielace wplywy postaci w formie listy f1,f2,f2 ..]: ').split(',')
    podzial = [float(n) for n in podzial]
    indeks = np.zeros((len(podzial) + 2,1), dtype=int)

    RESI = []
    POLE = []
    amp =[]
    if podzial != 0:
        for i in range(1,len(indeks)-1,1):
            indeks[i] = int(znajdz(podzial[i - 1],freq))
    elif podzial == 0:
        indeks = []

    indeks[len(indeks)-1] = i_max-i_min-1
    indeks[0] = 0

    for i in range(len(indeks) - 1):
        koniec_przedzialow = 'n'

        while koniec_przedzialow != 'y':
            plt.figure(3)
            plt.plot(freq[int(indeks[i]):int(indeks[i+1])], np.abs(FRF[int(indeks[i]):int(indeks[i+1])]))
            plt.grid()
            plt.show()


            N = int(input((' Podaj liczbe biegunów : ')))

            [Resis, Poles, alfa] = RFP(FRF[int(indeks[i]):int(indeks[i+1])], w[int(indeks[i]):int(indeks[i+1])] , N )
            [Hs, H] = tran_widm(Poles, Resis, w[int(indeks[i]):int(indeks[i+1])])
            f3 = plt.figure(figsize=(19.2, 10.8), dpi=dpii)
            a3 = f3.add_subplot(111)
            a3.plot(freq[int(indeks[i]):int(indeks[i+1])], np.abs(FRF[int(indeks[i]):int(indeks[i+1])]), 'b-', linewidth=linia)
            a3.plot(freq[int(indeks[i]):int(indeks[i+1])], np.abs(alfa), 'r--', linewidth=linia)
            a3.plot(freq[int(indeks[i]):int(indeks[i + 1])], np.abs(H), ':', linewidth=linia2)
            a3.set_title('Charakterystyka widmowa w postaci inertancji', fontsize=font2)
            a3.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=font1)
            a3.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
            a3.legend(['Inertancja - sygnał', 'Sumaryczna', 'Postać drgań'], fontsize=font1)
            ax3 = f3.axes[0]
            ax3.tick_params(axis='both', which='major', labelsize=font1)
            ax3.set_xlim(min(freq[int(indeks[i]):int(indeks[i+1])]), max(freq[int(indeks[i]):int(indeks[i+1])]))
            ax3.set_ylim(0, np.amax(np.abs(FRF[int(indeks[i]):int(indeks[i+1])])) + 0.1 * np.amax(np.abs(FRF[int(indeks[i]):int(indeks[i+1])])))
            ax3.grid()
            if zapis == 'y':
                plt.savefig(f'Inertancja - {freq[int(indeks[i])]}-{freq[int(indeks[i + 1])]}.png', dpi=dpii)
            else:
                plt.show()
            plt.clf()

            remember = 'y'
            remember = input('Czy zapamietać bieguny dla przedziału?: (y/n')

            if remember == 'y':

                for ii in range(len(Poles)):
                    if Poles[ii].real < 0 and np.abs(Poles[ii].imag) <= w[indeks[i + 1]] and np.abs(Poles[ii].imag) >= w[indeks[i]]:
                        RESI.append(Resis[ii])
                        POLE.append(Poles[ii])
                        indeksamp = znajdz(np.abs(Poles[ii].imag), w)
                        amp.append(np.abs(A[indeksamp]) * np.sign(FRF[indeksamp].imag))
                # del lista

            koniec_przedzialow = input(' Czy przejsc do kolejnego przedzialy?: (y/n)')

    koniec = input('Czy zakonczyć/powtorzyć?: (y/n)')

del Poles, Resis, ii, N, remember


[Hs, H] = tran_widm(POLE, RESI, w)
A_est = Hs / ((1j * w)**2)

f4 = plt.figure(figsize=(19.2, 10.8), dpi=dpii)
a4 = f4.add_subplot(111)
a4.plot(freq, np.abs(FRF), 'b-', linewidth=linia)
a4.plot(freq, np.abs(Hs), 'r--', linewidth=linia)
a4.set_title('Charakterystyka widmowa w postaci inertancji - sumaryczna', fontsize=font2)
a4.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=font1)
a4.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
a4.legend(['Inertancja odtworzona z sygnału', 'Inertancja powstała w wyniku estymacji'], fontsize=font1-8)
ax4 = f4.axes[0]
ax4.tick_params(axis='both', which='major', labelsize=font1)
ax4.set_xlim(min(freq), max(freq))
ax4.set_ylim(0, np.amax(np.abs(FRF)) + 0.1 * np.amax(np.abs(FRF)))
ax4.grid()
if zapis == 'y':
    plt.savefig(f'Inertancja - sumaryczna.png', dpi=dpii)
else:
    plt.show()
plt.clf()

f5 = plt.figure(figsize=(19.2, 10.8), dpi=dpii)
a5 = f5.add_subplot(111)
a5.plot(freq, np.abs(FRF), 'b-', linewidth=linia)
a5.plot(freq, np.abs(H), '-.', linewidth=linia)
a5.set_title('Charakterystyka widmowa w postaci inertancji - postacie drgań', fontsize=font2)
a5.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=font1)
a5.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
a5.legend(['Inertancja odtworzona z sygnału', 'Postacie drgań otrzymane w wyniku estymacji'], fontsize=font1-8)
ax5 = f5.axes[0]
ax5.tick_params(axis='both', which='major', labelsize=font1)
ax5.set_xlim(min(freq), max(freq))
ax5.set_ylim(0, np.amax(np.abs(FRF)) + 0.1 * np.amax(np.abs(FRF)))
ax5.grid()
if zapis == 'y':
    plt.savefig(f'Inertancja - postacie.png', dpi=dpii)
else:
    plt.show()
plt.clf()

f6 = plt.figure(figsize=(19.2, 10.8), dpi=dpii)
a6 = f6.add_subplot(111)
a6.plot(freq, np.abs(A), 'b-', linewidth=linia)
a6.plot(freq, np.abs(A_est), 'r--', linewidth=linia)
a6.set_title('Charakterystyka widmowa w postaci \npodatności dynamicznej - sumaryczna', fontsize=font2)
a6.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=font1)
a6.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=font1)
a6.legend(['Podatność dynamiczna odtworzona z sygnału', 'Podatność dynamiczna powstała w wyniku estymacji'], fontsize=font1-8)
ax6 = f6.axes[0]
ax6.tick_params(axis='both', which='major', labelsize=font1)
ax6.set_xlim(min(freq), max(freq))
ax6.set_ylim(0, np.amax(np.abs(A)) + 0.1 * np.amax(np.abs(A)))
ax6.grid()
ax6.ticklabel_format(axis='y', scilimits=(-3,3), useMathText=True)
if zapis == 'y':
    plt.savefig(f'Podatnosc - sumaryczna.png', dpi=dpii)
else:
    plt.show()
plt.clf()


FDAC_frf = (np.abs(FRF.conj() @ Hs))**2 / ((FRF.conj() @ FRF) * (Hs.conj() @ Hs))
FDAC = np.abs(A.conj() @ A_est)**2 / ((A.conj() @ A) * ( A_est.conj() @ A_est))

blad_sr_kwad_frf = sum((np.abs(FRF ) - np.abs(Hs))**2)
blad_sr_kwad_pod = sum((np.abs(A) - np.abs(A_est))**2)

blad_sr_proc_frf = (sum((np.abs(np.abs(FRF) - np.abs(Hs))) / np.abs(FRF))) / len(FRF) *100
blad_sr_proc_pod = (sum((np.abs(np.abs(A) - np.abs(A_est))) / np.abs(A))) / len(A) *100

parametry_est = parametry(RESI, POLE, L*0.25, amp)
print(parametry_est)

nazwa = f"_parametry_wyznaczone_od_{fmin}_do_{fmax}_Hz.txt"

naglowek = "Lp.     sigma    sigma_kor   w tł.    f tł.    w nie tł.   f nie tł.    ksi     ksi_kor     Re[R]    Im[R] ampl"
np.savetxt(nazwa, parametry_est, fmt="%f", header=naglowek)
