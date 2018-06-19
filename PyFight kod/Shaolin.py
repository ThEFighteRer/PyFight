from Zawodnik import Zawodnik
import threading
import random
import time


class Shaolin(Zawodnik, threading.Thread):

    def __init__(self, plansza):
        super().__init__(plansza)
        #super().super().__init__()
        threading.Thread.__init__(self)
        self.kim_jestem = 3000

    def rozbij_garde(self):#136, 138, 140
        """Obsluguje cios specjalny"""
        self.stan = 's'
        for i in range(0, 40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <= 10:
                    return self.szuraj_po_ziemii()
                else:
                    return self.animuj_bycie_uderzonym()
            if not self.jestem_graczem and self.jestem_uderzony:
                self.jestem_uderzony = False
                return self.animuj_bycie_uderzonym()
            #if self.jestem_graczem and self.jestem_przerzucany:
            #    return False
            if self.czy_koniec():
                return False
            self.aaanimacja = 136 + 2 * int((i) / 16)
            self.ustaw_przesuniecie(self.zwrot, 1, i)
            time.sleep(0.00625)

        x, y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
        if self.plansza.wspolrzedne_w_planszy(x, y) and self.plansza.plansza[y][x] != None\
                and self.plansza.plansza[y][x].stan != 'w' and self.plansza.plansza[y][x].stan != 'u':
            self.plansza.plansza[y][x].rozbita_garda = True
            self.plansza.plansza[y][x].zostan_uderzony(10, 2)
            self.ile_ciosow_otrzymalem_w_serii = 0

        for i in range(0, 40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <= 10:
                    return self.szuraj_po_ziemii()
                else:
                    return self.animuj_bycie_uderzonym()
            if not self.jestem_graczem and self.jestem_uderzony:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                return self.animuj_bycie_uderzonym()
            if self.jestem_graczem and self.jestem_przerzucany:
                return False
            if self.czy_koniec():
                return False
            self.aaanimacja = 140 - 2 * int((i) / 14)
            self.ustaw_przesuniecie(self.zwrot, 1, 40 - i)
            time.sleep(0.00625)

        self.reset_animacji()

    def run(self):
        """Tu podejmowane sa decyzje, dzialania i caly okres zycia watku"""
        while not self.plansza.konczymy:

            time.sleep(0.01)
            if self.czy_koniec():
                return

            self.stan = 'n'
            if self.jestem_kopniety:
                self.ile_ciosow_otrzymalem_w_serii += 1
                if self.energia <= 10:
                    self.szuraj_po_ziemii()
                else:
                    self.animuj_bycie_uderzonym()
                self.jestem_kopniety = False
                self.jestem_uderzony = False
            if self.jestem_uderzony:
                self.ile_ciosow_otrzymalem_w_serii += 1
                self.animuj_bycie_uderzonym()
                self.jestem_uderzony = False
                self.jestem_kopniety = False
            if self.czy_koniec():
                return

            self.co_robie = self.decyzja()

            if self.co_robie == 'g':
                self.trzymam_garde()
            elif self.co_robie == 'a':
                self.atakuje()
            elif self.co_robie == 'c':
                self.chodze_bez_sensu()
            elif self.co_robie == 'u':
                self.uciekam()

    def atakuje(self):
        """Funkcja odpowiedzialna za dzialania, gdy zawodnik zdecyduje sie atakowac gracza"""
        g = self.plansza.gracz
        while True:
            if self.czy_koniec():
                return
            if self.jestem_kopniety or self.jestem_uderzony:
                return
            self.plansza.czas_w_ktorym_gracz_zostal_zaatakowany = time.clock()

            self.co_robie = self.decyzja()
            if self.co_robie != 'a':
                break

            if self.jestem_zaraz_obok(g.x, g.y):
                v = self.ile_ludzi_okraza_gracza() - int(self.plansza.poziom_trudnosci / 2)
                if self.HP < self.plansza.poziom_trudnosci * 10:
                    v = int(v / self.plansza.poziom_trudnosci)
                v = v * 20
                for i in range(v, 2 * v):
                    time.sleep(0.05)
                    if self.czy_koniec():
                        return
                    if self.jestem_kopniety or self.jestem_uderzony:
                        return
                self.co_robie = self.decyzja()
                if self.co_robie != 'a':
                    break
                if self.jestem_zaraz_obok(g.x, g.y):
                    self.obroc_sie(self.w_ktora_to_strone(g.x, g.y))
                    if self.plansza.gracz.stan == 'g':
                        self.rozbij_garde()
                    else:
                        self.uderz()

            else:
                c = self.gdzie_isc(g.x, g.y, self.plansza.plansza)
                if c != 'n':
                    self.przesun(c)
                else:
                    for i in range(0, 10):
                        time.sleep(0.05)
                        if self.czy_koniec():
                            return
                        if self.jestem_kopniety or self.jestem_uderzony:
                            return
                if self.czy_koniec():
                    return
                if self.jestem_zaraz_obok(g.x, g.y):
                    self.obroc_sie(self.w_ktora_to_strone(g.x, g.y))
                    if self.plansza.gracz.stan == 'g':
                        self.rozbij_garde()
                    else:
                        self.uderz()





