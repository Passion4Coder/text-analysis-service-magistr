import pytest
from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())


@pytest.mark.integration
def test_tfidf_api():
    data = {
        "content": "Машинне навчання — це галузь штучного інтелекту.",
        "top_n": 5,
        "ngram_range": (1, 2),
        "max_features": 5000,
    }
    response = client.post("/analysis/tfidf", json=data)
    assert response.status_code == 200
    res = response.json()
    assert res["method"] == "TF-IDF"
    keywords = res["keywords"]
    assert isinstance(keywords, list) and len(keywords) == 1
    for term, score in keywords[0]:
        assert isinstance(term, str)
        assert isinstance(score, float)


@pytest.mark.integration
def test_rake_api():
    data = {"content": "Штучний інтелект є основою сучасних технологій.", "top_n": 5}
    response = client.post("/analysis/rake", json=data)
    assert response.status_code == 200
    res = response.json()
    assert res["method"] == "RAKE"
    keywords = res["keywords"]
    assert isinstance(keywords, list) and len(keywords) == 1
    for phrase, score in keywords[0]:
        assert isinstance(phrase, str)
        assert isinstance(score, float)


@pytest.mark.integration
def test_hybrid_api():
    data = {
        "content": "Машинне навчання і штучний інтелект працюють разом.",
        "method_name": "hybrid",
    }
    response = client.post("/analysis/hybrid", json=data)
    assert response.status_code == 200
    res = response.json()
    assert "keywords" in res
    keywords = res["keywords"]
    assert isinstance(keywords, list) and len(keywords) > 0

    for kw in keywords:
        assert isinstance(kw, dict)
        assert "term" in kw
        assert "score" in kw
        assert isinstance(kw["term"], str)
        assert isinstance(kw["score"], float)
