import re
import fitz
import os

def extract_text_from_pdf(pdf_path):
    """Extrage textul complet din documentul PDF."""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Eroare la citirea PDF-ului: {e}")
        return ""


def find_entries_with_keywords(text, keywords):
    """
    Identifică intrările principale care conțin cuvintele cheie specificate
    și extrage paragrafele relevante.
    """
    # Pattern pentru identificarea intrărilor principale (cuvinte cu majuscule + numere opționale)
    entry_pattern = re.compile(r'([A-ZĂÂÎȘȚ][A-ZĂÂÎȘȚ\-]+\d*)')

    # Împărțim textul în linii pentru procesare
    lines = text.split('\n')

    entries = {}
    current_entry = None
    current_content = []

    # Procesăm fiecare linie pentru a identifica intrările și conținutul lor
    for line in lines:
        # Verificăm dacă linia conține o intrare principală
        entry_match = entry_pattern.match(line.strip())

        if entry_match and (line.strip().isupper() or re.match(r'^[A-ZĂÂÎȘȚ][A-ZĂÂÎȘȚ\-]+\d+', line.strip())):
            # Dacă avem o intrare anterioară și conținut, o salvăm
            if current_entry and current_content:
                entries[current_entry] = '\n'.join(current_content)

            # Setăm noua intrare curentă
            current_entry = entry_match.group(1)
            current_content = [line.strip()]
        elif current_entry:
            # Adăugăm linia la conținutul intrării curente
            current_content.append(line.strip())

    # Adăugăm ultima intrare dacă există
    if current_entry and current_content:
        entries[current_entry] = '\n'.join(current_content)

    # Filtrăm intrările care conțin cuvintele cheie și extragem paragrafele relevante
    results = {}
    for entry, content in entries.items():
        paragraphs_with_keywords = []

        # Împărțim conținutul în paragrafe
        paragraphs = re.split(r'\n\s*\n', content)

        for paragraph in paragraphs:
            # Verificăm dacă paragraful conține vreunul din cuvintele cheie
            if any(keyword.lower() in paragraph.lower() for keyword in keywords):
                paragraphs_with_keywords.append(paragraph)

        if paragraphs_with_keywords:
            results[entry] = paragraphs_with_keywords

    return results


def save_results_to_file(results, output_file):
    """Salvează rezultatele într-un fișier text."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry, paragraphs in results.items():
            f.write(f"INTRARE: {entry}\n")
            f.write("-" * 50 + "\n")

            for i, paragraph in enumerate(paragraphs, 1):
                f.write(f"Paragraf {i}:\n{paragraph}\n\n")

            f.write("=" * 50 + "\n\n")


def main():
    # Calea către fișierul PDF (prestabilită la același nivel cu scriptul)
    pdf_path = "Toponimia de pe valea Sucevei.pdf"

    print(f"Se folosește fișierul: {pdf_path}")

    # Verificăm dacă fișierul există
    if not os.path.exists(pdf_path):
        print(f"Fișierul {pdf_path} nu există!")
        return

    # Cuvintele cheie de căutat
    keywords = ["pădur", "codr", "fiton", "dendron"]

    # Extragem textul din PDF
    print("Se extrage textul din PDF...")
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print("Nu s-a putut extrage text din PDF.")
        return

    # Găsim intrările cu cuvintele cheie și paragrafele relevante
    print("Se caută intrările cu cuvintele cheie...")
    results = find_entries_with_keywords(text, keywords)

    # Afișăm numărul de intrări găsite
    print(f"S-au găsit {len(results)} intrări care conțin cuvintele cheie.")

    # Salvăm rezultatele într-un fișier
    output_file = "rezultate_padure_codru.txt"
    save_results_to_file(results, output_file)

    print(f"Rezultatele au fost salvate în fișierul {output_file}")

    # Afișăm și un rezumat
    print("\nRezumat intrări găsite:")
    for entry in results.keys():
        print(f"- {entry}")


if __name__ == "__main__":
    main()








