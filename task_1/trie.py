class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None


class Trie:
    """Базове префіксне дерево (аналог trie.py з курсу)."""

    def __init__(self):
        self.root = TrieNode()
        self.size = 0

    def put(self, key, value=None):
        if not isinstance(key, str) or not key:
            raise TypeError("Key must be a non-empty string.")
        if value is None:
            value = True
        node = self.root
        for ch in key:
            node = node.children.setdefault(ch, TrieNode())
        if node.value is None:
            self.size += 1
        node.value = value

    def get(self, key):
        if not isinstance(key, str) or not key:
            raise TypeError("Key must be a non-empty string.")
        node = self.root
        for ch in key:
            node = node.children.get(ch)
            if node is None:
                return None
        return node.value

    def __len__(self):
        return self.size
