from typing import Optional
import re

try:
    import stanza

    _STANZA_OK = True
except Exception:
    _STANZA_OK = False

_stanza_pipeline = None


def ensure_stanza():
    global _stanza_pipeline
    if not _STANZA_OK:
        return None
    if _stanza_pipeline is None:
        try:
            stanza.download("uk", verbose=False)
        except Exception:
            return None
        _stanza_pipeline = stanza.Pipeline(
            "uk", processors="tokenize,mwt,pos,lemma", use_gpu=False
        )
    return _stanza_pipeline


def preprocess_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def lemmatize_text(text: str) -> Optional[str]:
    """Повернути лематизований текст, якщо stanza доступна, інакше None."""
    pipe = ensure_stanza()
    if not pipe:
        return None

    doc = pipe(text)
    lemmas = []
    allowed_pos = {"NOUN", "ADJ", "VERB"}

    for sent in doc.sentences:
        for w in sent.words:
            lemmas.append(w.lemma)
            if w.upos in allowed_pos:
                lemmas.append(w.lemma.lower())

    return " ".join(lemmas)
