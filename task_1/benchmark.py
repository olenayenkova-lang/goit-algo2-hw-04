import random
import string
import timeit

from main import Homework

random.seed(42)
N = 200_000
words = ["".join(random.choices(string.ascii_lowercase, k=random.randint(4, 12))) for _ in range(N)]
words = list(dict.fromkeys(words))  # унікальні слова
N = len(words)
suffixes = ["ab", "xyz", "e", "ing", "qw"]

t0 = timeit.default_timer()
trie = Homework()
for i, w in enumerate(words):
    trie.put(w, i)
build = timeit.default_timer() - t0


def naive(p):
    return sum(1 for w in words if w.endswith(p))


for p in suffixes:
    assert trie.count_words_with_suffix(p) == naive(p)

t_trie = timeit.timeit(lambda: [trie.count_words_with_suffix(p) for p in suffixes], number=100) / 100
t_naive = timeit.timeit(lambda: [naive(p) for p in suffixes], number=3) / 3
t_pref = timeit.timeit(lambda: [trie.has_prefix(p) for p in suffixes], number=1000) / 1000

print(f"Слів: {N}; побудова дерева: {build:.2f} с")
print(f"count_words_with_suffix (5 запитів): trie = {t_trie*1e6:.1f} мкс, послідовний перебір = {t_naive*1e3:.1f} мс")
print(f"has_prefix (5 запитів): {t_pref*1e6:.1f} мкс")
print(f"Прискорення: ~{t_naive/t_trie:,.0f}x")
