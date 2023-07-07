from bs4 import BeautifulSoup
import csv
import os

input_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_data')
output_filename = 'output.csv'


def read_htm(path):
    with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    

def limit_entries(raw_entries, start_lim: str, end_lim: str):
    limits, entries = [], []
    start_indexes = [i for i, entry in enumerate(raw_entries) if entry.text.strip() == start_lim]
    end_indexes = [i for i, entry in enumerate(raw_entries) if entry.text.strip() == end_lim]

    for start_index in start_indexes:
            end_index = next((i for i in end_indexes if i > start_index), None)
            if end_index is not None:
                limits.append((start_index + 1, end_index - 3))

    for limits in limits:
        start_index, end_index = limits
        entries.extend(raw_entries[start_index:end_index])
    return entries


def parse_htm(content, data):
    raw_entries = BeautifulSoup(content, 'html.parser').find_all('div', class_='S2')
    entries = limit_entries(raw_entries, start_lim='Trükitud', end_lim='Lk.')

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
    return data


def write_output(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f'Data extracted & saved to {filename} successfully!')


def main():
    data = []
    for filename in os.listdir(input_folder_path):
        if filename.endswith('.htm'):
            file_path = os.path.join(input_folder_path, filename)
            data.append({'NIMETUS': '_', 'SEERIA': '_', 'HIND': str(filename), 'LAOJAAK': '_', 'AEGUMINE': '_'})
            data = parse_htm(read_htm(file_path), data)
    write_output(output_filename, data)


if __name__ == '__main__':
     main()
