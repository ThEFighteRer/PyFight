import random
import time
import threading

class Punkt:
    def __init__(self):
        self.a, self.b, self.odn = 0, 0, None

class Przeciwnik: #funckje pomocnicze AI

    def __init__(self):
        #nie dziala
        print("przec")

    def podejmij_centrowanie_postaci(self):
        """Zwraca True jesli nie ma przeksztalcenia pozycji , lub False wpp zmieniajac o 1 przeksztalcenie w strone wlasniwego (0,0)"""
        if self.przesuniecie_y == 0 and self.przesuniecie_x == 0:
            return True
        if self.przesuniecie_x < 0:
            self.przesuniecie_x += 1
        elif self.przesuniecie_x > 0:
            self.przesuniecie_x -= 1
        if self.przesuniecie_y < 0:
            self.przesuniecie_y += 1
        elif self.przesuniecie_y > 0:
            self.przesuniecie_y -= 1
        return False

    def jestem_zaraz_obok(self, x, y):
        """Czy obiekt jest obok wspolrzednuch"""
        return (abs(x - self.x) + abs(y - self.y)) <= 1

    def w_ktora_to_strone(self, x, y):#zwraca zwrot w strone wsp(x,y)
        """Zwraca zwrot w dana strone"""
        if x == self.x + 1 and y == self.y:
            return 'p'
        elif x == self.x - 1 and y == self.y:
            return 'l'
        elif x == self.x and y == self.y - 1:
            return 'g'
        elif x == self.x and y == self.y + 1:
            return 'd'
        elif x > self.x:
            return 'p'
        elif x < self.x:
            return 'l'
        elif y > self.y:
            return 'd'
        elif y < self.y:
            return 'g'
        else:
            return self.zwrot

    def wylosuj_pole_z_zakresu(self, minx, maxx, miny, maxy):#zwraca (x, y)
        """Losuje pole z zakresu"""
        if minx < 0:
            minx = 0
        if maxx > 15:
            maxx = 15
        if miny < 0:
            miny = 0
        if maxy > 8:
            maxy = 8
        return random.randint(minx, maxx), random.randint(miny, maxy)

    def gdzie_uciekac(self, g):
        """Zwraca zwrot do ucieczki od gracza g"""
        minx, maxx, miny, maxy = 0, 15, 0, 8
        if self.x == g.x:
            if self.y < g.y:
                miny, maxy = 0, self.y
            else:
                miny, maxy = self.y, 8
        else:
            if self.y > g.y:
                miny, maxy = self.y, 9
            elif self.y < g.y:
                miny, maxy = 0, self.y
            if self.x > g.x:
                minx, maxx = self.x, 15
            elif self.x < g.x:
                minx, maxx = 0, self.x

        for i in range(0, 15):
            pole = self.wylosuj_pole_z_zakresu(minx, maxx, miny, maxy)
            wynik = self.gdzie_isc(pole[0], pole[1], self.plansza.plansza)
            if wynik != 'n':
                return wynik
        return 'n'

    def gracza_atakuja_wszyscy_lub_odp_liczba(self):
        """Funkcja pomocnicza"""
        return self.ile_ludzi_atakuje_gracza() >= self.ile_ludzi_nie_ucieka()\
               or self.ile_ludzi_atakuje_gracza() >= self.plansza.poziom_trudnosci

    def gracza_atakuja_jak_na_kopanie_lezacych(self):
        """Funkcja pomocnicza"""
        return self.ile_ludzi_atakuje_gracza() >= self.ile_ludzi_nie_ucieka()\
               or self.ile_ludzi_atakuje_gracza() >= self.plansza.poziom_trudnosci + 2

    def gracz_odwrocony_ode_mnie_tylem(self):
        """Funkcja pomocnicza"""
        g = self.plansza.gracz
        if g.zwrot == 'p':
            return self.x < g.x and self.y >= g.y - 1 and self.y <= g.y + 1
        elif g.zwrot == 'l':
            return self.x > g.x and self.y >= g.y - 1 and self.y <= g.y + 1
        elif g.zwrot == 'g':
            return self.y > g.y and self.x >= g.x - 1 and self.x <= g.x + 1
        elif g.zwrot == 'd':
            return self.y < g.y and self.x >= g.x - 1 and self.x <= g.x + 1

    def gracz_odwrocony_ode_mnie_bokiem(self):
        """Funkcja pomocnicza"""
        g = self.plansza.gracz
        if g.zwrot == 'p' or g.zwrot == 'l':
            return self.x == g.x or self.y >= g.y + 2 or self.y <= g.y - 2
        if g.zwrot == 'g' or g.zwrot == 'd':
            return self.y == g.y or self.x >= g.x + 2 or self.x <= g.x - 2

    def ile_ludzi_atakuje_gracza(self):
        """Funkcja pomocnicza"""
        a = 0
        for i in self.plansza.spis_zywych:
            if i.co_robie == 'a' and i != self:
                a += 1
        return a

    def ile_ludzi_nie_ucieka(self):
        """Funkcja pomocnicza"""
        a = 0
        for i in self.plansza.spis_zywych:
            if i.co_robie != 'u' and i != self:
                a += 1
        return a

    def ile_ludzi_ucieka(self):
        """Funkcja pomocnicza"""
        a = 0
        for i in self.plansza.spis_zywych:
            if i.co_robie == 'u' and i != self:
                a += 1
        return a

    def ile_ludzi_okraza_gracza(self):
        """Funkcja pomocnicza"""
        a = 0
        for i in self.plansza.spis_zywych:
            if i.co_robie != 'a' and i != self\
                    and i.jestem_zaraz_obok(self.plansza.gracz.x, self.plansza.gracz.y):
                a += 1
        return a

    def gracz_kopie_lezacych(self):
        """Funkcja pomocnicza"""
        return time.clock() - self.plansza.czas_w_ktorym_gracz_kopnal_lezacego < 3

    def gracz_nie_byl_atakowany_od(self, ile):
        """Funkcja pomocnicza"""
        return time.clock() - self.plansza.czas_w_ktorym_gracz_zostal_zaatakowany >= ile

    def jest_w_zasiegu(self, x, y, jakim):
        """Funkcja pomocnicza"""
        return jakim >= abs(self.x - x) + abs(self.y - y)

    def gdzie_isc(self, cx, cy, p):#pokazuje, gdzie skrecic by dojsc do celu o wsp (cx, cy)
         """Zwraca zwrot, do pierwszego pola w najkrotszej sciezce do wspolrzednych cx, cy"""
         ppx, ppy= self.x, self.y
         if((cx==ppx and cy==ppy)):
             return 'n'
         if(cx==ppx+1 and cy==ppy):
             return 'p'
         if(cx==ppx-1 and cy==ppy):
             return 'l'
         if(cx==ppx and cy==ppy+1):
             return 'd'
         if(cx==ppx and cy==ppy-1):
             return 'g'
         if(cx==ppx+2 and cy==ppy):
             return'p'
         elif(cx==ppx-2 and cy==ppy):
             return'l'

         licznik_dla_n=0
         ile=150
         z, c = [], []
         for i in range(0, ile):
             z.append(Punkt())
             c.append(Punkt())
         c[0].a=ppy
         c[0].b=ppx
         c[0].odn=0
         n=1
         s=0
         k=1
         endd = False
         #int kor_x_22=0, kor_y_14=0, kor_x_0=0, kor_y_0=0;
         #if(cx==0) kor_x_0=1; else if(cx==21) kor_x_22=1; else if(cy==0) kor_y_0=1; else if(cy==13) kor_y_14=1;
         while True:
            licznik_dla_n += 1
            if licznik_dla_n >= ile:
                return 'n'
            for  y in range(s, k):
                lewo, prawo, dol, gora = True, True, True, True

                u = n - 1
                while u>-1:
                    if c[u].b==c[y].b+1 and c[u].a==c[y].a:
                        prawo=False
                        break
                    u-=1
                u = n - 1
                while u > -1:
                    if c[u].b==c[y].b-1 and c[u].a==c[y].a:
                        lewo = False
                        break
                    u -= 1
                u = n - 1
                while u > -1:
                    if c[u].b==c[y].b and c[u].a==c[y].a-1:
                        gora = False
                        break
                    u -= 1
                u = n - 1
                while u > -1:
                    if c[u].b==c[y].b and c[u].a==c[y].a+1:
                        dol = False
                        break
                    u -= 1
                if (c[y].b+1<16 and prawo and (p[c[y].a][c[y].b+1]==None or c[y].a==cy and c[y].b+1==cx)):
                    c[n].odn=y
                    c[n].a=c[y].a
                    c[n].b=c[y].b+1
                    if c[n].a==cy and c[n].b==cx:
                        i=0
                        z[0]=c[n]
                        h=c[n].odn
                        u = 1
                        while True:
                            z[u]=c[h]
                            h=c[h].odn
                            if h==0:
                                i=u
                                break
                            u+=1
                        if z[i].a==c[0].a and z[i].b==c[0].b+1:
                            return 'p'
                        if z[i].a==c[0].a and z[i].b==c[0].b-1:
                            return 'l'
                        if z[i].a==c[0].a-1 and z[i].b==c[0].b:
                            return 'g'
                        if z[i].a==c[0].a+1 and z[i].b==c[0].b:
                            return 'd'
                    n += 1
                if c[y].b-1>-1 and lewo and (p[c[y].a][c[y].b-1]==None or c[y].a==cy and c[y].b-1==cx):
                    c[n].odn=y
                    c[n].a=c[y].a
                    c[n].b=c[y].b-1
                    if c[n].a==cy and c[n].b==cx:
                        i=0
                        z[0]=c[n]
                        h=c[n].odn
                        u = 1
                        while True:
                            z[u]=c[h]
                            h=c[h].odn
                            if h==0:
                                i=u
                                break
                            u += 1
                        if (z[i].a==c[0].a and z[i].b==c[0].b+1):
                            return 'p'
                        if (z[i].a==c[0].a and z[i].b==c[0].b-1):
                            return 'l'
                        if (z[i].a==c[0].a-1 and z[i].b==c[0].b):
                            return 'g'
                        if (z[i].a==c[0].a+1 and z[i].b==c[0].b):
                            return 'd'
                    n += 1
                if (c[y].a-1>-1 and gora and (p[c[y].a-1][c[y].b]==None or c[y].a-1==cy and c[y].b==cx)):
                    c[n].odn=y
                    c[n].a=c[y].a-1
                    c[n].b=c[y].b
                    if (c[n].a==cy and c[n].b==cx):
                        i=0
                        z[0]=c[n]
                        h=c[n].odn
                        u = 1
                        while True:
                            z[u]=c[h]
                            h=c[h].odn
                            if (h==0):
                                i=u
                                break
                            u += 1
                        if (z[i].a==c[0].a and z[i].b==c[0].b+1):
                            return 'p'
                        if (z[i].a==c[0].a and z[i].b==c[0].b-1):
                            return 'l'
                        if (z[i].a==c[0].a-1 and z[i].b==c[0].b):
                            return 'g'
                        if (z[i].a==c[0].a+1 and z[i].b==c[0].b):
                            return 'd'
                    n += 1
                if (c[y].a+1<9 and dol and (p[c[y].a+1][c[y].b]==None or c[y].a+1==cy and c[y].b==cx)):
                    c[n].odn=y
                    c[n].a=c[y].a+1
                    c[n].b=c[y].b
                    if (c[n].a==cy and c[n].b==cx):
                        i=0
                        z[0]=c[n]
                        h=c[n].odn
                        u = 1
                        while True:
                            z[u]=c[h]
                            h=c[h].odn
                            if h==0:
                                i=u
                                break
                            u += 1
                        if (z[i].a==c[0].a and z[i].b==c[0].b+1):
                            return 'p'
                        if (z[i].a==c[0].a and z[i].b==c[0].b-1):
                            return 'l'
                        if (z[i].a==c[0].a-1 and z[i].b==c[0].b):
                            return 'g'
                        if (z[i].a==c[0].a+1 and z[i].b==c[0].b):
                            return 'd'
                    n += 1
            s=k
            k=n
            if endd:
                break
         return 'n'

    def trzymam_garde(self):#168
        """Funkcja odpowiedzialna za dzialania, gdy zawodnik zdecyduje sie trzymac garde"""
        self.stan = 'g'
        i = 0
        while True:
            self.jestem_kopniety = False
            self.jestem_uderzony = False
            i += 1
            time.sleep(0.01)
            if self.czy_koniec():
                return
            if self.energia <= 10:
                self.co_robie = 'c'
                break
            if (i % 25) == 0:
                i = 0
                d = self.decyzja()
                if d != 'g':
                    self.ile_ciosow_otrzymalem_w_serii = 0
                    break
        self.stan = 'n'

    def uciekam(self):
        """Funkcja odpowiedzialna za dzialania, gdy zawodnik zdecyduje sie uciekac"""
        g = self.plansza.gracz
        while True:
            self.co_robie = self.decyzja()
            if self.co_robie != 'u':
                break
            time.sleep(0.01)
            self.przesun(self.gdzie_uciekac(g))
            if self.czy_koniec():
                return
            if self.jestem_kopniety or self.jestem_uderzony:
                self.co_robie = 'a'
                return

    def chodze_bez_sensu(self):
        """Funkcja odpowiedzialna za dzialania, gdy zawodnik zdecyduje sie na chwile odpuscic"""
        self.ile_ciosow_otrzymalem_w_serii = 0
        g = self.plansza.gracz
        while True:
            if self.czy_koniec():
                return
            if self.jestem_kopniety or self.jestem_uderzony:
                return
            self.co_robie = self.decyzja()
            if self.co_robie != 'c':
                break
            a = random.randint(0, 6)
            b = True
            if a == 0:
                b = self.przesun('p')
            elif a == 1:
                b = self.przesun('l')
            elif a == 2:
                b = self.przesun('g')
            elif a == 3:
                b = self.przesun('d')
            else:
                for i in range(50, random.randint(50, 250)):
                    time.sleep(0.01)
                    if self.czy_koniec():
                        return
                    if self.jestem_kopniety or self.jestem_uderzony:
                        return
                    if (i % 20) == 0:
                        self.co_robie = self.decyzja()
                        if self.co_robie != 'c':
                            break
            if not b:
                for i in range(50, random.randint(50, 250)):
                    time.sleep(0.01)
                    if self.czy_koniec():
                        return
                    if self.jestem_kopniety or self.jestem_uderzony:
                        return
                    if (i % 20) == 0:
                        self.co_robie = self.decyzja()
                        if self.co_robie != 'c':
                            break

    def decyzja(self):
        """Funkcja zwracajaca najlepsze na dana chwile dzialanie dla zawodnika"""
        g = self.plansza.gracz
        dec = self.co_robie

        if (self.energia >= 10 or self.co_robie == 'g') and self.ile_ciosow_otrzymalem_w_serii >= 3:#zawodnik dostal juz tyle ciosow ze ledwo widzi
            if self.jest_w_zasiegu(g.x, g.y, 2):
                if self.plansza.poziom_trudnosci >= 2 and self.gracz_odwrocony_ode_mnie_tylem():
                    self.ile_ciosow_otrzymalem_w_serii = 0
                    dec = 'a'
                elif self.plansza.poziom_trudnosci == 2 and self.gracz_odwrocony_ode_mnie_bokiem():
                    self.ile_ciosow_otrzymalem_w_serii = 0
                    dec = 'a'
                else:
                    dec = 'g'
            else:
                self.ile_ciosow_otrzymalem_w_serii = 0
                dec = 'c'

        elif self.HP > self.plansza.poziom_trudnosci * 10:#zawodnik w swietnej kondycji
            if self.jest_w_zasiegu(g.x, g.y, 2):
                dec = 'a'
            elif self.jest_w_zasiegu(g.x, g.y, 4):
                if not self.gracza_atakuja_wszyscy_lub_odp_liczba() or self.gracz_kopie_lezacych():
                    dec = 'a'
            elif self.jest_w_zasiegu(g.x, g.y, 7):
                if self.gracz_kopie_lezacych() and not self.gracza_atakuja_jak_na_kopanie_lezacych():
                    dec = 'a'
            else:
                dec = 'c'

        else:#zawodnik w slabej kondycji
            if self.jest_w_zasiegu(g.x, g.y, 1) or len(self.plansza.spis_zywych) - 1 <= self.ile_ludzi_ucieka():
                dec = 'a'
            elif self.jest_w_zasiegu(g.x, g.y, 5):
                if self.gracza_atakuja_wszyscy_lub_odp_liczba()\
                        or (self.gracz_kopie_lezacych()
                            and (self.ile_ludzi_atakuje_gracza() >= self.plansza.poziom_trudnosci
                                 or self.ile_ludzi_atakuje_gracza() >= self.ile_ludzi_nie_ucieka())):
                    dec = 'a'
                else:
                    dec = 'u'
            elif self.jest_w_zasiegu(g.x, g.y, 7):
                dec = 'u'
            else:
                dec = 'c'

        return dec



