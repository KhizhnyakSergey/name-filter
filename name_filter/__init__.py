from .main_filter import DefaultFilter
from .name_filter import NameFilter
from .api_filter import APIFilter


class ChainFilter(NameFilter, APIFilter, DefaultFilter):
    ...