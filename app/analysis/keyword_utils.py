import re

UK_STOPWORDS = {
    "і",
    "й",
    "та",
    "але",
    "або",
    "чи",
    "не",
    "на",
    "в",
    "у",
    "до",
    "з",
    "із",
    "ми",
    "ви",
    "вони",
    "він",
    "вона",
    "воно",
    "це",
    "того",
    "тому",
    "як",
    "що",
    "тож",
    "де",
    "коли",
    "який",
    "яка",
    "яке",
    "які",
}


def is_uk_word(word: str) -> bool:
    return bool(re.fullmatch(r"[а-яіїєґ’'-]+", word.lower()))


def clean_keyword(phrase: str) -> str:
    words = phrase.strip().lower().split()
    cleaned_words = []
    for word in words:
        word = re.sub(r"[^а-яіїєґ’'-]+", "", word)
        if len(word) < 3 or word in UK_STOPWORDS or not is_uk_word(word):
            return ""
        cleaned_words.append(word)
    return " ".join(cleaned_words)


def determine_top_n(text: str, base_n: int = 10, max_n: int = 20) -> int:
    word_count = len(text.split())
    return min(max(base_n, word_count // 50), max_n)
