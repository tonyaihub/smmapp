import streamlit as st
import openai
import requests
from googlesearch import search
from bs4 import BeautifulSoup
import random
import datetime
import tweepy
from wordpress_api import Client as WPClient
from PIL import Image
import io
from config import *  # Импорт ключей

openai.api_key = OPENAI_API_KEY

# Языки
LANGUAGES = {"ru": "русский", "uk": "украинский", "en": "английский"}

# Функция для исследования ключевых слов
def research_keywords(niche, lang="ru", num_keywords=10):
    keywords = []
    query = f"{niche} ключевые слова с низкой конкуренцией site:ru" if lang == "ru" else f"{niche} low competition keywords"
    if lang == "uk":
        query = f"{niche} ключові слова з низькою конкуренцією"
    for result in search(query, num_results=num_keywords * 2, lang=lang):
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = [tag.text.strip() for tag in soup.find_all(['h1', 'h2', 'h3'])]
            keywords.extend([t for t in titles if len(t.split()) > 1 and len(t) < 50][:num_keywords])
        except:
            pass
    keywords = list(set(keywords))[:num_keywords]
    if not keywords:
        keywords = [f"Пример ключевого слова для {niche} {i}" for i in range(1, num_keywords + 1)]
    return keywords

# Функция для создания 30-дневного плана контента
def create_content_plan(keywords):
    today = datetime.date.today()
    plan = {}
    for i in range(30):
        date = today + datetime.timedelta(days=i)
        kw = random.choice(keywords) if i >= len(keywords) else keywords[i]
        plan[date.strftime("%Y-%m-%d")] = kw
    return plan

# Функция для генерации статьи
def generate_article(keyword, niche, lang="ru", min_words=1200):
    lang_prompt = f" на {LANGUAGES[lang]} языке"
    prompt = f"Напиши SEO-оптимизированную статью{lang_prompt} по ключевому слову '{keyword}' в нише '{niche}'. Минимальная длина: {min_words} слов. Включи: заголовок, мета-описание, H2/H3 заголовки, списки, таблицы если нужно. Добавь места для внутренних/внешних ссылок и изображений."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    article = response.choices[0].message.content
    
    # Добавляем backlinks
    backlinks = get_backlinks(niche, lang)
    article += "\n\n### Релевантные ссылки:\n" + "\n".join([f"- [{link}]({link})" for link in backlinks[:3]])
    
    # Поиск YouTube видео
    yt_links = search_youtube(keyword, lang)
    if yt_links:
        article += "\n\n### Релевантное видео:\n" + yt_links[0]
    
    return article

# Функция для генерации изображения
def generate_image(description, lang="ru"):
    prompt = f"Generate an image for: {description}" if lang == "en" else f"Сгенерируй изображение для: {description}"
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    image_url = response['data'][0]['url']
    img_data = requests.get(image_url).content
    return Image.open(io.BytesIO(img_data))

# Функция для поиска YouTube видео
def search_youtube(keyword, lang="ru"):
    query = f"{keyword} site:youtube.com"
    yt_links = []
    for result in search(query, num_results=3, lang=lang):
        if "youtube.com/watch" in result:
            yt_links.append(result)
    return yt_links

# Функция для backlinks (симуляция обмена)
def get_backlinks(niche, lang="ru"):
    partners = BACKLINK_PARTNERS.copy()
    query = f"{niche} сайты для обмена backlinks" if lang == "ru" else f"{niche} backlink exchange sites"
    if lang == "uk":
        query = f"{niche} сайти для обміну backlinks"
    for result in search(query, num_results=5, lang=lang):
        partners.append(result)
    return random.sample(partners, min(5, len(partners)))

# Функция автопубликации в WordPress
def publish_to_wp(title, content, wp_url=WP_URL, wp_user=WP_USERNAME, wp_pass=WP_APP_PASSWORD):
    client = WPClient(wp_url + '/wp-json', wp_user, wp_pass)
    post = client.post('posts', {
        'title': title,
        'content': content,
        'status': 'publish'
    })
    return post['link'] if 'link' in post else "Ошибка публикации"

# Функция автопубликации в X (Twitter)
def publish_to_twitter(text, consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET,
                       access_token=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_TOKEN_SECRET):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(text[:280])  # Укорачиваем до лимита
    return "Опубликовано в X"

# Streamlit UI
st.title("Outrank Personal - SEO Автоматизатор")

niche = st.text_input("Введите нишу (например, 'SEO маркетинг')")
lang = st.selectbox("Выберите язык", list(LANGUAGES.keys()), format_func=lambda x: LANGUAGES[x])
num_keywords = st.number_input("Количество ключевых слов", min_value=5, max_value=30, value=10)

if st.button("Исследовать ключевые слова и создать план"):
    keywords = research_keywords(niche, lang, num_keywords)
    st.subheader("Ключевые слова:")
    st.write(keywords)
    
    plan = create_content_plan(keywords)
    st.subheader("30-дневный план контента:")
    for date, kw in plan.items():
        st.write(f"{date}: {kw}")

keyword = st.text_input("Ключевое слово для статьи (из плана)")
if st.button("Генерировать статью"):
    article = generate_article(keyword, niche, lang)
    st.subheader("Сгенерированная статья:")
    st.markdown(article)
    
    # Генерация изображения
    img_desc = st.text_input("Описание для изображения (опционально)")
    if img_desc:
        img = generate_image(img_desc, lang)
        st.image(img, caption="Сгенерированное изображение")
    
    # Backlinks
    st.subheader("Предложенные backlinks:")
    st.write(get_backlinks(niche, lang))

# Автопубликация
st.subheader("Автопубликация")
wp_publish = st.checkbox("Опубликовать в WordPress")
twitter_publish = st.checkbox("Опубликовать в X (Twitter)")

if st.button("Опубликовать"):
    if 'article' in locals():
        title = keyword.capitalize()  # Простой заголовок
        if wp_publish:
            link = publish_to_wp(title, article)
            st.write(f"Опубликовано в WP: {link}")
        if twitter_publish:
            teaser = article[:200] + "... Читать далее"
            result = publish_to_twitter(teaser)
            st.write(result)
    else:
        st.error("Сначала сгенерируйте статью")

# Экспорт
if 'article' in locals():
    st.download_button("Скачать в Markdown", article, file_name="article.md")