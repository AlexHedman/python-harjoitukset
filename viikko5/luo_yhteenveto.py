# Copyright (c) 2025 Alex Hedman
# License: MIT

from datetime import datetime
from typing import List, Dict
import csv

def lue_data(tiedoston_nimi: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa listan sanakirjoja."""
    data = []
    with open(tiedoston_nimi, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['aika'].strip() and row['aika'][0].isdigit():
                data.append(row)
    return data

def laske_viikon_summat(data: List[Dict]) -> List[Dict]:
    """Laskee viikon päiväkohtaiset summat (Wh → kWh)."""
    paivat = {}
    for row in data:
        aika = datetime.fromisoformat(row['aika'])
        paiva = aika.date()
        key = paiva.strftime("%Y-%m-%d")
        if key not in paivat:
            paivat[key] = {
                'paiva': paiva,
                'kulutus_v1': 0.0, 'kulutus_v2': 0.0, 'kulutus_v3': 0.0,
                'tuotanto_v1': 0.0, 'tuotanto_v2': 0.0, 'tuotanto_v3': 0.0
            }
        paivat[key]['kulutus_v1'] += float(row['kulutus_vaihe1_Wh']) / 1000
        paivat[key]['kulutus_v2'] += float(row['kulutus_vaihe2_Wh']) / 1000
        paivat[key]['kulutus_v3'] += float(row['kulutus_vaihe3_Wh']) / 1000
        paivat[key]['tuotanto_v1'] += float(row['tuotanto_vaihe1_Wh']) / 1000
        paivat[key]['tuotanto_v2'] += float(row['tuotanto_vaihe2_Wh']) / 1000
        paivat[key]['tuotanto_v3'] += float(row['tuotanto_vaihe3_Wh']) / 1000
    return sorted(paivat.values(), key=lambda x: x['paiva'])

def muodosta_viikon_raportti(summat: List[Dict], viikko: int) -> List[str]:
    """Muodostaa yhden viikon raporttirivit merkkijonoina."""
    rivit = []
    rivit.append(f"Viikon {viikko} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    rivit.append(f"{'Päivä':<12} {'Pvm':<12} {'Kulutus [kWh]':<30} {'Tuotanto [kWh]':<30}")
    rivit.append(f"{'':<12} {'(pv.kk.vvvv)':<12} {'v1':>8} {'v2':>8} {'v3':>8} {'v1':>8} {'v2':>8} {'v3':>8}")
    rivit.append("-" * 90)
    weekdays = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"]
    for s in summat:
        nimi = weekdays[s['paiva'].weekday()]
        pvm = f"{s['paiva'].day}.{s['paiva'].month}.{s['paiva'].year}"
        k1 = f"{s['kulutus_v1']:.2f}".replace(".", ",")
        k2 = f"{s['kulutus_v2']:.2f}".replace(".", ",")
        k3 = f"{s['kulutus_v3']:.2f}".replace(".", ",")
        t1 = f"{s['tuotanto_v1']:.2f}".replace(".", ",")
        t2 = f"{s['tuotanto_v2']:.2f}".replace(".", ",")
        t3 = f"{s['tuotanto_v3']:.2f}".replace(".", ",")
        rivit.append(f"{nimi:<12} {pvm:<12} {k1:>8} {k2:>8} {k3:>8} {t1:>8} {t2:>8} {t3:>8}")
    rivit.append("\n")
    return rivit

def main() -> None:
    """Lukee kolme viikkoa ja kirjoittaa yhteenvedon tiedostoon."""
    viikot = [41, 42, 43]
    kaikki_rivit = []
    for v in viikot:
        data = lue_data(f"Viikko5/viikko{v}.csv")
        summat = laske_viikon_summat(data)
        kaikki_rivit.extend(muodosta_viikon_raportti(summat, v))
    
    with open("Viikko5/yhteenveto.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(kaikki_rivit))
    
    print("Raportti luotu: Viikko5/yhteenveto.txt")

if __name__ == "__main__":
    main()
