from lru_cache import LRUCache
import argparse


def main():
    parser = argparse.ArgumentParser(description="LRUCache logger")
    parser.add_argument("-s", action="store_true", help="Enable stream logging")
    parser.add_argument("-f", action="store_true", help="Enable filter while logging")
    args = parser.parse_args()

    lc = LRUCache(2, is_debug=args.s, is_filter=args.f)

    lc.get("not_exist")  # get отсутствующего ключа

    lc.set("key1", "val1")  # set отсутствующего ключа

    lc.get("key1")  # get существующего ключа

    # set отсутствующего ключа для достижения предела емкости
    lc.set("key2", "val2")
    lc.set("key3", "val3")  # set отсутствующего ключа, когда достигнута ёмкость

    lc.set("key2", "updated_val2")  # set существующего ключа


if __name__ == "__main__":
    main()
