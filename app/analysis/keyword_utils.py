import re
import spacy
from .ukrainian_stop_words import UK_STOPWORDS

try:
    nlp = spacy.load("uk_core_news_md")
    print("SpaCy (uk_core_news_md) успішно ініціалізовано.")
except Exception as e:
    print(f"Помилка ініціалізації SpaCy: {e}. Буде використано лише очищення.")
    nlp = None


def is_uk_word(word: str) -> bool:
    return bool(re.fullmatch(r"[а-яіїєґ’'-]+", word.lower()))


def clean_keyword(phrase: str) -> str:
    words = phrase.strip().lower().split()

    if len(words) >= 2 and words[0] == words[1]:
        words.pop(0)

    text_to_process = " ".join(words)

    if nlp:
        doc = nlp(text_to_process)
        lemmas = []

        for token in doc:
            word_cleaned = re.sub(r"[^а-яіїєґ’'-]+", "", token.text.lower())

            lemma = token.lemma_
            if lemma in ("-PRON-", " "):
                lemma = word_cleaned

            if len(words) == 1 and lemma.endswith("ації"):
                lemma = lemma[:-1] + "я"

            if word_cleaned.startswith("ю") and len(word_cleaned) < 8:
                return ""

            if (
                not word_cleaned
                or len(lemma) < 3
                or lemma in UK_STOPWORDS
                or not is_uk_word(lemma)
            ):
                return ""

            lemmas.append(lemma)

        if lemmas:
            return " ".join(lemmas)
        else:
            return ""

    cleaned_words = []
    for word in words:
        word_cleaned = re.sub(r"[^а-яіїєґ’'-]+", "", word)

        if (
            not word_cleaned
            or len(word_cleaned) < 3
            or word_cleaned in UK_STOPWORDS
            or not is_uk_word(word_cleaned)
        ):
            return ""

        cleaned_words.append(word_cleaned)

    return " ".join(cleaned_words)


def determine_top_n(text: str, base_n: int = 10, max_n: int = 20) -> int:
    word_count = len(text.split())
    return min(max(base_n, word_count // 50), max_n)
