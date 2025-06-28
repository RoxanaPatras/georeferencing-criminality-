import pandas as pd


def is_a_locality(word: str) -> bool:
    """
    Determines if a word is likely a city or village based on a
    whitelist, a blacklist, and capitalization.
    """
    if not isinstance(word, str) or not word:
        return False

    # A set provides very fast lookups (O(1) on average)

    # Whitelist of major Romanian cities/towns to ensure they are always included.
    # This can be expanded.
    LOCALITIES_WHITELIST = {
        'Adjud', 'Aiud', 'Alba Iulia', 'Alexandria', 'Arad', 'Bacău', 'Baia Mare', 'Bârlad', 'Bechet',
        'Bistrița', 'Botoșani', 'Brăila', 'Brașov', 'București', 'Buzău', 'Călărași',
        'Câmpina', 'Câmpulung', 'Caracal', 'Cluj-Napoca', 'Constanța', 'Craiova',
        'Deva', 'Dorohoi', 'Drobeta-Turnu Severin', 'Făgăraș', 'Focșani', 'Galați',
        'Giurgiu', 'Hunedoara', 'Iași', 'Lugoj', 'Mediaș', 'Miercurea Ciuc', 'Oradea',
        'Panciu', 'Petroșani', 'Piatra Neamț', 'Pitești', 'Ploiești', 'Rădăuți', 'Reșița',
        'Râmnicu Vâlcea', 'Roman', 'Satu Mare', 'Sebeș', 'Sfântu Gheorghe', 'Sibiu',
        'Sighișoara', 'Slatina', 'Slobozia', 'Suceava', 'Târgoviște', 'Târgu Jiu',
        'Târgu Mureș', 'Tecuci', 'Timișoara', 'Tulcea', 'Turnu Măgurele', 'Vaslui', 'Zalău'
    }

    # Blacklist of capitalized words that are NOT cities/villages (countries, regions, rivers, etc.)
    NON_LOCALITIES_BLACKLIST = {
        'Albania', 'Ardeal', 'Asia', 'Austerlitz', 'Austria', 'Balcani', 'Banat', 'Basarabia',
        'Bahlui', 'Bârlăzel', 'Bistrița', 'Bîsca', 'Bosfor', 'Bucegi', 'Bugeac', 'Buila',
        'Bulgaria', 'Carpați', 'Cefalonia', 'Colomea', 'Constantinopol', 'Covurlui', 'Cozia',
        'Cracău', 'Cracovia', 'Crimeea', 'Dalmația', 'Dobrogea', 'Dunăre', 'Eforie', 'Europa',
        'Fanar', 'Fetislam', 'Galiția', 'Grecia', 'Istru', 'Izei', 'Lotru', 'Macedonia', 'Maramureș',
        'Milcov', 'Moldova', 'Motru', 'Muntenia', 'Neajlov', 'Nistru', 'Oituz', 'Olimp',
        'Oltenia', 'Olt', 'Ozana', 'Pelopones', 'Penteleu', 'Pind', 'Plevna', 'Polonia', 'Prahova',
        'Prut', 'România', 'Rusia', 'Serbia', 'Severin', 'Siret', 'Soloneț', 'Tesalia', 'Tisa',
        'Transilvania', 'Trotuș', 'Turcia', 'Tutova', 'Ungaria', 'Vâlcea', 'Vlăsia'
    }

    # Normalize the word for checking (e.g., remove leading/trailing spaces)
    word_normalized = word.strip()

    # Rule 1: If it's in our high-confidence whitelist, it's a locality.
    if word_normalized in LOCALITIES_WHITELIST:
        return True

    # Rule 2: If it's in our blacklist, it's definitely NOT a locality.
    if word_normalized in NON_LOCALITIES_BLACKLIST:
        return False

    # Rule 3: Fallback rule. If it's capitalized and not blacklisted,
    # assume it's a smaller village or locality we don't have on our lists.
    if word_normalized[0].isupper():
        return True

    return False

# --- How to use it ---
if __name__ == "__main__":
    input_filename = 'data.csv'
    output_filename = 'data2.csv'

    try:
        print(f"Reading data from '{input_filename}'...")
        # Use utf-8 encoding to handle Romanian diacritics correctly
        df = pd.read_csv(input_filename, encoding='utf-8')

        # Apply the filtering function to the 'cuvant' column
        # This creates a boolean Series (True/False for each row)
        is_locality_mask = df['cuvant'].apply(is_a_locality)

        # Use the boolean mask to select only the rows where the mask is True
        filtered_df = df[is_locality_mask]

        # Save the filtered DataFrame to a new CSV file
        # Use encoding='utf-8-sig' to ensure Excel and other programs read diacritics correctly
        # index=False prevents pandas from writing a new index column
        filtered_df.to_csv(output_filename, index=False, encoding='utf-8-sig')

        print("-" * 30)
        print(f"Filtering complete!")
        print(f"Original number of rows: {len(df)}")
        print(f"Number of rows after filtering: {len(filtered_df)}")
        print(f"Filtered data has been saved to '{output_filename}'")
        print("-" * 30)

    except FileNotFoundError:
        print(f"ERROR: The input file '{input_filename}' was not found.")
        print("Please make sure you have saved the data into this file in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")