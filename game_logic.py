import main
import haravasto as har


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina, kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    har.tyhjaa_ikkuna()         
    har.piirra_tausta()     
    har.aloita_ruutujen_piirto()    
    kentta = main.tila["kentta"]             
    for rivi in range(0, len(kentta)):       
        for sarake in range(0, len(kentta[rivi])):
            if (sarake, rivi) in main.tila["liput_xy"]:
                x = sarake * main.ruutukoko
                y = rivi * main.ruutukoko
                har.lisaa_piirrettava_ruutu("f", x, y)
            else:
                avain = kentta[rivi][sarake]
                if avain == "x" and not main.tila["paattymistila"] == 0:
                    avain = " "
                x = sarake * main.ruutukoko
                y = rivi * main.ruutukoko
                har.lisaa_piirrettava_ruutu(avain, x, y)
    har.piirra_ruudut()
    
    
def laske_miinat(xPos, yPos, kentta):
    """
    Laskee annetussa huoneessa yhden ruudun ympärillä olevat miinat ja palauttaa
    niiden lukumäärän. Funktio toimii sillä oletuksella, että valitussa ruudussa ei
    ole miinaa - jos on, sekin lasketaan mukaan.
    """
    miinat_lkm = 0
    for y in range(3):
        for x in range(3):
            tarkistus_y = yPos + y - 1
            tarkistus_x = xPos + x - 1
            if tarkistus_x >= 0 and tarkistus_y >= 0:
                if tarkistus_x < len(kentta[0]) and tarkistus_y < len(kentta):
                    if kentta[tarkistus_y][tarkistus_x] == "x":
                        miinat_lkm += 1
            
    return miinat_lkm


def tarkista_voitettiinko_peli():
    """
    Tarkistaa pelin päättymisehdon sillä perusteella,
    löytyykö pelikentältä vielä avaamattomia ruutuja.
    """
    paattymisehto = True
    for i in range(len(main.tila["kentta"])):            # Käy läpi kentän riveittäin
        for j in range(len(main.tila["kentta"][0])):     # Käy läpi kentän sarakkeittain    
            if main.tila["kentta"][i][j] == " ":         # Jos kentästä löytyy avaamattomia ruutuja:
                paattymisehto = False                   # Peli saa jatkua
                break
    if paattymisehto:
        main.tila["paattymistila"] = 1                   # Merkitsee pelin voitetuksi
        main.lopeta_peli()                               # Peli päättyy voittoon
        
        
def tulvataytto(kentta, xPos, yPos):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """  
    kentta[yPos][xPos] = "0"
    lista = []
    lista.append((xPos, yPos))  
    
    while not lista == []:
        xPos, yPos = lista[-1]
        del lista[-1]
        for y in range(3):      # Käy läpi kentän riveittäin     
            for x in range(3):  # Käy läpi kentän sarakkeittain
                uusi_x = xPos + x - 1
                uusi_y = yPos + y - 1
                if 0 <= uusi_x < len(kentta[0]):
                    if 0 <= uusi_y < len(kentta):
                        if (uusi_x, uusi_y) not in main.tila["liput_xy"]:
                            if kentta[uusi_y][uusi_x] == " ":
                                miinat = laske_miinat(uusi_x, uusi_y, kentta)
                                if miinat == 0:
                                    lista.append((uusi_x, uusi_y))
                                    kentta[uusi_y][uusi_x] = str(miinat)
                                else:
                                    kentta[uusi_y][uusi_x] = str(miinat)
                                    
                                    
def avaa_ruutu(x, y):
    """
    Avaa klikatun ruudun, jos mahdollista.
    Parametrit x ja y tarkoittavat klikatun ruudun koordinaatteja.
    """
    main.tila["vuorot"] += 1  # Lisätään main.tila-sanakirjaan yksi vuoro lisää
    avain = main.tila["kentta"][y][x]
    if avain == " ":
        miinat = laske_miinat(x, y, main.tila["kentta"])
        if miinat == 0:
            tulvataytto(main.tila["kentta"], x, y)
        else:
            main.tila["kentta"][y][x] = str(miinat)
    tarkista_voitettiinko_peli()


def tarkista_liput(x, y):
    """
    Tarkistaa, onko klikatussa ruudussa lippua.
    Parametrit x ja y tarkoittavat klikatun ruudun koordinaatteja.
    """
    on_listassa = False
    for i in main.tila["liput_xy"]:
        if i == (x, y):
            main.tila["liput_xy"].remove((x, y))
            on_listassa = True
            break
    if not on_listassa:
        main.tila["liput_xy"].append((x, y))
        

def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    """
    # Tarkistetaan, osuuko hiiren klikkaus pelialueelle:
    if x <= len(main.tila["kentta"][0]) * main.ruutukoko and y <= len(main.tila["kentta"]) * main.ruutukoko:
        if main.tila["paattymistila"] == -1:
            x = int(x / main.ruutukoko)
            y = int(y / main.ruutukoko)
            kentta = main.tila["kentta"]

            if nappi == har.HIIRI_VASEN:            # Jos klikataan hiiren vasenta: 
                if (x, y) not in main.tila["liput_xy"]:
                    if kentta[y][x] == " ":         # Jos ruutu on tyhjä:
                        avaa_ruutu(x, y)          # Avataan koordinaateissa x ja y sijaitseva ruutu
                    elif kentta[y][x] == "x":       # Jos ruudussa on miina:
                        main.tila["vuorot"] += 1         # Lisätään main.tila-sanakirjaan yksi vuoro lisää
                        main.tila["paattymistila"] = 0   # Merkitään peli hävityksi
                        main.lopeta_peli()               # Lopettaa pelisilmukan
            
            elif nappi == har.HIIRI_OIKEA:          # Jos klikataan hiiren oikeaa:
                if main.tila["kentta"][y][x] in (" ", "x"):
                    tarkista_liput(x, y)    
        else:
            if nappi == har.HIIRI_VASEN:
                har.lopeta()                        # Lopettaa pelin ja palaa alkuvalikkoon