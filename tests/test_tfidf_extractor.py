from app.methods.tfidf_extractor import extract_keywords_tfidf


def test_tfidf_ukrainian_keywords():
    doc = "Машинне навчання — це галузь штучного інтелекту, яка дозволяє системам навчатися на основі даних."
    keywords = extract_keywords_tfidf([doc], top_n=5)
    assert len(keywords) == 1
    assert isinstance(keywords[0], list)
    assert len(keywords[0]) <= 5
    assert any("машинне" in term for term, _ in keywords[0])
