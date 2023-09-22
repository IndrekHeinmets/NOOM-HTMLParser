from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from bs4 import BeautifulSoup
import csv
import os

input_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input_data')
output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output.csv')
output_format = 'excel' # 'excel' / 'csv'


def read_htm(path: str):
    with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    

def limit_entries(raw_entries: list, start_lim: str, end_lim: str):
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


def parse_htm(content: list, data: list, filename: str, error: bool):
    raw_entries = BeautifulSoup(content, 'html.parser').find_all('div', class_='S2')
    entries = limit_entries(raw_entries, start_lim='Trükitud', end_lim='Lk.')

    for i in range(0, len(entries), 7):
            try:
                data.append({'NIMETUS': str(entries[i].text.strip().replace(",", ".")),
                            'SEERIA': str(entries[i+1].text.strip().replace(",", ".")),
                            'HIND': float(entries[i+6].text.strip().replace(",", ".")),
                            'LAOJAAK': float(entries[i+2].text.strip().replace(",", ".")),
                            'AEGUMINE': str(entries[i+3].text.strip().replace(",", ".")),
                            'OSAKOND': str(filename[0])})
            except IndexError as Ie:
                print(f'\nFailed to parse line {i} in "{filename}": {Ie}')
                error = True
                continue
            except ValueError as Ve:
                print(f'\nFailed to parse line {i} in "{filename}": {Ve}')
                error = True
                continue
            except Exception as Ex:
                print(f'\nError occured in "{filename}": {Ex}')
                error = True
                break
    return data, error


def write_output(filename: str, data: list, output_format: str = 'csv'):
    if output_format == 'csv':
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[1].keys()))
            writer.writeheader()
            writer.writerows(data)
        print(f'\nData extracted & saved to "{filename}" successfully!')
    elif output_format == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.append(list(data[1].keys()))
        for row in data:
            ws.append(list(row.values()))
        
        # Formatting columns
        for col in ws.columns:
            column = col[0].column_letter
            if column == 'A' or column == 'F':  # 'NIMETUS' and 'OSAKOND'
                for cell in col:
                    cell.number_format = '@'  # text format
            elif column == 'B':  # 'SEERIA'
                for cell in col:
                    cell.number_format = 'General'
            elif column == 'C' or column == 'D':  # 'HIND' and 'LAOJAAK'
                for cell in col:
                    cell.number_format = '0.00'  # number format
            elif column == 'E':  # 'AEGUMINE'
                for cell in col:
                    cell.number_format = 'mm-dd-yy'  # date format

        wb.save(filename)
        print(f'\nData extracted & saved to "{filename}" successfully!')
    else:
        print(f'\nInvalid output format: "{output_format}"')


def main():
    error, exts, data = False, ['.htm', '.html'], []
    for filename in os.listdir(input_folder_path):
        if any(filename.endswith(ext) for ext in exts):
            file_path = os.path.join(input_folder_path, filename)
            data, error = parse_htm(read_htm(file_path), data, filename, error)
    if not error:
        write_output(output_file_path, data, output_format)


if __name__ == '__main__':
     main()
