import copy
from typing import TYPE_CHECKING

from tqdm import tqdm

from .base import BaseFilter
from config import path

if TYPE_CHECKING:
    from name_filter import ChainFilter


class NameFilter(BaseFilter):

    def __init__(self, users: dict, female_filename: str = 'female_names', male_filename: str = 'male_names') -> None:
        super().__init__(users)
        self.female_filename = female_filename
        self.male_filename = male_filename

    @staticmethod
    def _get_names_to_check(filename: str):
        with open(path('source', 'filter_names', f'{filename}.txt'), 'r', encoding='utf-8') as file:
            return tuple(map(lambda line: line.strip(), file))


    def gender_filter(self, gender: str) -> 'ChainFilter':
        match gender:
            case 'male':
                gender_file = self.male_filename
            case 'female':
                gender_file = self.female_filename
            case _:
                raise Exception('Incorrect gender')

        users = copy.deepcopy(self.users)
        names = self._get_names_to_check(filename=gender_file)

        for k, v in tqdm(users.items(), ascii=False, desc=f'Filter {gender}', total=len(users)):
            user_name = v['name'].lower().strip()
            if not k.startswith('NO USERNAME'):
                for name in names:
                    if name.lower() in user_name.lower() or name.lower() in k.lower():
                        self.save(filename=gender, user=k)
                        del self.users[k]
                        break
        return self
                
