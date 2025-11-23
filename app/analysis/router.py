from fastapi import APIRouter, HTTPException
from app.analysis.schemas import (
    AnalysisRequestHybrid,
    AnalysisRequestRake,
    AnalysisRequestTfidf,
    AnalysisResultList,
    AnalysisResultRead,
)
from app.analysis.service import (
    analyze_and_save,
    fetch_all_analyses,
    fetch_analysis_by_text_id,
)
from app.analysis.stopwords_dict import UK_STOPWORDS
from app.methods.rake_extractor import extract_keywords_rake
from app.methods.tfidf_extractor import extract_keywords_tfidf

router = APIRouter(prefix="/analysis", tags=["Результати 🔍"])


@router.post("/tfidf", summary="Отримати ключові слова за методом TF-IDF")
async def analyze_tfidf(data: AnalysisRequestTfidf):
    keywords = extract_keywords_tfidf(
        [data.content],
        top_n=data.top_n,
        ngram_range=data.ngram_range,
        max_features=data.max_features,
        stop_words=list(UK_STOPWORDS),
    )
    return {"method": "TF-IDF", "keywords": keywords}


@router.post("/rake", summary="Отримати ключові слова за методом RAKE")
async def analyze_rake(data: AnalysisRequestRake):
    keywords = extract_keywords_rake(
        [data.content],
        top_n=data.top_n,
        stop_words=list(UK_STOPWORDS),
    )
    return {"method": "RAKE", "keywords": keywords}


@router.post(
    "/hybrid", summary="Отримати ключові слова за комбінованим методом TF-IDF + RAKE"
)
async def analyze_text(data: AnalysisRequestHybrid):
    result = await analyze_and_save(
        content=data.content,
        title=data.title,
        text_id=data.text_id,
        method_name=data.method_name,
    )
    return result


@router.get(
    "/list",
    summary="Отримати список усіх проаналізованих текстів",
    response_model=AnalysisResultList,
)
async def get_analysis_list():
    analyses = await fetch_all_analyses()
    return {"count": len(analyses), "items": analyses}


@router.get(
    "/{text_id}",
    summary="Отримати повний результат аналізу",
    response_model=AnalysisResultRead,
)
async def get_analysis(text_id: int):
    analysis = await fetch_analysis_by_text_id(text_id)

    if analysis is None:
        raise HTTPException(status_code=404, detail="Аналіз не знайдено.")

    return analysis


@router.get("/{text_id}/keywords", summary="Отримати лише ключові слова")
async def get_keywords_only(text_id: int):
    analysis = await fetch_analysis_by_text_id(text_id)

    if analysis is None:
        raise HTTPException(status_code=404, detail="Аналіз не знайдено.")

    return {"keywords": analysis.get("keywords", [])}
