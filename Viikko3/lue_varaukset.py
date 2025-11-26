from datetime import datetime

# ==================== KAIKKI FUNKTIOt ====================

def hae_varausnumero(varaus):
    return int(varaus[0])

def hae_varaaja(varaus):
    return varaus[1]

def hae_paiva(varaus):
    pvm = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    return pvm.strftime("%d.%m.%Y")

def hae_aloitusaika(varaus):
    aika = datetime.strptime(varaus[3], "%H:%M").time()
    return aika.strftime("%H.%M")

def hae_tuntimaara(varaus):
    return int(varaus[4])

def hae_tuntihinta(varaus):
    hinta = float(varaus[5])
    return f"{hinta:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"
    # Vaihtoehtoisesti yksinkertaisemmin: return f"{hinta:.2f} €".replace(".", ",")

def laske_kokonaishinta(varaus):
    hinta = float(varaus[4]) * float(varaus[5])
    return f"{hinta:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"

def hae_maksettu(varaus):
    return "Kyllä" if varaus[6].strip().lower() == "true" else "Ei"

def hae_kohde(varaus):
    return varaus[7]

def hae_puhelin(varaus):
    return varaus[8]

def hae_sahkoposti(varaus):
    return varaus[9]

# ==================== PÄÄOHJELMA ====================

with open('Viikko3/varaukset.txt', 'r', encoding='utf-8') as tiedosto:
    for rivi in tiedosto:
        rivi = rivi.strip()
        if not rivi:
            continue
            
        varaus = rivi.split('|')  # ← tämä on se rivi 32, joka oli jo valmiina

        print(f"Varausnumero: {hae_varausnumero(varaus)}")
        print(f"Varaaja: {hae_varaaja(varaus)}")
        print(f"Päivämäärä: {hae_paiva(varaus)}")
        print(f"Aloitusaika: {hae_aloitusaika(varaus)}")
        print(f"Tuntimäärä: {hae_tuntimaara(varaus)}")
        print(f"Tuntihinta: {hae_tuntihinta(varaus)}")
        print(f"Kokonaishinta: {laske_kokonaishinta(varaus)}")
        print(f"Maksettu: {hae_maksettu(varaus)}")
        print(f"Kohde: {hae_kohde(varaus)}")
        print(f"Puhelin: {hae_puhelin(varaus)}")
        print(f"Sähköposti: {hae_sahkoposti(varaus)}")
        print("-" * 50)
