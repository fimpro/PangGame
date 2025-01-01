from classes import *

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