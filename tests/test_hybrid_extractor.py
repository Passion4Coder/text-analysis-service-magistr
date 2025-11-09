from app.methods.hybrid_extractor import combine_tfidf_rake


def test_hybrid_basic():
    doc = "Машинне навчання — це галузь штучного інтелекту, яка дозволяє системам навчатися на основі даних."
    res = combine_tfidf_rake([doc], top_n=5)
    assert isinstance(res, list)
    assert len(res) == 1
    assert isinstance(res[0], list)
    assert len(res[0]) <= 5
