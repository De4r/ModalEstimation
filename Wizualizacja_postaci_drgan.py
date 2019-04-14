from funkcje import model
import numpy as np

'''
Skrypt wizualizacji postaci dragn
ustawić parametry na dole skryptu:
rzut= 0,1,2,3
f- czest
f_tol - tolerancja
'''
def mode_shape(f, f_tol, sila=1000, zapis='n', nazwazapisu='obiekt', rzut=0):

    ''' Poniewaz 1 -36 to wymuszenie na X to wyniki{i}y są dla wymuszenia X ale odp na kierunku Y
    dlatego punkty do odwrocenia X uzete są w odpowiedzi Y, nadal nie wiem czy jest to dobrze obrazowane'''

    punkty_do_odwrocenia_znakuX = [3, 4, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24, 27, 28, 31, 32, 35, 36]
    punkty_do_odwrocenia_znakuY = [1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29, 32, 33, 36]
    nodes = np.loadtxt('nodes.txt')
    if f != 0:
        np.savetxt(fname='nodes1.txt', X=nodes, fmt="%.6f", header='lp x y z')
        nodes1 = np.loadtxt('nodes1.txt')
        [x, y] = np.shape(nodes1)

        try:
            for i in range(x):
                xdis = 0
                ydis = 0
                plik = f'parametry/wyniki{i+1}x.txt' # trzeba ustawić scieżke do plików
                temp = np.loadtxt(plik)
                [xx, yy] = np.shape(temp)
                for j in range(xx):
                    if temp[j, 4]>= f - f_tol and temp[j, 4]<= f + f_tol:
                        xdis = temp[j, 11] * 1000 * sila # na metry i razy Niuton
                        if i+1 in punkty_do_odwrocenia_znakuX:
                            xdis = xdis * -1
                plik = f'parametry/wyniki{i + 1}y.txt'
                temp = np.loadtxt(plik)
                [xx, yy] = np.shape(temp)
                for j in range(xx):
                    if temp[j, 4] >= f - f_tol and temp[j, 4] <= f + f_tol:
                        ydis = temp[j, 11] * 1000 * 1000  # na metry i razy Niuton

                nodes1[i, 1] += xdis
                nodes1[i, 2] += ydis

        except Exception as e:
             print(e)

    np.savetxt(fname='nodes1.txt', X=nodes1, fmt="%.6f", header='lp x y z')
    model.obiekt(nodes1, zapis=zapis, nazwa=nazwazapisu, rzut=rzut)


nodes = np.loadtxt('nodes.txt')
# sam model
model.obiekt(nodes, zapis='y', nazwa='obiekt_sam', rzut=0)

#rzut=: 0,1,2,3
f = 71.5
mode_shape(f=f, f_tol=1, sila=3000, zapis='y', nazwazapisu=f'postacdrgan60.7-{f}', rzut=0)
#!!! trzeba ustawić scieżke do plików w funkcji mode_shape!!!
