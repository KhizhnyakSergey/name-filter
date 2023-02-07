import os, json

from name_filter import ChainFilter
from config import path
from utils.logger import log


def main():
    for file in os.listdir(path('data')):
        if file.endswith('.json'):
            with open(path('data', file), 'r', encoding='utf-8') as f:
                data = json.load(f)
            filt = ChainFilter(users=data)
            log(f'Group --> {file}')
            # filt.gender_filter('female').gender_filter('male').api_filter().base_filter().drop_dublicates('male')
            filt.gender_filter('male').gender_filter('female').api_filter().base_filter().drop_dublicates('male')
            
        

if __name__ == '__main__':
    main()