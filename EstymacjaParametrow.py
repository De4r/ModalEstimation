from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from funkcje.metody import przeliczenie, okno_wykl, tichonow, WGM, nextpow2, zakres, tran_widm, parametry, znajdz
from funkcje.wyodrebnienie import wyodrebnienie
from funkcje.RFP import RFP
matplotlib.use('TkAgg')

'''
Program do estymacji parametrów modalnych
Wymaga folderu funkcje z plikami
__init__.py
metody.py
orthogonal.py
RFP.py
wyodrebnienie.py
'''

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Program do estymacji parametrów modalnych")
        self.minsize(1400,800)
        #self.resizable(width=False, height=False)
        # 1280,800

        self.font = tkFont.Font(family="Arial", size=14)
        self.font2 = ('Arial', '14')
        self.fontentry = ("Arial 14")
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=self.font)

        self.s2 = ttk.Style()
        self.s2.configure('.', font=('Arial', 14))

        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Estymacja")

        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Ocena jakości dopasowania")

        self.tabControl.pack(fill=BOTH, expand=True)

        self.tab1.grid_rowconfigure(0, weight=0, minsize=200)
        self.tab1.grid_rowconfigure(1, weight=1, minsize=200)
        self.tab1.grid_columnconfigure(0, weight=3, minsize=200)
        self.tab1.grid_columnconfigure(1, weight=3, minsize=200)


        self.upperframe = Frame(self.tab1)
        self.upperframe2 = Frame(self.tab1)
        self.lowerframe = Frame(self.tab1)

        self.upperframe.grid(row=0, column=0, sticky=NE) #sticky=NE
        self.lowerframe.grid(row=1, columnspan=2, sticky=S+E+W+N)
        self.upperframe2.grid(row=0, column=1, sticky=NW)#sticky=NW

        self.przyciski(self.upperframe)
        self.opcje(self.upperframe2)

        self.ktory_zapis = 0
        self.filename = ""
        self.x = []
        self.y = []
        self.a = []
        self.b = []
        self.c = []
        self.d = []
        self.prog = 2.25
        self.Vmax = 5
        self.RESI = []
        self.POLE = []
        self.amplitudy = []
        self.znaki = []
        self.ypodatnosc = []
        self.koherencja = []

        self.tab2.grid_rowconfigure(0, weight=0)
        self.tab2.grid_rowconfigure(1, weight=1)
        self.tab2.grid_columnconfigure(0, weight=3)
        self.tab2.grid_columnconfigure(1, weight=3)
        self.tab2.grid_columnconfigure(2, weight=3)

        self.upperframetab21 = Frame(self.tab2)
        self.upperframetab22 = Frame(self.tab2)
        self.upperframetab23 = Frame(self.tab2)
        self.lowerframetab2 = Frame(self.tab2)

        self.upperframetab21.grid(row=0, column=0, sticky=NE)
        self.upperframetab22.grid(row=0, column=1)
        self.upperframetab23.grid(row=0, column=2, sticky=NW)
        self.lowerframetab2.grid(row=1, columnspan=3, sticky=S+E+W+N)

        self.opcjetab2(self.upperframetab21)
        self.wynikitab2(self.upperframetab22)
        self.zapistab2(self.upperframetab23)

        self.matplotCanvas(self.x, self.y, self.lowerframe)
        self.matplotCanvas2(self.x, self.y, self.lowerframetab2)

    def opcje(self, parent):

        self.zakres = Label(parent, text='Zakres częstotliwości [Hz]', font=self.font)
        self.zakres.grid(row=0, columnspan=5)

        self.fmin = Label(parent, text='Od', font=self.font)
        self.fminin = Entry(parent, font=self.fontentry)
        self.fmin.grid(row=1, column=0, sticky=NW)
        self.fminin.grid(row=1, column=1, sticky=NE)

        self.fmax = Label(parent, text='do', font=self.font)
        self.fmaxin = Entry(parent, font=self.fontentry)
        self.fmax.grid(row=1, column=2, sticky=NW)
        self.fmaxin.grid(row=1, column=3, sticky=NE)

        self.frfobl = Button(parent, text='Oblicz charakterystkę', font=self.font, command=self.charakterystyka)
        self.frfobl.grid(row=1, column=4)

        self.przedziallabel = Label(parent, text='Przedział częstotliwości [Hz]', font=self.font)
        self.przedziallabel.grid(row=2, columnspan=5)

        self.f1 = Label(parent, text='Od', font=self.font)
        self.f1in = Entry(parent, font=self.fontentry)
        self.f1.grid(row=3, column=0, sticky=NW)
        self.f1in.grid(row=3, column=1, sticky=NE)

        self.f2 = Label(parent, text='do', font=self.font)
        self.f2in = Entry(parent, font=self.fontentry)
        self.f2.grid(row=3, column=2, sticky=NW)
        self.f2in.grid(row=3, column=3, sticky=NE)

        self.frfprzedzial = Button(parent, text='Oblicz FRF', font=self.font, command=self.przedzial_char)
        self.frfprzedzial.grid(row=3, column=4)

        self.liczban = Label(parent, text='Podaj ilość stopni swobody N: ', font=self.font)
        self.liczban.grid(row=4, columnspan=3)
        self.n = Entry(parent, font=self.fontentry)
        self.n.grid(row=4, column=3)

        self.estymacja = Button(parent, text='Oblicz', font=self.font, command=self.estymacja)
        self.estymacja.grid(row=4, column=4)

        self.podnaz = Label(parent, text='Podaj nazwę pliku do zapisu', font=self.font)
        self.podnaz.grid(row=5, columnspan=2)

        self.nazwa = Entry(parent, font=self.fontentry)
        self.nazwa.grid(row=5, column=3, columnspan=1)

        self.clearlabel = Label(parent, text='Nowa estymacja', font=self.font)
        self.clearlabel.grid(row=0, rowspan=2, column=5)

        self.clear = Button(parent, text='Wyczyść pamięć', font=self.font, command=self.wyczysc_bieguny)
        self.clear.grid(row=2, column=5)

        self.savepar = Button(parent, text='Zapisz bieguny estymacji', font=self.font, command=self.zapis_parametrów)
        self.savepar.grid(row=5, column=4, columnspan=2)

    def przyciski(self, parent):

        self.ustlabel = Label(parent, text='Ustawienia', font=self.font)
        self.ustlabel.grid(row=0, columnspan=4)

        self.s_acc = Label(parent, text='Czuł. akc. ', font=self.font)
        self.s_accin = Entry(parent, font=self.fontentry)
        self.s_acc.grid(row=1, column=0, sticky=NW)
        self.s_accin.grid(row=1, column=1, sticky=NE)

        self.s_ham = Label(parent, text='Czuł. młotka', font=self.font)
        self.s_hamin = Entry(parent, font=self.fontentry)
        self.s_ham.grid(row=2, column=0, sticky=NW)
        self.s_hamin.grid(row=2, column=1, sticky=NE)

        self.w_acc = Label(parent, text='Wzm. akc. ', font=self.font)
        self.w_accin = Entry(parent, font=self.fontentry)
        self.w_acc.grid(row=1, column=2, sticky=NW)
        self.w_accin.grid(row=1, column=3, sticky=NE)

        self.w_ham = Label(parent, text='Wzm. młotka ', font=self.font)
        self.w_hamin = Entry(parent, font=self.fontentry)
        self.w_ham.grid(row=2, column=2, sticky=NW)
        self.w_hamin.grid(row=2, column=3, sticky=NE)

        self.l_syg = Label(parent, text='L [s]', font=self.font)
        self.l_sygin = Entry(parent, font=self.fontentry)
        self.l_syg.grid(row=3, column=0, sticky=NW)
        self.l_sygin.grid(row=3, column=1, sticky=NE)

        self.h_pr = Label(parent, text='H [Hz]', font=self.font)
        self.h_prin = Entry(parent, font=self.fontentry)
        self.h_pr.grid(row=3, column=2, sticky=NW)
        self.h_prin.grid(row=3, column=3, sticky=NE)

        self.kan_wymlabel = Label(parent, text='Kanał wymuszenia ', font=self.font)
        self.kan_wymlabel.grid(row=4, column=0, sticky=NW)
        self.kan_wym = ttk.Combobox(parent, font=self.font2)
        self.kan_wym['values'] = ('1')
        self.kan_wym.grid(row=4, column=1, sticky=NE)

        self.kan_odplabel = Label(parent, text='Kanał odpowiedzi ', font=self.font)
        self.kan_odplabel.grid(row=4, column=2, sticky=NW)
        self.kan_odp = ttk.Combobox(parent, font=self.font2)
        self.kan_odp['values'] = ( '2', '3')
        self.kan_odp.grid(row=4, column=3, sticky=NE)

        self.zapis = Button(parent, text='Zapisz ustawienia', font=self.font, command=self.save)
        self.zapis.grid(row=3, column=4)

        self.odczyt = Button(parent, text='Wczytaj ustawienia', font=self.font, command=self.odczyt)
        self.odczyt.grid(row=4, column=4)

        self.nazwaotw = Label(parent, text='Plik', font=self.font)
        self.nazwaotw.grid(row=5, column=0, sticky=NW)

        self.nazwa_pliku = ttk.Button(parent, text='Wybierz plik', style='my.TButton', command=self.przegladarkaplikow)
        self.nazwa_pliku.grid(row=5, column=1)

        self.pliklabel = Label(parent, text=" ", font=self.font)
        self.pliklabel.grid(row=5, column=2, columnspan=3)

    def opcjetab2(self, parent):

        self.nazwaotw2 = Label(parent, text='Plik z biegunami', font=self.font)
        self.nazwaotw2.grid(row=0, column=0, sticky=NW)

        self.nazwa_pliku2 = ttk.Button(parent, text='Wybierz plik', style='my.TButton', command=self.przegladarkaplikow2)
        self.nazwa_pliku2.grid(row=0, column=1)

        self.pliklabel2 = Label(parent, text=" ", font=self.font)
        self.pliklabel2.grid(row=0, column=2, columnspan=3)

        self.labelopis = Label(parent, text='Sygnał, kanały, zakres pobierane są z poprzedniego okna,\n nalezy wybrać plik z biegunami oraz typ charakterystyki,\n '
                                            'wyniki są zapisane do pliku', font=self.font)
        self.labelopis.grid(row=1, columnspan=3)

        self.charakterystykajako = Label(parent, text='Typ charakterystyki ', font=self.font)
        self.charakterystykajako.grid(row=2, columnspan=2, sticky=NW)
        self.typ = ttk.Combobox(parent, font=self.font2)
        self.typ['values'] = ('Inertancja', 'Podatność dynamiczna')
        self.typ.grid(row=2, column=3, sticky=NE)

        self.charakterystykajako2 = Label(parent, text='Typ wykresu ', font=self.font)
        self.charakterystykajako2.grid(row=3, columnspan=2, sticky=NW)
        self.typ2 = ttk.Combobox(parent, font=self.font2)
        self.typ2['values'] = ('Sumaryczna', 'Postacie drgań')
        self.typ2.grid(row=3, column=3, sticky=NE)

        self.obliczjakosc = Button(parent, text='Oblicz', font=self.font, command=self.jakosc)
        self.obliczjakosc.grid(row=4, columnspan=4)

    def wynikitab2(self, parent):

        self.labelwyniki = Label(parent, text='Wskaźniki jakości dopasowania', font=self.font)
        self.labelwyniki.grid(row=0, columnspan=2)

        self.labelfdac_frf = Label(parent, text='FDAC dla iner.', font=self.font)
        self.labelfdac_frf.grid(row=1, column=1, sticky=NW)
        self.labelfdac_frf_Wyn = Entry(parent, font=self.fontentry)
        self.labelfdac_frf_Wyn.grid(row=1, column=2, sticky=NE)

        self.labelfdac = Label(parent, text='FDAC dla podat.', font=self.font)
        self.labelfdac.grid(row=2, column=1, sticky=NW)
        self.labelfdac_Wyn = Entry(parent, font=self.fontentry)
        self.labelfdac_Wyn.grid(row=2, column=2, sticky=NE)

        self.label_blad_srednio_kwad_frf = Label(parent, text='Bład śr. kwad. dla iner.', font=self.font)
        self.label_blad_srednio_kwad_frf.grid(row=3, column=1, sticky=NW)
        self.label_blad_srednio_kwad_frf_Wyn = Entry(parent, font=self.fontentry)
        self.label_blad_srednio_kwad_frf_Wyn.grid(row=3, column=2, sticky=NE)

        self.label_blad_srednio_kwad = Label(parent, text='Bład śr. kwad. dla podat.', font=self.font)
        self.label_blad_srednio_kwad.grid(row=4, column=1, sticky=NW)
        self.label_blad_srednio_kwad_Wyn = Entry(parent, font=self.fontentry)
        self.label_blad_srednio_kwad_Wyn.grid(row=4, column=2, sticky=NE)

        self.label_blad_srednio_proc_frf = Label(parent, text='Bład śr. proc.', font=self.font)
        self.label_blad_srednio_proc_frf.grid(row=5, column=1, rowspan=2, sticky=NW)
        self.label_blad_srednio_proc_frf_Wyn = Entry(parent, font=self.fontentry)
        self.label_blad_srednio_proc_frf_Wyn.grid(row=5, column=2, rowspan=2, sticky=NE)

        #self.label_blad_srednio_proc = Label(parent, text='Bład śr. proc. dla podat.')
        #self.label_blad_srednio_proc.grid(row=6, column=1, sticky=NW)
        #self.label_blad_srednio_proc_Wyn = Entry(parent)
        #self.label_blad_srednio_proc_Wyn.grid(row=6, column=2, sticky=NE)

    def zapistab2(self, parent):

        self.labelzapis = Label(parent, text="Podaje nazwę pliku", font=self.font)
        self.labelzapis.grid(row=0, columnspan=2)

        self.zapisjakosci = Entry(parent, font=self.fontentry)
        self.zapisjakosci.grid(row=1, columnspan=2)

        self.zapisjakoscibutton = Button(parent, text='Zapisz', font=self.font, command=self.save_par_jakosci)
        self.zapisjakoscibutton.grid(row=2, columnspan=2)

    def przegladarkaplikow(self):

        self.filename = filedialog.askopenfilename(initialdir = "/", title= "wybierz plik", filetype=(("lvm","*.lvm"),("txt", "*.txt"),("All Files")))
        self.pliklabel.configure(text=self.filename)

    def przegladarkaplikow2(self):

        self.filename2 = filedialog.askopenfilename(initialdir = "/parametry", title= "wybierz plik", filetype=(("txt", "*.txt"),("All Files")))
        self.pliklabel2.configure(text=self.filename2)

    def save(self):

        try:
            S_acc = self.s_accin.get()
            S_ham = self.s_hamin.get()
            W_acc = self.w_accin.get()
            W_ham = self.w_hamin.get()
            L = self.l_sygin.get()
            H_pr = self.h_prin.get()
            kosz = [str(S_acc)+"\n", str(S_ham)+"\n", str(W_acc)+"\n", str(W_ham)+"\n", str(L)+"\n", str(H_pr)]

            with open('ustawienia.txt', 'w') as write_file:
                write_file.writelines(kosz)

        except ValueError as e:
            self.popupmsg("Błąd wartości", "Podaj wszyskie wartości jako liczby rzeczywiste\n"+e)

    def odczyt(self):

        try:
            with open('ustawienia.txt') as read_file:
                kosz = read_file.readlines()
                for i in range(len(kosz)):
                    kosz[i] = float(kosz[i])
                [S_acc, S_ham, W_acc, W_ham, L, H_pr] = kosz
                print(S_acc, S_ham, W_acc, W_ham, L, H_pr)
                self.s_accin.delete(0, END)
                self.s_hamin.delete(0, END)
                self.w_accin.delete(0, END)
                self.w_hamin.delete(0, END)
                self.l_sygin.delete(0, END)
                self.h_prin.delete(0, END)

                self.s_accin.insert(END, S_acc)
                self.s_hamin.insert(END, S_ham)
                self.w_accin.insert(END, W_acc)
                self.w_hamin.insert(END, W_ham)
                self.l_sygin.insert(END, L)
                self.h_prin.insert(END, H_pr)

        except:
            self.popupmsg("Błąd", "Oczyt się nie powiodł.\n Wprowadz parametry na nowo i zapisz")

    def matplotCanvas(self, x, y, parent):

        self.f1 = Figure(figsize=(14, 6), dpi=100)
        self.a1 = self.f1.add_subplot(111)

        self.a1.plot(x, y, 'b', linewidth=2)
        self.a1.grid()
        self.a1.set_title('Charakterystyka widmowa w postaci inertancji', fontsize=20)
        self.a1.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=18)
        self.a1.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=18)
        self.a1.tick_params(axis='both', which='major', labelsize=14)
        self.canvas1 = FigureCanvasTkAgg(self.f1, parent)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas1, parent)
        self.canvas1._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        self.update()

    def matplotCanvas2(self, x, y, parent):

        self.f2 = Figure(figsize=(14, 6), dpi=100) #19.2, 8.0
        self.a2 = self.f2.add_subplot(111)

        self.a2.plot(x, y, 'b', linewidth=1.75)
        self.a2.grid()
        self.a2.set_title('Charakterystyka widmowa w postaci inertancji', fontsize=20)
        self.a2.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=18)
        self.a2.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=18)
        self.a2.tick_params(axis='both', which='major', labelsize=14)
        self.canvas2 = FigureCanvasTkAgg(self.f2, parent)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas2, parent)
        self.canvas2._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)
        self.update()

    def refreshFigure(self, x, y, koherencja):

        self.a1.clear()
        self.a1.plot(x, y, 'b', linewidth=1.75)
        self.a1.grid()
        self.a1.set_title('Charakterystyka widmowa w postaci inertancji', fontsize=20)
        self.a1.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=18)
        self.a1.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=18)
        ax1 = self.canvas1.figure.axes[0]
        ax1.set_xlim(min(x), max(x))
        ax1.set_ylim(0, np.amax(y)+0.1*np.amax(y))
        ax1c = ax1.twinx()
        ax1c.fill_between(x, 1, koherencja, facecolor='#0079a3', alpha=0.8)
        ax1c.tick_params(axis='both', which='major', labelsize=14)
        ax1c.set_ylabel('Koherencja', fontsize=18)
        ax1c.set_ylim(0,1)
        self.canvas1.draw()
        self.canvas1.figure.delaxes(ax1c)

    def refreshFigure2(self, x, y, a, b, c, d):

        self.a1.clear()
        self.a1.plot(x, y, 'b-', linewidth=1.75)
        self.a1.plot(a, b, 'r--', linewidth=1.5)
        self.a1.plot(c, d, ':', linewidth=1)
        self.a1.grid()
        self.a1.legend(['Inertancja - sygnał', 'Sumaryczna', 'Postac drgan'], fontsize=14)
        self.a1.set_title('Charakterystyka widmowa w postaci inertancji', fontsize=20)
        self.a1.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=18)
        self.a1.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=18)
        ax1 = self.canvas1.figure.axes[0]
        ax1.set_xlim(min(x), max(x))
        ax1.set_ylim(0, np.amax(y)+0.1*np.amax(y)) #np.amin(y
        self.canvas1.draw()

    def refreshFiguretab2(self, x, y, a, b, text="inertancji", text2='sumaryczna'):

        self.a2.clear()

        if text == 'inertancji':
            self.a2.set_title('Charakterystyka widmowa w postaci ' + text + ' - ' + text2, fontsize=20)
            self.a2.set_ylabel(r'Amplituda $[\frac{m}{Ns^2}]$', fontsize=18)

            if text2 == 'sumaryczna':
                self.a2.plot(x, y, 'b-', linewidth=1.75)
                self.a2.plot(a, b, 'r--', linewidth=1.5)
                self.a2.legend(['Inertancja odtworzona z sygnału', 'Inertancja powstała w wyniku estymacji'], fontsize=14)

            elif text2 == 'postacie drgań':
                self.a2.plot(x, y, 'b-', linewidth=1.75)
                self.a2.plot(a, b, '-.', linewidth=1.5)
                self.a2.legend(
                    ['Inertancja odtworzona z sygnału', 'Postacie drgań otrzymane w wyniku estymacji'], fontsize=14)

        elif text == 'podatności dynamicznej':
            self.a2.set_title('Charakterystyka widmowa w postaci ' + text + ' - ' + text2, fontsize=20)
            self.a2.set_ylabel(r'Amplituda $[\frac{m}{N}]$', fontsize=18)

            if text2 == 'sumaryczna':
                self.a2.plot(x, y, 'b-', linewidth=1.75)
                self.a2.plot(a, b, 'r-.', linewidth=1.5)
                self.a2.legend(['Podatność dynamiczna odtworzona z sygnału', 'Podatność dynamiczna powstała w wyniku estymacji'], fontsize=14)

            elif text2 == 'postacie drgań':
                self.a2.plot(x, y, 'b-', linewidth=2)
                self.a2.plot(a, b, '-.', linewidth=1.5)
                self.a2.legend(
                    ['Podatność dynamiczna odtworzona z sygnału', 'Postacie drgań otrzymane w wyniku estymacji'], fontsize=14)

        self.a2.grid()
        self.a2.set_xlabel(r'Częstotliwość $[Hz]$', fontsize=18)
        ax2 = self.canvas2.figure.axes[0]
        ax2.set_xlim(min(x), max(x))
        ax2.set_ylim(0, np.amax(y)+0.1*np.amax(y))
        self.canvas2.draw()

    def charakterystyka(self):

        try:
            self.nazwapliku = self.filename
            dane = np.loadtxt(self.nazwapliku)
            L = float(self.l_sygin.get())
            H_pr = float(self.h_prin.get())
            Fzero = 0
            Fmin = float(self.fminin.get())
            Fmax = float(self.fmaxin.get())
            S_ham = float(self.s_hamin.get())
            W_ham = float(self.w_hamin.get())
            S_acc = float(self.s_accin.get())
            W_acc = float(self.w_accin.get())

            print(L, type(L), H_pr,type(H_pr), Fzero, Fmax, type(Fmax), Fmin)
            dl_syg = int(L * H_pr)
            delay = int(dl_syg * 0.01)

            [kanal_1, kanal_2, kanal_3] = wyodrebnienie(dane, delay, self.prog, dl_syg, self.Vmax)
            kanal_1 = przeliczenie(kanal_1, S_ham, W_ham)
            kanal_2 = przeliczenie(kanal_2, S_acc, W_acc)
            kanal_3 = przeliczenie(kanal_3, S_acc, W_acc)

            kanal_1 = okno_wykl(kanal_1, L, H_pr)
            kanal_1 = tichonow(kanal_1, L, H_pr)
            kanal_2 = okno_wykl(kanal_2, L, H_pr)
            kanal_3 = okno_wykl(kanal_3, L, H_pr)

            nfft = 3 ** (nextpow2(dl_syg))

            [S11, S12, S13, S22, S33, freq] = WGM(kanal_1, kanal_2, kanal_3, H_pr, nfft, typ='fft')
            w = freq * 2.0 * np.pi
            [i_min, i_max] = zakres(Fmin, Fmax, freq)
            freq = freq[i_min:i_max]
            w = w[i_min:i_max]

            if self.kan_wym.get() == '1' and self.kan_odp.get() == '2':
                FRF = S12[i_min:i_max] / S11[i_min:i_max]
                Cxy = np.abs(S12[i_min:i_max] ** 2 / (S11[i_min:i_max] * S22[i_min:i_max]))
            elif self.kan_wym.get() == '1' and self.kan_odp.get() == '3':
                FRF = S13[i_min:i_max] / S11[i_min:i_max]
                Cxy = np.abs(S13[i_min:i_max] ** 2 / (S11[i_min:i_max] * S33[i_min:i_max]))
            elif self.kan_wym.get() != '1' or self.kan_odp.get() != '2' or self.kan_odp.get() != '3':
                self.popupmsg("Błąd", 'Kanał wymuszenia musi być 1\n Kanał odpowiedzi musi mieć numer 1 lub 2')

            A = FRF / ((1j * w) ** 2)

            self.w = w
            self.x = freq
            self.y = FRF
            self.ypodatnosc = A
            self.koherencja = Cxy
            self.refreshFigure(self.x, np.abs(self.y), self.koherencja)

        except Exception as e:
            self.popupmsg("Błąd", f"Sprawdź kanały, parametry, przedział częstotliwości\n{e}")

    def przedzial_char(self):

        try:
            f1 = float(self.f1in.get())
            f2 = float(self.f2in.get())
            [self.i1, self.i2] = zakres(f1, f2, self.x)
            self.refreshFigure(self.x[self.i1:self.i2], np.abs(self.y[self.i1:self.i2]), self.koherencja[self.i1:self.i2])

        except Exception as e:
            self.popupmsg("Bład", f"Sprawdź częstotliwości, musza się zwierać w <F_min, F_max>\n{e}")

    def estymacja(self):

        try:
            self.RESI = []
            self.POLE = []
            self.amplitudy =[]
            N = float(self.n.get())
            [Resis, Poles, alfa] = RFP(self.y[self.i1:self.i2], self.w[self.i1:self.i2], int(N))

            [Hs, H] = tran_widm(Poles, Resis, self.w[self.i1:self.i2])
            self.refreshFigure2(self.x[self.i1:self.i2], np.abs(self.y[self.i1:self.i2]), self.x[self.i1:self.i2], np.abs(alfa), self.x[self.i1:self.i2], np.abs(H))


            for ii in range(len(Poles)):
                if float(self.f2in.get()) >= float(self.fmaxin.get()):
                    if Poles[ii].real < 0 and np.abs(Poles[ii].imag) >= self.w[self.i1]:
                        self.RESI.append(Resis[ii])
                        self.POLE.append(Poles[ii])
                        indeksamp = znajdz(np.abs(Poles[ii].imag), self.w)
                        self.amplitudy.append(np.abs(self.ypodatnosc[indeksamp]) * np.sign(self.y[indeksamp].imag))  # m/N
                else:
                    if Poles[ii].real < 0 and np.abs(Poles[ii].imag) <= self.w[self.i2] and np.abs(Poles[ii].imag) >= self.w[self.i1]:
                        self.RESI.append(Resis[ii])
                        self.POLE.append(Poles[ii])
                        indeksamp = znajdz(np.abs(Poles[ii].imag), self.w)
                        self.amplitudy.append(np.abs(self.ypodatnosc[indeksamp]) * np.sign(self.y[indeksamp].imag)) # m/N


        except Exception as e:
            self.popupmsg("Błąd", f"Wystąpił błąd. Sprawdź czy podana wartość N jest liczba naturalną.\n Jeśli tak to spróbuj zmienić zakres częstotliwości.\n{e}")

    def zapis_parametrów(self):

        save_name = 'parametry/' + self.nazwa.get() + '.txt'
        L = float(self.l_sygin.get())
        if self.ktory_zapis == 0:
            parametry_est = parametry(self.RESI, self.POLE, L * 0.25, self.amplitudy)
            naglowek = "Lp. sigma sigma_kor w_tł. f_tł. w_nie_tł. f_nie_tł. ksi ksi_kor Re[R] Im[R] Amplituda"
            np.savetxt(save_name, parametry_est, fmt="%.8f", header=naglowek)
            self.ktory_zapis += 1

        elif self.ktory_zapis > 0:
            parametry_est = parametry(self.RESI, self.POLE, L*0.25, self.amplitudy)
            tekst = 'Bieguny w przedziale od ' + self.f1in.get() +' do ' + self.f2in.get() + ' Hz'

            with open(save_name,'ab') as plik:
                np.savetxt(plik, parametry_est, fmt="%.8f", header=tekst)

    def wyczysc_bieguny(self):

        self.RESI = []
        self.POLE = []
        self.ktory_zapis = 0
        self.nazwa.delete(0, END)
        self.amplitudy = []
        self.znaki =[]
        self.popupmsg("Info", "Wyczysczono bieguny z pamięci.")

    def jakosc(self):

        try:
            self.nazwapliku = self.filename
            dane = np.loadtxt(self.nazwapliku)
            L = float(self.l_sygin.get())
            H_pr = float(self.h_prin.get())
            Fzero = 0
            Fmin = float(self.fminin.get())
            Fmax = float(self.fmaxin.get())
            S_ham = float(self.s_hamin.get())
            W_ham = float(self.w_hamin.get())
            S_acc = float(self.s_accin.get())
            W_acc = float(self.w_accin.get())

            dl_syg = int(L * H_pr)
            delay = int(dl_syg * 0.01)

            [kanal_1, kanal_2, kanal_3] = wyodrebnienie(dane, delay, self.prog, dl_syg, self.Vmax)
            kanal_1 = przeliczenie(kanal_1, S_ham, W_ham)
            kanal_2 = przeliczenie(kanal_2, S_acc, W_acc)
            kanal_3 = przeliczenie(kanal_3, S_acc, W_acc)

            kanal_1 = okno_wykl(kanal_1, L, H_pr)
            kanal_1 = tichonow(kanal_1, L, H_pr)
            kanal_2 = okno_wykl(kanal_2, L, H_pr)
            kanal_3 = okno_wykl(kanal_3, L, H_pr)

            nfft = 3 ** (nextpow2(dl_syg))

            [S11, S12, S13, S22, S33, freq] = WGM(kanal_1, kanal_2, kanal_3, H_pr, nfft, typ='fft')
            w = freq * 2.0 * np.pi
            [i_min, i_max] = zakres(Fmin, Fmax, freq)
            freq = freq[i_min:i_max]
            w = w[i_min:i_max]

            if self.kan_wym.get() == '1' and self.kan_odp.get() == '2':
                FRF = S12[i_min:i_max] / S11[i_min:i_max]

            elif self.kan_wym.get() == '1' and self.kan_odp.get() == '3':
                FRF = S13[i_min:i_max] / S11[i_min:i_max]

            elif self.kan_wym.get() != '1' or self.kan_odp.get() != '2' or self.kan_odp.get() != '3':
                self.popupmsg("Błąd", 'Kanał wymuszenia musi być 1\n Kanał odpowiedzi musi mieć numer 1 lub 2')

            self.w = w
            self.x = freq
            self.y = FRF

            self.nazwapliku2 = self.filename2
            a = np.loadtxt(self.nazwapliku2)
            [r, c] = np.shape(a)
            resi = []
            pole = []
            for rs in range(int(r)):
                resi.append(a[rs, 9] + 1j * a[rs, 10])
                pole.append(a[rs, 1] + 1j * a[rs, 3])

            [Hs, H] = tran_widm(pole, resi, self.w)

            A_est = Hs / ((1j * w) ** 2)
            A_estbieg = np.zeros(np.shape(H), dtype='complex')
            for rs in range(int(r)):
                A_estbieg[:, rs] = H[:, rs] / ((1j * w) ** 2)
            A = FRF / ((1j * w) ** 2)
            #kryterium oceny fdac dla inertnacji
            self.FDAC_frf = ((np.abs(FRF.conj() @ Hs)) ** 2 / ((FRF.conj() @ FRF) * (Hs.conj() @ Hs))).real
            self.labelfdac_frf_Wyn.delete(0, END)
            self.labelfdac_frf_Wyn.insert(END, f'{self.FDAC_frf:.4f}')
            #kryterium oceny fdac dla podatnosci
            self.FDAC = (np.abs(A.conj() @ A_est) ** 2 / ((A.conj() @ A) * (A_est.conj() @ A_est))).real
            self.labelfdac_Wyn.delete(0, END)
            self.labelfdac_Wyn.insert(END, f'{self.FDAC:.4f}')
            #blad srednio kwadratowy dla inertancji
            self.blad_sr_kwad_frf = sum((np.abs(FRF) - np.abs(Hs)) ** 2)
            self.label_blad_srednio_kwad_frf_Wyn.delete(0, END)
            self.label_blad_srednio_kwad_frf_Wyn.insert(END, f'{self.blad_sr_kwad_frf:.4f}')
            #blad srednio kwadratowy dla podatnosci
            self.blad_sr_kwad_pod = sum((np.abs(A) - np.abs(A_est)) ** 2)
            self.label_blad_srednio_kwad_Wyn.delete(0, END)
            self.label_blad_srednio_kwad_Wyn.insert(END, f'{self.blad_sr_kwad_pod:.2e}')
            #bład srednio procentowy dla inertancji
            self.blad_sr_proc_frf = (sum((np.abs(np.abs(FRF) - np.abs(Hs))) / np.abs(FRF))) / len(FRF) * 100
            self.label_blad_srednio_proc_frf_Wyn.delete(0, END)
            self.label_blad_srednio_proc_frf_Wyn.insert(END, f'{self.blad_sr_proc_frf:.4f}%')
            #bład srednio-procentowy dla podatnosci
            #self.blad_sr_proc_pod = (sum((np.abs(np.abs(A) - np.abs(A_est))) / np.abs(A))) / len(A) * 100
            #self.label_blad_srednio_proc_Wyn.delete(0, END)
            #self.label_blad_srednio_proc_Wyn.insert(END, f'{self.blad_sr_proc_pod:.4f}%')

            if self.typ.get() == 'Inertancja':
                if self.typ2.get() == 'Sumaryczna':
                    self.refreshFiguretab2(self.x, np.abs(self.y), self.x, np.abs(Hs), text="inertancji", text2='sumaryczna')
                elif self.typ2.get() == 'Postacie drgań':
                    self.refreshFiguretab2(self.x, np.abs(self.y), self.x, np.abs(H), text="inertancji", text2='postacie drgań')

            elif self.typ.get() == 'Podatność dynamiczna':
                if self.typ2.get() == 'Sumaryczna':
                    self.refreshFiguretab2(self.x, np.abs(A), self.x, np.abs(A_est), text="podatności dynamicznej", text2='sumaryczna')
                elif self.typ2.get() == 'Postacie drgań':
                    self.refreshFiguretab2(self.x, np.abs(A), self.x, np.abs(A_estbieg), text="podatności dynamicznej", text2='postacie drgań')

        except:
            self.popupmsg("Błąd", "Wystąpił błąd, sprawdz poprawność wprowadzonych danych.")

    def save_par_jakosci(self):
        nazwa = 'jakosc/' + self.zapisjakosci.get() + '.txt'
        naglowek = 'Parametry oceny jakości dopasowania charakterystyki otrzymanej z estmyacji parametrów modalnych\nParametry otrzymane dla:\n'
        dla = 'Sygnał: ' + self.nazwapliku + '\nZakres: ' + self.fminin.get() +' do ' + self.fmaxin.get() +' Hz\nKanały: wymuszenie- '\
              + self.kan_wym.get() + ' odpowiedz- ' + self.kan_odp.get() + '\nBieguny z pliku: ' + self.nazwapliku2 +'\n'

        kosz =[naglowek, dla, 'FDAC dla inertancji [-]: ', str(self.FDAC_frf) +'\n', 'FDAC dla podatności [-]: ',
               str(self.FDAC) +'\n', 'Bład średniokwadratowy dla inertancji [-]: ', str(self.blad_sr_kwad_frf) + '\n', 'Bład średnio kwadratowy dla podatnosci [-]: ',
               str(self.blad_sr_kwad_pod) + '\n', 'Bład średnioprocentowy [%]: ', str(self.blad_sr_proc_frf) + '\n']

               #'Bład średnio procentowy dla podatnosci [%]: ', str(self.blad_sr_proc_pod)]

        with open(nazwa, 'w') as write_file:
            write_file.writelines(kosz)

    def popupmsg(self, tytul, msg):
         var = messagebox.showinfo(tytul, msg)


if __name__ == '__main__':

    app = Root()
    app.mainloop()