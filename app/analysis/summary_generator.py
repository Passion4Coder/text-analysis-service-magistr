import re
from typing import List
import ollama
from .adaptive_utils import calculate_optimal_summary_length
from app.core.config import settings
import asyncio
from concurrent.futures import ThreadPoolExecutor

ollama_client = ollama.Client(host=settings.OLLAMA_HOST)
executor = ThreadPoolExecutor()


def split_into_sentences(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in sentences if s.strip()]


async def generate_text_embedding(text: str) -> List[float]:
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            executor,
            lambda: ollama_client.embeddings(
                model=settings.EMBEDDING_MODEL, prompt=text
            ),
        )
        return response["embedding"]
    except Exception as e:
        print(f"Помилка Ollama при генерації ембеддінгу тексту: {e}")
        return []


async def generate_sentence_embeddings(text: str) -> List[List[float]]:
    sentences = split_into_sentences(text)
    if not sentences:
        return []

    embeddings = []
    loop = asyncio.get_running_loop()

    for sentence in sentences:
        try:
            response = await loop.run_in_executor(
                executor,
                lambda: ollama_client.embeddings(
                    model=settings.EMBEDDING_MODEL, prompt=sentence
                ),
            )
            embeddings.append(response["embedding"])
        except Exception as e:
            print(f"Помилка Ollama при генерації ембеддінгу речення: {e}")
            continue

    return embeddings


async def generate_summary_with_keywords(
    keywords: list[str], text_word_count: int
) -> str:
    keywords_str = ", ".join([f'"{k}"' for k in keywords])

    R_opt, L_opt, T_opt = calculate_optimal_summary_length(text_word_count)

    prompt = f"""
    Ти — експертний помічник для генерації **детального, стислого та зв'язного глибокого викладу (Summary)** на основі ключових термінів.
    
    Твоя задача — створити **розгорнутий виклад**, що об'єднує та пояснює взаємозв'язок між наведеними термінами.
    Уяви, що ти пишеш фінальний висновок лекції або розділу навчальної програми.
    
    Обов'язкові вимоги:
    1.  **Формат:** Вивід повинен складатися **2-3 логічно пов'язаних абзаци**, без нумерованих списків чи заголовків.
    2.  **Зміст:** Використовуй **всі** або більшість наданих термінів, інтегруючи їх у змістовну та логічну розповідь.
    3.  **Мова:** Резюме має бути чистою українською мовою.
    4.  **Довжина:** Має складатися з **{R_opt} інформативних речень**, загальною довжиною приблизно **{L_opt} слів**, що розкривають тему.
    
    Ключові терміни: {keywords_str}
    """

    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            executor,
            lambda: ollama_client.chat(
                model=settings.LLM_SUMMARY_MODEL,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                options={"temperature": 0.1, "num_predict": T_opt},
            ),
        )

        return response["message"]["content"].strip()

    except Exception as e:
        return f"Помилка при генерації summary: {e}"
