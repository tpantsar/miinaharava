import main
import time

def nayta_tilastot():
    """
    Avaa tiedoston, joka sisältää tiedot pelatuista peleistä ja
    tulostaa ne näytölle riveittäin.
    """
    try:
        with open(main.tulostiedosto, "r") as kohde:
            tulokset = kohde.readlines()
            for rivi in tulokset:
                print(rivi)
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Lukeminen epäonnistui.")
        
        
def tallenna_tulokset(tulos):
    """
    Tallentaa tiedot pelatusta pelistä erilliseen tiedostoon.
    """
    paivamaara = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    peliaika = round(main.tila["pelin_lopetus"] - main.tila["pelin_aloitus"])
    tunnit = int(peliaika / 3600)
    minuutit = int((peliaika - tunnit * 60) / 60)
    sekunnit = round(((peliaika - tunnit * 60) - minuutit * 60))

    try:
        with open(main.tulostiedosto, "a") as kohde:
            kohde.write("{} | {} | Kenttä: {}x{} | Miinoja: {} | Pelin kesto: {}:{:02}:{:02} | Siirrot: {}\n".format(
                paivamaara,
                tulos,
                main.tila["leveys"],
                main.tila["korkeus"],
                main.tila["miinat_lkm"],
                tunnit,
                minuutit,
                sekunnit,
                main.tila["vuorot"]
            ))      
    except IOError:
        print("Kohdetiedostoa ei voitu avata.")
        
        
def lopeta_peli():
    """
    Lopettaa pelin ja kutsuu tallennusfunktiota,
    joka tulostaa tiedot pelatusta pelistä erilliseen tiedostoon.
    """
    # Määrittää pelin loppumisajan
    main.tila["pelin_lopetus"] = time.time()         

    # Jos peli on hävitty, tallennetaan peli hävityksi
    if main.tila["paattymistila"] == 0:                      
        tallenna_tulokset("Häviö")

    # Jos peli on voitettu, tallennetaan peli voitetuksi
    elif main.tila["paattymistila"] == 1:              
        tallenna_tulokset("Voitto")