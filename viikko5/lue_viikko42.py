# Copyright (c) 2025 Alex Hedman
# License: MIT

from datetime import datetime
from typing import List, Dict
import csv

def lue_data(tiedosto: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa listan riveistä."""
    data = []
    with open(tiedosto, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def laske_summat(data: List[Dict]) -> List[Dict]:
    """Laskee päiväkohtaiset summat kWh:ssa."""
    summat = {}
    for row in data:
        aika = datetime.fromisoformat(row['aika'])
        paiva = aika.date()
        key = paiva.strftime("%Y-%m-%d")
        if key not in summat:
            summat[key] = {
                'paiva': paiva,
                'kulutus_v1': 0.0, 'kulutus_v2': 0.0, 'kulutus_v3': 0.0,
                'tuotanto_v1': 0.0, 'tuotanto_v2': 0.0, 'tuotanto_v3': 0.0
            }
        summat[key]['kulutus_v1'] += float(row['kulutus_vaihe1_Wh']) / 1000
        summat[key]['kulutus_v2'] += float(row['kulutus_vaihe2_Wh']) / 1000
        summat[key]['kulutus_v3'] += float(row['kulutus_vaihe3_Wh']) / 1000
        summat[key]['tuotanto_v1'] += float(row['tuotanto_vaihe1_Wh']) / 1000
        summat[key]['tuotanto_v2'] += float(row['tuotanto_vaihe2_Wh']) / 1000
        summat[key]['tuotanto_v3'] += float(row['tuotanto_vaihe3_Wh']) / 1000
    return sorted(summat.values(), key=lambda x: x['paiva'])

def tulosta_taulukko(summat: List[Dict]) -> None:
    """Tulostaa siistin taulukon."""
    weekdays = ["maanantai", "tiistai", "keskiviikko", "torstai", "perjantai", "lauantai", "sunnuntai"]
    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    print(f"{'Päivä':<12} {'Pvm':<12} {'Kulutus [kWh]':<30} {'Tuotanto [kWh]':<30}")
    print(f"{'':<12} {'(pv.kk.vvvv)':<12} {'v1':>8} {'v2':>8} {'v3':>8} {'v1':>8} {'v2':>8} {'v3':>8}")
    print("-" * 90)
    
    for s in summat:
        nimi = weekdays[s['paiva'].weekday()]
        pvm = f"{s['paiva'].day}.{s['paiva'].month}.{s['paiva'].year}"
        k1 = f"{s['kulutus_v1']:.2f}".replace(".", ",")
        k2 = f"{s['kulutus_v2']:.2f}".replace(".", ",")
        k3 = f"{s['kulutus_v3']:.2f}".replace(".", ",")
        t1 = f"{s['tuotanto_v1']:.2f}".replace(".", ",")
        t2 = f"{s['tuotanto_v2']:.2f}".replace(".", ",")
        t3 = f"{s['tuotanto_v3']:.2f}".replace(".", ",")
        print(f"{nimi:<12} {pvm:<12} {k1:>8} {k2:>8} {k3:>8} {t1:>8} {t2:>8} {t3:>8}")

def main() -> None:
    """Pääfunktio."""
    data = lue_data("Viikko5/viikko42.csv")
    summat = laske_summat(data)
    tulosta_taulukko(summat)

if __name__ == "__main__":
    main()
