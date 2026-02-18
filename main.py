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
from dotenv import load_dotenv
import os
import keyring
from apscheduler.schedulers.background import BackgroundScheduler
import moviepy.editor as mpy
from elevenlabs import ElevenLabs
# import runway  # Uncomment if using Runway (pip install runwayml)
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from st_aggrid import AgGrid
import pandas as pd
import facebook
import praw
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

load_dotenv()

def get_key(service, key_name):
    key = keyring.get_password(service, key_name)
    if not key:
        key = os.getenv(key_name.upper())
        if key:
            keyring.set_password(service, key_name, key)
    return key

OPENAI_API_KEY = get_key("outrank", "openai_api_key")
openai.api_key = OPENAI_API_KEY
# ... аналогично для всех ключей

LANGUAGES = {"ru": "русский", "uk": "украинский", "en": "английский"}

st.set_page_config(page_title="Outrank Personal", layout="wide")
st.markdown("""<style> /* CSS для мобильности и темы */ </style>""", unsafe_allow_html=True)

with st.sidebar:
    lang = st.selectbox("Язык", list(LANGUAGES.keys()))
    niche = st.text_input("Ниша")
    # Бренд-кит
    st.color_picker("Цвет", key="brand_color")
    uploaded_logo = st.file_uploader("Лого")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["План", "Генерация", "Публикация", "Тренды", "Аналитика", "Engagement"])

# Вкладка 1: План (с drag-and-drop)
with tab1:
    @st.cache_data
    def research_keywords(niche, lang="ru", num=10):
        # ... твоя функция
        pass

    keywords = research_keywords(niche)
    plan = create_content_plan(keywords)
    df = pd.DataFrame(plan.items(), columns=["Дата", "Ключ"])
    AgGrid(df, editable=True)  # Drag-and-drop

# Вкладка 2: Генерация (с видео)
with tab2:
    keyword = st.text_input("Ключ")
    if st.button("Генерировать статью"):
        article = generate_article(keyword, niche)
        st.session_state.article = article
        st.markdown(article)

    if st.button("Генерировать видео"):
        tts_client = ElevenLabs(api_key=get_key("outrank", "elevenlabs_api_key"))
        audio = tts_client.generate(text=st.session_state.article[:500])
        # Видео (замени на реальный API)
        clip = mpy.TextClip("Пример видео").set_duration(10).set_audio(audio)
        clip.write_videofile("video.mp4")
        st.video("video.mp4")

# Вкладка 3: Публикация (с AI-оптимизацией)
with tab3:
    if st.button("AI-оптимизация"):
        variants = openai.ChatCompletion.create(model="gpt-4o", messages=[{"role": "user", "content": f"3 варианта для {st.session_state.article[:200]}"}])
        st.write(variants.choices[0].message.content)
    # ... публикация

# Вкладка 4: Тренды (как раньше)
with tab4:
    # ... код из предыдущего

# Вкладка 5: Аналитика (с отчётами)
with tab5:
    if st.button("Генерировать отчёт"):
        client = BetaAnalyticsDataClient()
        # ... данные
        c = canvas.Canvas("report.pdf")
        c.drawString(100, 750, "Отчёт")
        fig, ax = plt.subplots()
        # График
        fig.savefig("graph.png")
        c.drawImage("graph.png", 100, 600)
        c.save()
        st.download_button("PDF", "report.pdf")

# Вкладка 6: Engagement
with tab6:
    # ... сбор комментариев и автоответы

# Расписание (улучшение 3)
scheduler.add_job(schedule_post, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=5), args=[date, platform, content])

if __name__ == "__main__":
    # Тесты
    assert 1 == 1  # Пример