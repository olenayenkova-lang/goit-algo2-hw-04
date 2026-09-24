from trie import Trie


class _SuffixNode:
    __slots__ = ("children", "count")

    def __init__(self):
        self.children = {}
        self.count = 0  # скільки слів має суфікс, що веде до цього вузла


class Homework(Trie):
    """Trie з підтримкою підрахунку слів за суфіксом та перевірки префікса.

    Окрім прямого дерева (базовий Trie), підтримується дзеркальне дерево
    слів, записаних навпаки. У кожному його вузлі зберігається лічильник
    слів, що проходять через вузол, тому кількість слів із суфіксом
    визначається за O(m), де m — довжина шаблону.
    """

    def __init__(self):
        super().__init__()
        self._suffix_root = _SuffixNode()

    @staticmethod
    def _check_str(value, name):
        if not isinstance(value, str):
            raise TypeError(f"{name} must be a string, got {type(value).__name__}.")

    def put(self, key, value=None):
        is_new = self.get(key) is None  # також валідує key
        super().put(key, value)
        if is_new:  # повторне додавання слова не має дублювати лічильники
            node = self._suffix_root
            node.count += 1
            for ch in reversed(key):
                node = node.children.setdefault(ch, _SuffixNode())
                node.count += 1

    def count_words_with_suffix(self, pattern) -> int:
        self._check_str(pattern, "pattern")
        node = self._suffix_root
        for ch in reversed(pattern):
            node = node.children.get(ch)
            if node is None:
                return 0
        return node.count

    def has_prefix(self, prefix) -> bool:
        self._check_str(prefix, "prefix")
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return False
        # порожній префікс збігається з будь-яким словом, якщо дерево не порожнє
        return self.size > 0


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat

    # --- Додаткові перевірки ---
    assert trie.count_words_with_suffix("xyz") == 0          # немає слів
    assert trie.count_words_with_suffix("E") == 0            # регістр
    assert trie.count_words_with_suffix("apple") == 1        # суфікс = слово
    assert trie.count_words_with_suffix("applesauce") == 0   # довший за слово
    assert trie.has_prefix("App") == False                   # регістр
    assert trie.has_prefix("applications") == False

    trie.put("apple", 99)                                    # дубль слова
    assert trie.count_words_with_suffix("e") == 1

    trie.put("pineapple", 10)
    assert trie.count_words_with_suffix("apple") == 2
    assert trie.count_words_with_suffix("le") == 2

    # Некоректні вхідні дані
    for bad in (None, 123, 3.14, ["a"], b"a"):
        for method in (trie.count_words_with_suffix, trie.has_prefix):
            try:
                method(bad)
            except TypeError:
                pass
            else:
                raise AssertionError(f"{method.__name__}({bad!r}) має кидати TypeError")

    # Порожнє дерево
    empty = Homework()
    assert empty.count_words_with_suffix("a") == 0
    assert empty.has_prefix("a") == False
    assert empty.has_prefix("") == False

    print("Усі тести пройдено.")
