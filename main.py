import new_game


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
      
       
def main():
    """
    Aloittaa ohjelman ja määrittää alkuvalikon.
    """
    new_game.alkuvalikko()


if __name__ == "__main__":
    main()