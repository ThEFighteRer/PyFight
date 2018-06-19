import pygame
import threading
from Zawodnik import Zawodnik
import time


class Protagonista(Zawodnik):

    def __init__(self, plansza):
        Zawodnik.__init__(self, plansza)
        self.energia = 0
        self.jestem_graczem = True
        self.jestem_przerzucany = False
        self.jestem_swiadomy_bycia_przerzucanym = False
        self.HP = self.maks_hp_i_energii()[0]

    def reset(self):
        """resetujemy pola klasy, w przygotowaniu na nowa rozgrywke"""
        self.jestem_przerzucany = False
        self.jestem_swiadomy_bycia_przerzucanym = False
        self.zwrot = 'p'
        self.kierunek = 'p'
        self.przesuniecie_x = 0
        self.przesuniecie_y = 0
        self.aaanimacja = 0
        self.stan = 'n'
        self.pom = 0
        self.jestem_kopniety, self.jestem_uderzony = False, False

    def czekaj_az_odkliknie(przycisk):
        """"Funckja pomocnicza"""
        while True:
            pygame.event.pump()
            if not pygame.key.get_pressed()[przycisk]:
                return

    def dodaj_hp(self, ile):
        """"Funckja pomocnicza"""
        if self.HP + ile > self.makshp:
            self.HP = self.makshp
        else:
            self.HP += ile

    def steruj(self):
        """"Przechwytywanie wszystkich przyciskow, jedyny kontakt gracza na rozgrywke"""
        self.plansza.ktore_menu = 0
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.clear()
        while True:

            if not self.HP <= 0 and not len(self.plansza.spis_zywych) == 1:
                pygame.event.pump()
                state = pygame.key.get_pressed()
                if state[pygame.K_UP] or state[pygame.K_DOWN] or state[pygame.K_LEFT] or state[pygame.K_RIGHT]:
                    pygame.event.clear()
                    if state[pygame.K_UP]:
                        self.przesun('g')
                    elif state[pygame.K_DOWN]:
                        self.przesun('d')
                    elif state[pygame.K_LEFT]:
                        self.przesun('l')
                    elif state[pygame.K_RIGHT]:
                        self.przesun('p')
                    continue

                #print("czekam na event")
                event = pygame.event.wait()
                #print(event)
            if self.HP <= 0:
                self.plansza.okno_koncowe = 1
                while True:
                    pygame.event.pump()
                    state = pygame.key.get_pressed()
                    if state[pygame.K_SPACE]:
                        pygame.event.clear()
                        break
                    time.sleep(0.01)
                while True:
                    pygame.event.pump()
                    state = pygame.key.get_pressed()
                    if not state[pygame.K_SPACE]:
                        pygame.event.clear()
                        break
                    time.sleep(0.01)
                self.plansza.okno_koncowe = 0
                return
            if len(self.plansza.spis_zywych) == 1:
                self.plansza.okno_koncowe = 2
                while True:
                    pygame.event.pump()
                    state = pygame.key.get_pressed()
                    if state[pygame.K_SPACE]:
                        pygame.event.clear()
                        break
                    time.sleep(0.01)
                while True:
                    pygame.event.pump()
                    state = pygame.key.get_pressed()
                    if not state[pygame.K_SPACE]:
                        pygame.event.clear()
                        break
                    time.sleep(0.01)
                self.plansza.okno_koncowe = 0
                return
            if self.jestem_przerzucany:
                self.badz_przerzucany()
                continue
            pygame.event.clear()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.turlanie()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.przesun('g')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.przesun('d')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.przesun('p')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.przesun('l')
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                x, y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
                if ((self.plansza.wspolrzedne_w_planszy(x, y) and self.plansza.plansza[y][x] == None)\
                        or (not self.plansza.wspolrzedne_w_planszy(x, y)))\
                        and self.plansza.lezy_tu_ktos(self.x, self.y):
                    self.dobijanie_na()
                elif self.plansza.wspolrzedne_w_planszy(x, y) \
                        and self.plansza.plansza[y][x] == None and self.plansza.lezy_tu_ktos(x, y):
                    self.dobijanie_od_boku()
                else:
                    self.uderz()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                x, y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
                if self.plansza.wspolrzedne_w_planszy(x, y) \
                        and self.plansza.plansza[y][x] == None and self.plansza.lezy_tu_ktos(x, y):
                    self.dobijanie_od_boku()
                elif ((self.plansza.wspolrzedne_w_planszy(x, y) and self.plansza.plansza[y][x] == None) \
                        or (not self.plansza.wspolrzedne_w_planszy(x, y))) \
                        and self.plansza.lezy_tu_ktos(self.x, self.y):
                    self.dobijanie_na()
                else:
                    self.kopniecie()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.unik(False)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                self.kolanko()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.rozbita_garda = False
                state = pygame.key.get_pressed()
                while state[pygame.K_a]:
                    time.sleep(0.001)
                    pygame.event.pump()
                    state = pygame.key.get_pressed()
                    if self.jestem_przerzucany:
                        self.badz_przerzucany()
                        break
                    if state[pygame.K_s]:
                        self.unik(True)
                    if state[pygame.K_RIGHT]:
                        self.zwrot, self.kierunek = 'p', 'p'
                    elif state[pygame.K_LEFT]:
                        self.zwrot, self.kierunek = 'l', 'l'
                    elif state[pygame.K_UP]:
                        self.zwrot = 'g'
                    elif state[pygame.K_DOWN]:
                        self.zwrot = 'd'
                    if self.HP <= 0:
                        # tu moze jakas pentelka i enter
                        break
                    self.stan = 'g'
                    if self.rozbita_garda:
                        self.rozbita_garda = False
                        break
                self.stan = 'n'
                pygame.event.clear()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.plansza.ktore_menu = 3
                return

        self.plansza.ktore_menu = 3

    def zostan_uderzony(self, obr, en):
        """"Funckja flagujaca odpowiednie efekty, wywolywana przez inny watek, ktore sa potem obslugiwane przez nasz watek"""
        if self.stan == 'g' or self.stan == 'w' or self.stan == 'j':
            pass
        elif self.stan == 'u':
            pass
        else:
            self.plansza.zaplam(self.x, self.y, 1)
            self.odejmij_hp(obr)

    def zostan_kopniety(self, obr, en):
        """"Funckja flagujaca odpowiednie efekty, wywolywana przez inny watek, ktore sa potem obslugiwane przez nasz watek"""
        if self.stan == 'w' or self.stan == 'j':
            pass
        elif self.stan == 'g':
            self.plansza.zaplam(self.x, self.y, 1)
            self.odejmij_hp(int(obr*0.5))
        else:
            self.plansza.zaplam(self.x, self.y, 1)
            self.odejmij_hp(obr)

    def badz_przerzucany(self):  # tylko dla gracza
        """"Funckja flagujaca odpowiednie efekty, wywolywana przez inny watek, ktore sa potem obslugiwane przez nasz watek"""
        self.stan = 'v'
        self.jestem_swiadomy_bycia_przerzucanym = True
        while self.jestem_przerzucany:
            if self.czy_koniec():
                return False
            time.sleep(0.05)
        self.jestem_swiadomy_bycia_przerzucanym = False
        self.odejmij_hp(10)
        if self.czy_koniec():
            return False
        return self.lez_na_ziemii(False)

    def lez_na_ziemii(self, czy_z_animacja_przewrocenia):#lezenie 152, wstawanie 154, 156, 158
        """Obsluguje lezenie i wstawanie z ziemii gracza, definiuje co sie wtedy dzieje"""
        self.stan = 'l'
        self.aaanimacja = 152
        for i in range(0, 30):
             if self.czy_koniec():
                 return False
             time.sleep(0.1)

        for i in range(0, 3):
            if self.czy_koniec():
                return False
            self.aaanimacja = 154 + 2 * i
            time.sleep(0.2)

        self.reset_animacji()
        return True

    def unik(self, czy_w_trakcie_gardy): # 54, 56, 58 w staniu; 60, 62, 64 w gardzie
        """Obsluguje unik gracza"""
        self.stan = 'u'
        a = 0
        if czy_w_trakcie_gardy:
            a = 6
        for i in range(0, 5):
            if self.czy_koniec():
                return False
            if i < 3:
                self.aaanimacja = 54 + i * 2 + a
            else:
                self.aaanimacja = 56 - (i-3) * 2 + a
            time.sleep(0.15)
        if czy_w_trakcie_gardy:
            self.stan = 'g'
        else:
            self.reset_animacji()

    def kolanko(self): #30, 32, 34, 36
        """Obsluguje cios kolankowy gracza"""
        self.stan = 'c'
        for i in range(0, 40):
            if self.czy_koniec():
                return False
            if self.jestem_przerzucany:
                self.badz_przerzucany()
                return False
            self.aaanimacja = 30 + 2 * int((i) / 11)
            self.ustaw_przesuniecie(self.zwrot, 1, i)
            time.sleep(0.00625)

        x, y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
        if self.plansza.wspolrzedne_w_planszy(x, y) and self.plansza.plansza[y][x] != None:
            self.plansza.plansza[y][x].zostan_skolankowany(5, 12)

        for i in range(0, 39):
            if self.czy_koniec():
                return False
            if self.jestem_przerzucany:
                self.badz_przerzucany()
                return False
            self.aaanimacja = 36 - 2 * int((i) / 10)
            self.ustaw_przesuniecie(self.zwrot, 1, 40 - i)
            time.sleep(0.00625)

        self.reset_animacji()

    def dobijanie_na(self):# 66, 68, 70, 72, 74
        """Obsluguje cios gracza na lezacym przeciwniku"""
        self.stan = 'd'
        for i in range(0, 9):
            if self.czy_koniec():
                return False
            if self.jestem_przerzucany:
                self.badz_przerzucany()
                return False
            if i<5:
                self.aaanimacja = 66 + i*2
            else:
                self.aaanimacja = 72 - (i-5)*2
            if i == 5:
                for k in self.plansza.lezacy:
                    if k[0] == self.x and k[1] == self.y:
                        k[2].zostan_uderzony(10, 10)
                        self.plansza.czas_w_ktorym_gracz_kopnal_lezacego = time.clock()
            time.sleep(0.05)

        self.reset_animacji()

    def dobijanie_od_boku(self):#82, 84, 86, 88, 90, 92, 94
        """Obsluguje cios gracza na lezacym obok przeciwniku"""
        self.stan = 'd'
        for i in range(0, 40):
            if self.czy_koniec():
                return False
            if self.jestem_przerzucany:
                self.badz_przerzucany()
                return False
            self.aaanimacja = 82 + 2 * int(i / 6)
            self.ustaw_przesuniecie(self.zwrot, 1, i/2)
            time.sleep(0.0035)

        x, y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
        for i in self.plansza.lezacy:
            if i[0] == x and i[1] == y:
                i[2].zostan_uderzony(8, 8)
                self.plansza.czas_w_ktorym_gracz_kopnal_lezacego = time.clock()

        for i in range(0, 40):
            if self.czy_koniec():
                return False
            self.aaanimacja = 94 - 2 * int((i) / 6)
            self.ustaw_przesuniecie(self.zwrot, 1, (40 - i)/2)
            time.sleep(0.0035)

        self.reset_animacji()

    def turlanie(self): # 38,40,42,44,46,48,50
        """Obsluguje rozgwiazdy gracza"""
        self.stan = 't'
        nadal_sie_przesuwamy = True
        idziemy_do = True
        self.przesuniecie_x, self.przesuniecie_y == 0, 0  # profilaktycznie
        i = 0
        while i<316:
            i += 1
            if self.czy_koniec():
                return False
            #tu sprawdz czy nie dojechalismy do nowej kratki i czy nadal sie przesuwamy
            if nadal_sie_przesuwamy:
                if self.przesuniecie_x == 0 and self.przesuniecie_y == 0:
                    if self.plansza.zajmij_pole(self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)):
                        idziemy_do = True
                        i += 1
                    else:
                        nadal_sie_przesuwamy = False
                #print(nadal_sie_przesuwamy)
                if nadal_sie_przesuwamy:
                    if self.wysuniecie_skrajne(self.zwrot):
                        self.plansza.zwolnij_pole(self.x, self.y)
                        self.przesuniecie_x *= -1
                        self.przesuniecie_y *= -1
                        self.plansza.odmelduj_sie(self.x, self.y)
                        self.x, self.y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
                        self.plansza.zamelduj_sie(self)
                        idziemy_do = False
                    if idziemy_do:
                        self.ustaw_przesuniecie(self.zwrot, 1, (i%40) + 1)
                    else:
                        self.ustaw_przesuniecie(self.zwrot, -1, 40 - (i%40) - 2)
                #przesuwanie
            #animacja
            if i < 38 or i > 281:
                self.aaanimacja = 2
            elif self.kierunek == 'p':
                self.aaanimacja = 36 + 2*int(i / 38)
            else:
                self.aaanimacja = 52 - 2*int(i / 38)

            time.sleep(0.0012)

        self.reset_animacji()