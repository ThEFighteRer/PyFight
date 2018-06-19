import time
from Przeciwnik import Przeciwnik
import random

class Zawodnik(Przeciwnik):

    def __init__(self, plansza):
        self.co_robie = 'n' #n nic, u uciekam, a atakuje, g trzymam garde, c chodze
        self.x = 0
        self.y = 0
        self.plansza = plansza
        self.zwrot = 'p'
        self.kierunek = 'p'
        self.przesuniecie_x = 0
        self.przesuniecie_y = 0
        self.aaanimacja = 0
        self.stan = 'n'
        self.ile_ciosow_otrzymalem_w_serii = 0
        ### n nic nie robi (stoi), p przesuwa sie, g garda, u unik, w garda i unik, j uskok, s uderza,
        ### k kopie lub atak specjalny , c kolanko, t turlanie, d dobija, b wstaje, l lezy, m martwy, q dostaje
        ### v przewracanie_sie, h - jest skontrowany
        self.kim_jestem = 0
        ### 0 gracz, 1000 taekwondo, 2000 judo, 3000 kung fu
        self.energia = 50
        self.HP = 100
        self.pom = 0
        self.jestem_kopniety, self.jestem_uderzony = False, False
        self.jestem_graczem = False
        self.obrazenia_do_obsluzenia = 0
        self.rozbita_garda = False
        # 38,40,42,44,46,48,50 to animacje przyjecia ciosu, u gracza to animacje turlania
        self.makshp, self.maksen = 70, 70

    def ustaw_wsp(self, x, y):
        """Funkcja Pomocnicza"""
        self.x = x
        self.y = y

    def odejmij_hp(self, ile):
        """Funkcja Pomocnicza"""
        if self.HP - ile <= 0:
            self.HP = 0
        else:
            self.HP -= ile
        return self.HP > 0

    def odejmij_en(self, ile):
        """Funkcja Pomocnicza"""
        if self.energia - ile <= 0:
            self.energia = 0
        else:
            self.energia -= ile
        return self.energia > 0

    def reset_animacji(self):
        """Funkcja Pomocnicza"""
        self.przesuniecie_y = 0
        self.przesuniecie_x = 0
        self.stan = 'n'

    def obroc_sie(self, zwrot):
        """Funkcja Pomocnicza"""
        self.zwrot = zwrot
        if zwrot == 'p':
            self.kierunek = 'p'
        elif zwrot == 'l':
            self.kierunek = 'l'

    def wysuniecie_skrajne(self, zwrot):
        """Czy wysunelismy sie o 40 pikseli w zwrocie w ktorym patrzymy"""
        return ((zwrot == 'p' and self.przesuniecie_x == 40) or (zwrot == 'l' and self.przesuniecie_x == -40))\
               or ((self.przesuniecie_y == 40 and zwrot == 'd') or (zwrot == 'g' and self.przesuniecie_y == -40))

    def maks_hp_i_energii(self):
        """Jakie sa nasze maksymalne HP i energia w danej rozgrywce"""
        return (self.makshp, self.maksen)

    def animation(self):
        """Zwraca aktualna animacje dodajac informacje o naszym zwrocie"""
        hp = int(self.HP/self.maks_hp_i_energii()[0]*74)
        en = int(self.energia/self.maks_hp_i_energii()[1]*74)
        if not self.jestem_graczem and self.stan == 'l':
            return (self.kim_jestem + int(self.kierunek == 'l'), hp, en)
        if self.stan == 'n':
            self.aaanimacja = 2
        elif self.stan == 'g':
            self.aaanimacja = 52
        if self.kierunek == 'l':
            self.pom = 1
        else:
            self.pom = 0
        return (self.aaanimacja + self.kim_jestem + self.pom, hp, en)

    def czy_koniec(self): #przy okazji trzyma pauze
        """Sprawdza, czy jest koniec rozgrywki/konca gry oraz obsluguje pauze gry"""
        if self.plansza.konczymy or self.plansza.zakoncz_watki:
            self.przesuniecie_x = 0
            self.przesuniecie_y = 0
            return True
        while self.plansza.ktore_menu != 0:
            time.sleep(0.005)
            if self.plansza.konczymy or self.plansza.zakoncz_watki:
                self.przesuniecie_x = 0
                self.przesuniecie_y = 0
                return True
        if self.HP <=0:
            if self.stan!='m':
                if self != self.plansza.gracz:
                    self.plansza.gracz.dodaj_hp(50 - self.plansza.poziom_trudnosci*10)
                self.plansza.zaplam(self.x, self.y, 1000)
                self.plansza.spis_zywych.remove(self)
                self.plansza.spis_martwych.append(self)
                if self.stan == 'l':
                    self.plansza.usun_lezacego(self)
                else:
                    self.plansza.zwolnij_pole(self.x, self.y)
                    self.plansza.odmelduj_sie(self.x, self.y)
                self.stan = 'm'
            return True
        return False

    def ustaw_przesuniecie(self, zwrot, do_przodu, ile):
        """Funkcja Pomocnicza"""
        if zwrot == 'p':
            self.przesuniecie_x = ile*do_przodu
        elif zwrot == 'l':
            self.przesuniecie_x = -ile*do_przodu
        elif zwrot == 'd':
            self.przesuniecie_y = ile*do_przodu
        elif zwrot == 'g':
            self.przesuniecie_y = -ile*do_przodu

    def przesun(self, zwrot): # 4,6,8 animacje
        """Funkcja przesuwajaca zawodnika w danym zwrocie"""
        if zwrot == 'n':
            return
        assert (zwrot == 'l' or zwrot == 'p' or zwrot == 'g' or zwrot == 'd')
        self.zwrot = zwrot
        if self.kierunek == 'p' and zwrot == 'l':
            self.kierunek = 'l'
        elif self.kierunek == 'l' and zwrot == 'p':
            self.kierunek = 'p'

        if (self.x + 1 > 15 and zwrot == 'p') \
                or (self.x - 1 < 0 and zwrot == 'l') \
                or (self.y - 1 < 0 and zwrot == 'g') \
                or (self.y + 1 > 8 and zwrot == 'd'):
            return False
        if not self.plansza.zajmij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot)):
            return False

        self.stan = 'p'

        for i in range(0, 40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.odejmij_hp(int(self.obrazenia_do_obsluzenia))
                self.jestem_uderzony, self.jestem_kopniety = False, False
                self.obrazenia_do_obsluzenia = 0
                self.plansza.zwolnij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot))
                self.odejmij_en(90)
                return self.szuraj_po_ziemii()
            if self.jestem_graczem and self.jestem_przerzucany:
                self.plansza.zwolnij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot))
                return False

            if not self.jestem_graczem and self.jestem_uderzony:
                self.odejmij_hp(int(self.obrazenia_do_obsluzenia/2))
                self.jestem_uderzony, self.jestem_kopniety = False, False
                self.obrazenia_do_obsluzenia = 0

            if self.czy_koniec():
                self.plansza.zwolnij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot))
                return False
            self.ustaw_przesuniecie(zwrot, 1, i)
            time.sleep(0.005)
            self.aaanimacja = 2 + 2*int(i/11)

        self.plansza.zwolnij_pole(self.x, self.y)
        self.przesuniecie_x *= -1
        self.przesuniecie_y *= -1
        self.plansza.odmelduj_sie(self.x, self.y)
        self.x, self.y = self.zwroc_x(zwrot), self.zwroc_y(zwrot)
        self.plansza.zamelduj_sie(self)

        for i in range(0, 40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.odejmij_hp(int(self.obrazenia_do_obsluzenia))
                self.jestem_uderzony, self.jestem_kopniety = False, False
                self.obrazenia_do_obsluzenia = 0
                #self.plansza.zwolnij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot))
                self.odejmij_en(90)
                return self.lez_na_ziemii(True)

            if self.jestem_graczem and self.jestem_przerzucany:
                return False

            if not self.jestem_graczem and self.jestem_uderzony:
                self.odejmij_hp(int(self.obrazenia_do_obsluzenia))
                self.jestem_uderzony = False
                self.obrazenia_do_obsluzenia = 0
                if not self.animuj_bycie_uderzonym():
                    return False
                return True
            if self.czy_koniec():
                return False
            self.ustaw_przesuniecie(zwrot, -1, 40-i)
            time.sleep(0.005)
            self.aaanimacja = 8 - 2*int((i)/11)

        self.reset_animacji()
        return True

    def zwroc_x(self, zwrot):
        """Funkcja Pomocnicza"""
        if zwrot == 'd' or zwrot == 'g':
            return self.x
        if zwrot == 'p':
            return self.x + 1
        if zwrot == 'l':
            return self.x - 1
        raise Exception


    def zwroc_y(self, zwrot):
        """Funkcja Pomocnicza"""
        if zwrot == 'p' or zwrot == 'l':
            return self.y
        if zwrot == 'd':
            return self.y + 1
        if zwrot == 'g':
            return self.y - 1
        raise Exception

    def uderz(self): #10,12,14,16,18,  bycie skontrowanym 158, 160, 162,  krecenie w glowie 164, 166
        """Funkcja odpowiedzialna za uderzanie"""
        self.stan = 's'
        for i in range(0,40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <=10:
                    return self.szuraj_po_ziemii()
                else:
                    return self.animuj_bycie_uderzonym()
            if not self.jestem_graczem and self.jestem_uderzony:
                self.jestem_uderzony = False
                return self.animuj_bycie_uderzonym()
            if self.jestem_graczem and self.jestem_przerzucany:
                return False
            if self.czy_koniec():
                return False
            self.aaanimacja = 10 + 2*int((i)/9)
            self.ustaw_przesuniecie(self.zwrot, 1, i)
            time.sleep(0.007)

        x, y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
        if self.plansza.wspolrzedne_w_planszy(x, y) and self.plansza.plansza[y][x]!=None:
                if not self.jestem_graczem and (self.plansza.plansza[y][x].stan == 'g' or self.plansza.plansza[y][x].stan == 'w'):
                    return self.bycie_skontrowanym()
                else:
                    self.plansza.plansza[y][x].zostan_uderzony(15, 4)

        for i in range(0, 40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <=10:
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
            self.aaanimacja = 18 - 2*int((i)/8)
            self.ustaw_przesuniecie(self.zwrot, 1, 40 - i)
            time.sleep(0.007)

        self.reset_animacji()
        #500 ms
        #przeciwnik:
        #cios w trackcie, ktory nie jest kolanem, to oddalenie sie z animacja otrzymywania ciosu zakonczona na miejscu zameldowania
        #w trakcie dojscia do uderzenia:
        #nie ma nikogo to normalny powrot
        #jest garda + unik to oszolomienie
        #jest sama garda to nic
        #jest sam unik to 2/3 ataku
        #cios w trakcie powrotu to tez plynny powrot
        pass

    def bycie_skontrowanym(self):#bycie skontrowanym 158, 160, 162,  krecenie w glowie 164, 166
        """Obsluga skontrowania i gwiazdek na oczami gdy zawodnik uderzy nas w garde"""
        self.stan = 'h'
        for i in range(1, 41):
            if not self.jestem_graczem and self.jestem_kopniety and self.energia <=30:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                return self.szuraj_po_ziemii()
            if self.czy_koniec():
                return False
            self.aaanimacja = 158 + 2*int((i)/14)
            self.podejmij_centrowanie_postaci()
            time.sleep(0.005)
        for i in range(0, random.randint(20, 100)):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <=30:
                    return self.szuraj_po_ziemii()
                else:
                    return self.animuj_bycie_uderzonym()
            if not self.jestem_graczem and self.jestem_uderzony:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                return self.animuj_bycie_uderzonym()
            if self.czy_koniec():
                return False
            if i%5 == 0:
                if self.aaanimacja == 164:
                    self.aaanimacja = 166
                else:
                    self.aaanimacja = 164
            time.sleep(0.05)
        self.reset_animacji()

    def kopniecie(self): #20,22,24,26,28
        """Funkcja obslugujaca kopniecie"""
        self.stan = 'k'
        for i in range(0, 40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <=10:
                    return self.szuraj_po_ziemii()
                else:
                    return self.animuj_bycie_uderzonym()
            if not self.jestem_graczem and self.jestem_uderzony:
                self.jestem_uderzony = False
                return self.animuj_bycie_uderzonym()
            if self.jestem_graczem and self.jestem_przerzucany:
                return False
            if self.czy_koniec():
                return False
            self.aaanimacja = 20 + 2 * int((i) / 9)
            self.ustaw_przesuniecie(self.zwrot, 1, i)
            time.sleep(0.00625)

        x, y = self.zwroc_x(self.zwrot), self.zwroc_y(self.zwrot)
        if self.plansza.wspolrzedne_w_planszy(x, y) and self.plansza.plansza[y][x] != None:
            self.plansza.plansza[y][x].zostan_kopniety(10, 8)

        for i in range(0, 40):
            if not self.jestem_graczem and self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.energia <=10:
                    return self.szuraj_po_ziemii()
                else:
                    return self.animuj_bycie_uderzonym()
            if not self.jestem_graczem and self.jestem_uderzony:
                self.jestem_uderzony = False
                return self.animuj_bycie_uderzonym()
            if self.jestem_graczem and self.jestem_przerzucany:
                return False
            if self.czy_koniec():
                return False
            self.aaanimacja = 28 - 2 * int((i) / 8)
            self.ustaw_przesuniecie(self.zwrot, 1, 40 - i)
            time.sleep(0.00625)

        self.reset_animacji()
        # przeciwnik:
        # cios w trackcie, ktory nie jest kolanem, to oddalenie sie z animacja otrzymywania ciosu zakonczona na miejscu zameldowania
        # w trakcie dojscia do uderzenia:
        # nie ma nikogo to normalny powrot
        # jest garda + unik to oszolomienie
        # jest sama garda to atak razy 2/3
        # jest sam unik to nic
        # cios w trakcie powrotu to tez plynny powrot
        pass

    def oszolomienie(self):
        #1 s
        #uderzenie to przerwanie
        pass

    def animuj_bycie_uderzonym(self):
        """Funkcja odpowiedzialna za animacje i nie tylko bycia uderzanym"""
        self.stan = 'q'
        for i in range(0, 70):
            self.aaanimacja = 38 + 2*int(i/10)
            if self.przesuniecie_y != 0:
                if self.przesuniecie_y > 0:
                    self.przesuniecie_y -= 1
                else:
                    self.przesuniecie_y +=1
            if self.przesuniecie_x != 0:
                if self.przesuniecie_x > 0:
                    self.przesuniecie_x -= 1
                else:
                    self.przesuniecie_x += 1
            time.sleep(0.00625)
        self.reset_animacji()

    def zwrot_przeciwny(self, zwr):
        """Funkcja Pomocnicza"""
        if zwr == 'p':
            return 'l'
        elif zwr == 'l':
            return 'p'
        elif zwr == 'g':
            return 'd'
        elif zwr == 'd':
            return 'g'

    def szuraj_po_ziemii(self):#102, 104, 106, 108, 110, 112, 114, 116, 118
        """Funkcja obslugujaca suniecie po ziemi po byciu kopnietym majac malo energii, konczy sie lezeniem"""
        #przesuniecia <= 40 zalozenie
        self.ile_ciosow_otrzymalem_w_serii = 0
        self.stan = 't'
        nadal_sie_przesuwamy = True
        idziemy_do = True
        zwrot = self.zwrot_przeciwny(self.zwrot)
        #self.przesuniecie_x, self.przesuniecie_y == 0, 0  # nie mozna bo beda skoki
        i = 0
        if self.przesuniecie_x >= 40:
            self.przesuniecie_x = 39
        elif self.przesuniecie_x <= -40:
            self.przesuniecie_x = -39
        if self.przesuniecie_y >= 40:
            self.przesuniecie_y = 39
        elif self.przesuniecie_y <= -40:
            self.przesuniecie_y = -39

        if (zwrot == 'p' and self.przesuniecie_x>0) or (zwrot == 'l' and self.przesuniecie_x<0):#wysuniety w strone w ktora ma byc odkopniety
            i = abs(self.przesuniecie_x)
            nadal_sie_przesuwamy = self.plansza.zajmij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot))
        elif (zwrot == 'd' and self.przesuniecie_y>0) or (zwrot == 'g' and self.przesuniecie_y<0):#wysuniety w strone w ktora ma byc odkopniety
            i = abs(self.przesuniecie_y)
            nadal_sie_przesuwamy = self.plansza.zajmij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot))
        elif (self.zwrot == 'p' and self.przesuniecie_x>0) or (self.zwrot == 'l' and self.przesuniecie_x<0):
            self.aaanimacja = 102
            while self.przesuniecie_x!=0:
                if self.przesuniecie_x>0:
                    self.przesuniecie_x -= 1
                elif self.przesuniecie_x<0:
                    self.przesuniecie_x += 1
                time.sleep(0.0025)
                if self.czy_koniec():
                    return False
        elif (self.zwrot == 'd' and self.przesuniecie_y>0) or (self.zwrot == 'g' and self.przesuniecie_y<0):
            self.aaanimacja = 102
            while self.przesuniecie_y!=0:
                if self.przesuniecie_y>0:
                    self.przesuniecie_y -= 1
                elif self.przesuniecie_y<0:
                    self.przesuniecie_y += 1
                time.sleep(0.0025)
                if self.czy_koniec():
                    return False

        while i < 314:

            if self.czy_koniec():
                return False
            if (i%2) == 0:
                if zwrot == 'p' or zwrot == 'l':
                    if self.przesuniecie_y<0:
                        self.przesuniecie_y += 1
                    elif self.przesuniecie_y>0:
                        self.przesuniecie_y -= 1
                elif zwrot == 'g' or zwrot == 'd':
                    if self.przesuniecie_x<0:
                        self.przesuniecie_x += 1
                    elif self.przesuniecie_x>0:
                        self.przesuniecie_x -= 1

            # tu sprawdz czy nie dojechalismy do nowej kratki i czy nadal sie przesuwamy
            if nadal_sie_przesuwamy:
                if (self.przesuniecie_x == 0 and (zwrot == 'p' or zwrot == 'l'))\
                        or (self.przesuniecie_y == 0 and (zwrot == 'g' or zwrot == 'd')):
                    if self.plansza.zajmij_pole(self.zwroc_x(zwrot), self.zwroc_y(zwrot)):
                        idziemy_do = True
                        i += 1
                    else:
                        nadal_sie_przesuwamy = False
                # print(nadal_sie_przesuwamy)
                if nadal_sie_przesuwamy:
                    if self.wysuniecie_skrajne(zwrot):
                        self.plansza.zwolnij_pole(self.x, self.y)
                        if zwrot == 'p' or zwrot == 'l':
                            self.przesuniecie_x *= -1
                        else:
                            self.przesuniecie_y *= -1
                        self.plansza.odmelduj_sie(self.x, self.y)
                        self.x, self.y = self.zwroc_x(zwrot), self.zwroc_y(zwrot)
                        self.plansza.zamelduj_sie(self)
                        idziemy_do = False
                    if idziemy_do:
                        self.ustaw_przesuniecie(zwrot, 1, (i % 40) + 1)
                    else:
                        self.ustaw_przesuniecie(zwrot, -1, 40 - (i % 40) - 2)
            else:#na wypadek gdybysmy sie juz nie przesuwali ale mieli przesuniece z chwila wejscia w funkcje
                if zwrot == 'p' or zwrot == 'l':
                    if self.przesuniecie_x < 0:
                        self.przesuniecie_x += 1
                    elif self.przesuniecie_x > 0:
                        self.przesuniecie_x -= 1
                elif zwrot == 'g' or zwrot == 'd':
                    if self.przesuniecie_y < 0:
                        self.przesuniecie_y += 1
                    elif self.przesuniecie_y > 0:
                        self.przesuniecie_y -= 1

                # przesuwanie
            # animacja
            self.aaanimacja = 102 + 2 * int(i / 35)
            #print(self.aaanimacja)

            time.sleep(0.0025)
            self.odejmij_en(1)
            i += 1

        self.odejmij_hp(self.obrazenia_do_obsluzenia)
        self.obrazenia_do_obsluzenia = 0
        if self.czy_koniec():
            return
        return self.lez_na_ziemii(False)

        ### n nic nie robi (stoi), p przesuwa sie, g garda, u unik, w garda i unik, j uskok, s uderza,
        ### k kopie lub atak specjalny , c kolanko, t turlanie, d dobija, b wstaje, l lezy, m martwy, q dostaje
        ### v przewracanie_sie, h - jest skontrowany

    def zostan_skolankowany(self, obr, en):
        """Funkcja wywieszajaca flagi do obsluzenia odpowiednich zdarzen przez watek wlasciwy"""
        if self.stan == 'g':
            self.odejmij_hp(int(obr/2))
            self.odejmij_en(en)
            return
        if self.stan == 'p':
            return
        elif self.stan == 'q' or self.stan == 'h': #dostaje
            self.odejmij_hp(int(obr/2))
            self.odejmij_en(en)
        elif self.stan == 'b':
            self.jestem_uderzony = True
            self.odejmij_hp(obr)
        else:
            self.odejmij_hp(obr)
            self.odejmij_en(en)
        self.plansza.zaplam(self.x, self.y, 1)

    def zostan_uderzony(self, obr, en):
        """Funkcja wywieszajaca flagi do obsluzenia odpowiednich zdarzen przez watek wlasciwy"""
        self.ile_ciosow_otrzymalem_w_serii += 1
        if self.stan == 'g':
            return
        self.plansza.zaplam(self.x, self.y, 1)
        if self.stan == 'p':
            self.jestem_uderzony = True
            self.obrazenia_do_obsluzenia += obr
            #funkcja sama musi obsluzyc zadawanie obrazen
        elif self.stan == 'q': #dostaje
            self.odejmij_hp(int(obr/2))
        elif self.stan == 'k' or self.stan == 'n' or self.stan == 's' or self.stan == 'h':
            self.jestem_uderzony = True
            self.odejmij_hp(obr)
        elif self.stan == 'l' or self.stan == 'v':
            self.odejmij_hp(obr)
        elif self.stan == 'b':
            self.jestem_uderzony = True
            self.odejmij_hp(obr)

    def zostan_kopniety(self, obr, en):
        """Funkcja wywieszajaca flagi do obsluzenia odpowiednich zdarzen przez watek wlasciwy"""
        self.ile_ciosow_otrzymalem_w_serii += 1
        if self.energia <= 10:
            self.jestem_kopniety = True
            self.obrazenia_do_obsluzenia += obr
            self.plansza.zaplam(self.x, self.y, 1)
            return
        elif self.stan == 'g':
            self.odejmij_hp(5)
            self.odejmij_en(6)
            return
        self.plansza.zaplam(self.x, self.y, 1)
        if self.stan == 'p':
            self.jestem_kopniety = True
            self.obrazenia_do_obsluzenia += obr
            #funkcja sama musi obsluzyc zadawanie obrazen
        elif self.stan == 'q': #dostaje
            self.odejmij_hp(int(obr/2))
        elif self.stan == 'k' or self.stan == 'n' or self.stan == 'b' or self.stan == 's' or self.stan == 'h':
            self.jestem_kopniety = True
            self.odejmij_hp(obr)
        elif self.stan == 'l' or self.stan == 'v':
            self.odejmij_hp(obr)

    def lez_na_ziemii(self, czy_z_animacja_przewrocenia):
        """Obsluga lezenia na ziemii"""
        self.ile_ciosow_otrzymalem_w_serii = 0
        while True:
            time.sleep(0.01)
            if czy_z_animacja_przewrocenia:
                self.przewracanie()
            self.stan = 'l'
            self.aaanimacja = 2
            self.plansza.odmelduj_sie(self.x, self.y)
            self.plansza.zwolnij_pole(self.x, self.y)
            self.plansza.dodaj_lezacego(self)
            while self.energia < self.maksen:
                if self.czy_koniec():
                    return False
                time.sleep(0.1)
                self.energia += 2
            while True:
                if self.czy_koniec():
                    return False
                time.sleep(0.1)
                if self.plansza.zajmij_pole(self.x, self.y):
                    w = self.wstawanie()
                    if self.czy_koniec():
                        return False
                    if not w:
                        self.plansza.zwolnij_pole(self.x, self.y)
                        czy_z_animacja_przewrocenia = True
                        break
                    else:
                        return True

    def przewracanie(self):
        """Obsluga animacji przewracania sie"""
        self.stan = 'v'
        for i in range(0, 5):
            if self.czy_koniec():
                return False
            self.aaanimacja = 102 + 2 * i
            time.sleep(0.1)

        self.reset_animacji()
        return True

    def wstawanie(self): #76, 78, 80 zwraca, czy udalo sie wstac
        """Obsluga wstawania po lezeniu"""
        self.stan = 'b'
        self.plansza.usun_lezacego(self)
        self.plansza.zamelduj_sie(self)
        for i in range(0, 3):
            if self.czy_koniec():
                return False
            self.aaanimacja = 76 + 2 * i
            time.sleep(0.25)
            if self.jestem_uderzony or self.jestem_kopniety:
                self.jestem_uderzony, self.jestem_kopniety = False, False
                if self.czy_koniec():
                    return False
                else:
                    self.odejmij_en(50)
                    return False

        self.reset_animacji()
        return True


