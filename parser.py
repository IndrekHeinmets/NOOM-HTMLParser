from bs4 import BeautifulSoup
import csv
import os

folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_data')
out_filename = 'output.csv'

for filename in os.listdir(folder_path):
    if filename.endswith('.htm'):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        limits, entries = [], []
        raw_entries = BeautifulSoup(content, 'html.parser').find_all('div', class_='S2')
        start_indexes = [i for i, entry in enumerate(raw_entries) if entry.text.strip() == 'Trükitud']
        end_indexes = [i for i, entry in enumerate(raw_entries) if entry.text.strip() == 'Lk.']

        for start_index in start_indexes:
            end_index = next((i for i in end_indexes if i > start_index), None)
            if end_index is not None:
                limits.append((start_index + 1, end_index - 3))

        for limits in limits:
            start_index, end_index = limits
            entries.extend(raw_entries[start_index:end_index])

        data = []
        for i in range(0, len(entries), 7):
            try:
                nimetus = entries[i].text.strip().replace(",", ".")
                seeria = entries[i+1].text.strip().replace(",", ".")
                hind = entries[i+6].text.strip().replace(",", ".")
                laojaak = entries[i+2].text.strip().replace(",", ".")
                aegumine = entries[i+3].text.strip().replace(",", ".")
                data.append({'NIMETUS': str(nimetus),
                            'SEERIA': str(seeria),
                            'HIND': float(hind),
                            'LAOJAAK': float(laojaak),
                            'AEGUMINE': str(aegumine)})
            except IndexError:
                continue

with open(out_filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)

print(f"Data extracted and saved to {out_filename} successfully.")
