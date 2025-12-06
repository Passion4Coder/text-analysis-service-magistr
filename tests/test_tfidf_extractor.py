# from app.methods.tfidf_extractor import extract_keywords_tfidf
# from app.analysis.stopwords_dict import UK_STOPWORDS


# def test_tfidf_basic_output_structure():
#     doc = "Машинне навчання — це галузь штучного інтелекту."
#     res = extract_keywords_tfidf([doc], top_n=5)

#     assert isinstance(res, list)
#     assert len(res) == 1
#     assert isinstance(res[0], list)
#     assert len(res[0]) <= 5

#     for term, score in res[0]:
#         assert isinstance(term, str)
#         assert isinstance(score, float)


# def test_tfidf_detects_expected_keywords():
#     doc = "Машинне навчання — це галузь штучного інтелекту."
#     res = extract_keywords_tfidf([doc], top_n=10)

#     keywords = [t.lower() for t, _ in res[0]]

#     assert any("машинне" in k.lower() for k in keywords)
#     assert any("інтелекту" in k.lower() for k in keywords)


# def test_tfidf_respects_stopwords():
#     doc = "Це приклад речення, яке містить стоп-слова."
#     res = extract_keywords_tfidf([doc], top_n=10)

#     keywords = [t.lower() for t, _ in res[0]]

#     assert not any(k in UK_STOPWORDS for k in keywords)


# def test_tfidf_multiple_documents():
#     docs = ["Штучний інтелект аналізує дані.", "Машинне навчання використовує дані."]

#     res = extract_keywords_tfidf(docs, top_n=5)

#     assert len(res) == 2
#     assert all(isinstance(doc_res, list) for doc_res in res)
