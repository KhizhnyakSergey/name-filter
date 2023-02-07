from config import path

from transliterate import translit


def translit_name(filename: str):
    with open(filename, 'r+', encoding='utf-8') as file:
        data = [name for raw in file.readlines() if (name := raw.strip()) and len(name) > 3]
        transliterated = [translit(name, 'ru') for name in data]

        data += transliterated
        file.seek(0, 0)
        for name in data:
            file.write(f'{name}\n')
        file.truncate()


def drop_dublicates(filename: str) -> None:
        with open(path('source', 'filter_names', f'{filename}.txt'), 'r+', encoding='utf-8') as file:
            data = {row for raw in file.read().split('\n') if (row := raw.strip())}
            file.seek(0)
            for row in data:
                file.write(f'{row}\n')
            file.truncate()
        
# translit_name('female_names.txt')
drop_dublicates('female_names')
drop_dublicates('male_names')
