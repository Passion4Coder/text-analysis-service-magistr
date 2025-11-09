from typing import List, Optional, Tuple, Sequence
from sklearn.feature_extraction.text import TfidfVectorizer
import re

uk_stopwords = [
    "і",
    "в",
    "у",
    "на",
    "з",
    "до",
    "та",
    "але",
    "що",
    "як",
    "це",
    "то",
    "ж",
    "ви",
    "ми",
    "він",
    "вона",
    "вони",
    "цей",
    "такий",
    "той",
    "або",
    "чи",
    "для",
    "про",
    "після",
    "перед",
    "через",
    "тому",
    "бути",
    "є",
    "був",
    "була",
    "аби",
    "де",
    "коли",
    "так",
    "ні",
]


def _simple_preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^0-9a-z\u0400-\u04FF\s\-]", " ", text)
    return text.strip()


def extract_keywords_tfidf(
    docs: Sequence[str],
    top_n: int = 10,
    ngram_range: Tuple[int, int] = (1, 2),
    stop_words: Optional[Sequence[str]] = None,
    max_features: Optional[int] = 5000,
) -> List[List[Tuple[str, float]]]:
    """Повернути рейтингові списки (токен, бал) для кожного документа.

    stop_words: if None -> за замовчуванням використовуються українські стоп-слова.
    """
    cleaned = [_simple_preprocess(d) for d in docs]

    if stop_words is None:
        stop_words = uk_stopwords

    vectorizer = TfidfVectorizer(
        stop_words=stop_words, ngram_range=ngram_range, max_features=max_features
    )
    X = vectorizer.fit_transform(cleaned)
    feature_names = vectorizer.get_feature_names_out()

    results: List[List[Tuple[str, float]]] = []
    for i in range(X.shape[0]):
        row = X.getrow(i)
        coo = row.tocoo()
        tuples = list(zip(coo.col, coo.data))
        ranked = sorted(
            ((feature_names[idx], float(score)) for idx, score in tuples),
            key=lambda x: x[1],
            reverse=True,
        )
        results.append(ranked[:top_n])
    return results
