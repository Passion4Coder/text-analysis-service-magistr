from app.methods.hybrid_extractor import combine_tfidf_rake
from app.analysis.stopwords_dict import UK_STOPWORDS


def test_hybrid_structure():
    doc = "Машинне навчання — це галузь штучного інтелекту."
    res = combine_tfidf_rake([doc], top_n=5)

    assert isinstance(res, list)
    assert len(res) == 1
    assert isinstance(res[0], list)
    assert len(res[0]) <= 5

    for term, score in res[0]:
        assert isinstance(term, str)
        assert isinstance(score, float)


def test_hybrid_detects_keywords():
    doc = "Машинне навчання і штучний інтелект працюють разом."
    res = combine_tfidf_rake([doc], top_n=10)

    terms = [t for t, _ in res[0]]

    assert any("машинне" in t for t in terms)
    assert any("інтелект" in t for t in terms)


def test_hybrid_no_stopwords():
    doc = "Це текст, який містить багато стоп-слів, але вони не повинні потрапити у результат."
    res = combine_tfidf_rake([doc], top_n=15)

    terms = [t for t, _ in res[0]]

    assert not any(t in UK_STOPWORDS for t in terms)


def test_hybrid_multiple_docs():
    docs = ["Штучний інтелект аналізує дані.", "Машинне навчання використовує дані."]
    res = combine_tfidf_rake(docs, top_n=5)

    assert len(res) == 2
    assert all(isinstance(doc_res, list) for doc_res in res)
