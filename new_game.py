import time
import main
import random
import save_results
import haravasto as har


def uusi_peli():
    """
    Asettaa käsittelijäfunktiot, avaa peli-ikkunan ja käynnistää uuden pelin.
    Tallentaa pelin alkamisajan tila -sanakirjaan.
    """
    main.tila["pelin_aloitus"] = time.time()     # Määrittää pelin alkamisajan
    har.lataa_kuvat("spritet.zip\spritet")  # Lataa pelissä käytettävät symbolit 
    har.luo_ikkuna(main.tila["leveys"] * main.ruutukoko, main.tila["korkeus"] * main.ruutukoko + 120)
    har.aseta_hiiri_kasittelija(main.kasittele_hiiri)
    har.aseta_piirto_kasittelija(main.piirra_kentta)  
    har.aloita()                            # Aloittaa pelin
    
    
def alustus():
    """
    Nollaa edellisen pelin tulokset.
    """
    main.tila["kentta"] = []
    main.tila["liput_xy"] = []
    main.tila["paattymismain.tila"] = -1
    main.tila["vuorot"] = 0
    main.tila["miinat_lkm"] = 0
    
    
def kysy_aloitusasetukset():
    """
    Kysyy uuden pelin asetukset,
    eli kentän leveyden ja korkeuden sekä miinojen lukumäärän.
    """
    while True:
        try:
            main.tila["leveys"] = int(input("Anna kentän leveys väliltä 2 - 25: "))
            if not 2 <= main.tila["leveys"] <= 25:
                raise ValueError

            main.tila["korkeus"] = int(input("Anna kentän korkeus väliltä 2 - 25: "))
            if not 2 <= main.tila["korkeus"] <= 25:
                raise ValueError

            miinat_max = main.tila["leveys"] * main.tila["korkeus"] - 1
            main.tila["miinat_lkm"] = int(input("Anna miinojen lukumäärä väliltä 1 - {}: ".format(miinat_max)))
            if not 1 <= main.tila["miinat_lkm"] <= miinat_max:
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
            luo_kentta(main.tila["leveys"], main.tila["korkeus"])
            miinoita(main.tila["kentta"], main.tila["jaljella"], main.tila["miinat_lkm"])
            uusi_peli()
        elif valinta == "l":    # Lopeta peli
            break
        elif valinta == "t":    # Katso tilastoja
            save_results.nayta_tilastot()   
        else:
            print("Väärä näppäin!")
            

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
        
        
def luo_kentta(leveys, korkeus):
    """
    Luo kentän pelaajan valitsemilla asetuksilla.
    """
    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")

    main.tila["kentta"] = kentta

    jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))

    main.tila["jaljella"] = jaljella