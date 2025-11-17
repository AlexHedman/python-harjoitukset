from datetime import datetime

with open('Viikko2/varaukset.txt', 'r', encoding='utf-8') as tiedosto:
    for rivi in tiedosto:
        rivi = rivi.strip()
        if not rivi:
            continue
        
        varaus = rivi.split('|')
        
        varausnumero = int(varaus[0])
        varaaja = varaus[1]
        paiva_raw = varaus[2]
        aika_raw = varaus[3]
        tuntimaara = int(varaus[4])
        tuntihinta = float(varaus[5])
        maksettu = varaus[6].strip().lower() == 'true'
        kohde = varaus[7]
        puhelin = varaus[8]
        email = varaus[9]
        
        paiva = datetime.strptime(paiva_raw, "%Y-%m-%d").date()
        suomalainen_paiva = paiva.strftime("%d.%m.%Y")
        aika = datetime.strptime(aika_raw, "%H:%M").time()
        suomalainen_aika = aika.strftime("%H.%M")
        
        kokonaishinta = round(tuntimaara * tuntihinta, 2)
        
        print(f"Varausnumero: {varausnumero}")
        print(f"Varaaja: {varaaja}")
        print(f"Päivämäärä: {suomalainen_paiva}")
        print(f"Aloitusaika: {suomalainen_aika}")
        print(f"Tuntimäärä: {tuntimaara}")
        print(f"Tuntihinta: {tuntihinta} €")
        print(f"Kokonaishinta: {kokonaishinta} €")
        print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
        print(f"Kohde: {kohde}")
        print(f"Puhelin: {puhelin}")
        print(f"Sähköposti: {email}")
        print("-" * 40)
