import time
import random
import haravasto as har


ruutukoko = 40
tulostiedosto = "tulokset.txt"


tila = {
    "kentta": [],
    "liput_xy": [],
    "paattymistila": int == -1,
    "vuorot": int == 0, 
    "leveys": int,
    "korkeus": int,
    "miinat_lkm": int == 0,
    "pelin_aloitus".lstrip("0:"): str,
    "pelin_lopetus".lstrip("0:"): str,
}


def alustus():
    """
    Nollaa edellisen pelin tulokset.
    """
    tila["kentta"] = []
    tila["liput_xy"] = []
    tila["paattymistila"] = -1
    tila["vuorot"] = 0
    tila["miinat_lkm"] = 0


def kysy_aloitusasetukset():
    """
    Kysyy uuden pelin asetukset,
    eli kentän leveyden ja korkeuden sekä miinojen lukumäärän.
    """
    while True:
        try:
            tila["leveys"] = int(input("Anna kentän leveys väliltä 2 - 25: "))
            if not 2 <= tila["leveys"] <= 25:
                raise ValueError

            tila["korkeus"] = int(input("Anna kentän korkeus väliltä 2 - 25: "))
            if not 2 <= tila["korkeus"] <= 25:
                raise ValueError

            miinat_max = tila["leveys"] * tila["korkeus"] - 1
            tila["miinat_lkm"] = int(input("Anna miinojen lukumäärä väliltä 1 - {}: ".format(miinat_max)))
            if not 1 <= tila["miinat_lkm"] <= miinat_max:
                raise ValueError
        except ValueError:
            print("Virheellinen syöte!")
        else:
            break


def alkuvalikko():
    """
    Tulostaa alkuvalikon ja kysyy, haluaako pelaaja aloittaa uuden pelin,
    lopettaa pelin vai katsoa tilastoja.
    """
    print("Tervetuloa miinaharavaan!")
    print("Uusi peli (U)")
    print("Lopeta peli (L)")
    print("Tilastot (T)")
    
    while True:
        valinta = input("Valitse jokin seuraavista jatkaaksesi (U, L, T): ").strip().lower()
        if valinta == "u":      # Uusi peli
            alustus()
            kysy_aloitusasetukset()
            luo_kentta(tila["leveys"], tila["korkeus"])
            miinoita(tila["kentta"], tila["jaljella"], tila["miinat_lkm"])
            uusi_peli()
        elif valinta == "l":    # Lopeta peli
            break
        elif valinta == "t":    # Katso tilastoja
            nayta_tilastot()   
        else:
            print("Väärä näppäin!")


def nayta_tilastot():
    """
    Avaa tiedoston, joka sisältää tiedot pelatuista peleistä ja
    tulostaa ne näytölle riveittäin.
    """
    try:
        with open(tulostiedosto, "r") as kohde:
            tulokset = kohde.readlines()
            for rivi in tulokset:
                print(rivi)
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Lukeminen epäonnistui.")


def uusi_peli():
    """
    Asettaa käsittelijäfunktiot, avaa peli-ikkunan ja käynnistää uuden pelin.
    Tallentaa pelin alkamisajan tila -sanakirjaan.
    """
    tila["pelin_aloitus"] = time.time()     # Määrittää pelin alkamisajan
    har.lataa_kuvat("spritet.zip\spritet")  # Lataa pelissä käytettävät symbolit 
    har.luo_ikkuna(tila["leveys"] * ruutukoko, tila["korkeus"] * ruutukoko + 120)
    har.aseta_hiiri_kasittelija(kasittele_hiiri)
    har.aseta_piirto_kasittelija(piirra_kentta)  
    har.aloita()                            # Aloittaa pelin


def luo_kentta(leveys, korkeus):
    """
    Luo kentän pelaajan valitsemilla asetuksilla.
    """
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")

    tila["kentta"] = kentta

    jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))

    tila["jaljella"] = jaljella


def miinoita(kentta, jaljella, miinat):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinat):
        tulos = random.randint(0, len(jaljella) - 1)
        x = jaljella[tulos][0]
        y = jaljella[tulos][1]
        kentta[y][x] = "x"
        jaljella.remove(jaljella[tulos])


def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    """
    # Tarkistetaan, osuuko hiiren klikkaus pelialueelle:
    if x <= len(tila["kentta"][0]) * ruutukoko and y <= len(tila["kentta"]) * ruutukoko:
        if tila["paattymistila"] == -1:
            x = int(x / ruutukoko)
            y = int(y / ruutukoko)
            kentta = tila["kentta"]

            if nappi == har.HIIRI_VASEN:            # Jos klikataan hiiren vasenta: 
                if (x, y) not in tila["liput_xy"]:
                    if kentta[y][x] == " ":         # Jos ruutu on tyhjä:
                        avaa_ruutu(x, y)          # Avataan koordinaateissa x ja y sijaitseva ruutu
                    elif kentta[y][x] == "x":       # Jos ruudussa on miina:
                        tila["vuorot"] += 1         # Lisätään tila-sanakirjaan yksi vuoro lisää
                        tila["paattymistila"] = 0   # Merkitään peli hävityksi
                        lopeta_peli()               # Lopettaa pelisilmukan
            
            elif nappi == har.HIIRI_OIKEA:          # Jos klikataan hiiren oikeaa:
                if tila["kentta"][y][x] in (" ", "x"):
                    tarkista_liput(x, y)    
        else:
            if nappi == har.HIIRI_VASEN:
                har.lopeta()                        # Lopettaa pelin ja palaa alkuvalikkoon


def avaa_ruutu(x, y):
    """
    Avaa klikatun ruudun, jos mahdollista.
    Parametrit x ja y tarkoittavat klikatun ruudun koordinaatteja.
    """
    tila["vuorot"] += 1  # Lisätään tila-sanakirjaan yksi vuoro lisää
    avain = tila["kentta"][y][x]
    if avain == " ":
        miinat = laske_miinat(x, y, tila["kentta"])
        if miinat == 0:
            tulvataytto(tila["kentta"], x, y)
        else:
            tila["kentta"][y][x] = str(miinat)
    tarkista_voitettiinko_peli()


def tarkista_liput(x, y):
    """
    Tarkistaa, onko klikatussa ruudussa lippua.
    Parametrit x ja y tarkoittavat klikatun ruudun koordinaatteja.
    """
    on_listassa = False
    for i in tila["liput_xy"]:
        if i == (x, y):
            tila["liput_xy"].remove((x, y))
            on_listassa = True
            break
    if not on_listassa:
        tila["liput_xy"].append((x, y))

        
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
                        if (uusi_x, uusi_y) not in tila["liput_xy"]:
                            if kentta[uusi_y][uusi_x] == " ":
                                miinat = laske_miinat(uusi_x, uusi_y, kentta)
                                if miinat == 0:
                                    lista.append((uusi_x, uusi_y))
                                    kentta[uusi_y][uusi_x] = str(miinat)
                                else:
                                    kentta[uusi_y][uusi_x] = str(miinat)


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
    for i in range(len(tila["kentta"])):            # Käy läpi kentän riveittäin
        for j in range(len(tila["kentta"][0])):     # Käy läpi kentän sarakkeittain    
            if tila["kentta"][i][j] == " ":         # Jos kentästä löytyy avaamattomia ruutuja:
                paattymisehto = False                   # Peli saa jatkua
                break
    if paattymisehto:
        tila["paattymistila"] = 1                   # Merkitsee pelin voitetuksi
        lopeta_peli()                               # Peli päättyy voittoon


def lopeta_peli():
    """
    Lopettaa pelin ja kutsuu tallennusfunktiota,
    joka tulostaa tiedot pelatusta pelistä erilliseen tiedostoon.
    """
    tila["pelin_lopetus"] = time.time()         # Määrittää pelin loppumisajan

    if tila["paattymistila"] == 0:              # Jos peli on hävitty:        
        tallenna_tulokset("Häviö")              # Tallennetaan peli hävityksi

    elif tila["paattymistila"] == 1:            # Jos peli on voitettu:  
        tallenna_tulokset("Voitto")             # Tallennetaan peli voitetuksi
                 

def tallenna_tulokset(tulos):
    """
    Tallentaa tiedot pelatusta pelistä erilliseen tiedostoon.
    """
    paivamaara = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    peliaika = round(tila["pelin_lopetus"] - tila["pelin_aloitus"])
    tunnit = int(peliaika / 3600)
    minuutit = int((peliaika - tunnit * 60) / 60)
    sekunnit = round(((peliaika - tunnit * 60) - minuutit * 60))

    try:
        with open(tulostiedosto, "a") as kohde:
            kohde.write("{} | {} | Kenttä: {}x{} | Miinoja: {} | Pelin kesto: {}:{:02}:{:02} | Siirrot: {}\n".format(
                paivamaara,
                tulos,
                tila["leveys"],
                tila["korkeus"],
                tila["miinat_lkm"],
                tunnit,
                minuutit,
                sekunnit,
                tila["vuorot"]
            ))      
    except IOError:
        print("Kohdetiedostoa ei voitu avata.")   


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina, kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    har.tyhjaa_ikkuna()         
    har.piirra_tausta()     
    har.aloita_ruutujen_piirto()    
    kentta = tila["kentta"]             
    for rivi in range(0, len(kentta)):       
        for sarake in range(0, len(kentta[rivi])):
            if (sarake, rivi) in tila["liput_xy"]:
                x = sarake * ruutukoko
                y = rivi * ruutukoko
                har.lisaa_piirrettava_ruutu("f", x, y)
            else:
                avain = kentta[rivi][sarake]
                if avain == "x" and not tila["paattymistila"] == 0:
                    avain = " "
                x = sarake * ruutukoko
                y = rivi * ruutukoko
                har.lisaa_piirrettava_ruutu(avain, x, y)
    har.piirra_ruudut()
      
       
def main():
    """
    Aloittaa ohjelman ja määrittää alkuvalikon.
    """
    alkuvalikko()


if __name__ == "__main__":
    main()