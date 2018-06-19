import pygame
import Plansza
import threading
import time


class Grafika:

        def __init__(self, plansza):
                """Wczytuje obrazki i rozpoczyna watki rysujace"""
                self.FPS = 0.016
                self.plansza = plansza
                self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                self.wczytaj_obrazki()
                self.menu_otwarte = False
                self.x_kropki, self.y_kropki = 0, 0
                self.numerki = []
                for i in range(0, 9):
                        a = []
                        for j in range(0, 16):
                                a.append(0)
                        self.numerki.append(a)

                self.przesuniecia = []
                for i in range(0, 9):
                    a = []
                    for j in range(0, 16):
                        a.append((0, 0))
                    self.przesuniecia.append(a)
                threading.Timer(1, Grafika.rysuj_obrazki, args = (self,)).start()
                threading.Timer(1, Grafika.uzupelniaj_numerki, args = (self,)).start()

        def rysuj_obrazki(self):
            """Watek, gdzie rysujemy na podstawie odpowiednich danych"""
            if not self.plansza.konczymy:
                threading.Timer(self.FPS, Grafika.rysuj_obrazki, (self,)).start()

            #try:
            #    print(self.plansza.spis_zywych[1].co_robie)
            #except Exception:
            #    pass

            if self.plansza.ktore_menu != 0:
                if self.plansza.ktore_menu == 1:#glowne
                    self.screen.blit(self.menu_glowne, (0, 0))
                    if self.plansza.ktora_opcja == 1:
                        self.screen.blit(self.menu_znak, (497, 180))
                        self.screen.blit(self.menu_znak, (704, 180))
                    elif self.plansza.ktora_opcja == 2:
                        self.screen.blit(self.menu_znak, (451, 261))
                        self.screen.blit(self.menu_znak, (753, 261))
                    elif self.plansza.ktora_opcja == 3:
                        self.screen.blit(self.menu_znak, (327, 339))
                        self.screen.blit(self.menu_znak, (868, 339))
                    elif self.plansza.ktora_opcja == 4:
                        self.screen.blit(self.menu_znak, (476, 534))
                        self.screen.blit(self.menu_znak, (726, 534))
                    self.screen.blit(self.poziomy, (540, 430), (0, (self.plansza.poziom_trudnosci-1)*60, 200, 60))
                elif self.plansza.ktore_menu == 2:#graj
                    self.screen.blit(self.menu_graj, (0, 0))
                    if self.plansza.ktora_opcja == 1:
                        self.screen.blit(self.menu_znak, (424, 228))
                        self.screen.blit(self.menu_znak, (785, 228))
                    elif self.plansza.ktora_opcja == 2:
                        self.screen.blit(self.menu_znak, (424, 326))
                        self.screen.blit(self.menu_znak, (785, 326))
                    elif self.plansza.ktora_opcja == 3:
                        self.screen.blit(self.menu_znak, (416, 408))
                        self.screen.blit(self.menu_znak, (800, 408))
                    elif self.plansza.ktora_opcja == 4:
                        self.screen.blit(self.menu_znak, (492, 484))
                        self.screen.blit(self.menu_znak, (719, 484))
                elif self.plansza.ktore_menu == 3:#pauza
                    self.screen.blit(self.menu_pauza, (0, 0))
                    if self.plansza.ktora_opcja == 1:
                        self.screen.blit(self.menu_znak, (421, 178))
                        self.screen.blit(self.menu_znak, (775, 178))
                    elif self.plansza.ktora_opcja == 2:
                        self.screen.blit(self.menu_znak, (451, 277))
                        self.screen.blit(self.menu_znak, (755, 277))
                    elif self.plansza.ktora_opcja == 3:
                        self.screen.blit(self.menu_znak, (449, 359))
                        self.screen.blit(self.menu_znak, (751, 359))
                elif self.plansza.ktore_menu == 4:#graj
                    self.screen.blit(self.menu_wolna_gra, (0, 0))
                    if self.plansza.ktora_opcja == 1:
                        self.screen.blit(self.menu_znak, (423, 177))
                        self.screen.blit(self.menu_znak, (785, 177))
                    elif self.plansza.ktora_opcja == 2:
                        self.screen.blit(self.menu_znak, (454, 331))
                        self.screen.blit(self.menu_znak, (735, 331))
                    elif self.plansza.ktora_opcja == 3:
                        self.screen.blit(self.menu_znak, (489, 457))
                        self.screen.blit(self.menu_znak, (698, 457))
                    elif self.plansza.ktora_opcja == 4:
                        self.screen.blit(self.menu_znak, (403, 584))
                        self.screen.blit(self.menu_znak, (797, 584))
                    self.screen.blit(self.przelacz, (443 + 20 * self.plansza.p1, 423))
                    self.screen.blit(self.przelacz, (443 + 20 * self.plansza.p2, 548))
                    self.screen.blit(self.przelacz, (443 + 20 * self.plansza.p3, 677))
                elif self.plansza.ktore_menu >= 10:#instrukcja
                    self.screen.blit(self.instrukcja[self.plansza.ktore_menu - 10], (0, 0))

            else:
                self.screen.blit(self.tlo, (0, 0))
                for i in range(0, 9):
                    for j in range(0, 16):
                        if self.plansza.krew[i][j] == 0:
                            continue
                        a = self.plansza.krew[i][j]
                        self.screen.blit(self.krew, (j * 80, i * 80),(int(int(a>=5)+int(a>=10)+int(a>=15)+int(a>=1000)+int(a>=2000)+int(a>=3000))*80, 0, 80, 80))

                for i in self.plansza.lezacy:
                    self.screen.blit(self.lezacy, (i[0]*80, i[1]*80),(((i[2].animation())[0]/1000)*80, (((i[2].animation())[0]%10) == 1) * 80, 80, 80))
                    en, zy = int(i[2].energia/i[2].maks_hp_i_energii()[1]*74)\
                        , int(i[2].HP/i[2].maks_hp_i_energii()[0]*74)

                    self.screen.blit(self.pasek_zdrowia, (i[0] * 80 + i[2].przesuniecie_x + 3,
                                                          i[1] * 80 + i[2].przesuniecie_y + 70),
                                     (0, 0, zy, 6))

                    if i == self.plansza.gracz:
                        continue

                    self.screen.blit(self.pasek_energii, (i[0] * 80 + i[2].przesuniecie_x + 3,
                                                          i[1] * 80 + i[2].przesuniecie_y + 76),
                                     (0, 0, en, 3))
                for i in range(0, 9):
                    for j in range(0, 16):
                        if self.numerki[i][j] == None or self.numerki[i][j] == 0:
                            continue
                        a = self.numerki[i][j][0]
                        if a<1000:
                            wsp = 0
                            awsp = 1
                            if a%2 == 1:
                                a -=1
                                wsp = 1
                                awsp = -1
                            if a == 2:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 ((0+(wsp*240)), wsp*80, 80, 80))
                            elif a>=4 and a<=8:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp*320+(awsp)*(80*(a/2-1)), wsp * 80, 80, 80))
                            elif a>=10 and a<=18:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp*320+(awsp)*(80*(a/2-5)), 240 + wsp * 80, 80, 80))
                            elif a>=20 and a<=28:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp*320+(awsp)*(80*(a/2-10)), 640 + wsp * 80, 80, 80))
                            elif a>=30 and a<=36:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp*240+(awsp)*(80*(a/2-15)), 1680 + wsp * 80, 80, 80))
                            elif a>=38 and a<=50:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 ((80*(a/2-19)), 400, 80, 80))
                            elif a == 52:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (80 * (int(round(time.time() * 10))%6 < 3), 160, 80, 80))
                            elif a>=54 and a<=58:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (80*wsp + wsp * 160 + (awsp) * (80 * (a / 2 - 27)), 880 + wsp * 80, 80, 80))
                            elif a>=60 and a<=64:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (80*wsp + wsp * 160 + (awsp) * (80 * (a / 2 - 30)), 1040 + wsp * 80, 80, 80))
                            elif a>=66 and a<=74:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 320 + (awsp) * (80 * (a / 2 - 33)), 1840 + wsp * 80, 80, 80))
                            elif a>=76 and a<=80:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 160 + (awsp) * (80 * (a / 2 - 38)), 480 + wsp * 80, 80, 80))
                            elif a>=82 and a<=94:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 480 + (awsp) * (80 * (a / 2 - 41)), 2000 + wsp * 80, 80, 80))
                            elif a>=136 and a<=150:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 560 + (awsp) * (80 * (a / 2 - 68)), 1360 + wsp * 80, 80, 80))
                            elif a==152:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (0, 1520 + wsp * 80, 80, 80))
                            elif a>=154 and a<=158:
                                self.screen.blit(self.p, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (80 + wsp * 160 + (awsp) * (80 * (a / 2 - 77)), 1520 + wsp * 80, 80, 80))
                        elif a>=1000 and a<=4000:
                            bmp = self.tknd
                            if a>=3000:
                                bmp = self.shln
                                a-=3000
                            elif a>=2000:
                                bmp = self.judo
                                a-=2000
                            else:
                                a-=1000
                            wsp = 0
                            awsp = 1
                            if a % 2 == 1:
                                a -= 1
                                wsp = 1
                                awsp = -1
                            if a == 2:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 ((0 + (wsp * 240)), wsp * 80, 80, 80))
                            elif a>=4 and a<=8:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp*320+(awsp)*(80*(a/2-1)), wsp * 80, 80, 80))
                            elif a>=10 and a<=18:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp*320+(awsp)*(80*(a/2-5)), 240 + wsp * 80, 80, 80))
                            elif a>=20 and a<=28:#przystosowane tylko do tkwndo
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp*320+(awsp)*(80*(a/2-10)), 960 + wsp * 80, 80, 80))
                            elif a>=38 and a<=50:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 480 + (awsp) * (80 * (a / 2 - 19)), 400 + wsp * 80, 80, 80))
                            elif a>=76 and a<=80:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 160 + (awsp) * (80 * (a / 2 - 38)), 800 + wsp * 80, 80, 80))
                            elif a>=102 and a<=118:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (int(wsp==0)*640 - (awsp) * (80 * (a / 2 - 51)), 640 + wsp * 80, 80, 80))
                            elif a>=120 and a<=134:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                       i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 560 + (awsp) * (80 * (a / 2 - 60)), 960 + wsp * 80, 80, 80))
                            elif a>=136 and a<=140:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                       i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 160 + (awsp) * (80 * (a / 2 - 68)), 960 + wsp * 80, 80, 80))
                            elif a>=142 and a<=156:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                       i * 80 + self.przesuniecia[i][j][1]),
                                                 (wsp * 560 + (awsp) * (80 * (a / 2 - 71)), 960 + wsp * 80, 80, 80))
                            elif a>=158 and a<=162:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                       i * 80 + self.przesuniecia[i][j][1]),
                                                 (400 + wsp * 160 + (awsp) * (80 * (a / 2 - 79)), 240 + wsp * 80, 80, 80))
                            elif a>=164 and a<=166:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                       i * 80 + self.przesuniecia[i][j][1]),
                                                 (320 + wsp * 80 + (awsp) * (80 * (a / 2 - 82)), wsp * 80, 80, 80))
                            elif a == 52:
                                self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                                                          i * 80 + self.przesuniecia[i][j][1]),
                                                 (80 * (int(round(time.time() * 10)) % 6 < 3), 160, 80, 80))


                        en, zy = self.numerki[i][j][2], self.numerki[i][j][1]

                        self.screen.blit(self.pasek_zdrowia, (j * 80 + self.przesuniecia[i][j][0] + 3,
                                                              i * 80 + self.przesuniecia[i][j][1] + 70),
                                         (0, 0, zy, 6))

                        self.screen.blit(self.pasek_energii, (j * 80 + self.przesuniecia[i][j][0] + 3,
                                                              i * 80 + self.przesuniecia[i][j][1] + 76),
                                         (0, 0, en, 3))
                    #self.screen.blit(bmp, (j * 80 + self.przesuniecia[i][j][0],
                    #                       i * 80 + self.przesuniecia[i][j][1]),
                    #                 (wsp * 320 + (awsp) * (80 * (a / 2 - 10)), 960 + wsp * 80, 80, 80))

                #for i in self.plansza.lezacy:



                if self.plansza.gracz.zwrot == 'p':
                    self.x_kropki, self.y_kropki = 65, 33
                elif self.plansza.gracz.zwrot == 'l':
                    self.x_kropki, self.y_kropki = 0, 33
                elif self.plansza.gracz.zwrot == 'g':
                    self.x_kropki, self.y_kropki = 33, 0
                elif self.plansza.gracz.zwrot == 'd':
                    self.x_kropki, self.y_kropki = 33, 65

                self.screen.blit(self.zwrt, (self.plansza.gracz.x * 80 + self.plansza.gracz.przesuniecie_x + self.x_kropki,
                                        self.plansza.gracz.y * 80 + self.plansza.gracz.przesuniecie_y + self.y_kropki),
                                    (0, 0, 15, 15))

                if self.plansza.okno_koncowe != 0:
                    self.screen.blit(self.okno_koncowe, (390, 260), ((self.plansza.okno_koncowe-1)*500, 0, 500, 400))

            pygame.display.flip()




        def uzupelniaj_numerki(self):
            """Osobny watek do liczenia czesci animacji dla odciazenia watku rysujacego"""
            if not self.plansza.konczymy:
                threading.Timer(self.FPS, Grafika.uzupelniaj_numerki, (self,)).start()

            for i in range(0, 9):
                for j in range(0, 16):
                    self.numerki[i][j] = self.plansza.pozyskaj_animacje(j, i)
                    self.przesuniecia[i][j] = self.plansza.pozyskaj_przesuniecie(j, i)

        def wczytaj_obrazki(self):
            """Wczytujemy obrazki"""
            self.tlo = pygame.image.load("img/tlo.bmp")
            self.p = pygame.image.load("img/p.bmp")
            self.tknd = pygame.image.load("img/tkwndo.bmp")
            self.shln = pygame.image.load("img/shln.bmp")
            self.judo = pygame.image.load("img/judo.bmp")
            self.zwrt = pygame.image.load("img/zwrot.bmp")
            self.lezacy = pygame.image.load("img/lezacy.bmp")
            self.pasek_energii = pygame.image.load("img/pasek_energii.bmp")
            self.pasek_zdrowia = pygame.image.load("img/pasek_zdrowia.bmp")
            self.krew = pygame.image.load("img/krew.bmp")

            transColor = self.tlo.get_at((0, 0))
            self.p.set_colorkey(transColor)
            self.tknd.set_colorkey(transColor)
            self.shln.set_colorkey(transColor)
            self.judo.set_colorkey(transColor)
            self.zwrt.set_colorkey(transColor)
            self.lezacy.set_colorkey(transColor)
            self.krew.set_colorkey(transColor)

            self.menu_glowne = pygame.image.load("img/menu_glowne.bmp")
            self.menu_graj = pygame.image.load("img/menu_graj.bmp")
            self.menu_pauza = pygame.image.load("img/menu_pauza.bmp")
            self.menu_wolna_gra = pygame.image.load("img/menu_wolna_gra.bmp")
            self.przelacz = pygame.image.load("img/przelacz.bmp")
            self.menu_znak = pygame.image.load("img/menu_znak.bmp")
            self.poziomy = pygame.image.load("img/poziomy.bmp")
            self.okno_koncowe = pygame.image.load("img/message1.bmp")

            self.instrukcja = []
            for i in range(1, 7):
                self.instrukcja.append(pygame.image.load("img/instrukcja"+str(i)+".bmp"))

            greencol = self.menu_glowne.get_at((0, 0))

            self.przelacz.set_colorkey(greencol)
            self.menu_znak.set_colorkey(greencol)
            self.poziomy.set_colorkey(greencol)