import pygame
import Grafika
import Protagonista
import Plansza
import time
import random

class Gra:
    """"Klasa ktora definiuje cale nasze obcowanie z programem"""

    def __init__(self):
        """"Tworzymy te gre od podstaw"""
        pygame.init()
        pygame.mouse.set_visible(False)
        self.plansza = Plansza.Plansza()
        self.gracz = Protagonista.Protagonista(self.plansza)
        self.plansza.dodaj_gracza(self.gracz)
        self.grafika = Grafika.Grafika(self.plansza)

    def Rozpocznij(self):
        """"Funkcja ktora otwiera nam gre, jej zakonczenie to zamkniecie programu"""
        tryb_testowania = False
        if tryb_testowania:
            self.plansza.ktore_menu = 0
            self.plansza.dodaj_zawodnikow(1, 0, 0)
            self.gracz.steruj()#
        else:
            self.menu_glowne()
            self.plansza.konczymy = True


    def menu_glowne(self):
        """"Menu ktore widzimy po odpaleniu gry"""
        self.plansza.ktora_opcja = 1
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        while True:
            self.plansza.ktore_menu = 1
            time.sleep(0.01)
            pygame.event.pump()
            event = pygame.event.poll()
            if event != pygame.NOEVENT:
                if event.type == pygame.KEYDOWN \
                        and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    if self.plansza.ktora_opcja == 1:
                        self.menu_graj()
                        self.plansza.ktora_opcja = 1
                    elif self.plansza.ktora_opcja == 2:
                        self.instrukcja()
                    elif self.plansza.ktora_opcja == 3:
                        pass
                    elif self.plansza.ktora_opcja == 4:
                        return
                elif self.plansza.ktora_opcja == 3 \
                        and event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if self.plansza.poziom_trudnosci > 1:
                        self.plansza.poziom_trudnosci -= 1
                elif self.plansza.ktora_opcja == 3 \
                        and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if self.plansza.poziom_trudnosci < 3:
                        self.plansza.poziom_trudnosci += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if self.plansza.ktora_opcja == 4:
                        self.plansza.ktora_opcja = 1
                    else:
                        self.plansza.ktora_opcja += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if self.plansza.ktora_opcja == 1:
                        self.plansza.ktora_opcja = 4
                    else:
                        self.plansza.ktora_opcja -= 1

    def menu_graj(self):
        """"Menu wyboru trybu rozgrywki"""
        self.plansza.ktora_opcja = 1
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        while True:
            self.plansza.ktore_menu = 2
            time.sleep(0.01)
            pygame.event.pump()
            event = pygame.event.poll()
            if event != pygame.NOEVENT:
                if event.type == pygame.KEYDOWN \
                        and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    if self.plansza.ktora_opcja == 1:
                        self.menu_wolna_gra()
                        self.plansza.ktora_opcja = 1
                    elif self.plansza.ktora_opcja == 2:
                        pass
                    elif self.plansza.ktora_opcja == 3:
                        self.plansza.resetuj_calosc()
                        b = self.plansza.poziom_trudnosci*3
                        self.plansza.dodaj_zawodnikow(random.randint(0, b), random.randint(0, b), random.randint(0, b))
                        self.menu_pauza()
                        self.plansza.ktora_opcja = 1
                    elif self.plansza.ktora_opcja == 4:
                        return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if self.plansza.ktora_opcja == 4:
                        self.plansza.ktora_opcja = 1
                    else:
                        self.plansza.ktora_opcja += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if self.plansza.ktora_opcja == 1:
                        self.plansza.ktora_opcja = 4
                    else:
                        self.plansza.ktora_opcja -= 1

    def menu_pauza(self):
        """"Menu, gdy przerwiemy na chwile rozpoczeta rozgrywke"""
        self.plansza.ktora_opcja = 1
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        self.gracz.steruj()
        while True:
            if self.gracz.HP <= 0 or len(self.plansza.spis_zywych) == 1:
                return
            self.plansza.ktore_menu = 3
            time.sleep(0.01)
            pygame.event.pump()
            event = pygame.event.poll()
            if event != pygame.NOEVENT:
                if event.type == pygame.KEYDOWN \
                        and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    if self.plansza.ktora_opcja == 1:
                        self.gracz.steruj()
                        self.plansza.ktora_opcja = 1
                    elif self.plansza.ktora_opcja == 2:
                        return
                    elif self.plansza.ktora_opcja == 3:
                        self.instrukcja()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.gracz.steruj()
                    self.plansza.ktora_opcja = 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if self.plansza.ktora_opcja == 3:
                        self.plansza.ktora_opcja = 1
                    else:
                        self.plansza.ktora_opcja += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if self.plansza.ktora_opcja == 1:
                        self.plansza.ktora_opcja = 3
                    else:
                        self.plansza.ktora_opcja -= 1

    def menu_wolna_gra(self):
        """"Menu wyboru opcji dla trybu wolnej gry"""
        self.plansza.ktora_opcja = 1
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        while True:
            self.plansza.ktore_menu = 4
            time.sleep(0.01)
            pygame.event.pump()
            event = pygame.event.poll()
            if event != pygame.NOEVENT:
                if event.type == pygame.KEYDOWN \
                        and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    if self.plansza.ktora_opcja == 1:
                        #print("chce nowa gre")
                        self.plansza.resetuj_calosc()
                        #print("zresetowalem")
                        self.plansza.dodaj_zawodnikow(self.plansza.p1, self.plansza.p2, self.plansza.p3)
                        #print("nowa gra")
                        self.menu_pauza()
                        self.plansza.ktora_opcja = 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if self.plansza.ktora_opcja == 2 and self.plansza.p1 < 20:
                        self.plansza.p1 += 1
                    elif self.plansza.ktora_opcja == 3 and self.plansza.p2 < 20:
                        self.plansza.p2 += 1
                    elif self.plansza.ktora_opcja == 4 and self.plansza.p3 < 20:
                        self.plansza.p3 += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if self.plansza.ktora_opcja == 2 and self.plansza.p1 > 0:
                        self.plansza.p1 -= 1
                    elif self.plansza.ktora_opcja == 3 and self.plansza.p2 > 0:
                        self.plansza.p2 -= 1
                    elif self.plansza.ktora_opcja == 4 and self.plansza.p3 > 0:
                        self.plansza.p3 -= 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    if self.plansza.ktora_opcja == 4:
                        self.plansza.ktora_opcja = 1
                    else:
                        self.plansza.ktora_opcja += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    if self.plansza.ktora_opcja == 1:
                        self.plansza.ktora_opcja = 4
                    else:
                        self.plansza.ktora_opcja -= 1

    def instrukcja(self):
        """"Nasza instrukcja"""
        self.plansza.ktore_menu = 10
        pygame.event.set_allowed(None)
        pygame.event.set_allowed(pygame.KEYDOWN)
        while True:
            time.sleep(0.01)
            pygame.event.pump()
            event = pygame.event.poll()
            if event != pygame.NOEVENT:
                if event.type == pygame.KEYDOWN \
                        and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if self.plansza.ktore_menu == 16:
                        self.plansza.ktore_menu = 10
                    else:
                        self.plansza.ktore_menu += 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if self.plansza.ktore_menu == 10:
                        self.plansza.ktore_menu = 16
                    else:
                        self.plansza.ktore_menu -= 1