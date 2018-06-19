import threading
import random
from Shaolin import Shaolin
from Judo import Judo
from Taekwondo import Taekwondo
import time

class Plansza:

    def __init__(self):
        self.okno_koncowe = 0
        self.ktore_menu = 1
        self.ktora_opcja = 1
        self.p1, self.p2, self.p3 = 1, 0, 0
        self.zakoncz_watki = False

        self.czas_w_ktorym_gracz_kopnal_lezacego = 0
        self.czas_w_ktorym_gracz_zostal_zaatakowany = 0
        self.gracz = None
        self.poziom_trudnosci = 1 ##1, 2, 3 przewidziane
        self.konczymy = False
        self.menu = False
        self.lock = threading.Lock()
        self.lezacy = [] #jej typ to [(int,int,Zawodnik)]
        self.krew = []
        for i in range(0, 9):
            a = []
            for j in range(0, 16):
                a.append(0)
            self.krew.append(a)
        self.rezerwacja = []
        for i in range(0, 9):
            a = []
            for j in range(0, 16):
                a.append(False)
            self.rezerwacja.append(a)
        self.plansza = []
        for i in range(0, 9):
            a = []
            for j in range(0, 16):
                a.append(None)
            self.plansza.append(a)
        self.spis_zywych, self.spis_martwych = [], []

    def dodaj_zawodnikow(self, s, j, t):
        """Dodaje do planszy zawodnikow"""
        for i in range(0, s):
            self.spis_zywych.append(Shaolin(self))
        for i in range(0, j):
            self.spis_zywych.append(Judo(self))
        for i in range(0, t):
            self.spis_zywych.append(Taekwondo(self))
        for i in self.spis_zywych:
            if i == self.gracz:
                continue
            self.wloz_kogos_gdzies(i)
            if self.poziom_trudnosci == 1:
                i.HP, i.en, i.makshp, i.maksen = 70, 70 , 70 ,70
            elif self.poziom_trudnosci == 1:
                i.HP, i.en, i.makshp, i.maksen = 100, 100 , 100 ,100
            elif self.poziom_trudnosci == 1:
                i.HP, i.en, i.makshp, i.maksen = 120, 120 , 120 ,120
            i.start()

    def pozakancza_watki(self):
        """Niszczy wszystkich zawodnikow"""
        for i in self.spis_zywych:
            if i != self.gracz:
                print(i.stan)
                i.join()
                print("zjoinowany")
        self.zakoncz_watki = False

    class niszczyciel(threading.Thread):
        """Watek do niszczenia watkow"""
        def __init__(self, p):
            threading.Thread.__init__(self)
            self.p = p
        def run(self):
            self.p.pozakancza_watki()

    def resetuj_calosc(self):
        """Niszczy stara i przygotowuje nowa podstawe pod nowa gre"""
        #print("resetujemy")
        self.zakoncz_watki = True
        #print("tworzymy niszczyciela")
        a = self.niszczyciel(self)
        #print("zaraz_zaczne niszczyc watki")
        a.start()
        #print("zaczelam niszczyc watki")
        while self.zakoncz_watki:
            time.sleep(0.01)
            #print("koncze watki")

        #print("zakonczylem watki")
        if self.poziom_trudnosci == 1:
            self.gracz.makshp, self.gracz.maksen = 300, 300
        elif self.poziom_trudnosci == 2:
            self.gracz.makshp, self.gracz.maksen = 200, 200
        elif self.poziom_trudnosci == 3:
            self.gracz.makshp, self.gracz.maksen = 150, 150
        self.gracz.HP = self.gracz.maks_hp_i_energii()[0]
        self.gracz.reset()

        self.czas_w_ktorym_gracz_kopnal_lezacego = 0
        self.czas_w_ktorym_gracz_zostal_zaatakowany = 0
        self.lezacy = []
        for i in range(0, 9):
            for j in range(0, 16):
                self.krew[i][j] = 0
                self.rezerwacja[i][j] = False
                self.plansza[i][j] = None
        self.spis_zywych, self.spis_martwych = [], []
        self.dodaj_gracza(self.gracz)

    def dodaj_gracza(self, gracz):
        """Wrzuca gracza na plansze"""
        self.gracz = gracz
        self.spis_zywych.append(gracz)
        if self.plansza[4][7] == None:
            self.plansza[4][7] = gracz
            gracz.ustaw_wsp(7, 4)
        else:
            self.wloz_kogos_gdzies(gracz)

    def dodaj_lezacego(self, zawodnik):
        """Komunikuje planszy, ze dany gracz tu lezy czyli np pole nie jest zajete"""
        for i in self.lezacy:
            if i[2] == zawodnik:
                return
        self.lezacy.append((zawodnik.x, zawodnik.y, zawodnik))

    def lezy_tu_ktos(self, x, y):
        """Mowi czy ktos lezy na polu o tych wspolrzednych"""
        for i in self.lezacy:
            if i[0] == x and i[1] == y:
                return True
        return False

    def usun_lezacego(self, zawodnik):
        """Usuwa lezacego"""
        for i in self.lezacy:
            if(i[2] == zawodnik):
                self.lezacy.remove(i)

    def zaplam(self, x, y, ile):
        """Nanosi krew na plansze"""
        if ile == 1000:
            self.krew[y][x] -= self.krew[y][x]%1000
            self.krew[y][x] += 1000
        else:
            if self.krew[y][x] == 0 or self.krew[y][x]%1000!=0:
                self.krew[y][x] += ile

    def wspolrzedne_w_planszy(self, x, y):
        """Mowi czy wspolrzedne naleza do planszy"""
        return (x>-1 and x<16 and y>-1 and y<9)

    def wloz_kogos_gdzies(self, ktos):
        """Wrzuca zawodnika na plansze"""
        while True:
            x, y = random.randint(0, 15), random.randint(0, 8)
            if (x != 7 or y != 4) and self.plansza[y][x] == None:
                ktos.ustaw_wsp(x, y)
                self.plansza[y][x] = ktos
                break

    def zajmij_pole(self, x, y):
        """Rezerwuje pole na planszy"""
        if x<0 or x>15 or y<0 or y>8:
            return False
        udalo_sie = False
        self.lock.acquire()
        if not self.rezerwacja[y][x] and self.plansza[y][x] == None:
            self.rezerwacja[y][x] = True
            udalo_sie = True
        self.lock.release()
        return udalo_sie

    def zwolnij_pole(self, x, y):
        """Zdejmuje rezerwacje pola"""
        self.rezerwacja[y][x] = False

    def pozyskaj_animacje(self, x, y):
        """Daje animacje danego obiektu na odpowiednim miejscu na planszy"""
        if self.plansza[y][x] == None:
            return None
        return self.plansza[y][x].animation()

    def pozyskaj_przesuniecie(self, x, y):
        """Daje przeksztalcenie w pozycji danego obiektu na odpowiednim miejscu na planszy"""
        #wydajniej jest zrobic ja oddzielna od pozyskaj animacje
        if self.plansza[y][x] == None:
            return (0, 0)
        return self.plansza[y][x].przesuniecie_x, self.plansza[y][x].przesuniecie_y

    def zamelduj_sie(self, zawodnik):
        """Wskazuje planszy na realne istnienie obiektu w tym miejscu planszy"""
        assert self.wspolrzedne_w_planszy(zawodnik.x, zawodnik.y)
        assert self.plansza[zawodnik.y][zawodnik.x] == None
        self.plansza[zawodnik.y][zawodnik.x] = zawodnik

    def odmelduj_sie(self, x, y):
        """Wskazuje na brak obiektow w tym miejscu"""
        self.plansza[y][x] = None





