import numpy as np
import matplotlib.pyplot as plt
'''
Wykresy okien czasowych
'''
zapis = 'n' #zapis - 'y' / wyswietlanie - 'n'

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

L=2
H_pr=2000

n = float(15)
alfa = 1 / 30 * L * H_pr
e = np.arange(0, L, 1 / H_pr)
e2 = np.copy(e)

for i in range(len(e)):
    e2[i] = 1 - (i**n) / (i**n + alfa**n)


tal = 0.25 * L
e3 = np.arange(0, L, 1/H_pr)
e4=np.exp(-1 / tal * e)
linia = 3


plt.figure(figsize=(19.2, 10.8), dpi=dpii)
plt.plot(e, e2, linewidth=linia, label=r'$\omega_r (t)$')
plt.plot(e, e4, linewidth=linia, label=r'$\omega_f (t)$')
plt.plot(e, e4*e2, linewidth=linia-1.5, label=r'$\omega_r (t) + \omega_f (t)$')
plt.title('Wykres okien czasowych', fontsize=font2)
plt.tick_params(axis='both', which='major', labelsize=font1, pad=6)
plt.xlabel(r'Czas $[s]$', fontsize=font1)
plt.ylabel('Wzmocnienie', fontsize=font1)
plt.legend(fontsize=font1)
plt.grid()
if zapis == 'y':
    plt.savefig(fname="wykresyokien.png", dpi=dpii)
else:
    plt.show()