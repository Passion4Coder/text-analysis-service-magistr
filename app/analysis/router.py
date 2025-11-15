from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from analysis.service import analyze_and_save
from analysis.stopwords_dict import UK_STOPWORDS
from methods.rake_extractor import extract_keywords_rake
from methods.tfidf_extractor import extract_keywords_tfidf

router = APIRouter(prefix="/analysis", tags=["Analysis"])


class AnalysisRequestTfidf(BaseModel):
    content: str
    top_n: int = 10
    ngram_range: tuple[int, int] = (1, 2)
    max_features: int | None = 5000


class AnalysisRequestRake(BaseModel):
    content: str
    top_n: int = 10


class AnalysisRequestHybrid(BaseModel):
    title: Optional[str] = None
    content: str
    method_name: str = "hybrid"
    text_id: Optional[int] = None


@router.post("/tfidf", summary="Отримати ключові слова за методом TF-IDF")
async def analyze_tfidf(data: AnalysisRequestTfidf):
    keywords = extract_keywords_tfidf(
        [data.content],
        top_n=data.top_n,
        ngram_range=data.ngram_range,
        max_features=data.max_features,
        stop_words=UK_STOPWORDS,
    )
    return {"method": "TF-IDF", "keywords": keywords}


@router.post("/rake", summary="Отримати ключові слова за методом RAKE")
async def analyze_rake(data: AnalysisRequestRake):
    keywords = extract_keywords_rake(
        [data.content],
        top_n=data.top_n,
        stop_words=UK_STOPWORDS,
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
