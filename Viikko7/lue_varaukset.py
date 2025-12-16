# Copyright (c) 2025 Alex Hedman
# License: MIT

# Refaktorointi: muutin listat sanakirjoiksi, koska näin koodi on paljon selkeämpää.
# Ei enää tarvitse muistaa, mikä indeksi on mikä kenttä (esim. varaus[1] = nimi).
# Nyt käytetään avaimia kuten varaus["nimi"], varaus["vahvistettu"] jne.

from datetime import datetime

def muunna_sanakirjaksi(rivi: list) -> dict:
    """Muuntaa splitatun rivin sanakirjaksi selkeillä avaimilla."""
    return {
        "id": int(rivi[0]),
        "nimi": rivi[1],
        "sahkoposti": rivi[2],
        "puhelin": rivi[3],
        "paiva": datetime.strptime(rivi[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(rivi[5], "%H:%M").time(),
        "kesto": int(rivi[6]),
        "hinta": float(rivi[7]),
        "vahvistettu": rivi[8].lower() == "true",
        "kohde": rivi[9],
        "luotu": datetime.strptime(rivi[10], "%Y-%m-%d %H:%M:%S")
    }

def hae_varaukset(tiedosto: str) -> list:
    """Lukee tiedoston ja palauttaa listan sanakirjoja."""
    varaukset = []
    with open(tiedosto, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:  # ohitetaan tyhjät rivit
                rivi = line.split("|")
                varaus = muunna_sanakirjaksi(rivi)
                varaukset.append(varaus)
    return varaukset

def main() -> None:
    varaukset = hae_varaukset("Viikko7/varaukset.txt")

    print("1) Vahvistetut varaukset")
    for v in varaukset:
        if v["vahvistettu"]:
            pvm = v["paiva"].strftime("%d.%m.%Y")
            klo = v["kellonaika"].strftime("%H.%M")
            print(f"- {v['nimi']}, {v['kohde']}, {pvm} klo {klo}")

    print("\n2) Pitkät varaukset (≥ 3 h)")
    for v in varaukset:
        if v["kesto"] >= 3:
            pvm = v["paiva"].strftime("%d.%m.%Y")
            klo = v["kellonaika"].strftime("%H.%M")
            print(f"- {v['nimi']}, {pvm} klo {klo}, kesto {v['kesto']} h, {v['kohde']}")

    print("\n3) Varausten vahvistusstatus")
    for v in varaukset:
        status = "Vahvistettu" if v["vahvistettu"] else "EI vahvistettu"
        print(f"{v['nimi']} → {status}")

    vahvistetut = sum(1 for v in varaukset if v["vahvistettu"])
    print("\n4) Yhteenveto vahvistuksista")
    print(f"- Vahvistettuja varauksia: {vahvistetut} kpl")
    print(f"- Ei-vahvistettuja varauksia: {len(varaukset) - vahvistetut} kpl")

    tulot = sum(v["kesto"] * v["hinta"] for v in varaukset if v["vahvistettu"])
    print("\n5) Vahvistettujen varausten kokonaistulot")
    print(f"Vahvistettujen varausten kokonaistulot: {tulot:.2f}".replace(".", ",") + " €")

if __name__ == "__main__":
    main()
