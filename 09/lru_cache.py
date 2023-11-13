import logging


class LRUCache:
    class OnlyUpperFilter(logging.Filter):
        def filter(self, record):
            method = record.msg.split(":")[0]
            return method.isupper()

    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(
        self, limit=42, log_file_name="cache.log", is_debug=False, is_filter=False
    ):
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("Limit must be a positive integer.")

        self.limit = limit
        self.cache = {}
        self.head = self.Node(None, None)
        self.tail = self.Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

        self.is_debug = is_debug
        self.is_filter = is_filter

        # Getting logger
        self.logger = logging.getLogger("LRUCache")
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            "%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
        )

        # File logging
        self.file_handler = logging.FileHandler(log_file_name, mode="w")
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)
        if self.is_filter:
            self.file_handler.addFilter(self.OnlyUpperFilter())
        self.logger.addHandler(self.file_handler)

        # Stream logging
        if self.is_debug:
            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setLevel(logging.DEBUG)
            self.stream_handler.setFormatter(self.formatter)
            if self.is_filter:
                self.stream_handler.addFilter(self.OnlyUpperFilter())
            self.logger.addHandler(self.stream_handler)

    def get(self, key):
        self.logger.debug("GET: STARTED")
        if key in self.cache:
            self.logger.info("GET: Key '%s' was cached", key)
            node = self.cache[key]
            self._move_to_front(node)
            self.logger.debug("GET: ENDED")
            return node.value
        self.logger.warning("GET: Key '%s' wasn`t found in cache", key)
        self.logger.debug("GET: ENDED")
        return None

    def set(self, key, value):
        self.logger.debug("SET: STARTED")
        if key in self.cache:
            node = self.cache[key]
            self.logger.info(
                "SET: Key '%s' was cached with value '%s', new value '%s'",
                key,
                node.value,
                value,
            )

            node.value = value
            self._move_to_front(node)
        else:
            self.logger.info(
                "SET: Key '%s' wasn`t found in cache so it creating with value '%s'",
                key,
                value,
            )
            self.logger.debug(
                "SET: head id: '%s', tail id: '%s'",
                id(self.head),
                id(self.tail),
            )

            if len(self.cache) >= self.limit:
                self.logger.warning(
                    "SET: CACHE IS FULL len(self.cache): %s, limit: %s, DELETING LAST",
                    len(self.cache),
                    self.limit,
                )
                self._remove_last()

            new_node = self.Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

        self.logger.debug("SET: ENDED")

    def _move_to_front(self, node):
        self.logger.debug(
            "_move_to_front: node {'key': '%s', 'value': '%s', \
                'prev_key': '%s', 'next_key': '%s'} moving to front",
            node.key,
            node.value,
            node.prev.key,
            node.next.key,
        )
        self._remove_node(node)
        self._add_to_front(node)

    def _remove_node(self, node):
        self.logger.debug(
            "_remove_node: node {'key': '%s', 'value': '%s', \
                'prev_key': '%s', 'next_key': '%s'} removing",
            node.key,
            node.value,
            node.prev.key,
            node.next.key,
        )
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node):
        self.logger.debug(
            "_add_to_front: node {'key': '%s', 'value': '%s'}", node.key, node.value
        )
        old_first = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = old_first
        old_first.prev = node
        self.logger.debug(
            "_add_to_front: old_first {id: '%s', key': '%s', 'value': '%s'}",
            id(old_first),
            old_first.key,
            old_first.value,
        )

    def _remove_last(self):
        last_node = self.tail.prev
        self.logger.debug(
            "_remove_last: Last node {id: '%s', 'key': '%s', \
                'value': '%s'} removing from cache & nodes",
            id(last_node),
            last_node.key,
            last_node.value,
        )
        del self.cache[last_node.key]
        self._remove_node(last_node)
