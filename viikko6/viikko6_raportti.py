# Copyright (c) 2025 Alex Hedman
# License: MIT

from datetime import datetime
from typing import List, Dict
import csv

def lue_data(tiedosto: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa listan riveistä."""
    data = []
    with open(tiedosto, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['aika'] = datetime.fromisoformat(row['aika'])
            row['kulutus_kWh'] = float(row['kulutus_kWh'])
            row['tuotanto_kWh'] = float(row['tuotanto_kWh'])
            row['keskilaempo'] = float(row['keskilaempo'])
            data.append(row)
    return data

def paivakohtainen_raportti(data: List[Dict], alku: str, loppu: str) -> List[str]:
    """Laskee päiväkohtaisen yhteenvedon annetulta aikaväliltä."""
    alku_pvm = datetime.strptime(alku, "%d.%m.%Y").date()
    loppu_pvm = datetime.strptime(loppu, "%d.%m.%Y").date()
    
    kulutus_yht = 0.0
    tuotanto_yht = 0.0
    lampo_yht = 0.0
    maara = 0
    
    for row in data:
        pvm = row['aika'].date()
        if alku_pvm <= pvm <= loppu_pvm:
            kulutus_yht += row['kulutus_kWh']
            tuotanto_yht += row['tuotanto_kWh']
            lampo_yht += row['keskilaempo']
            maara += 1
    
    if maara == 0:
        return ["Ei tietoja annetulta aikaväliltä."]
    
    keski_lampo = lampo_yht / maara
    rivit = []
    rivit.append(f"Päiväkohtainen yhteenveto {alku}-{loppu}")
    rivit.append(f"Kokonaiskulutus: {kulutus_yht:.2f}".replace(".", ",") + " kWh")
    rivit.append(f"Kokonais tuotanto: {tuotanto_yht:.2f}".replace(".", ",") + " kWh")
    rivit.append(f"Keskimääräinen lämpötila: {keski_lampo:.2f}".replace(".", ",") + " °C")
    return rivit

def kuukausiraportti(data: List[Dict], kk: int) -> List[str]:
    """Laskee yhteenvedon yhdeltä kuukaudelta."""
    kulutus_yht = 0.0
    tuotanto_yht = 0.0
    lampo_yht = 0.0
    maara = 0
    
    for row in data:
        if row['aika'].month == kk:
            kulutus_yht += row['kulutus_kWh']
            tuotanto_yht += row['tuotanto_kWh']
            lampo_yht += row['keskilaempo']
            maara += 1
    
    if maara == 0:
        return [f"Ei tietoja kuukaudelta {kk}."]
    
    keski_lampo = lampo_yht / maara
    rivit = []
    rivit.append(f"Kuukausiyhteenveto kuukaudelta {kk}/2025")
    rivit.append(f"Kokonaiskulutus: {kulutus_yht:.2f}".replace(".", ",") + " kWh")
    rivit.append(f"Kokonais tuotanto: {tuotanto_yht:.2f}".replace(".", ",") + " kWh")
    rivit.append(f"Keskimääräinen lämpötila: {keski_lampo:.2f}".replace(".", ",") + " °C")
    return rivit

def vuosiraportti(data: List[Dict]) -> List[str]:
    """Laskee koko vuoden yhteenvedon."""
    kulutus_yht = 0.0
    tuotanto_yht = 0.0
    lampo_yht = 0.0
    maara = len(data)
    
    for row in data:
        kulutus_yht += row['kulutus_kWh']
        tuotanto_yht += row['tuotanto_kWh']
        lampo_yht += row['keskilaempo']
    
    keski_lampo = lampo_yht / maara if maara > 0 else 0
    rivit = []
    rivit.append("Vuoden 2025 kokonaisyhteenveto")
    rivit.append(f"Kokonaiskulutus: {kulutus_yht:.2f}".replace(".", ",") + " kWh")
    rivit.append(f"Kokonais tuotanto: {tuotanto_yht:.2f}".replace(".", ",") + " kWh")
    rivit.append(f"Keskimääräinen lämpötila: {keski_lampo:.2f}".replace(".", ",") + " °C")
    return rivit

def tulosta_raportti(rivit: List[str]) -> None:
    """Tulostaa raportin konsoliin."""
    for rivi in rivit:
        print(rivi)

def kirjoita_tiedostoon(rivit: List[str]) -> None:
    """Kirjoittaa raportin tiedostoon raportti.txt."""
    with open("Viikko6/raportti.txt", "w", encoding="utf-8") as f:
        for rivi in rivit:
            f.write(rivi + "\n")
    print("Raportti tallennettu tiedostoon Viikko6/raportti.txt")

def main() -> None:
    """Pääohjelma: valikot ja raporttien luonti."""
    data = lue_data("Viikko6/2025.csv")
    viimeinen_raportti = []

    while True:
        print("\nValitse raporttityyppi:")
        print("1) Päiväkohtainen yhteenveto aikaväliltä")
        print("2) Kuukausikohtainen yhteenveto")
        print("3) Vuoden 2025 kokonaisyhteenveto")
        print("4) Lopeta ohjelma")
        valinta = input("Valintasi: ")

        if valinta == "1":
            alku = input("Anna alkupäivä (pv.kk.vvvv): ")
            loppu = input("Anna loppupäivä (pv.kk.vvvv): ")
            viimeinen_raportti = paivakohtainen_raportti(data, alku, loppu)
        elif valinta == "2":
            kk = int(input("Anna kuukauden numero (1-12): "))
            viimeinen_raportti = kuukausiraportti(data, kk)
        elif valinta == "3":
            viimeinen_raportti = vuosiraportti(data)
        elif valinta == "4":
            print("Kiitos ja näkemiin!")
            break
        else:
            print("Virheellinen valinta, yritä uudestaan.")
            continue

        tulosta_raportti(viimeinen_raportti)

        while True:
            print("\nMitä haluat tehdä seuraavaksi?")
            print("1) Kirjoita raportti tiedostoon raportti.txt")
            print("2) Luo uusi raportti")
            print("3) Lopeta")
            toiminto = input("Valintasi: ")
            if toiminto == "1":
                kirjoita_tiedostoon(viimeinen_raportti)
                break
            elif toiminto == "2":
                break
            elif toiminto == "3":
                print("Kiitos ja näkemiin!")
                return
            else:
                print("Virheellinen valinta.")

if __name__ == "__main__":
    main()
