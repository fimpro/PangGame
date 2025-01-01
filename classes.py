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