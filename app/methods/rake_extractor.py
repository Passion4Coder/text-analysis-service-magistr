import re
from typing import List, Tuple, Optional, Sequence
from rake_nltk import Rake

from ..analysis.stopwords_dict import UK_STOPWORDS


ABBREVIATIONS = [
    "т.д",
    "т.п",
    "і.т.д",
    "і.н",
    "напр",
    "ім",
    "проф",
    "ст",
    "вул",
    "просп",
    "пл",
    "обл",
    "р",
]

ABBR_PATTERN = "|".join(re.escape(a) for a in ABBREVIATIONS)

SENTENCE_SPLIT_REGEX = re.compile(
    r"""
        ([.!?…])              
        ["”»]*                
        \s+                  
        (?=                   
            [A-ZА-ЯІЇЄ]       
        )
    """,
    re.VERBOSE | re.UNICODE,
)


def advanced_sentence_split(text: str) -> List[str]:
    """Надійний sentence splitter без lookbehind."""
    marked = SENTENCE_SPLIT_REGEX.sub(r"\1<SPLIT>", text)

    parts = marked.split("<SPLIT>")
    sentences = []

    for i in range(len(parts)):
        part = parts[i].strip()

        if not part:
            continue

        if re.search(rf"(?:{ABBR_PATTERN})\.$", part):
            if i + 1 < len(parts):
                full = part + " " + parts[i + 1]
                sentences.append(full.strip())
            continue

        sentences.append(part)

    return sentences


def normalize_phrase(phrase: str) -> str:
    phrase = phrase.lower()
    phrase = re.sub(r"\s+", " ", phrase).strip()
    return phrase


def deduplicate_ranked_phrases(
    ranked: List[Tuple[str, float]],
) -> List[Tuple[str, float]]:
    seen = set()
    result = []
    for phrase, score in ranked:
        norm = normalize_phrase(phrase)
        if norm not in seen:
            seen.add(norm)
            result.append((norm, score))
    return result


def extract_keywords_rake(
    docs: Sequence[str],
    top_n: int = 10,
    stop_words: Optional[Sequence[str]] = None,
) -> List[List[Tuple[str, float]]]:
    """Повернути ключові слова RAKE для кожного документа у вигляді (фраза, оцінка)."""
    if stop_words is None:
        stop_words = list(UK_STOPWORDS)
    else:
        stop_words = list(stop_words)

    results = []
    for doc in docs:
        r = Rake(
            stopwords=set(stop_words),
            language="uk",
            sentence_tokenizer=advanced_sentence_split,
        )
        r.extract_keywords_from_text(doc)

        ranked = [
            (phrase, score) for score, phrase in r.get_ranked_phrases_with_scores()
        ]
        ranked = deduplicate_ranked_phrases(ranked)
        results.append(ranked[:top_n])

    return results
