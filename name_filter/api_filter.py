import requests, random
from tqdm import tqdm

import copy
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from .base import BaseFilter
from .utils import get_proxy
from utils.logger import log

if TYPE_CHECKING:
    from name_filter import ChainFilter

class APIFilter(BaseFilter):

    def __init__(self, users: dict) -> None:
        super().__init__(users)
        self.session = requests.Session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }
        self.proxies = get_proxy()
    
    def __del__(self) -> None:
        self.session.close()

    def _filter_name(self, username: str) -> None:
        if not self.users:
            return
        if not username.startswith('NO USERNAME'):
            proxy = random.choice(self.proxies)
            proxies = dict(http=proxy, https=proxy)
            name = self.users[username]['name']
            stripped_name = ''.join([letter for letter in name.split()[0] if letter.isalpha()])
            try:
                response = self.session.get(f'https://api.genderize.io/?name={stripped_name}', headers=self.headers, proxies=proxies, timeout=10)
            except Exception:
                ...
            else:
                json_response = response.json()

                if (result := json_response.get('gender', False)):
                    if json_response.get('probability') >= 0.8:
                        match result:
                            case 'male':
                                self.save(filename='male', user=username)
                            case 'female':
                                self.save(filename='female', user=username)
                        del self.users[username]
                        log(f'{username}:{name} -> {result}')
                        return username
            

    def api_filter(self, workers: int = 50) -> 'ChainFilter':
        copied_users = copy.deepcopy(self.users)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            executor.map(self._filter_name, copied_users)

        return self