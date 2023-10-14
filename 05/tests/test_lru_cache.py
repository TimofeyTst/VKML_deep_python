import pytest
from lru_cache import LRUCache
import functools

functools.lru_cache


def test_lru_cache_overflow_deleting_last():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")

    assert cache.get("k1") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k3") == "val3"


def test_lru_cache_exist_after_get_empty_key():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k1") == "val1"
    assert cache.get("k2") == "val2"


def test_lru_cache_overflow_del_after_empty_key_in_correct_order():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k1") == "val1"
    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None


def test_lru_cache_overflow_deleting_last_use():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


def test_lru_cache_not_keep_key1_after_100_inserts():
    cache = LRUCache(2)

    for i in range(1, 101):
        key = f"key{i}"
        value = f"val{i}"
        cache.set(key, value)

    # После 100 вставок key1 должен остаться
    assert cache.get("key1") is None
    assert cache.get("key99") == "val99"
    assert cache.get("key100") == "val100"


def test_lru_cache_keep_key1_after_100_inserts():
    cache = LRUCache(2)
    key1 = "key1"
    val1 = "val1"

    for i in range(1, 101):
        key = f"key{i}"
        value = f"val{i}"
        cache.set(key, value)
        assert cache.get(key1) == val1

    # После 100 вставок key1 должен остаться
    assert cache.get(key1) == val1
    assert cache.get("key99") is None
    assert cache.get("key100") == "val100"


def test_lru_cache_keep_all_keys_after_not_full():
    cache = LRUCache(10000)

    for i in range(1, 1001):
        key = f"k{i}"
        value = f"val{i}"
        cache.set(key, value)

    for i in range(1, 1001):
        key = f"k{i}"
        value = f"val{i}"
        assert cache.get(key) == value

    for i in range(1001, 10001):
        key = f"k{i}"
        value = f"val{i}"
        assert cache.get(key) is None

    assert cache.get("k1") == "val1"


def test_lru_cache_keep_all_keys_after_full():
    cache = LRUCache(1000)

    for i in range(1, 1001):
        key = f"k{i}"
        value = f"val{i}"
        cache.set(key, value)

    for i in range(1, 1001):
        key = f"k{i}"
        value = f"val{i}"
        assert cache.get(key) == value

    assert cache.get("k1") == "val1"


def test_lru_cache_zero_cache():
    with pytest.raises(ValueError, match="Limit must be greater than 0."):
        LRUCache(0)


def test_lru_cache_default_size():
    default_size = 42
    insert_iters = 100
    cache = LRUCache()

    # Добавляем 100 значений
    for i in range(1, insert_iters + 1):
        key = f"k{i}"
        value = f"val{i}"
        cache.set(key, value)

    for i in range(1, default_size + 1):
        key = f"k{i}"
        assert cache.get(key) is None

    for i in range(insert_iters - default_size + 1, 101):
        key = f"k{i}"
        value = f"val{i}"
        assert cache.get(key) == value


def test_lru_cache_access_nonexistent_key():
    cache = LRUCache(3)

    assert cache.get("nonexistent_key") is None


def test_lru_cache_update_to_zero():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    # Обновляем значение "k1" до нуля
    cache.set("k1", "val0")

    # Проверяем, что "k1" все еще доступен
    assert cache.get("k1") == "val0"
    assert cache.get("k2") == "val2"
