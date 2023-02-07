import pymorphy2
from tqdm import tqdm
from transliterate import translit
from gender_guesser.detector import Detector

import unicodedata, copy
from typing import TYPE_CHECKING

from .base import BaseFilter
from utils.logger import log


if TYPE_CHECKING:
    from name_filter import ChainFilter


class DefaultFilter(BaseFilter):
    
    def __init__(self, users: dict) -> None:
        super().__init__(users)
        self.en_gender = Detector(case_sensitive=False)
        self.ru_gender = pymorphy2.MorphAnalyzer()
        

    def base_filter(self) -> 'ChainFilter':
        users = copy.deepcopy(self.users)
        for k, v in tqdm(users.items(), ascii=False, desc=f'BaseFilter', total=len(users)):
            name = v['name'].split()[0].strip() if len(v['name'].split()) >= 1 else v['name'].strip()
            if name:
                stripped_name = ''.join([letter for letter in name if letter.isalpha()])
                stripped_name = unicodedata.normalize('NFKD', stripped_name)
                
                en_name = translit(stripped_name, 'ru', reversed=True)
                en_gender = self.en_gender.get_gender(en_name)

                ru_name = translit(stripped_name, 'ru')
                ru_gender = self.ru_gender.parse(ru_name.capitalize())[0].tag.gender

                # log(f'RU: {ru_gender} || EN: {en_gender}')

                if not k.startswith('NO USERNAME'): 
                    username = name.split('_')[0]
                    en_username = translit(username, 'ru', reversed=True)
                    u_en_gender = self.en_gender.get_gender(en_username)
                    
                    ru_username = translit(username, 'ru')
                    u_ru_gender = self.ru_gender.parse(ru_username.capitalize())[0].tag.gender
                    self._filter(
                        username=k, 
                        en_gender=en_gender,
                        ru_gender=ru_gender,
                        r_en_gender=u_en_gender,
                        r_ru_gender=u_ru_gender
                        )
            del self.users[k]

        return self


    def _filter(self, username: str, en_gender: str, ru_gender: str, r_en_gender: str, r_ru_gender: str):

        match [en_gender, ru_gender, r_en_gender, r_ru_gender]:
            case ['male', None, 'female', None]:
                self.save(filename='female', user=username)
            case ['male', None, None, 'femn']:
                self.save(filename='female', user=username)
            case ['male', None, 'unknown', 'femn']:
                self.save(filename='female', user=username)
            case ['unknown', 'masc', 'unknown', 'femn']:
                self.save(filename='female', user=username)
            case ['male', 'femn', 'unknown', 'femn']:
                self.save(filename='female', user=username)
            case ['male', 'femn', None, 'femn']:
                self.save(filename='female', user=username)
            case ['male', 'femn', 'unknown', 'femn']:
                self.save(filename='female', user=username)
            case ['female', 'masc', 'female', 'femn']:
                self.save(filename='female', user=username)
            case ['female', 'masc', 'male', 'masc']:
                self.save(filename='male', user=username)
            case ['female', 'masc', None, None]:
                self.save(filename='female', user=username)
            case ['female', 'masc', 'unknown', 'femn']:
                self.save(filename='female', user=username)
            case [None, 'masc', 'male', 'masc']:
                self.save(filename='male', user=username)
            case [None, 'masc', 'male', None]:
                self.save(filename='male', user=username)
            case [None, 'masc', 'female', None]:
                self.save(filename='female', user=username)
            case [None, 'masc', 'unknown', None]:
                self.save(filename='female', user=username)
            case [None, 'femn', None, None ]:
                self.save(filename='female', user=username)
            case [None, 'femn', 'female', None ]:
                self.save(filename='female', user=username)
            case [None, 'femn', None, 'female' ]:
                self.save(filename='female', user=username)
            case [None, None, 'unknown', None]:
                self.save(filename='male', user=username)
            case [None, None, 'mostly_male', None]:
                self.save(filename='male', user=username)
            case [None, None, 'mostly_female', None]:
                self.save(filename='female', user=username)
            case ['unknown', None, 'unknown', None]:
                self.save(filename='male', user=username)
            case ['unknown', None, 'unknown', 'masc']:
                self.save(filename='male', user=username)
            case ['unknown', None, 'female', 'femn']:
                self.save(filename='female', user=username)
            case ['unknown', None, None, 'femn']:
                self.save(filename='female', user=username)
            case ['unknown', None, 'female', None]:
                self.save(filename='female', user=username)
            case ['mostly_female', 'femn', 'female', 'femn']:
                self.save(filename='female', user=username)
            case ['mostly_female', None, 'female', 'femn']:
                self.save(filename='female', user=username)
            case ['mostly_female', None, 'female', 'masc']:
                self.save(filename='female', user=username)
            case ['mostly_female', 'masc', 'female', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_female', 'masc', 'male', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_female', 'masc', 'male', None]:
                self.save(filename='male', user=username)
            case ['mostly_female', 'masc', None, None]:
                self.save(filename='female', user=username)
            case ['mostly_female', 'masc', 'unknown', None]:
                self.save(filename='female', user=username)
            case ['mostly_female', None, 'male', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_female', None, 'male', 'femn']:
                self.save(filename='female', user=username)
            case ['mostly_male', None, 'male', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_male', None, 'male', 'femn']:
                self.save(filename='male', user=username)
            case ['mostly_male', None, None, 'femn']:
                self.save(filename='male', user=username)
            case ['mostly_male', 'masc', None, 'femn']:
                self.save(filename='male', user=username)
            case ['mostly_male', 'masc', 'unknown', 'femn']:
                self.save(filename='male', user=username)
            case ['mostly_male', 'masc', 'unknown', None]:
                self.save(filename='male', user=username)
            case ['mostly_male', 'masc', None, None]:
                self.save(filename='male', user=username)
            case ['mostly_male', 'femn', None, None]:
                self.save(filename='male', user=username)
            case ['mostly_male', 'femn', 'unknown', None]:
                self.save(filename='male', user=username)
            case ['mostly_male', 'femn', 'unknown', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_male', 'femn', 'male', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_male', 'femn', 'male', 'femn']:
                self.save(filename='male', user=username)
            case ['mostly_male', 'femn', None, 'femn']:
                self.save(filename='female', user=username)
            case ['mostly_female', 'masc', None, None]:
                self.save(filename='female', user=username)
            case ['mostly_female', 'masc', None, None]:
               self.save(filename='female', user=username)
            case ['mostly_female', 'masc', 'unknown', None]:
                self.save(filename='female', user=username)
            case ['mostly_female', 'masc', 'unknown', 'femn']:
                self.save(filename='female', user=username)
            case ['mostly_female', 'masc', 'male', 'femn']:
                self.save(filename='male', user=username)
            case ['mostly_female', 'masc', 'male', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_female', None, 'male', 'masc']:
                self.save(filename='male', user=username)
            case ['mostly_female', None, 'female', 'masc']:
                self.save(filename='female', user=username)
            case ['mostly_female', None, 'female', 'femn']:
                self.save(filename='female', user=username)
            case ['male', 'femn', 'male', *_]:
                self.save(filename='male', user=username)
            case ['male', 'femn', 'female', *_]:
                self.save(filename='female', user=username)
            case ['unknown', 'femn', *_]:
               self.save(filename='female', user=username)
            case ['male', 'masc', *_]:
                self.save(filename='male', user=username)
            case ['female', 'femn', *_]:
                self.save(filename='male', user=username)
            case ['female', None, *_]:
                self.save(filename='female', user=username)
            case ['male', None, *_]:
                self.save(filename='male', user=username)
            case ['unknown', 'masc', *_]:
                self.save(filename='male', user=username)
            case _:
                self.save(filename='male', user=username)