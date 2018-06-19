from Zawodnik import Zawodnik
import threading
import random
import time
import pygame


class Judo(Zawodnik, threading.Thread):

    def __init__(self, plansza):
        super().__init__(plansza)
        #super().super().__init__()
        threading.Thread.__init__(self)
        self.kim_jestem = 2000

    def przerzuc(self):#120, 122, 124, 126, 128, 130, 132, 134
        """Obsluguje cios specjalny"""
        self.ile_ciosow_otrzymalem_w_serii = 0
        g = self.plansza.gracz
        if not self.zwrot == 'p' and not self.zwrot == 'l':
            return False
        if g.stan == 'v' or g.stan == 'l' or g.stan == 't' or g.stan == 'w' or g.stan == 'u' \
                or not self.plansza.zajmij_pole(self.zwroc_x(self.zwrot_przeciwny(self.zwrot)),
                                                self.zwroc_y(self.zwrot_przeciwny(self.zwrot))):
            return False
        self.stan = 'k'
        #zajmujemy pole na ktore bedziemy rzucali

        self.aaanimacja = 120
        for i in range(0, 40): #podchodzenie do gracza z wyciagnietymi rekoma
            time.sleep(0.0125)
            if self.jestem_kopniety or self.jestem_uderzony:
                self.plansza.zwolnij_pole(self.zwroc_x(self.zwrot_przeciwny(self.zwrot)),
                                          self.zwroc_y(self.zwrot_przeciwny(self.zwrot)))
                k, u = self.jestem_kopniety, self.jestem_uderzony
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <=10 and k:
                    return self.szuraj_po_ziemii()
                else:
                    return self.animuj_bycie_uderzonym()
            if self.czy_koniec():
                self.plansza.zwolnij_pole(self.zwroc_x(self.zwrot_przeciwny(self.zwrot)),
                                         self.zwroc_y(self.zwrot_przeciwny(self.zwrot)))
                return False
            self.ustaw_przesuniecie(self.zwrot, 1, i)


        #gdy okaze sie ze gracz juz nie jest na tym polu lub lezy
        if g.stan == 'v' or g.stan == 'l' or g.stan == 't' or g.stan == 'w' or g.stan == 'u'\
                or not self.plansza.plansza[self.zwroc_y(self.zwrot)][self.zwroc_x(self.zwrot)] == self.plansza.gracz:
            self.plansza.zwolnij_pole(self.zwroc_x(self.zwrot_przeciwny(self.zwrot)),
                                      self.zwroc_y(self.zwrot_przeciwny(self.zwrot)))
            while not self.podejmij_centrowanie_postaci():
                time.sleep(0.00625)
                if self.czy_koniec():
                    return False
                if not self.jestem_graczem and (self.jestem_kopniety or self.jestem_uderzony):
                    k, u = self.jestem_kopniety, self.jestem_uderzony
                    self.jestem_uderzony, self.jestem_kopniety = False, False
                    if self.energia <= 10 and k:
                        return self.szuraj_po_ziemii()
                    else:
                        return self.animuj_bycie_uderzonym()
            self.reset_animacji()
            return False

        #trzymamy juz gracza, judo jest maksymalnie w strone jego wysuniety
        #dla gracza animacje przerzucenia zaleznie od kierunku gracza
        #136, 138, 140, 142, 144, 146, 148, 150

        g.jestem_przerzucany = True
        self.ile_ciosow_otrzymalem_w_serii = 0
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN))
        while not g.jestem_swiadomy_bycia_przerzucanym:
            #czekamy az gracz bedzie swiadom bycia przerzucanym
            #tu nie moze byc uderzony, bo nie ma przez kogo(gracz jest juz trzymany)
            time.sleep(0.01)
            if self.czy_koniec():
                self.plansza.zwolnij_pole(self.zwroc_x(self.zwrot_przeciwny(self.zwrot)),
                                          self.zwroc_y(self.zwrot_przeciwny(self.zwrot)))
                return False




        g.obroc_sie(g.w_ktora_to_strone(self.x, self.y))
        #zakladamy tutaj tylko wysuniecie gracza w krzyzowych zwrotach
        # (conajmniej jedno przesuniecie jest rowne 0)

        oddalenie = 0
        gracz_wycentrowany = True #wycentrowany juz byl jesli jest przyblziony
        if self.zwrot == 'p' and g.przesuniecie_x < 0:
            oddalenie = -abs(g.przesuniecie_x)
        elif self.zwrot == 'l' and g.przesuniecie_x > 0:
            oddalenie = -abs(g.przesuniecie_x)
        elif self.zwrot == 'd' and g.przesuniecie_y < 0:
            oddalenie = -abs(g.przesuniecie_y)
        elif self.zwrot == 'g' and g.przesuniecie_y > 0:
            oddalenie = -abs(g.przesuniecie_y)
        else:
            gracz_wycentrowany = False
            oddalenie = max(abs(g.przesuniecie_x), abs(g.przesuniecie_y))

        okres_zmiany_animacji_judo = int((160 + oddalenie)/8)
        while int(okres_zmiany_animacji_judo/8) >= 134:
            okres_zmiany_animacji_judo -= 1
        okres_zmiany_animacji_gracza = 20
        if oddalenie < 0:
            okres_zmiany_animacji_gracza = int((160 + oddalenie) / 8)
        while int(okres_zmiany_animacji_gracza/8) >= 150:
            okres_zmiany_animacji_gracza -= 1

        gracz_minal_judo = False
        i = 0
        if oddalenie < 0:
            i += -oddalenie
        x_przejechal, y_przejechal = False, False

        while True:#tu sie dzieje cala animacja
            time.sleep(0.005)
            if self.czy_koniec():
                self.plansza.zwolnij_pole(self.zwroc_x(self.zwrot_przeciwny(self.zwrot)),
                                          self.zwroc_y(self.zwrot_przeciwny(self.zwrot)))
                return False

            a = 120 + 2 * int(i/okres_zmiany_animacji_judo)
            if a <= 134:
                self.aaanimacja = a
            else:
                self.aaanimacja = 134

            if g.przesuniecie_x == 0 and g.przesuniecie_y == 0:
                gracz_wycentrowany = True
            if not gracz_wycentrowany:
                g.podejmij_centrowanie_postaci()
            else:
                h = i
                if oddalenie < 0:
                    h -= oddalenie
                a = 136 + 2 * int(h/okres_zmiany_animacji_gracza)
                if a <= 150:
                    g.aaanimacja = a
                else:
                    g.aaanimacja = 150

                if not y_przejechal and (i%4) == 0:
                    if self.zwrot == 'p' or self.zwrot == 'l':
                        if gracz_minal_judo:
                            g.przesuniecie_y += 1
                        else:
                            g.przesuniecie_y -= 1

                if (self.zwrot == 'p' and g.przesuniecie_x == -80) or (self.zwrot == 'l' and g.przesuniecie_x == 80):
                    self.plansza.zwolnij_pole(g.x, g.y)
                    self.plansza.odmelduj_sie(g.x, g.y)
                    g.x, g.y = self.zwroc_x(self.zwrot_przeciwny(self.zwrot)), self.zwroc_y(self.zwrot_przeciwny(self.zwrot))
                    if self.zwrot == 'p' or self.zwrot == 'l':
                        g.przesuniecie_x *= -1
                    else:
                        g.przesuniecie_y *= -1
                    self.plansza.zamelduj_sie(g)
                    gracz_minal_judo = True

                if g.przesuniecie_x == 0 and gracz_minal_judo:
                    x_przejechal = True
                if g.przesuniecie_y == 0 and gracz_minal_judo:
                    y_przejechal = True

                if self.zwrot == 'p' and not x_przejechal:
                    g.przesuniecie_x -= 1
                elif self.zwrot == 'l' and not x_przejechal:
                    g.przesuniecie_x += 1

            if self.podejmij_centrowanie_postaci() and gracz_minal_judo\
                    and g.przesuniecie_x == 0 and g.przesuniecie_y == 0:
                break

            i += 1


        self.reset_animacji()
        g.jestem_przerzucany = False
        return True


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
                    if random.randint(0,1 + (3 - self.plansza.poziom_trudnosci)) == 0 \
                            and (self.zwrot == 'p' or self.zwrot == 'l'):
                        self.przerzuc()
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
                    if random.randint(0,1 + (3 - self.plansza.poziom_trudnosci)) == 0 \
                            and (self.zwrot == 'p' or self.zwrot == 'l'):
                        self.przerzuc()
                    else:
                        self.uderz()
                continue
