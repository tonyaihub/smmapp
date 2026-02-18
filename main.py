import streamlit as st
import openai
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import random
import datetime

# Вставьте ваш OpenAI API ключ здесь
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# Функция для исследования ключевых слов (симуляция: поиск релевантных запросов с низкой конкуренцией)
def research_keywords(niche, num_keywords=10):
    keywords = []
    query = f"{niche} ключевые слова с низкой конкуренцией"
    for result in search(query, num_results=num_keywords * 2, lang="ru"):
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Извлекаем потенциальные ключевые слова из заголовков и текста
            titles = [tag.text.strip() for tag in soup.find_all(['h1', 'h2', 'h3'])]
            keywords.extend([t for t in titles if len(t.split()) > 1 and len(t) < 50][:num_keywords])
        except:
            pass
    keywords = list(set(keywords))[:num_keywords]  # Удаляем дубликаты
    if not keywords:
        keywords = [f"Пример ключевого слова для {niche} {i}" for i in range(1, num_keywords + 1)]
    return keywords

# Функция для создания 30-дневного плана контента
def create_content_plan(keywords):
    today = datetime.date.today()
    plan = {}
    for i, kw in enumerate(keywords):
        date = today + datetime.timedelta(days=i)
        plan[date.strftime("%Y-%m-%d")] = kw
    # Дополняем план, если ключевых слов меньше 30
    while len(plan) < 30:
        date = today + datetime.timedelta(days=len(plan))
        plan[date.strftime("%Y-%m-%d")] = random.choice(keywords)
    return plan

# Функция для генерации SEO-оптимизированной

