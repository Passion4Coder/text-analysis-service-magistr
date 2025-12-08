# ExtractLab (Text Analysis Service)

Система для вилучення, аналізу та структурування тексту з різних форматів файлів (DOCX, PDF, PPTX, TXT) з автоматичним створенням резюме, вилученням ключових слів та виявленням глосарію.

## 👀 Відкриті питання

- Покращення якості відповідності термінів і визначень у глосарії.
- Додавання панелі інтерфейсу для управління завантаженими нотатками.
- Покращення точності гібридного вилучення ключових слів.

## 🚀 Як запустити

1\. Створити віртуальне середовище

```bash
python -m venv venv
```

2\. Активувати віртуальне середовище
Windows PowerShell

```bash
venv\Scripts\Activate
```

Windows CMD

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

3\. Встановити залежності

```bash
pip install -r requirements.txt
```

4\. Створити міграції

```bash
alembic init app/migrations

alembic revision -m "Add a column"

alembic upgrade head

alembic downgrade -1

export PYTHONPATH=$PWD
python app/seed.py
```

5\. Запустити бекенд

Uvicorn:

```bash
uvicorn app.main:app --reload
```

## 📄 Генерація PDF

ExtractLab включає вбудований генератор PDF на основі ReportLab, який підтримує:

- Налаштування форматування тексту
- Виділення ключових слів (TF-IDF, RAKE, Гібрид)
- Розділ «Глосарій»
- Використання шрифтів DejaVuSans
- Автоматичні метадані та нумерацію сторінок

Завантаження PDF через API:

```bash
GET /pdf/summary/{note_id}?method=hybrid
```

## 💻 Вимоги перед внесенням змін

Оновлення requirements.txt

```bash
pip install pipreqs
pipreqs . --force --ignore "venv"
```

## 🐍 Поради для Python

Оновлення пакету:

```bash
pip install --upgrade <package-name>
```

Встановлення конкретної версії:

```bash
pip install <package-name>==<version>
```

Приклад:

```bash
pip install --upgrade reportlab==4.2.2
```

## 🔧 Віртуальне середовище (.venv)

Створення середовища:

```bash
python -m venv .venv
```

Активація:

```bash
source .venv/Scripts/activate        # bash
.venv/Scripts/activate               # cmd
.venv/Scripts/Activate.ps1           # PowerShell
```

## 🧩 Налаштування VSCode

1\. Натисніть Ctrl + Shift + P

2\. Виберіть Python: Select Interpreter

3\. Клацніть Enter interpreter path

4\. Вкажіть:

```bash
.venv/Scripts/python.exe
```

Додайте до .vscode/settings.json:

```bash
{
  "python.terminal.activateEnvironment": true
}
```

Перезапустіть термінал.

## 📚 Використані бібліотеки

- **[FastAPI](https://fastapi.tiangolo.com/)** – фреймворк для створення REST API на Python
- **[Uvicorn](https://www.uvicorn.org/)** – ASGI сервер для запуску FastAPI
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – ORM для роботи з базою даних
- **[asyncpg](https://pypi.org/project/asyncpg/)** – асинхронний драйвер для PostgreSQL
- **[psycopg2-binary](https://pypi.org/project/psycopg2/)** – драйвер PostgreSQL
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** – валідація даних та моделі
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** – завантаження змінних середовища з `.env`
- **[NLTK](https://www.nltk.org/)** – бібліотека для NLP, аналіз тексту
- **[rake-nltk](https://pypi.org/project/rake-nltk/)** – алгоритм для виділення ключових слів
- **[scikit-learn](https://scikit-learn.org/stable/)** – алгоритми машинного навчання (наприклад, TF-IDF)
- **[numpy](https://numpy.org/)** – числові обчислення та підтримка масивів
- **[pandas](https://pandas.pydata.org/)** – обробка табличних даних
- **[scipy](https://www.scipy.org/)** – наукові обчислення та статистика
- **[stanza](https://stanfordnlp.github.io/stanza/)** – NLP pipeline для аналізу тексту
- **[spaCy](https://spacy.io/)** – сучасний NLP фреймворк
- **[ReportLab](https://www.reportlab.com/dev/docs/)** – генерація PDF-документів з кастомним форматуванням
- **[httpx](https://www.python-httpx.org/)** – HTTP-клієнт
- **[pytest](https://docs.pytest.org/)** – тестування
- **[pytest-asyncio](https://pypi.org/project/pytest-asyncio/)** – асинхронне тестування
- **[stop-words](https://pypi.org/project/stop-words/)** – списки стоп-слів для NLP
