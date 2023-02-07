import logging, re
from config import colorize
from functools import reduce

logging.getLogger('telethon').setLevel(logging.CRITICAL)

def log(msg: str, name: str | None = None, level: str = 'info'):


    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )

    logger = logging.getLogger(name)

    levels = dict(
        info=logger.info,
        error=logger.error,
        exception=logger.exception
    )
    keywords = {
        'successfuly': colorize('successfully', 'green'),
        'error': colorize('error', 'red'),
        'failed': colorize('failed', 'red'),
        'updated': colorize('updated', 'cyan'),
        'reported': colorize('reported', 'magenta'),
        'joining': colorize('joining', 'yellow')
    }
    msg = reduce(lambda msg, keyword: re.sub(fr'\b{keyword}\b', keywords[keyword], msg, flags=re.IGNORECASE), keywords, msg)
    return levels[level](msg)
