from config import path


class BaseFilter:
    """Base filter class"""
    __slots__ = ('users', )

    def __init__(self, users: dict) -> None:
        self.users = users
        
    @staticmethod
    def drop_dublicates(filename: str) -> None:
        with open(path('output', f'{filename}.txt'), 'r+', encoding='utf-8') as file:
            data = {row for raw in file.read().split('\n') if (row := raw.strip())}
            file.seek(0)
            for row in data:
                file.write(f'{row}\n')
            file.truncate()

    @staticmethod
    def save(filename: str, user: str) -> None:
        with open(path('output', f'{filename}.txt'), 'a', encoding='utf-8') as file:
            file.write(f'\n{user}')
            
    