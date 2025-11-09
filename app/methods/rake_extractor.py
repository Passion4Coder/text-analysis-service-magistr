from rake_nltk import Rake
from typing import List, Tuple, Optional, Sequence
from stop_words import get_stop_words


def extract_keywords_rake(
    docs: Sequence[str],
    top_n: int = 10,
    stop_words: Optional[Sequence[str]] = None,
) -> List[List[Tuple[str, float]]]:
    """Повернути ключові слова RAKE для кожного документа у вигляді (фраза, оцінка)."""
    if stop_words is None:
        stop_words = get_stop_words("ukrainian")

    results = []
    for doc in docs:
        r = Rake(stopwords=set(stop_words), language="uk")
        r.extract_keywords_from_text(doc)
        ranked = [
            (phrase, score) for phrase, score in r.get_ranked_phrases_with_scores()
        ]
        results.append(ranked[:top_n])
    return results
