from datetime import datetime, date, time

def muunna_varaustiedot(rivi):
    """Muuntaa yhden splitatun rivin oikeisiin tietotyypeihin"""
    varaus_id = int(rivi[0])
    nimi = rivi[1]
    sahkoposti = rivi[2]
    puhelin = rivi[3]
    varauksen_pvm = datetime.strptime(rivi[4], "%Y-%m-%d").date()
    varauksen_klo = datetime.strptime(rivi[5], "%H:%M").time()
    varauksen_kesto = int(rivi[6])
    hinta = float(rivi[7])
    varaus_vahvistettu = (rivi[8] == "True")
    varattu_tila = rivi[9]
    varaus_luotu = datetime.strptime(rivi[10], "%Y-%m-%d %H:%M:%S")
    
    return [
        varaus_id, nimi, sahkoposti, puhelin,
        varauksen_pvm, varauksen_klo, varauksen_kesto,
        hinta, varaus_vahvistettu, varattu_tila, varaus_luotu
    ]

# ==================== PÄÄOHJELMA ====================

varaukset = []

# Lue tiedosto ja muunna jokainen rivi
with open('Viikko4/varaukset.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            rivi = line.split('|')
            varaus = muunna_varaustiedot(rivi)
            varaukset.append(varaus)

# ------------------ 1) Vahvistetut varaukset ------------------
print("1) Vahvistetut varaukset")
for v in varaukset:
    if v[8]:  # varaus_vahvistettu
        pvm = v[4].strftime("%d.%m.%Y")
        klo = v[5].strftime("%H.%M")
        print(f"- {v[1]}, {v[9]}, {pvm} klo {klo}")

# ------------------ 2) Pitkät varaukset (≥ 3 h) ------------------
print("\n2) Pitkät varaukset (≥ 3 h)")
for v in varaukset:
    if v[6] >= 3:
        pvm = v[4].strftime("%d.%m.%Y")
        klo = v[5].strftime("%H.%M")
        print(f"- {v[1]}, {pvm} klo {klo}, kesto {v[6]} h, {v[9]}")

# ------------------ 3) Vahvistusstatus ------------------
print("\n3) Varausten vahvistusstatus")
for v in varaukset:
    status = "Vahvistettu" if v[8] else "EI vahvistettu"
    print(f"{v[1]} → {status}")

# ------------------ 4) Yhteenveto vahvistuksista ------------------
vahvistetut = sum(1 for v in varaukset if v[8])
ei_vahvistetut = len(varaukset) - vahvistetut
print("\n4) Yhteenveto vahvistuksista")
print(f"- Vahvistettuja varauksia: {vahvistetut} kpl")
print(f"- Ei-vahvistettuja varauksia: {ei_vahvistetut} kpl")

# ------------------ 5) Kokonaistulot (vahvistetuista) ------------------
kokonaissumma = sum(v[6] * v[7] for v in varaukset if v[8])
summa_str = f"{kokonaissumma:.2f}".replace(".", ",")
print("\n5) Vahvistettujen varausten kokonaistulot")
print(f"Vahvistettujen varausten kokonaistulot: {summa_str} €")
