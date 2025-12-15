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

Выяви все географические объекты и точки остановок. Объекты должны быть точечными, никаких крупных территорий. Для каждой точки определи:
- **id** — уникальный идентификатор (можно просто порядковый номер, начиная с 1)
- **Название** (имя собственное или описательное: "поляна у ручья", "Перевал Орлиный")(Если у точки есть собственное имя записывай его без типа объекта, например "Перевал Орлиный" → "Орлиный")
- **Тип** (озеро, родник, поляна, стоянка, ночёвка, перевал, водопад, вершина, приют, обрыв, пещера, памятник и т.д.)
- **Описание** (краткое, 1-2 предложения, что это за точка)
  - Если это перевал, то вставь полное описание перевала из текста.
- **Категория сложности** — ОБЯЗАТЕЛЬНО ДЛЯ ПЕРЕВАЛОВ.
  - Если в тексте указана категория (например, 1А или 3Б) — используй её. Существуют категории(н/к — некатегорийный, 1А, 1Б, 2А, 2Б, 3А, 3Б, 4А, 4Б, 5А, 5Б).
  - Если категория не указана, но перевал описан как простой (без технических сложностей), проставь "н/к".
  - Для любых других типов объектов этот параметр **не добавляется**.

---

## 2. АНАЛИЗ СЕГМЕНТОВ И ИХ СЛОЖНОСТИ

Раздели весь маршрут на последовательные сегменты.  
**Каждый сегмент — это путь строго между двумя точками: начальной и конечной.**
Не учитывай сегменты включающее города или крупные населённые пункты.

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
  `[ "id точки начала", "id точки конца" ]`(id бери из списка точек маршрута)
- **Описание сегмента** — описание пути между дву точками максимально приближенное к оригинальному тексту.
- **Наличие ночевки** — если в сегменте была ночевка, начался в описании новый день — добавь в поле "is_camp": true, иначе — "is_camp": false.
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
      "is_camp",
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
        model="gpt-4.1-mini", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    url = "https://skitalets.ru/tourism-types/all/otchet-o-gornom-pokhode-1-k-s-po-zapadnomu-kavkazu-arkhyz"

    if not url.startswith(("http://", "https://")):
        print("Неверная ссылка.")
        exit(1)

    full_text = fetch_page_text(url)

    answer_text = call_openai(system_prompt, full_text)


    try:
        parsed = json.loads(answer_text)
    except json.JSONDecodeError:
        parsed = {"error": "LLM did not return valid JSON", "raw": answer_text}

    pois_file = 'parsing/results/pois.json'
    segments_file = 'parsing/results/segments.json'


    required_fields = ["category", "description"]

    pois = parsed["points"]
    segments = parsed["segments"]

    for poi in pois:
        poi.setdefault("category", None)
        poi.setdefault("description", None)
      


    with open(pois_file, "w", encoding="utf-8") as f:
        json.dump(pois, f, ensure_ascii=False, indent=2)

    with open(segments_file, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)