def lue_data(tiedoston_nimi: str) -> List[Dict]:
    """
    Lukee CSV-tiedoston ja palauttaa listan sanakirjoja, joissa avaimina sarakkeiden nimet.
    Ohittaa tyhjät rivit ja rivit, jotka eivät ala kellonajalla.
    """
    data = []
    with open(tiedoston_nimi, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Ohitetaan rivit, joissa 'aika'-kenttä ei ala numerolla (esim. kommenttirivit)
            if row['aika'].strip() and row['aika'][0].isdigit():
                data.append(row)
    return data
