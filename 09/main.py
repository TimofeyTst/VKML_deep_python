from lru_cache import LRUCache
from logger import get_lru_cache_logger, OnlyUpperFilter
import argparse


def main():
    parser = argparse.ArgumentParser(description="LRUCache logger")
    parser.add_argument("-s", action="store_true", help="Enable stream logging")
    parser.add_argument("-f", action="store_true", help="Enable filter while logging")
    args = parser.parse_args()

    logger_filter = OnlyUpperFilter() if args.f else None
    logger = get_lru_cache_logger(
        log_file_name="cache.log", is_debug=args.s, logger_filter=logger_filter
    )
    lc = LRUCache(2, logger)

    lc.get("not_exist")  # get отсутствующего ключа

    lc.set("key1", "val1")  # set отсутствующего ключа

    lc.get("key1")  # get существующего ключа

    # set отсутствующего ключа для достижения предела емкости
    lc.set("key2", "val2")
    lc.set("key3", "val3")  # set отсутствующего ключа, когда достигнута ёмкость

    lc.set("key2", "updated_val2")  # set существующего ключа


if __name__ == "__main__":
    main()
