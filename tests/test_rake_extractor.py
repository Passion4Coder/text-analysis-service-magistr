from app.methods.rake_extractor import extract_keywords_rake
from app.analysis.stopwords_dict import UK_STOPWORDS


def test_rake_basic_structure():
    doc = "Машинне навчання є частиною штучного інтелекту."
    res = extract_keywords_rake([doc], top_n=5)

    assert isinstance(res, list)
    assert len(res) == 1
    assert isinstance(res[0], list)
    assert len(res[0]) <= 5

    for phrase, score in res[0]:
        assert isinstance(phrase, str)
        assert isinstance(score, float)


def test_rake_finds_keywords():
    doc = "Штучний інтелект є основою сучасних технологій."
    res = extract_keywords_rake([doc], top_n=10)

    phrases = [p for p, _ in res[0]]

    assert any("штучний інтелект" in p for p in phrases)


def test_rake_respects_stopwords():
    stops = list(UK_STOPWORDS)
    doc = "Це дуже простий приклад для перевірки роботи стоп-слів."
    res = extract_keywords_rake([doc], top_n=15)

    phrases = [p for p, _ in res[0]]

    for phrase in phrases:
        for word in phrase.split():
            assert word not in stops
