import asyncio
import re
from concurrent.futures import ThreadPoolExecutor
from typing import List

import ollama

from app.core.config import settings

from app.analysis.adaptive_utils import calculate_optimal_summary_length

ollama_client = ollama.Client(host=settings.OLLAMA_HOST)
executor = ThreadPoolExecutor()


def _split_into_sentences(text: str) -> List[str]:
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
    sentences = _split_into_sentences(text)
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


async def llm_keyword_refinement(
    title: str,
    initial_keywords: List[str],
) -> List[str]:
    initial_keywords_str = ", ".join(initial_keywords)

    prompt = f"""
    Ти — експерт з аналізу текстів і ключових слів. Твоє завдання - відібрати ключові слова та фрази, які найбільш точно описують тему тексту.
    
    Вхідні дані:
    - Тема поданого тексту: "{title}"
    - Початковий список ключових слів: {initial_keywords_str}
    
    Завдання:
    1. Відфільтруй слова, які не відповідають темі тексту.
    2. Залиш змістовні ключові слова та короткі фрази (1-3 слова), які реально описують тему.
    3. Не роби буквальну нормалізацію усіх слів у леми, залиш змістовні словосполучення (наприклад, "футбольний клуб", "чемпіонат Іспанії").
    4. Вибери лише найбільш релевантні ключові слова/фрази, які найкраще розкривають тему.
    5. Не додавай зайвого тексту, коментарів або пояснень.
    6. Поверни результат **через кому**, без лапок, пояснень нумерації або додаткового тексту.

    """

    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            executor,
            lambda: ollama_client.chat(
                model=settings.LLM_SUMMARY_MODEL,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.0, "num_predict": 64},
            ),
        )

        raw_output = response["message"]["content"].strip()

        filtered_keywords = [
            kw.strip().replace('"', "").capitalize()
            for kw in raw_output.split(",")
            if kw.strip()
        ]

        return filtered_keywords

    except Exception as e:
        return f"Помилка LLM-фільтрації та нормалізації ключових слів: {e}"


async def generate_summary_with_keywords(
    title: str, keywords: list[str], text_word_count: int
) -> str:
    keywords_str = ", ".join([f'"{k}"' for k in keywords])

    R_opt, L_opt, T_opt = calculate_optimal_summary_length(text_word_count)

    prompt = f"""
    Ти — помічник, який генерує максимально детальний, глибокий, стислий, логічний та зв'язний висновок (summary) на основі теми та поданих ключових слів.
    
    Мета роботи — побудувати якісний summary, який пояснює основну ідею тексту та демонструє взаємозв'язок між ключовими словами.
    
    Тема роботи (title): "{title}"
    
    Ключові слова: {keywords_str}
    
    Оптимальні параметри викладу:
    - Кількість речень: {R_opt}
    - Орієнтована довжина: {L_opt} слів
    
    Створи 2-3 логічно пов'язані абзаци українською мовою, де:
    1. Тема документа (title) має задавати основний контекст викладу.
    2. Ключові слова повинні бути природно інтегровані у текст, без їхнього перенасичення.
    3. Результат тексту має розкривати зміст таким чином, ніби це фінальний висновок лекції або розділу навчального матеріалу.
    4. Мова повинна бути чіткою та без формальних маркерів (списків, заголовків).
    5. Уникай поверхневих фраз.
    6. Дотримуйся заданої довжини: {R_opt} речень і приблизно {L_opt} слів.
    
    Якщо ключові слова частково суперечать темі або виходять за її межі - інтегруй їх так, щоб вони підтримували розкриття теми, але не спотворювали її.
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
