import csv
from docx import Document
import re


def transfer_word_to_csv(input_file, output_file):
    """
    Transferă date din fișierul Word în format CSV, păstrând header-ul exact cum este
    și adăugând datele în coloanele corespunzătoare

    Args:
        input_file (str): Calea către fișierul .docx
        output_file (str): Calea către fișierul .csv de ieșire
    """
    try:
        # Citește documentul Word
        doc = Document(input_file)

        # Lista pentru a stoca datele procesate
        new_data_rows = []

        # Citește fișierul CSV existent
        existing_rows = []
        try:
            with open(output_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                existing_rows = list(reader)
        except FileNotFoundError:
            print(f"Avertisment: Fișierul {output_file} nu a fost găsit!")
            return

        # Găsește următorul index disponibil
        next_index = 1
        if len(existing_rows) > 1:  # Dacă are header + date
            for row in existing_rows[1:]:  # Skip header-ul
                if row and len(row) > 0:
                    try:
                        current_index = int(row[0])
                        next_index = max(next_index, current_index + 1)
                    except (ValueError, IndexError):
                        continue

        # Procesează fiecare paragraf din document
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()

            # Sare peste paragrafele goale
            if not text:
                continue

            # Împarte textul după virgule
            parts = [part.strip() for part in text.split(',')]

            # Verifică dacă are exact 4 părți (nume, locație, lat, lng)
            if len(parts) == 4:
                nume_padure = parts[0]
                locatie = parts[1]

                try:
                    # Convertește coordonatele la float pentru validare
                    latitudine = float(parts[2])
                    longitudine = float(parts[3])

                    # Creează rândul nou FĂRĂ index: [nume_padure, locatie, latitudine, longitudine]
                    new_row = [nume_padure, locatie, latitudine, longitudine]
                    new_data_rows.append(new_row)

                except ValueError:
                    print(f"Avertisment: Coordonate invalide pentru linia: {text}")
                    continue
            else:
                print(f"Avertisment: Format incorect pentru linia: {text}")

        # Rescrie fișierul CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Scrie header-ul EXACT cum era (fără modificări)
            if existing_rows:
                writer.writerow(existing_rows[0])

            # Scrie datele existente (dacă sunt)
            if len(existing_rows) > 1:
                for row in existing_rows[1:]:
                    if row:
                        writer.writerow(row)

            # Adaugă datele noi
            writer.writerows(new_data_rows)

        print(f"✅ Transfer completat cu succes!")
        print(f"📄 Fișier sursă: {input_file}")
        print(f"📊 Fișier destinație: {output_file}")
        print(f"📈 Numărul de înregistrări noi adăugate: {len(new_data_rows)}")
        print(f"📊 Datele au fost adăugate direct în coloanele corespunzătoare (fără index automat)")

    except FileNotFoundError:
        print(f"❌ Eroare: Fișierul {input_file} nu a fost găsit!")
    except Exception as e:
        print(f"❌ Eroare neașteptată: {str(e)}")


def main():
    """Funcția principală cu path-urile specifice"""
    input_file = "./paduri_oltenia.docx"
    output_file = "./paduri_oltenia.csv"

    print("🌲 Începe transferul datelor despre pădurile din Oltenia...")
    transfer_word_to_csv(input_file, output_file)


if __name__ == "__main__":
    main()

