import math
from typing import List, Tuple, Sequence, Optional, Dict
from .tfidf_extractor import extract_keywords_tfidf
from .rake_extractor import extract_keywords_rake

from ..analysis.stopwords_dict import UK_STOPWORDS


def _normalize_scores(items: List[Tuple[str, float]]) -> Dict[str, float]:
    if not items:
        return {}
    vals = [v for _, v in items]
    maxv = max(vals)
    minv = min(vals)
    out = {}
    if math.isclose(maxv, minv):
        for k, _ in items:
            out[k] = 1.0
        return out
    for k, v in items:
        out[k] = (v - minv) / (maxv - minv)
    return out


def combine_tfidf_rake(
    docs: Sequence[str],
    top_n: int = 15,
    tfidf_weight: float = 0.6,
    rake_weight: float = 0.4,
    stop_words: Optional[Sequence[str]] = None,
):
    """Повернути комбіновані рейтингові ключові слова для кожного документа у вигляді списку (термін, оцінка)."""
    if stop_words is None:
        stop_words = list(UK_STOPWORDS)
    else:
        stop_words = list(stop_words)

    tfidf_res = extract_keywords_tfidf(docs, top_n=top_n, stop_words=stop_words)
    try:
        rake_res = extract_keywords_rake(docs, top_n=top_n, stop_words=stop_words)
    except Exception:
        rake_res = [[] for _ in docs]

    combined_list = []
    for i, doc in enumerate(docs):
        tfidf_norm = _normalize_scores(tfidf_res[i])
        rake_norm = _normalize_scores(rake_res[i])

        scores: Dict[str, float] = {}
        for term, s in tfidf_norm.items():
            scores[term] = scores.get(term, 0.0) + tfidf_weight * s
        for term, s in rake_norm.items():
            scores[term] = scores.get(term, 0.0) + rake_weight * s

        stopset = set(stop_words)
        filtered = []
        for term, score in scores.items():
            t = term.strip()
            tokens = [tok for tok in t.split() if tok]
            if not tokens:
                continue
            if all(tok in stopset for tok in tokens):
                continue
            if all(len(tok) <= 2 for tok in tokens):
                continue
            filtered.append((t, score))

        ranked = sorted(filtered, key=lambda x: x[1], reverse=True)
        combined_list.append(ranked[:top_n])

    return combined_list
