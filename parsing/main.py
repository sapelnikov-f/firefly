import requests
from bs4 import BeautifulSoup
import json
from openai import OpenAI
import llm_config

API_KEY = llm_config.API_KEY 

system_prompt = """
Ты — опытный помощник для анализа туристических отчётов. Твоя задача — преобразовать текстовое описание похода в структурированные данные о точках маршрута и его сегментах с оценкой сложности.

### ИНСТРУКЦИЯ:
Проанализируй предоставленный текст и выполни два последовательных действия.

---

## 1. ИЗВЛЕЧЕНИЕ ТОЧЕК МАРШРУТА

Выяви все географические объекты и точки остановок. Для каждой точки определи:

- **Название** (имя собственное или описательное: "поляна у ручья", "Перевал Орлиный")
- **Тип** (озеро, родник, поляна, стоянка, ночёвка, перевал, река, хребет, водопад, вершина, приют, обрыв, пещера, памятник и т.д.)
- **Краткое описание** (1–2 предложения: ключевая характеристика, причина упоминания, внешний вид)
- **Категория сложности** — ОБЯЗАТЕЛЬНО ДЛЯ ПЕРЕВАЛОВ.
  - Если в тексте указана категория (например, 1А или 3Б) — используй её.
  - Если категория не указана — присвоить значение и записать **"None"**.
  - Для любых других типов объектов этот параметр **не добавляется**.

---

## 2. АНАЛИЗ СЕГМЕНТОВ И ИХ СЛОЖНОСТИ

Раздели весь маршрут на последовательные сегменты.  
**Каждый сегмент — это путь строго между двумя точками: начальной и конечной.**

 Если в описании движение идёт через несколько точек подряд, разбивай на цепочку сегментов:

пример  
"лагерь → поляна → перевал → озеро"  
превращается в 3 сегмента:  
- лагерь → поляна  
- поляна → перевал  
- перевал → озеро  

Для каждого сегмента укажи:

- **Порядковый номер** (1, 2, 3, …)
- **Точки_в_сегменте** — строго массив из ДВУХ названий:  
  `[ "точка начала", "точка конца" ]`
- **Описание сегмента** — краткое объяснение, что происходило между этими двумя точками.
- **Сложность (вес)** — оценка от 1 до 5:

    *1 (очень легко):* ровная тропа, препятствий почти нет  
    *2 (легко):* лёгкие подъёмы/спуски  
    *3 (средне):* продолжительный подъём/спуск, камни, корни  
    *4 (трудно):* крутой рельеф, элементы страховки  
    *5 (очень трудно):* экстремальные участки, техническое лазание, ледник, опасные переправы

---

## 3. ФОРМАТ ОТВЕТА (строго JSON)

Верни один JSON-объект:

{
  "points": [
    {
      "name": "...",
      "type": "...",
      "category": "...",
      "description": "..."
    }
  ],
  "segments": [
    {
      "index": 1,
      "start_end": ["...", "..."],
      "segment_description": "...",
      "difficulty": 3
    }
  ]
}

Если точек нет — верни пустой список.
"""

def fetch_page_text(url: str) -> str:
    """Скачать страницу и собрать текст."""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return "\n".join(soup.stripped_strings)


def call_openai(system_prompt: str, user_text: str) -> str:
    """Отправить запрос к OpenAI ChatCompletion API."""
    client = OpenAI(api_key=API_KEY)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # можешь заменить на gpt-4.1, gpt-4.1-turbo, o3-mini
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    url = "https://skitalets.ru/tourism-types/all/otchet-o-pokhode-1-k-s-po-z-kavkazu-arkhyz-teberda"

    if not url.startswith(("http://", "https://")):
        print("Неверная ссылка.")
        exit(1)

    full_text = fetch_page_text(url)

    user_text = full_text[:5000]  # как и раньше — ограничение

    answer_text = call_openai(system_prompt, user_text)

    # Попробуем распарсить JSON
    try:
        parsed = json.loads(answer_text)
    except json.JSONDecodeError:
        parsed = {"error": "LLM did not return valid JSON", "raw": answer_text}

    with open("parsing/output.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)

    print("Готово! Ответ сохранён в output.json")