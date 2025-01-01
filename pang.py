import pygame
import sys
import math
import time
import random
from timeit import default_timer as timer
import multiprocessing
AdresSkinaKulki= "Grafika\kula.png"
AdresSkinaGracza = "Grafika\Gracz.png"
AdresSkinaPocisk='Grafika\strzal.png'
AdresSkinaBomby="Grafika\Bomba.png"
LaserSkin="Grafika\laser.png"
PistoletSkin="Grafika\pistolet.png"
PompaSkin="Grafika\pompa.png"
AdresSkinaShotgunPocisk="Grafika\kulashotgun.png"
AdresSkinaSerce="Grafika\serce.png"

import pygame
import sys
import math
import time
import random
from timeit import default_timer as timer
import multiprocessing
AdresSkinaKulki= "Grafika\kula.png"
AdresSkinaGracza = "Grafika\Gracz.png"
AdresSkinaPocisk='Grafika\strzal.png'
AdresSkinaBomby="Grafika\Bomba.png"
LaserSkin="Grafika\laser.png"
PistoletSkin="Grafika\pistolet.png"
PompaSkin="Grafika\pompa.png"
AdresSkinaShotgunPocisk="Grafika\kulashotgun.png"
AdresSkinaSerce="Grafika\serce.png"

KulaSpeed=5
KulaSpeedX=1
GraczSpeed=5
PociskSpeed=10
Screen_width=1600
Screen_height=900
g=0.02
wspY=0.98
wspX=0.98
class Kula(pygame.sprite.Sprite):                                                   #definicja duszka do ktorego bedziemy strzelac
    def __init__(self,pos_x,pos_y,promien,changeX,changeY,niesmiertelnosc):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.r = promien
        self.changeX =changeX
        self.changeY = changeY
        self.image=pygame.image.load(AdresSkinaKulki).convert_alpha()
        self.image=pygame.transform.rotozoom(self.image,0,(self.r/32))             #zwiekszenie lub zmiejszenie kulki w zaleznosci od promienia
        self.rect=self.image.get_rect()
        self.immortal=niesmiertelnosc
    def move(self):                                                                                #funkcja ktora zmienia polozenie kulki
        if(self.x+self.changeX<self.r or self.x+self.changeX>Screen_width-self.r):                  #dzieki tym ifom kulka wytraca predkosc
            self.changeX=0-(self.changeX)*wspX
        if(self.y+self.changeY<self.r or self.y+self.changeY>Screen_height-self.r):
            self.changeY=0-(self.changeY)*wspY
        self.x+=self.changeX*KulaSpeedX
        self.y+=self.changeY*self.r/32
        self.changeY+=g
        self.rect.center=[self.x,self.y]

class Pocisk(pygame.sprite.Sprite):                                                           #utworzenie klasy pocisku
     def __init__(self,pos_x,pos_y):
        super().__init__()
        self.x= pos_x
        self.y= pos_y
        self.image=pygame.image.load(AdresSkinaPocisk).convert_alpha()
        self.rect=self.image.get_rect()
     def move(self):                                                                        #funckcja ktora przesuwa pocisk
        self.y-=PociskSpeed
        self.rect.center=[self.x,self.y]

class Gracz(pygame.sprite.Sprite):                                                           #definicja postaci gracza
    def __init__(self,pos_x,pos_y,sg,speed):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.g=sg                                                                           #g-wsp. przyciagania ziemskiego
        self.changeX=0
        self.changeY=0
        self.czy_speed=speed
        self.image=pygame.image.load(AdresSkinaGracza).convert_alpha()
        self.rect=self.image.get_rect()
        self.imageZwykly=pygame.image.load(AdresSkinaGracza).convert_alpha()
        self.imageBlink=pygame.image.load("Grafika\czarny.png").convert_alpha()
        self.Grawitacja=True
        self.imagedrabina1=pygame.image.load("Grafika//drabina1.png").convert_alpha()
        self.imagedrabina2=pygame.image.load("Grafika//drabina2.png").convert_alpha()
        self.imageprawo1=pygame.image.load("Grafika//krok w prawo 1.png").convert_alpha()
        self.imageprawo2=pygame.image.load("Grafika//srodek w prawo.png").convert_alpha()
        self.imageprawo3=pygame.image.load("Grafika//krok w prawo 2.png").convert_alpha()
        self.imagelewo1=pygame.image.load("Grafika//krok w lewo 1.png").convert_alpha()
        self.imagelewo2=pygame.image.load("Grafika//srodek w lewo.png").convert_alpha()
        self.imagelewo3=pygame.image.load("Grafika//krok w lewo 2.png").convert_alpha()
        self.imagelaser=pygame.image.load("Grafika//w miejscu laser strzal.png").convert_alpha()
        self.imagelaser2=pygame.image.load("Grafika//w miejscu laser.png").convert_alpha()
        self.imageshotgunstrzal=pygame.image.load("Grafika//w miejscu shotgun strzal.png").convert_alpha()
        self.imageshotgun=pygame.image.load("Grafika//w miejscu shotgun.png").convert_alpha()
        self.imagepociskstrzal=pygame.image.load("Grafika//pocisk w miejscu strzal.png").convert_alpha()
        self.imagepocisk=pygame.image.load(AdresSkinaGracza).convert_alpha()
        self.imagebomba=pygame.image.load("Grafika//w miejscu bomba.png").convert_alpha()
        if(self.czy_speed):
            GraczSpeed=GraczSpeed*2
    def move(self,Prostokaty,Drabiny,GraczSpeed):                                                          #ruch gracza
        RuchX=True
        self.RuchY=False
        self.Grawitacja=True
        for drabina in Drabiny:                                                                                           #sprawdzamy czy gracz jest na drabinie
            if(self.x>drabina.x1 and self.x<drabina.x2 and self.y>drabina.y1-34 and self.y<drabina.y2+32):
                self.RuchY=True
                self.Grawitacja=False
                self.g=0
                if(self.y+self.changeY<drabina.y1-32):
                    self.y=drabina.y1-32
                    self.RuchY=False
                if(self.y+self.changeY>drabina.y2-32):
                    drabina.y2+32
                    self.RuchY=False
            if(self.x>drabina.x1 and self.x<drabina.x2):
                if(self.y+33>drabina.y1 and self.y<drabina.y2):
                    self.Grawitacja=False
                    self.g=0
        for prostokat in Prostokaty:                                                                                        #sprawdzamy czy gracz po ruchu nie wejdzie w sciane
            if(self.x+self.changeX>prostokat.x1-16 and self.x+self.changeX<prostokat.x2+16):
                if(self.y<prostokat.y2+32 and self.y>prostokat.y1-32):
                    if(self.changeX>0):
                        if(self.x<prostokat.x1):
                            self.x=prostokat.x1-16
                    else:
                        if(self.x>prostokat.x2):
                            self.x=prostokat.x2+16
                    RuchX=False
            if(self.y+self.changeY>prostokat.y1-32 and self.y+self.changeY<prostokat.y2+32):
                if(self.x<prostokat.x2+16 and self.x>prostokat.x1-16):
                    if(self.changeY>0):
                        if(self.y<prostokat.y1):
                            self.y=prostokat.y1-32
                    else:
                        if(self.y>prostokat.y2):
                            self.y=prostokat.y2+32
                    self.RuchY=False
            if(self.y+self.g>prostokat.y1-32 and self.y+self.g<prostokat.y2+32):
                if(self.x<prostokat.x2+16 and self.x>prostokat.x1-16):
                    self.Grawitacja=False
                    self.g=0
            if(self.x>prostokat.x1-16 and self.x<prostokat.x2+16):
                if(self.y+33>prostokat.y1 and self.y<prostokat.y2):
                    self.Grawitacja=False
                    self.g=0
        if(self.y+self.changeY>Screen_height-32 or self.y+self.changeY<32):                                 #sprawdzamy czy gracz nie wyjdzie poza plansze
            self.RuchY=False
        if(self.x+self.changeX>Screen_width-16 or self.x+self.changeX<16):
            RuchX=False

        if(RuchX):                                                                                          #wykonujemy ruch
            self.x+=self.changeX
        if(self.RuchY):
            self.y+=self.changeY

        if(self.y+33>Screen_height):
            self.Grawitacja=False
            self.g=0
        if(self.Grawitacja):                                                                                    #zwiekszamy predkosc w osi y o przyspieszenie ziemskie
            self.y+=self.g
            self.g+=0.3
        if(self.y>Screen_height-32):
            self.y=Screen_height-32

    def draw(self,x,atak,czylaser,strzal):
        if(x>0 and (x%4==1 or x%4==2)):
            self.image=self.imageBlink
        elif(atak=="laser" and czylaser>0):
            self.image=self.imagelaser
            strzal=False
        elif(self.changeX>0 and (x%40<10)):
            self.image=self.imageprawo1
            strzal=False
        elif(self.changeX>0 and (x%40<20)):
            self.image=self.imageprawo2
            strzal=False
        elif(self.changeX>0 and (x%40<30)):
            self.image=self.imageprawo3
            strzal=False
        elif(self.changeX>0 and (x%40<40)):
            self.image=self.imageprawo2
            strzal=False
        elif(self.changeX<0 and (x%40<10)):
            self.image=self.imagelewo1
            strzal=False
        elif(self.changeX<0 and (x%40<20)):
            self.image=self.imagelewo2
            strzal=False
        elif(self.changeX<0 and (x%40<30)):
            self.image=self.imagelewo3
            strzal=False
        elif(self.changeX<0 and (x%40<40)):
            self.image=self.imagelewo2
            strzal=False
        elif(self.RuchY and self.changeY!=0 and (x%16<8) and not(self.Grawitacja)):
            self.image=self.imagedrabina1
            strzal=False
        elif(self.RuchY and self.changeY!=0 and (x%16>=8) and not(self.Grawitacja)):
            self.image=self.imagedrabina2
            strzal=False
        elif(atak=="laser"):
            self.image=self.imagelaser2
            strzal=False
        elif(atak=="shotgun" and strzal):
            self.image=self.imageshotgunstrzal
        elif(atak=="shotgun"):
            self.image=self.imageshotgun
        elif(atak=="pociski" and strzal):
            self.image=self.imagepociskstrzal
        elif(atak=="pociski"):
            self.image=self.imagepocisk
        elif(atak=="bomba"):
            self.image=self.imagebomba
        else:
            self.image=self.imageZwykly

        self.rect.center=[self.x,self.y]
        return strzal


class Prostokat(pygame.sprite.Sprite):                                                          #klasa tworzaca sciany

    def __init__(self,posx1,posx2,posy1,posy2,zycie):
        super().__init__()
        self.x1=min(posx1,posx2)
        self.x2=max(posx1,posx2)
        self.y1=min(posy1,posy2)
        self.y2=max(posy1,posy2)
        self.hp=zycie

        if(self.hp>=100000):                                                                                #jesli sciana ma wiecej hp niz 1000000 to jest niesmiertelna, i ma inna grafike
            self.image=pygame.image.load("Grafika\sciana "+str(int(self.x2-self.x1))+"x"+str(int(self.y2-self.y1))+" px.png").convert_alpha()           #wczytywanie grafiki o odpowiedniej nazwie
        else:
            self.image=pygame.image.load("Grafika\mur "+str(int(self.x2-self.x1))+"x"+str(int(self.y2-self.y1))+" px.png").convert_alpha()              #wczytywanie grafiki o odpowiedniej nazwie
        self.rect=self.image.get_rect()
        self.rect.center=[abs(self.x2+self.x1)/2,abs(self.y1+self.y2)/2]

class Drabina(pygame.sprite.Sprite):                                                                                    #klasa tworzaca drabiny, analogiczna do Prostokat
    def __init__(self,posx1,posx2,posy1,posy2):
        super().__init__()
        self.x1=min(posx1,posx2)
        self.x2=max(posx1,posx2)
        self.y1=min(posy1,posy2)
        self.y2=max(posy1,posy2)
        self.image=pygame.image.load("Grafika\drabina "+str(int(self.x2-self.x1))+"x"+str(int(self.y2-self.y1))+" px.png").convert_alpha()                  #wczytujemy grafike o odpowiedniej nazwie
        self.rect=self.image.get_rect()
        self.rect.center=[abs(self.x2+self.x1)/2,abs(self.y1+self.y2)/2]
class Laser(pygame.sprite.Sprite):                                                                              #klasa pocisku laserowego
    def __init__(self,x,y1,y2):
        super().__init__()
        self.image=pygame.Surface([2,abs(y2-y1)+2])                                                         #rysujemy prostokat, i wypełniamy go kolorem morskim
        self.image.fill((163,255,241))
        self.rect=self.image.get_rect()
    def move(self,Prostokaty,gracz):
        maxy=0
        for prstk in Prostokaty:                                            #sprawdzamy dokad moze dojsc laser
            if(gracz.x>prstk.x1 and gracz.x<prstk.x2):
                if prstk.y2>maxy and prstk.y2<gracz.y:
                    maxy=prstk.y2
        self.image=pygame.Surface([2,gracz.y-maxy-32+2])                                                    #rysujemy prostokat, i wypełniamy go kolorem morskim
        self.image.fill((163,255,241))
        self.rect=self.image.get_rect()
        self.rect.center=[gracz.x,(gracz.y-32+maxy)/2]                  #przesuwamy laser nad gracza
class Bomba(pygame.sprite.Sprite):                                                                  #klasa bomby
    def __init__(self,pos_x,pos_y,time):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.czas=time
        self.image=pygame.transform.scale(pygame.image.load("Grafika\\bombawybuch.png").convert_alpha(),(32,32))                                #wczytujemy grafike
        self.rect=self.image.get_rect()
        self.rect.center=[self.x,self.y+16]
    def wybuch(self,r):                                                                                 #zmiana grafiki
        self.image=wybuchy[r]                                                                                                                       #zmieniamy grafike na kolejna klatke animacji wybuchu
        self.rect=self.image.get_rect()
        self.rect.center=[self.x,self.y+16]
class PociskShotgun(pygame.sprite.Sprite):                                                  #klasa pocisku do shotguna, analogiczna co do zwyklego pocisku
    def __init__(self,posx,posy,changeX):
        super().__init__()
        self.x=posx
        self.y=posy
        self.cx=changeX
        self.image=pygame.image.load(AdresSkinaShotgunPocisk).convert_alpha()
        self.image=pygame.transform.rotozoom(self.image,0,(1/8))
        self.rect=self.image.get_rect()
    def move(self):
        self.x+=self.cx
        self.y-=10
        self.rect.center=[self.x,self.y]
class Artefakt(pygame.sprite.Sprite):                                                               #klasa artefaktu
    def __init__(self,posx,posy,typ_artefaktu,ilosc_score):
        super().__init__()
        self.x=posx
        self.y=posy
        self.typ=typ_artefaktu
        self.ScoreWhenStart=ilosc_score
        if(self.typ=="serce"):                                                                                      #odpowiednia grafika do odpowiedniego typu artefaktu
            self.image=pygame.image.load("Grafika\\artefaktserce.png").convert_alpha()
        elif(self.typ=="amunicja"):
            self.image=pygame.image.load("Grafika\\artefaktamunicja.png").convert_alpha()
        elif(self.typ=="speed"):
            self.image=pygame.image.load("Grafika\\artefakt speed.png").convert_alpha()

        self.rect=self.image.get_rect()
        self.rect.center=[self.x,self.y]
class Lod(pygame.sprite.Sprite):                                                                        #klasa lodu
    def __init__(self,posx1,posx2,posy):
        super().__init__()
        self.x1=posx1
        self.x2=posx2
        self.y=posy
        self.image=pygame.Surface([abs(self.x1-self.x2),10])                                                   #rysujemy lod
        self.image.fill('white')
        self.rect=self.image.get_rect()
        self.rect.center=[(self.x1+self.x2)/2,self.y]
class Kolec(pygame.sprite.Sprite):                                                                  #klasa kolca
    def __init__(self,posx,posy,rotation):                                                              #wsp X, wsp Y, oraz w ktora strone ma byc skierowany kolec
        super().__init__()
        self.x=posx
        self.y=posy
        self.angle=rotation
        self.image=pygame.image.load("Grafika\kolec.png").convert_alpha()
        self.image=pygame.transform.rotozoom(self.image,self.angle,1).convert_alpha()                                           #ladujemy grafike i obracamy
        self.rect=self.image.get_rect()
        self.rect.center=([self.x,self.y])
class button():                                                             #klasa przycisku, skopiowana z poradnika tech with tim
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-4,self.y-4,self.width+8,self.height+8),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.SysFont('freesansbold.ttf', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
def WypiszSerca(screen,serca):                                      #wypisuje ilosc serc na ekranie
    screen.blit(Serce,(0,0))
    Wypisz(30-len(str(int(serca)))*5,15,screen,str(int(serca)),"black")
def WypiszAmunicje(screen,amunicja):                            #wypisuje amunicje na ekranie
    screen.blit(Amunicja,(0,64))
    Wypisz(30-len(str(int(amunicja)))*5,87,screen,str(int(amunicja)),"black")

def zderzenie(Kula,Prostokat):                      #sprawdza czy kula nie odbija sie od prostokata, i jesli tak to z jakiej strony

    if(Kula.x+Kula.changeX<Prostokat.x2+Kula.r and Kula.x+Kula.changeX>Prostokat.x1-Kula.r):

        if(Kula.y<Prostokat.y2+Kula.r and Kula.y>Prostokat.y1-Kula.r):
            Kula.changeX=0-(Kula.changeX)*wspX
    if(Kula.y+Kula.changeY<Prostokat.y2+Kula.r  and Kula.y+Kula.changeY>Prostokat.y1-Kula.r):
        if(Kula.x<Prostokat.x2+Kula.r and Kula.x>Prostokat.x1-Kula.r):
            Kula.changeY=0-(Kula.changeY)*wspY
    return(Kula.changeX,Kula.changeY)
def Wypisz(x,y,okno,napis,color=(255,255,255)):                     #Wypisuje dany napis
    font = base_font
    Wynik = font.render(napis,True,color)
    okno.blit(Wynik,(x,y))
def odczyt(sciezka):                            #funkcja zwraca obiekty ktore zostaly zapisane w pliku za pomoca funkcji zapis()
    file=open(sciezka,"r")
    zapisane=file.readlines()
    Kule=[]
    i=0
    while(zapisane[i]!="Kule\n"):
        kulax,kulay,kular,kulaCX,kulaCY,niesmiertelnosc=zapisane[i].split("#")
        Kule.append(Kula(float(kulax),float(kulay),float(kular),float(kulaCX),float(kulaCY),float(niesmiertelnosc.rstrip())))
        i+=1
    i+=1
    Drabiny=[]
    while(zapisane[i]!="Drabiny\n"):
        drabinyx1,drabinyx2,drabinyy1,drabinyy2=zapisane[i].split("#")
        Drabiny.append(Drabina(float(drabinyx1),float(drabinyx2),float(drabinyy1),float(drabinyy2.rstrip())))
        i+=1
    i+=1
    Prostokaty=[]
    while(zapisane[i]!="Prostokaty\n"):
        prostokatyx1,prostokatyx2,prostokatyy1,prostokatyy2,hp=zapisane[i].split("#")
        Prostokaty.append(Prostokat(float(prostokatyx1),float(prostokatyx2),float(prostokatyy1),float(prostokatyy2),float(hp.rstrip())))
        i+=1
    i+=1
    Pociski=[]
    while(zapisane[i]!="Pociski\n"):
        pociskix,pociskiy=zapisane[i].split("#")
        Pociski.append(Pocisk(float(pociskix),float(pociskiy.rstrip())))
        i+=1
    i+=1
    Bomby=[]
    while(zapisane[i]!="Bomby\n"):
        bombyx,bombyy,bombyczas=zapisane[i].split("#")
        Bomby.append(Bomba(float(bombyx),float(bombyy),float(bombyczas.rstrip())))
        i+=1
    i+=1
    PociskiShotgun=[]
    while(zapisane[i]!="PociskiShotgun\n"):
        psx,psy,pscx=zapisane[i].split('#')
        PociskiShotgun.append(PociskShotgun(float(psx),float(psy),float(pscx.rstrip())))
        i+=1
    i+=1
    Artefakty=[]
    while(zapisane[i]!="Artefakty\n"):
        ax,ay,atyp,ascore=zapisane[i].split("#")
        Artefakty.append(Artefakt(float(ax),float(ay),atyp,float(ascore.rstrip())))
        i+=1
    i+=1
    tarcza="True"
    graczx,graczy,graczg,gracztarcza=zapisane[i].split("#")
    gracz=Gracz(float(graczx),float(graczy),float(graczg),tarcza==gracztarcza.rstrip())
    i+=2
    amunicja_pocisk=float(zapisane[i])
    i+=2
    amunicja_laser=float(zapisane[i])
    i+=2
    amunicja_bomba=float(zapisane[i])
    i+=2
    amunicja_shotgun=float(zapisane[i])
    i+=2
    score=float(zapisane[i])
    i+=2
    serca=float(zapisane[i])
    i+=2
    immortal=float(zapisane[i])
    i+=2
    Lody=[]
    while(zapisane[i]!="Lody\n"):
        lx1,lx2,ly=zapisane[i].split('#')
        Lody.append(Lod(float(lx1),float(lx2),float(ly.rstrip())))
        i+=1
    i+=1
    Kolce=[]
    while(zapisane[i]!="Kolce\n"):
        kx,ky,ka=zapisane[i].split('#')
        Kolce.append(Kolec(float(kx),float(ky),float(ka.rstrip())))
        i+=1
    i+=1
    max_score=float(zapisane[i])
    i+=2
    tryb=zapisane[i].rstrip()
    i+=2
    mapa=int(zapisane[i])
    i+=2
    sumapunktow=float(zapisane[i])
    file.close()

    return(Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
def zapis(sciezka,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow):
    file=open(sciezka,"w")                      #otwieramy plik, i dla kazdego elemntu gry zapisujemy aktualny stan rozgrywki. po zakonczeniu wypisywaniu objektow danego typu wypisywana jest ich nazwa (np. Kule). poszczegolne obiekty oddzielone sa znakiem nowej lini
    Kule_zapis=[]
    for kula in Kule:
        Kule_zapis.append(str(kula.x)+"#"+str(kula.y)+"#"+str(kula.r)+"#"+str(kula.changeX)+"#"+str(kula.changeY)+"#"+str(kula.immortal)+"\n")
    for x in Kule_zapis:
        file.write(x)
    file.write("Kule\n")
    Drabiny_zapis=[]
    for drabina in Drabiny:
        Drabiny_zapis.append(str(drabina.x1)+"#"+str(drabina.x2)+"#"+str(drabina.y1)+"#"+str(drabina.y2)+"\n")
    for x in Drabiny_zapis:
        file.write(x)
    file.write("Drabiny\n")
    Prostokaty_zapis=[]
    for prostokat in Prostokaty:
        Prostokaty_zapis.append(str(prostokat.x1)+"#"+str(prostokat.x2)+"#"+str(prostokat.y1)+"#"+str(prostokat.y2)+"#"+str(prostokat.hp)+"\n")
    for x in Prostokaty_zapis:
        file.write(x)
    file.write("Prostokaty\n")
    Pociski_zapis=[]
    for pocisk in Pociski:
        Pociski_zapis.append(str(pocisk.x)+"#"+str(pocisk.y)+"\n")
    for x in Pociski_zapis:
        file.write(x)
    file.write("Pociski\n")
    Bomby_zapis=[]
    for bomba in Bomby:
        Bomby_zapis.append(str(bomba.x)+"#"+str(bomba.y)+"#"+str(bomba.czas)+"\n")
    for x in Bomby_zapis:
        file.write(x)
    file.write("Bomby\n")
    PociskiShotgun_zapis=[]
    for pociskShotgun in PociskiShotgun:
        PociskiShotgun_zapis.append(str(pociskShotgun.x)+"#"+str(pociskShotgun.y)+"#"+str(pociskShotgun.cx)+"\n")
    for x in PociskiShotgun_zapis:
        file.write(x)
    file.write("PociskiShotgun\n")
    Artefakty_zapis=[]
    for artefakt in Artefakty:
        Artefakty_zapis.append(str(artefakt.x)+"#"+str(artefakt.y)+"#"+str(artefakt.typ)+"#"+str(artefakt.ScoreWhenStart)+"\n")
    for x in Artefakty_zapis:
        file.write(x)
    file.write("Artefakty\n")

    file.write(str(gracz.x)+"#"+str(gracz.y)+"#"+str(gracz.g)+"#"+str(gracz.czy_speed)+"\n")
    file.write("Gracz\n")
    file.write(str(amunicja_pocisk)+"\n")
    file.write("amunicja_pocisk\n")
    file.write(str(amunicja_laser)+"\n")
    file.write("amunicja_laser\n")
    file.write(str(amunicja_bomba)+"\n")
    file.write("amunicja_bomba\n")
    file.write(str(amunicja_shotgun)+"\n")
    file.write("amunicja_shotgun\n")
    file.write(str(score)+"\n")
    file.write("Score\n")
    file.write(str(serca)+"\n")
    file.write("Serca\n")
    file.write(str(immortal)+"\n")
    file.write("immortal\n")
    Lody_zapis=[]
    for lod in Lody:
        Lody_zapis.append(str(lod.x1)+"#"+str(lod.x2)+"#"+str(lod.y)+"\n")
    for x in Lody_zapis:
        file.write(x)
    file.write("Lody\n")
    Kolce_zapis=[]
    for kolec in Kolce:
        Kolce_zapis.append(str(kolec.x)+"#"+str(kolec.y)+"#"+str(kolec.angle)+"\n")
    for x in Kolce_zapis:
        file.write(x)
    file.write("Kolce\n")
    file.write(str(max_score)+"\n")
    file.write("MaxScore\n")
    file.write(str(tryb)+"\n")
    file.write('Tryb\n')
    file.write(str(mapa)+"\n")
    file.write("Mapa\n")
    file.write(str(sumapunktow)+"\n")
    file.write("Sumapunktow\n")
    file.close()
def zapis_lobby(screen,Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow1):           #funkcja analogiczna do odczyt_lobby(), tylko do zapisu
    motorolla_jest_lepsza_od_nokii=True
    plik1=open("ZapisaneGry/Zapis1.txt", "r")
    plik2=open("ZapisaneGry/Zapis2.txt", "r")
    plik3=open("ZapisaneGry/Zapis3.txt", "r")
    plik4=open("ZapisaneGry/Zapis4.txt", "r")
    plik5=open("ZapisaneGry/Zapis5.txt", "r")
    linie_plik1=plik1.readlines()
    if(len(linie_plik1)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis1.txt")
        Slot1=button((0,255,0),100,50,1400,150,"Score: "+str(int(score))+" "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot1=True
    else:
        Slot1=button((255,0,0),100,50,1400,150,"Wolny slot")
        Czy_slot1=False
    linie_plik2=plik2.readlines()
    if(len(linie_plik2)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis2.txt")
        Slot2=button((0,255,0),100,225,1400,150,"Score: "+str(int(score))+", "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot2=True
    else:
        Slot2=button((255,0,0),100,225,1400,150,"Wolny slot")
        Czy_slot2=False
    linie_plik3=plik3.readlines()
    if(len(linie_plik3)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis3.txt")
        Slot3=button((0,255,0),100,400,1400,150,"Score: "+str(int(score))+", "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot3=True
    else:
        Slot3=button((255,0,0),100,400,1400,150,"Wolny slot")
        Czy_slot3=False
    linie_plik4=plik4.readlines()
    if(len(linie_plik4)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis4.txt")
        Slot4=button((0,255,0),100,575,1400,150,"Score: "+str(int(score))+", "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot4=True
    else:
        Slot4=button((255,0,0),100,575,1400,150,"Wolny slot")
        Czy_slot4=False
    linie_plik5=plik5.readlines()
    if(len(linie_plik5)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis5.txt")
        Slot5=button((0,255,0),100,750,1400,150,"Score: "+str(score)+", "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot5=True
    else:
        Slot5=button((255,0,0),100,750,1400,150,"Wolny slot")
        Czy_slot5=False
    plik1.close()
    plik2.close()
    plik3.close()
    plik4.close()
    plik5.close()
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    motorolla_jest_lepsza_od_nokii=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(Slot1.isOver(pos)):
                    zapis("ZapisaneGry\Zapis1.txt",Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow1)
                    motorolla_jest_lepsza_od_nokii=False
                if(Slot2.isOver(pos)):
                    zapis("ZapisaneGry\Zapis2.txt",Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow1)
                    motorolla_jest_lepsza_od_nokii=False
                if(Slot3.isOver(pos)):
                    zapis("ZapisaneGry\Zapis3.txt",Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow1)
                    motorolla_jest_lepsza_od_nokii=False
                if(Slot4.isOver(pos)):
                    zapis("ZapisaneGry\Zapis4.txt",Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow1)
                    motorolla_jest_lepsza_od_nokii=False
                if(Slot5.isOver(pos)):
                    zapis("ZapisaneGry\Zapis5.txt",Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow1)
                    motorolla_jest_lepsza_od_nokii=False
            if event.type == pygame.MOUSEMOTION:
                if Slot1.isOver(pos):
                    Slot1.color=(0,0,255)
                else:
                    if(Czy_slot1):
                        Slot1.color=(0,255,0)
                    else:
                        Slot1.color=(255,0,0)
                if Slot2.isOver(pos):
                    Slot2.color=(0,0,255)
                else:
                    if(Czy_slot2):
                        Slot2.color=(0,255,0)
                    else:
                        Slot2.color=(255,0,0)
                if Slot3.isOver(pos):
                    Slot3.color=(0,0,255)
                else:
                    if(Czy_slot3):
                        Slot3.color=(0,255,0)
                    else:
                        Slot3.color=(255,0,0)
                if Slot4.isOver(pos):
                    Slot4.color=(0,0,255)
                else:
                    if(Czy_slot4):
                        Slot4.color=(0,255,0)
                    else:
                        Slot4.color=(255,0,0)
                if Slot5.isOver(pos):
                    Slot5.color=(0,0,255)
                else:
                    if(Czy_slot5):
                        Slot5.color=(0,255,0)
                    else:
                        Slot5.color=(255,0,0)




        screen.blit(tlogra,(0,0))
        Slot1.draw(screen,(0,0,0))
        Slot2.draw(screen,(0,0,0))
        Slot3.draw(screen,(0,0,0))
        Slot4.draw(screen,(0,0,0))
        Slot5.draw(screen,(0,0,0))

        pygame.display.flip()
def odczyt_lobby(screen):                           #funkcja odpowiedzialna za wybor zapisu gry do wczytania analogiczna do lobby()
    motorolla_jest_lepsza_od_nokii=True
    plik1=open("ZapisaneGry/Zapis1.txt", "r")            #odczytujemy wyniki, zeby wypisac odpowiedni text na przyciskach
    plik2=open("ZapisaneGry/Zapis2.txt", "r")
    plik3=open("ZapisaneGry/Zapis3.txt", "r")
    plik4=open("ZapisaneGry/Zapis4.txt", "r")
    plik5=open("ZapisaneGry/Zapis5.txt", "r")
    linie_plik1=plik1.readlines()
    if(len(linie_plik1)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis1.txt")
        Slot1=button((0,255,0),100,50,1400,150,"Score: "+str(int(score))+" "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot1=True
    else:
        Slot1=button((255,0,0),100,50,1400,150,"Wolny slot")
        Czy_slot1=False
    linie_plik2=plik2.readlines()
    if(len(linie_plik2)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis2.txt")
        Slot2=button((0,255,0),100,225,1400,150,"Score: "+str(int(score))+", "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot2=True
    else:
        Slot2=button((255,0,0),100,225,1400,150,"Wolny slot")
        Czy_slot2=False
    linie_plik3=plik3.readlines()
    if(len(linie_plik3)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis3.txt")
        Slot3=button((0,255,0),100,400,1400,150,"Score: "+str(int(score))+" "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot3=True
    else:
        Slot3=button((255,0,0),100,400,1400,150,"Wolny slot")
        Czy_slot3=False
    linie_plik4=plik4.readlines()
    if(len(linie_plik4)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis4.txt")
        Slot4=button((0,255,0),100,575,1400,150,"Score: "+str(int(score))+", "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot4=True
    else:
        Slot4=button((255,0,0),100,575,1400,150,"Wolny slot")
        Czy_slot4=False
    linie_plik5=plik5.readlines()
    if(len(linie_plik5)>2):
        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis5.txt")
        Slot5=button((0,255,0),100,750,1400,150,"Score: "+str(int(score))+" "+str(tryb)+", mapa: "+str(mapa))
        Czy_slot5=True
    else:
        Slot5=button((255,0,0),100,750,1400,150,"Wolny slot")
        Czy_slot5=False
    plik1.close()
    plik2.close()
    plik3.close()
    plik4.close()
    plik5.close()
    kosz1=button((0,0,0),1510,100,50,50)
    kosz2=button((0,0,0),1510,275,50,50)
    kosz3=button((0,0,0),1510,450,50,50)
    kosz4=button((0,0,0),1510,625,50,50)
    kosz5=button((0,0,0),1510,800,50,50)
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(Slot1.isOver(pos)):
                    if(Czy_slot1):
                        motorolla_jest_lepsza_od_nokii=False
                        pygame.mixer.music.stop()
                        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis1.txt")
                        gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                if(Slot2.isOver(pos)):
                    if(Czy_slot2):
                        pygame.mixer.music.stop()
                        motorolla_jest_lepsza_od_nokii=False
                        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis2.txt")
                        gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                if(Slot3.isOver(pos)):
                    if(Czy_slot3):
                        pygame.mixer.music.stop()
                        motorolla_jest_lepsza_od_nokii=False
                        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis3.txt")
                        gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                if(Slot4.isOver(pos)):
                    if(Czy_slot4):
                        pygame.mixer.music.stop()
                        motorolla_jest_lepsza_od_nokii=False
                        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis4.txt")
                        gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                if(Slot5.isOver(pos)):
                    if(Czy_slot5):
                        pygame.mixer.music.stop()
                        motorolla_jest_lepsza_od_nokii=False
                        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("ZapisaneGry\Zapis5.txt")
                        gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                if(kosz1.isOver(pos)):
                    plik=open("ZapisaneGry/Zapis1.txt", "w")
                    plik.close()
                    odczyt_lobby(screen)
                if(kosz2.isOver(pos)):
                    plik=open("ZapisaneGry/Zapis2.txt", "w")
                    plik.close()
                    odczyt_lobby(screen)
                if(kosz3.isOver(pos)):
                    plik=open("ZapisaneGry/Zapis3.txt", "w")
                    plik.close()
                    odczyt_lobby(screen)
                if(kosz4.isOver(pos)):
                    plik=open("ZapisaneGry/Zapis4.txt", "w")
                    plik.close()
                    odczyt_lobby(screen)
                if(kosz5.isOver(pos)):
                    plik=open("ZapisaneGry/Zapis5.txt", "w")
                    plik.close()
                    odczyt_lobby(screen)
            if event.type == pygame.MOUSEMOTION:
                if Slot1.isOver(pos):
                    Slot1.color=(0,0,255)
                else:
                    if(Czy_slot1):
                        Slot1.color=(0,255,0)
                    else:
                        Slot1.color=(255,0,0)
                if Slot2.isOver(pos):
                    Slot2.color=(0,0,255)
                else:
                    if(Czy_slot2):
                        Slot2.color=(0,255,0)
                    else:
                        Slot2.color=(255,0,0)
                if Slot3.isOver(pos):
                    Slot3.color=(0,0,255)
                else:
                    if(Czy_slot3):
                        Slot3.color=(0,255,0)
                    else:
                        Slot3.color=(255,0,0)
                if Slot4.isOver(pos):
                    Slot4.color=(0,0,255)
                else:
                    if(Czy_slot4):
                        Slot4.color=(0,255,0)
                    else:
                        Slot4.color=(255,0,0)
                if Slot5.isOver(pos):
                    Slot5.color=(0,0,255)
                else:
                    if(Czy_slot5):
                        Slot5.color=(0,255,0)
                    else:
                        Slot5.color=(255,0,0)




        screen.blit(tlogra,(0,0))
        Slot1.draw(screen,(0,0,0))
        Slot2.draw(screen,(0,0,0))
        Slot3.draw(screen,(0,0,0))
        Slot4.draw(screen,(0,0,0))
        Slot5.draw(screen,(0,0,0))
        screen.blit(kosz,(1510,100))
        screen.blit(kosz,(1510,275))
        screen.blit(kosz,(1510,450))
        screen.blit(kosz,(1510,625))
        screen.blit(kosz,(1510,800))

        pygame.display.flip()

def wypisz_ranking(screen,linie):                           #funkcja odpowiedzialna za wypisywanie rankingu na ekranie
    motorolla_jest_lepsza_od_nokii=True
    while motorolla_jest_lepsza_od_nokii:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(tlogra,(0,0))
        for x in range(len(linie)):
            Wypisz(600,100+x*80,screen,linie[x].rstrip())                   # wypisujemy wyniki
        pygame.display.flip()
def panel_przerwy(screen):                          #funkcja odpowiedzialna za wypisywanie panelu przerwy po zakonczeniu poziomu dzialanie analogiczne do lobby()
    motorolla_jest_lepsza_od_nokii=True
    przycisk_kontynuuj=button((0,255,0),180,150,300,100,"Kontynnuj")                    #tworze przyciski
    przycisk_zapisz=button((0,255,0),180,300,300,100,"Zapisz")
    przycisk_wroc_do_menu=button((0,255,0),180,450,300,100,"Wróć do menu")
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(przycisk_kontynuuj.isOver(pos)):
                    return "kontynuuj"
                if(przycisk_zapisz.isOver(pos)):
                    return "zapis"
                if(przycisk_wroc_do_menu.isOver(pos)):
                    return "koniec gry"
            if event.type == pygame.MOUSEMOTION:
                if przycisk_kontynuuj.isOver(pos):
                    przycisk_kontynuuj.color=(255,0,0)
                else:
                    przycisk_kontynuuj.color=(0,255,0)
                if przycisk_zapisz.isOver(pos):
                    przycisk_zapisz.color=(255,0,0)
                else:
                    przycisk_zapisz.color=(0,255,0)
                if przycisk_wroc_do_menu.isOver(pos):
                    przycisk_wroc_do_menu.color=(255,0,0)
                else:
                    przycisk_wroc_do_menu.color=(0,255,0)

        screen.blit(tlolobby,(0,0))
        przycisk_kontynuuj.draw(screen,(0,0,255))
        przycisk_zapisz.draw(screen,(0,0,255))
        przycisk_wroc_do_menu.draw(screen,(0,0,255))
        pygame.display.flip()
def ranking_lobby(screen):                                                  #funkcja odpowiedzialna za wypisywanie menu rankinow dzialanie analogiczne do lobby()
    motorolla_jest_lepsza_od_nokii=True
    przycisk_module1=button((0,255,0),250,150,350,100,"Tryb Losowy")
    przycisk_module2=button((0,255,0),250,300,350,100,"Kampania")
    przycisk_module3=button((0,255,0),220,450,410,100,"Poziomy Specjalne")
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(przycisk_module1.isOver(pos)):
                    plik=open("rankingi/Ranking1.txt", "r")
                    linie=plik.readlines()
                    plik.close()
                    wypisz_ranking(screen,linie)
                if(przycisk_module2.isOver(pos)):
                    plik=open("rankingi/Ranking2.txt", "r")
                    linie=plik.readlines()
                    plik.close()
                    wypisz_ranking(screen,linie)
                if(przycisk_module3.isOver(pos)):
                    plik=open("rankingi/Ranking3.txt", "r")
                    linie=plik.readlines()
                    plik.close()
                    wypisz_ranking(screen,linie)
            if event.type == pygame.MOUSEMOTION:
                if przycisk_module1.isOver(pos):
                    przycisk_module1.color=(255,0,0)
                else:
                    przycisk_module1.color=(0,255,0)
                if przycisk_module2.isOver(pos):
                    przycisk_module2.color=(255,0,0)
                else:
                    przycisk_module2.color=(0,255,0)
                if przycisk_module3.isOver(pos):
                    przycisk_module3.color=(255,0,0)
                else:
                    przycisk_module3.color=(0,255,0)

        screen.blit(tlolobby,(0,0))
        przycisk_module1.draw(screen,(0,0,255))
        przycisk_module2.draw(screen,(0,0,255))
        przycisk_module3.draw(screen,(0,0,255))
        pygame.display.flip()
def Wygrana(screen,score,tryb):                                             #ekran wypisywany w wypadku wygranej. dzialanie analogiczne do lobby()
    motorolla_jest_lepsza_od_nokii=True
    przycisk_lobby=button((0,255,0),325,600,250,100,"Lobby")
    przycisk_ranking=button((0,255,0),900,600,400,100,"Zobacz Ranking")
    wygranatlo=pygame.image.load("Grafika\\wygranatlo.png").convert_alpha()
    wygranatlo=pygame.transform.scale(wygranatlo,(1600,900))
    if(tryb=="modul 1"):                        #jesli wynik kwalifikuje sie do rankingu, to zapisujemy go w rankingu
        plik=open("rankingi/Ranking1.txt", "r")
        linie=plik.readlines()
        plik.close()
    if(tryb=="modul 2"):
        plik=open("rankingi/Ranking2.txt", "r")
        linie=plik.readlines()
        plik.close()
    if(tryb=="modul 3"):
        plik=open("rankingi/Ranking3.txt", "r")
        linie=plik.readlines()
        plik.close()

    wyniki=[]
    for x in linie:
        a=x.split(" ")
        a[2]=int(a[2])
        wyniki.append((a[1],a[2]))
    if(score>wyniki[len(wyniki)-1][1]):
        nowe_wyniki=dodaj_rekord(screen,score,wyniki)
        if(tryb=="modul 1"):
            plik=open("rankingi/Ranking1.txt", "w")

        if(tryb=="modul 2"):
            plik=open("rankingi/Ranking2.txt", "w")

        if(tryb=="modul 3"):
            plik=open("rankingi/Ranking3.txt", "w")
        for x in range(len(nowe_wyniki)-1):
            plik.write(str(x+1)+". "+nowe_wyniki[x][0]+" "+str(int(nowe_wyniki[x][1]))+"\n")
        plik.close()
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(przycisk_lobby.isOver(pos)):
                    lobby(screen)
                if(przycisk_ranking.isOver(pos)):
                    if(tryb=="modul 1"):
                        plik=open("rankingi/Ranking1.txt", "r")
                        linie=plik.readlines()
                        plik.close()
                        wypisz_ranking(screen,linie)
                    if(tryb=="modul 2"):
                        plik=open("rankingi/Ranking2.txt", "r")
                        linie=plik.readlines()
                        plik.close()
                        wypisz_ranking(screen,linie)
                    if(tryb=="modul 3"):
                        plik=open("rankingi/Ranking3.txt", "r")
                        linie=plik.readlines()
                        plik.close()
                        wypisz_ranking(screen,linie)
            if event.type == pygame.MOUSEMOTION:
                if przycisk_lobby.isOver(pos):
                    przycisk_lobby.color=(255,0,0)
                else:
                    przycisk_lobby.color=(0,255,0)
                if przycisk_ranking.isOver(pos):
                    przycisk_ranking.color=(255,0,0)
                else:
                    przycisk_ranking.color=(0,255,0)
        screen.blit(wygranatlo,(0,0))
        Wypisz(700,500,screen,"Wynik: "+str(int(score)))

        przycisk_lobby.draw(screen,(0,0,255))
        przycisk_ranking.draw(screen,(0,0,255))
        pygame.display.flip()
def Przegrana(screen,score,tryb):               #ekran wypisywany w wypadku przegranej. dzialanie analogiczne do lobby()
    motorolla_jest_lepsza_od_nokii=True
    przegranatlo=pygame.image.load("Grafika\\przegranatlo.png").convert_alpha()
    przegranatlo=pygame.transform.scale(przegranatlo,(1600,900))
    przycisk_lobby=button((0,255,0),325,600,250,100,"Lobby")
    przycisk_ranking=button((0,255,0),900,600,400,100,"Zobacz Ranking")
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(przycisk_lobby.isOver(pos)):
                    lobby(screen)
                if(przycisk_ranking.isOver(pos)):
                    if(tryb=="modul 1"):
                        plik=open("rankingi/Ranking1.txt", "r")
                        linie=plik.readlines()
                        plik.close()
                        wypisz_ranking(screen,linie)
                    if(tryb=="modul 2"):
                        plik=open("rankingi/Ranking2.txt", "r")
                        linie=plik.readlines()
                        plik.close()
                        wypisz_ranking(screen,linie)
                    if(tryb=="modul 3"):
                        plik=open("rankingi/Ranking3.txt", "r")
                        linie=plik.readlines()
                        plik.close()
                        wypisz_ranking(screen,linie)
            if event.type == pygame.MOUSEMOTION:
                if przycisk_lobby.isOver(pos):
                    przycisk_lobby.color=(255,0,0)
                else:
                    przycisk_lobby.color=(0,255,0)
                if przycisk_ranking.isOver(pos):
                    przycisk_ranking.color=(255,0,0)
                else:
                    przycisk_ranking.color=(0,255,0)
        screen.blit(przegranatlo,(0,0))
        Wypisz(700,500,screen,"Wynik: "+str(int(score)))
        przycisk_lobby.draw(screen,(0,0,255))
        przycisk_ranking.draw(screen,(0,0,255))
        pygame.display.flip()
def dodaj_rekord(screen,score,wyniki):                      #funkcja odpowiedzialna za pobranie nicku, oraz dodanie go do listy rekordow
    motorolla_jest_lepsza_od_nokii=True

    user_text = ''
    input_rect = pygame.Rect(650, 200, 300, 32)

    color = pygame.Color('white')
    text_1=base_font.render("Podaj swoj nick",True,(255,255,255))
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key== pygame.K_RETURN:         #enter konczy wpisywanie
                    motorolla_jest_lepsza_od_nokii=False
                #jesli wcisniety backspace, usuwamy ostani znak
                if event.key == pygame.K_BACKSPACE:

                    user_text = user_text[:-1]
                else:
                    if len(user_text)<20:
                        user_text += event.unicode                  #dodaje nacisniety klawisz do nazwy
        screen.fill((0, 0, 0))


        pygame.draw.rect(screen, color, input_rect)                             #rysuje pole do wpisywania
        screen.blit(text_1,(650,150))
        text_surface = base_font.render(user_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))                     #wypisuje już wprowadzony text
        pygame.display.flip()
    user_text=user_text.replace(" ","_")
    wyniki.append((user_text.rstrip(),score))
    l = len(wyniki)                                        #zwykly bubblesort
    for i in range(l-1):
        for j in range(0, l-i-1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if wyniki[j][1] > wyniki[j + 1][1] :
                wyniki[j], wyniki[j + 1] = wyniki[j + 1], wyniki[j]
    wyniki.reverse()
    return wyniki
def gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow): #ta funckja jest odpowiedzialna za gameplay
    pygame.mixer.music.load('Grafika\muzykagra.mp3')
    KulaSpeed=5
    KulaSpeedX=1
    GraczSpeed=5
    PociskSpeed=10
    Drabiny_render=pygame.sprite.Group() #tworzenie grup, żeby mozna bylo pokazac duszki
    Drabiny_render.add(Drabiny)

    Kula_render=pygame.sprite.RenderUpdates()

    Prostokat_render=pygame.sprite.Group()
    Prostokat_render.add(Prostokaty)

    Gracz_render=pygame.sprite.Group()
    Gracz_render.add(gracz)

    Pociski_render=pygame.sprite.Group()
    laser_time=0


    Bomby_render=pygame.sprite.Group()

    laser=Laser(gracz.x,0,gracz.y)              #tworzenie lasera
    Laser_render=pygame.sprite.Group()
    Laser_render.add(laser)

    Lody_render=pygame.sprite.Group()
    Lody_render.add(Lody)
    PociskiShotgun_render=pygame.sprite.Group()
    clock = pygame.time.Clock()

    Kolce_render=pygame.sprite.Group()
    Kolce_render.add(Kolce)

    Artefakty_render=pygame.sprite.Group()
    attack_type="pociski"
    czy_laser=False
    zmianapowyjsciu=0
    start=timer()
    petla=True
    strzal=False
    pygame.mixer.music.play(-1)
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        gracz.changeX-=GraczSpeed
    if keys[pygame.K_RIGHT]:
        gracz.changeX+=GraczSpeed
    while(serca>0 and len(Kule)>0 and petla):
        czynalodzie=False
        for lod in Lody:                                        #for sprawdzajacy czy gracz jest na lodzie
            if(pygame.sprite.collide_rect(lod,gracz)):
                czynalodzie=True
        if(not(czynalodzie)):
            gracz.changeX+=zmianapowyjsciu
            if(zmianapowyjsciu!=0):
                gracz.x+=zmianapowyjsciu*(-1)
            zmianapowyjsciu=0
        for event in pygame.event.get():                        #for sprawdzający klawisze naciskane przez gracza
            if event.type==pygame.QUIT:                         #zamykanie okna jesli wcisniety x
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_LEFT:
                        czynalodzie=False
                        for lod in Lody:
                            if(pygame.sprite.collide_rect(lod,gracz)):
                                czynalodzie=True
                        if(czynalodzie):

                            zmianapowyjsciu-=5
                        else:
                            gracz.changeX-=GraczSpeed
                    if event.key == pygame.K_RIGHT:
                        czynalodzie=False
                        for lod in Lody:
                            if(pygame.sprite.collide_rect(lod,gracz)):
                                czynalodzie=True
                        if(czynalodzie):
                            zmianapowyjsciu+=5
                        else:

                            gracz.changeX+=GraczSpeed
                    if event.key == pygame.K_UP:

                            gracz.changeY-=GraczSpeed
                    if event.key == pygame.K_DOWN:
                        gracz.changeY+=GraczSpeed
                    if event.key == pygame.K_q:
                        attack_type="pociski"
                    if event.key == pygame.K_w:
                        attack_type="laser"
                    if event.key == pygame.K_e:
                        attack_type="bomba"
                    if event.key == pygame.K_r:
                        attack_type="shotgun"
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        pauza=panel_przerwy(screen)
                        if keys[pygame.K_LEFT]:
                            gracz.changeX-=GraczSpeed
                        if keys[pygame.K_RIGHT]:
                            gracz.changeX+=GraczSpeed
                        if(not(keys[pygame.K_LEFT]) and not(keys[pygame.K_RIGHT])):
                            gracz.changeX=0
                        if(pauza=="zapis"):
                            zapis_lobby(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                        if(pauza=="koniec gry"):
                            petla=False
                        pygame.mixer.music.play(-1)
                    if event.key == pygame.K_SPACE:                     # jesli spacja, wystrzel pocisk

                        if(gracz.changeY==0):           #if ktory nie pozwala skakac na drabinach
                            if attack_type=="pociski":
                                if(amunicja_pocisk>=1):
                                    Pociski.append(Pocisk(gracz.x,gracz.y))
                                    amunicja_pocisk-=1
                                    strzal=True
                            if attack_type=="laser":
                                if(amunicja_laser>=1 and laser_time<0):
                                    amunicja_laser-=1
                                    laser_time=120
                                    strzal=True
                            if attack_type=="bomba":
                                if(amunicja_bomba>=1 and len(Bomby)==0):
                                    Bomby.append(Bomba(gracz.x,gracz.y,240))
                                    amunicja_bomba-=1
                                    strzal=True
                            if attack_type=="shotgun":
                                if(amunicja_shotgun>0):
                                    strzal=True
                                    PociskiShotgun.append(PociskShotgun(gracz.x,gracz.y,3))
                                    PociskiShotgun.append(PociskShotgun(gracz.x,gracz.y,1))
                                    PociskiShotgun.append(PociskShotgun(gracz.x,gracz.y,-1))
                                    PociskiShotgun.append(PociskShotgun(gracz.x,gracz.y,-3))
                                    amunicja_shotgun-=1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:

                    if(czynalodzie):
                        zmianapowyjsciu+=5
                    else:

                        gracz.changeX+=GraczSpeed
                if event.key == pygame.K_RIGHT:
                    czynalodzie=False
                    for lod in Lody:
                        if(pygame.sprite.collide_mask(lod,gracz)):
                            czynalodzie=True
                    if(czynalodzie):

                        zmianapowyjsciu-=5
                    else:

                        gracz.changeX-=GraczSpeed
                if event.key == pygame.K_UP:
                    gracz.changeY+=GraczSpeed
                if event.key == pygame.K_DOWN:
                    gracz.changeY-=GraczSpeed
        for kolec in Kolce:                                 #for sprawdzajcy czy gracz na kolcu, oraz czy kolec nie powienien zostac zniszczony
            if(pygame.sprite.collide_rect(kolec,gracz) and immortal<0):
                serca-=1
                immortal=120*2
            for bomba in Bomby:
                if(pygame.sprite.collide_rect(kolec,bomba) and bomba.czas<0):
                    kolec.kill()
                    Kolce.remove(kolec)

        for kula in Kule:           #for przesuwajacy kule
            kula.move()
            kula.immortal-=1
        for kula in Kule:              #for sprawdzający odbicia
            for Prostokat in Prostokaty:
                kula.changeX,Kula.changeY=zderzenie(kula,Prostokat)
        for kula in Kule:               #for sprawczający czy kula nie uderza w gracza
            if pygame.sprite.collide_mask(kula,gracz) and immortal<0:
                immortal=120*2
                serca-=1
        for pocisk in Pociski:              #for przesuwajacy pociski
            pocisk.move()
        for pocisk in Pociski:                  #for ktory sprawdza czy pocisk trafil w kule
            for kula in Kule:
                if(pygame.sprite.collide_rect(kula,pocisk) and kula.immortal<0):
                    if(kula.r>8):
                        Kule.append(Kula(kula.x,kula.y,kula.r/2,kula.changeX/1.5,kula.changeY,60))
                        Kule.append(Kula(kula.x,kula.y,kula.r/2,0-kula.changeX/1.5,kula.changeY,60))
                    score+=kula.r
                    Kule.remove(kula)
                    kula.kill()

                    Pociski.remove(pocisk)
                    pocisk.kill()
                    break
        for pocisk in Pociski:                      #for ktory sprawdza czy pocisk trafil w artefakt
            for artefakt in Artefakty:
                if(pygame.sprite.collide_rect(artefakt,pocisk) and artefakt.ScoreWhenStart<score):
                    if(artefakt.typ=="serce"):
                        serca+=1
                    if(artefakt.typ=="amunicja"):
                        amunicja_pocisk=amunicja_pocisk*2
                    if(artefakt.typ=="speed"):
                        GraczSpeed=GraczSpeed*2
                        gracz.changeX=gracz.changeX*2
                        gracz.changeY=gracz.changeY*2
                    Artefakty.remove(artefakt)
                    artefakt.kill()
                    Pociski.remove(pocisk)
                    pocisk.kill()

        for pocisk in Pociski:                          #for ktory sprawdza czy pocisk trafil w prostokat
            for prostokat in Prostokaty:
                if(pygame.sprite.collide_rect(pocisk,prostokat)):
                    pocisk.kill()
                    Pociski.remove(pocisk)
                    if(prostokat.hp<100000):
                        prostokat.hp-=100
                    break
        for pocisk in Pociski:                      #for ktory sprawdza czy pocisk wyszedl za mape
            if(pocisk.y<0):
                pocisk.kill()
                Pociski.remove(pocisk)

        if(laser_time>0):
            for prstk in Prostokaty:                    #for sprawdzajacy czy laser nie "pali" prostokata
                if(pygame.sprite.collide_rect(laser,prstk)):
                    if(prstk.hp<100000):
                        prstk.hp-=1
            for kula in Kule:                            #for sprawdzajacy czy laser nie "pali" kuli
                if(pygame.sprite.collide_rect(kula,laser) and kula.immortal<0):
                    if(kula.r>8):
                        Kule.append(Kula(kula.x,kula.y,kula.r/2,kula.changeX/1.5,kula.changeY,60))
                        Kule.append(Kula(kula.x,kula.y,kula.r/2,0-kula.changeX/1.5,kula.changeY,60))
                    score+=kula.r
                    Kule.remove(kula)
                    kula.kill()
            for artefakt in Artefakty:                    #for sprawdzajacy czy laser nie "pali" artefaktu
                if(pygame.sprite.collide_rect(laser,artefakt) and artefakt.ScoreWhenStart<score):
                    if(artefakt.typ=="serce"):
                        serca+=1
                    if(artefakt.typ=="amunicja"):
                        amunicja_pocisk=amunicja_pocisk*2
                    if(artefakt.typ=="speed"):
                        GraczSpeed=GraczSpeed*2
                        gracz.changeX=gracz.changeX*2
                        gracz.changeY=gracz.changeY*2
                    Artefakty.remove(artefakt)
                    artefakt.kill()
        for bomba in Bomby:                                             #for odpowiedzalny za wybuchanie bomb, i sprawdzanie czy kule nie wybuchly gracza lub kuli
            bomba.czas-=1
            if bomba.czas<0:
                for kula in Kule:
                    if(pygame.sprite.collide_rect(bomba,kula) and kula.immortal<0):
                        if(kula.r>8):
                            Kule.append(Kula(kula.x,kula.y,kula.r/2,kula.changeX/1.5,kula.changeY,60))
                            Kule.append(Kula(kula.x,kula.y,kula.r/2,0-kula.changeX/1.5,kula.changeY,60))
                        score+=kula.r
                        Kule.remove(kula)
                        kula.kill()

                if(pygame.sprite.collide_rect(bomba,gracz) and immortal<0):

                    serca-=1
                    immortal=240
                bomba.wybuch(-bomba.czas)

                                                    #for sprawdzajacy czy bomby wybuchaja artefakty lub prostokaty
                for artefakt in Artefakty:
                    if(pygame.sprite.collide_rect(bomba,artefakt) and artefakt.ScoreWhenStart<score):
                        if(artefakt.typ=="serce"):
                            serca+=1
                        if(artefakt.typ=="amunicja"):
                            amunicja_pocisk=amunicja_pocisk*2
                        if(artefakt.typ=="speed"):
                            GraczSpeed=GraczSpeed*2
                            gracz.changeX=gracz.changeX*2
                            gracz.changeY=gracz.changeY*2
                        Artefakty.remove(artefakt)
                        artefakt.kill()
                for prstk in Prostokaty:
                    if(pygame.sprite.collide_rect(bomba,prstk)):
                        if(prstk.hp<100000):
                            prstk.hp-=500
        for bomba in Bomby:
            if(bomba.czas<-60):
                Bomby.remove(bomba)
                bomba.kill()
        for pociskshotgun in PociskiShotgun:                #for odpowiedzialny za poruszanie pociskow od shotguna, i wybuchanie kulek
            pociskshotgun.move()
            for kula in Kule:
                if(pygame.sprite.collide_rect(pociskshotgun,kula) and kula.immortal<0):
                    if(kula.r>8):
                        Kule.append(Kula(kula.x,kula.y,kula.r/2,kula.changeX/1.5,kula.changeY,60))
                        Kule.append(Kula(kula.x,kula.y,kula.r/2,0-kula.changeX/1.5,kula.changeY,60))
                    score+=kula.r
                    Kule.remove(kula)
                    kula.kill()
                    PociskiShotgun.remove(pociskshotgun)
                    pociskshotgun.kill()
                    break
        for pociskshotgun in PociskiShotgun:                #for odpowiedzialny za usuwanie pociskow do shotgunow
            for prstk in Prostokaty:
                if(pygame.sprite.collide_rect(pociskshotgun,prstk)):
                    if(prstk.hp<100000):
                        prstk.hp-=100
                    PociskiShotgun.remove(pociskshotgun)
                    pociskshotgun.kill()
        for pociskishotgun in PociskiShotgun:               #for odpowiedzialny za trafianie w artefakty
            for artefakt in Artefakty:
                if(pygame.sprite.collide_rect(pociskishotgun,artefakt) and artefakt.ScoreWhenStart<score):
                    if(artefakt.typ=="serce"):
                        serca+=1
                    if(artefakt.typ=="amunicja"):
                        amunicja_pocisk=amunicja_pocisk*2
                    if(artefakt.typ=="speed"):
                        GraczSpeed=GraczSpeed*2
                        gracz.changeX=gracz.changeX*2
                        gracz.changeY=gracz.changeY*2
                    Artefakty.remove(artefakt)
                    artefakt.kill()
        for pociskshotgun in PociskiShotgun:
            if(pociskshotgun.y<0):                      #usuwam pociski poza mapą
                pociskshotgun.kill()
                PociskiShotgun.remove(pociskshotgun)
        for prostokat in Prostokaty:                        #usuwam zniszczone prostokaty
            if(prostokat.hp<0):

                prostokat.kill()
                Prostokaty.remove(prostokat)

        for lod in Lody:                        # usuwam Lod z rozwalonych prostokatow
            podstawalod=False
            for prstk in Prostokaty:
                if(pygame.sprite.collide_mask(lod,prstk)):
                    podstawalod=True
            if(not(podstawalod)):
                Lody.remove(lod)
                lod.kill()
        screen.blit(tlogra,(0,0))                           #rysuje tlo
        Drabiny_render.draw(screen)                     #rysuje drabiny


        Prostokat_render.draw(screen)                   #rysuje prostkaty
        Kolce_render.draw(screen)                       #rysuje kolce
        gracz.move(Prostokaty,Drabiny,GraczSpeed)               #poruszam gracza
        for artefakt in Artefakty:                          #pokazuje artefakty
            if(artefakt.ScoreWhenStart<score):
                Artefakty_render.add(artefakt)
        Artefakty_render.draw(screen)                       #rysuje artefakty

        if(laser_time>0):                                   #rysuje laser
            laser.move(Prostokaty,gracz)
            Laser_render.draw(screen)
        strzal=gracz.draw(immortal,attack_type,laser_time,strzal)                   #zmieniam skina gracza
        Gracz_render.draw(screen)                           #rysuje gracza
        Gracz_render.update()

        Pociski_render.add(Pociski)
        Pociski_render.draw(screen)                     #rysuje pociski

        PociskiShotgun_render.add(PociskiShotgun)                   #rysuje pociski do shotguna
        PociskiShotgun_render.draw(screen)

        Bomby_render.add(Bomby)                             #rysuje bomby
        Bomby_render.draw(screen)

        Kula_render.remove(Kule)
        Kula_render.add(Kule)
        Kula_render.draw(screen)                    #rysuje kule

        Lody_render.draw(screen)                            #rysuje lod

        WypiszSerca(screen,serca)                       # wypisuje hp

        if(attack_type=="pociski"):                         #wypisuje amunicje
            WypiszAmunicje(screen,amunicja_pocisk)
        elif(attack_type=="laser"):
            WypiszAmunicje(screen,amunicja_laser)
        elif(attack_type=="bomba"):
            WypiszAmunicje(screen,amunicja_bomba)
        elif(attack_type=="shotgun"):
            WypiszAmunicje(screen,amunicja_shotgun)
        Wypisz(1500-len(str(int(score)))*10,0,screen,"Wynik "+str(int(score)))              #wypisuje wynik
        if(attack_type=="pociski"):                                                             #elif odpowiedzalny za pokazywanie broni z lewej strony
            screen.blit(pistoletDuzy,(0,300))
        else:
            screen.blit(pistolet,(0,300))
        if(attack_type=="laser"):
            screen.blit(laserBronDuza,(0,400))
        else:
            screen.blit(laserBron,(0,400))
        if(attack_type=="bomba"):
            screen.blit(BombaDuza,(0,500))
        else:
            screen.blit(BombaMala,(0,500))
        if(attack_type=="shotgun"):
            screen.blit(StrzelbaDuza,(0,600))
        else:
            screen.blit(StrzelbaMala,(0,600))

        pygame.display.flip()                               #update ekranu
        clock.tick(90)                                       #ustawienie liczby klatek na sekunde
        amunicja_pocisk+=0.002                          #dodwanie amunicji
        amunicja_laser+=0.0005
        amunicja_bomba+=0.0005
        amunicja_shotgun+=0.002
        laser_time-=1
        immortal-=1
    pygame.mixer.music.stop()
    end=timer()
    time=end-start
    score=(score*1000/time)*score/max_score     #licze punkty, w zależnosci od czasu
    sumapunktow+=score
    if(tryb=="modul 2"):            #elif odpowiedzalny za rozpaczecie nastepnego poziomu, lub wypisanie wyniku
        if(len(Kule)==0):
            if(mapa!=15):
                sumapunktow+=score
                wybor=panel_przerwy(screen)
                if(wybor=="kontynuuj"):
                    sciezka="poziomymodul2\poziom"+str(mapa+1)+".txt"
                    Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow1=odczyt(sciezka)
                    gra(screen,Kule1,Drabiny1,Prostokaty1,Pociski1,Bomby1,PociskiShotgun1,Artefakty1,gracz1,amunicja_pocisk1,amunicja_laser1,amunicja_bomba1,amunicja_shotgun1,score1,serca1,immortal1,Lody1,Kolce1,max_score1,tryb1,mapa1,sumapunktow)
                elif(wybor=="zapis"):
                    zapis_lobby(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
            else:
                Wygrana(screen, sumapunktow, tryb)
        else:
            Przegrana(screen, sumapunktow, tryb)

    elif(tryb=="modul 3"):
        if(len(Kule)==0):
            Wygrana(screen, score, tryb)
        else:
            Przegrana(screen, score, tryb)
    elif(tryb=="modul 1"):
        if(len(Kule)==0):
            Wygrana(screen, score, tryb)
        else:
            Przegrana(screen, score, tryb)
def lobby(screen):                          #funkcja ktora pokazuje lob
    pygame.mixer.music.load('Grafika\\lobby.mp3')
    pygame.mixer.music.play(-1)
    motorolla_jest_lepsza_od_nokii=True
    Nowa_gra=False
    Zapis_gry=False
    przycisk_module1=button((0,255,0),220,100,400,100,"Tryb Losowy")                    #tworze przyciski
    przycisk_module2=button((0,255,0),220,250,400,100,"Kampania")
    przycisk_module3=button((0,255,0),220,400,400,100,"Poziomy Specjalne")
    przycisk_wczytaj=button((0,255,0), 220,550,400,100,"Odczyt poziomu")
    przycisk_rankingi=button((0,255,0), 220,700,400,100,"Rankingi")
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(przycisk_module1.isOver(pos)):                           #sprawdzam czy naciskam przycisk

                    lobbymodul1(screen)
                if(przycisk_module2.isOver(pos)):

                    lobbymodul2(screen)
                if(przycisk_module3.isOver(pos)):

                    lobbymodul3(screen)
                if(przycisk_wczytaj.isOver(pos)):

                    odczyt_lobby(screen)
                if(przycisk_rankingi.isOver(pos)):

                    ranking_lobby(screen)
            if event.type == pygame.MOUSEMOTION:
                if przycisk_module1.isOver(pos):                                       #zmieniam kolor pociskow, jesli jest nad nimi kursor
                    przycisk_module1.color=(255,0,0)
                else:
                    przycisk_module1.color=(0,255,0)
                if przycisk_module2.isOver(pos):
                    przycisk_module2.color=(255,0,0)
                else:
                    przycisk_module2.color=(0,255,0)
                if przycisk_module3.isOver(pos):
                    przycisk_module3.color=(255,0,0)
                else:
                    przycisk_module3.color=(0,255,0)
                if przycisk_wczytaj.isOver(pos):
                    przycisk_wczytaj.color=(255,0,0)
                else:
                    przycisk_wczytaj.color=(0,255,0)
                if przycisk_rankingi.isOver(pos):
                    przycisk_rankingi.color=(255,0,0)
                else:
                    przycisk_rankingi.color=(0,255,0)

        screen.blit(tlolobby,(0,0))
        przycisk_module1.draw(screen,(0,0,0))             #rysuje przyciski
        przycisk_module2.draw(screen,(0,0,0))
        przycisk_module3.draw(screen,(0,0,0))
        przycisk_wczytaj.draw(screen,(0,0,0))
        przycisk_rankingi.draw(screen,(0,0,0))
        pygame.display.flip()
def lobbymodul1(screen):                                    #lobby modulu 1, dzialanie analogiczne do funkcji lobby()
    motorolla_jest_lepsza_od_nokii=True
    Nowa_gra=False
    Zapis_gry=False
    przycisklatwy=button((0,255,0),220,150,250,100,"Łatwy")                    #tworze przyciski
    przycisksredni=button((0,255,0),220,300,250,100,"Średni")
    przycisktrudny=button((0,255,0),220,450,250,100,"Trudny")
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if(przycisklatwy.isOver(pos)):
                    pygame.mixer.music.stop()
                    liczba=random.randint(1,5)
                    Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("poziomymodul1\poziom"+str(liczba)+'.txt')
                    gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                    motorolla_jest_lepsza_od_nokii=False
                if(przycisksredni.isOver(pos)):
                    pygame.mixer.music.stop()
                    liczba=random.randint(6,10)
                    Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("poziomymodul1\poziom"+str(liczba)+'.txt')
                    gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                    motorolla_jest_lepsza_od_nokii=False
                if(przycisktrudny.isOver(pos)):
                    pygame.mixer.music.stop()
                    liczba=random.randint(11,15)
                    Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("poziomymodul1\poziom"+str(liczba)+'.txt')
                    gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                    motorolla_jest_lepsza_od_nokii=False
            if event.type == pygame.MOUSEMOTION:
                if przycisklatwy.isOver(pos):
                    przycisklatwy.color=(255,0,0)
                else:
                    przycisklatwy.color=(0,255,0)
                if przycisksredni.isOver(pos):
                    przycisksredni.color=(255,0,0)
                else:
                    przycisksredni.color=(0,255,0)
                if przycisktrudny.isOver(pos):
                    przycisktrudny.color=(255,0,0)
                else:
                    przycisktrudny.color=(0,255,0)

        screen.blit(tlolobby,(0,0))
        przycisklatwy.draw(screen,(0,0,0))
        przycisksredni.draw(screen,(0,0,0))
        przycisktrudny.draw(screen,(0,0,0))
        pygame.display.flip()
def lobbymodul2(screen):                            #lobby modulu 2, dzialanie analogiczne do funkcji lobby()
    motorolla_jest_lepsza_od_nokii=True
    tlolobbymodul2=pygame.image.load("Grafika\_tlolobbymodule2.png")
    poziomy_przyciski=[]
    for x in range(15):
        if(x<5):
            kolor="green"
        elif(x<10):
            kolor="yellow"
        else:
            kolor="red"
        poziomy_przyciski.append(button((kolor),150+x%5*300,200+math.floor(x/5)*250,100,100,str(x+1)))
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(len(poziomy_przyciski)):
                    if(poziomy_przyciski[x].isOver(pos)):
                        pygame.mixer.music.stop()
                        sciezka="poziomymodul2\poziom"+str(x+1)+".txt"
                        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt(sciezka)
                        gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                        motorolla_jest_lepsza_od_nokii=False
            if event.type == pygame.MOUSEMOTION:
                for x in range(len(poziomy_przyciski)):
                    if(poziomy_przyciski[x].isOver(pos)):
                        poziomy_przyciski[x].color=(0,0,255)
                    else:
                        if(x<5):
                            kolor="green"
                        elif(x<10):
                            kolor="yellow"
                        else:
                            kolor="red"
                        poziomy_przyciski[x].color=kolor
        screen.blit(tlolobbymodul2,(0,0))
        for x in poziomy_przyciski:
            x.draw(screen,(0,0,0))

        pygame.display.flip()
def lobbymodul3(screen):                                                            #lobby modulu 3, dzialanie analogiczne do funkcji lobby()
    motorolla_jest_lepsza_od_nokii=True
    tlolobbymodul2=pygame.image.load("Grafika\_tlolobbymodule2.png")
    poziomy_przyciski=[]
    for x in range(5):
        kolor=(173, 29, 29)
        poziomy_przyciski.append(button((kolor),150+x%5*300,450,100,100,str(x+1)))
    while(motorolla_jest_lepsza_od_nokii):
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    lobby(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for x in range(len(poziomy_przyciski)):
                    if(poziomy_przyciski[x].isOver(pos)):
                        pygame.mixer.music.stop()
                        Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow=odczyt("poziomymodul3\poziom"+str(x+1)+'.txt')
                        gra(screen,Kule,Drabiny,Prostokaty,Pociski,Bomby,PociskiShotgun,Artefakty,gracz,amunicja_pocisk,amunicja_laser,amunicja_bomba,amunicja_shotgun,score,serca,immortal,Lody,Kolce,max_score,tryb,mapa,sumapunktow)
                        motorolla_jest_lepsza_od_nokii=False
            if event.type == pygame.MOUSEMOTION:
                for x in range(len(poziomy_przyciski)):
                    if(poziomy_przyciski[x].isOver(pos)):
                        poziomy_przyciski[x].color=(0,0,255)
                    else:
                        poziomy_przyciski[x].color=kolor
        screen.blit(tlolobbymodul2,(0,0))
        for x in poziomy_przyciski:
            x.draw(screen,(0,0,0))
        pygame.display.flip()
if __name__ == '__main__':          #glowny program, laduje grafiki, inicjuje silnik gry, wywoluje funkcje lobby() ktora zajmuje sie reszta
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    f = open("settings.txt", "r")
    fullscreen=f.readline()
    f.close()
    fullscreen,if_fullscreen = fullscreen.split("=")
    if(if_fullscreen=="1"):
        screen=pygame.display.set_mode((Screen_width,Screen_height),pygame.FULLSCREEN)
    else:
        screen=pygame.display.set_mode((Screen_width,Screen_height))
    tlogra=pygame.image.load('Grafika\\tlo.png').convert_alpha()
    koniecgry=pygame.image.load("Grafika\gameover.png").convert_alpha()
    wygrana=pygame.image.load("Grafika\wygrana.png").convert_alpha()
    tlolobby=pygame.image.load("Grafika\\tlolobby.png").convert_alpha()
    tlolobby=pygame.transform.scale(tlolobby,(1600,900))
    BombaDuza=pygame.transform.rotozoom(pygame.image.load(AdresSkinaBomby),0,1.5).convert_alpha()
    BombaMala=pygame.image.load(AdresSkinaBomby).convert_alpha()
    StrzelbaDuza=pygame.transform.rotozoom(pygame.image.load(PompaSkin),0,1.5).convert_alpha()
    StrzelbaMala=pygame.image.load(PompaSkin).convert_alpha()
    base_font = pygame.font.Font(None, 32)
    laserBron=pygame.image.load(LaserSkin).convert_alpha()
    laserBronDuza=pygame.transform.rotozoom(laserBron,0,(1.5)).convert_alpha()
    pistolet=pygame.image.load(PistoletSkin).convert_alpha()
    pistoletDuzy=pygame.transform.rotozoom(pistolet,0,(1.5)).convert_alpha()
    Serce=pygame.image.load("Grafika\serce.png").convert_alpha()
    Amunicja=pygame.image.load("Grafika\\amunicja.png").convert_alpha()
    kosz=pygame.image.load("Grafika\\kosz.png").convert_alpha()
    kosz=pygame.transform.scale(kosz,(50,50))
    wybuchy=[]
    wybuch1=pygame.image.load("Grafika\eksplozja 1.png").convert_alpha()
    wybuch2=pygame.image.load("Grafika\eksplozja 2.png").convert_alpha()
    wybuch3=pygame.image.load("Grafika\eksplozja 3.png").convert_alpha()


    i=0
    while(i<20):
        wybuchy.append(pygame.transform.scale(wybuch1,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch1,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch1,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch1,(i*3+64,i*3+64)).convert_alpha())
        i+=1
    while(i<40):
        wybuchy.append(pygame.transform.scale(wybuch2,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch2,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch2,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch2,(i*3+64,i*3+64)).convert_alpha())
        i+=1
    while(i<70):
        wybuchy.append(pygame.transform.scale(wybuch3,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch3,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch3,(i*3+64,i*3+64)).convert_alpha())
        i+=1
        wybuchy.append(pygame.transform.scale(wybuch3,(i*3+64,i*3+64)).convert_alpha())
        i+=1



    lobby(screen)




