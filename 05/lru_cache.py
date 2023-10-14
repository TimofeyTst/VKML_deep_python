class LRUCache:
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None

    def __init__(self, limit=42):
        if limit <= 0:
            raise ValueError("Limit must be greater than 0.")

        self.limit = limit
        self.cache = {}
        self.head = self.Node(None, None)
        self.tail = self.Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._move_to_front(node)
            return node.value
        return None

    def set(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
        else:
            if len(self.cache) >= self.limit:
                self._remove_last()
            new_node = self.Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_to_front(node)

    def _remove_node(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node):
        old_first = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = old_first
        old_first.prev = node

    def _remove_last(self):
        last_node = self.tail.prev
        del self.cache[last_node.key]
        self._remove_node(last_node)
