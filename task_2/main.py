from trie import Trie


class LongestCommonWord(Trie):
    """Пошук найдовшого спільного префікса за допомогою префіксного дерева."""

    def find_longest_common_word(self, strings) -> str:
        if not isinstance(strings, (list, tuple)):
            raise TypeError("strings must be a list of strings.")
        if not strings:
            return ""
        for s in strings:
            if not isinstance(s, str):
                raise TypeError(f"All items must be strings, got {type(s).__name__}.")
        if any(s == "" for s in strings):
            return ""  # порожній рядок → спільного префікса немає

        Trie.__init__(self)  # скидаємо дерево, щоб не змішувати виклики
        for i, s in enumerate(strings):
            self.put(s, i)

        # Йдемо вниз, доки шлях однозначний (рівно одна дитина)
        # і жодне слово тут не закінчується.
        prefix = []
        node = self.root
        while len(node.children) == 1 and node.value is None:
            ch, node = next(iter(node.children.items()))
            prefix.append(ch)
        return "".join(prefix)


if __name__ == "__main__":
    # Тести
    trie = LongestCommonWord()
    strings = ["flower", "flow", "flight"]
    assert trie.find_longest_common_word(strings) == "fl"

    trie = LongestCommonWord()
    strings = ["interspecies", "interstellar", "interstate"]
    assert trie.find_longest_common_word(strings) == "inters"

    trie = LongestCommonWord()
    strings = ["dog", "racecar", "car"]
    assert trie.find_longest_common_word(strings) == ""

    # --- Додаткові перевірки ---
    t = LongestCommonWord()
    assert t.find_longest_common_word([]) == ""
    assert t.find_longest_common_word(["alone"]) == "alone"
    assert t.find_longest_common_word(["flow", "flower"]) == "flow"  # слово-префікс
    assert t.find_longest_common_word(["same", "same"]) == "same"
    assert t.find_longest_common_word(["abc", ""]) == ""
    assert t.find_longest_common_word(["Abc", "abc"]) == ""          # регістр
    assert t.find_longest_common_word(["flower", "flow", "flight"]) == "fl"  # повторний виклик

    for bad in (None, "abc", 123, [1, 2], ["a", None], ["a", 5]):
        try:
            t.find_longest_common_word(bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"{bad!r} має кидати TypeError")

    print("Усі тести пройдено.")
