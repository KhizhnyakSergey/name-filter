from config import path

def get_proxy(foldername: str = 'source', filename: str = 'proxy') -> tuple:
    with open(path(foldername, f'{filename}.txt'), 'r', encoding='utf-8') as file:
        return tuple(map(lambda proxy: proxy.strip(), file))
