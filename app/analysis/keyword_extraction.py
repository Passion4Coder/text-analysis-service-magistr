from keybert import KeyBERT
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from .embeddings import model
from .keyword_utils import clean_keyword, determine_top_n
from .ukrainian_stop_words import UK_STOPWORDS

executor = ThreadPoolExecutor(max_workers=4)
kw_model = KeyBERT(model=model)


def _extract_keywords_sync(
    text: str,
    top_n: int,
    diversity: float,
) -> List[Tuple[str, float]]:
    top_n = determine_top_n(text, base_n=top_n)
    raw_keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 1),
        stop_words=list(UK_STOPWORDS),
        top_n=top_n * 3,
        use_mmr=True,
        diversity=diversity,
    )

    cleaned = []
    seen = set()
    for phrase, score in raw_keywords:
        cleaned_phrase = clean_keyword(phrase)
        if cleaned_phrase and cleaned_phrase not in seen:
            cleaned.append((cleaned_phrase, score))
            seen.add(cleaned_phrase)
        if len(cleaned) >= top_n:
            break

    return cleaned


async def extract_keywords(
    text: str, top_n: int = 10, diversity: float = 0.5
) -> List[Tuple[str, float]]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        executor, lambda: _extract_keywords_sync(text, top_n, diversity)
    )
