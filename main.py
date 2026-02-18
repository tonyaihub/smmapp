import streamlit as st
import os
from dotenv import load_dotenv
import openai
import pandas as pd
from st_aggrid import AgGrid

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Outrank Personal", layout="wide")

st.title("🚀 Outrank Personal")

with st.sidebar:
    st.header("Настройки")
    lang = st.selectbox("Язык контента", ["ru", "uk", "en"])
    niche = st.text_input("Ниша")
    st.divider()
    st.caption("API статусы")
    st.success("OpenAI: подключено") if openai.api_key else st.error("OpenAI: ключ отсутствует")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "План контента",
    "Генерация",
    "Публикация",
    "Тренды & Идеи",
    "Аналитика"
])

with tab1:
    st.subheader("30-дневный план")
    # Пример данных
    dates = pd.date_range(start="2026-02-18", periods=30).strftime("%Y-%m-%d")
    plan = pd.DataFrame({"Дата": dates, "Ключевое слово": ["Тема " + str(i) for i in range(1, 31)]})
    AgGrid(plan, editable=True, height=400)

with tab2:
    st.subheader("Генерация контента")
    keyword = st.text_input("Ключевое слово")
    if st.button("Создать статью"):
        st.info("Генерация статьи… (заглушка)")
        st.markdown("**Пример статьи** — здесь будет полный текст 1200+ слов")

with tab3:
    st.subheader("Публикация")
    platforms = st.multiselect("Выберите платформы", ["Instagram Reels", "TikTok", "YouTube Shorts", "Facebook", "X", "Reddit", "WordPress"])
    if st.button("Опубликовать"):
        st.success("Публикация запущена (заглушка)")

with tab4:
    st.subheader("Тренды и идеи")
    if st.button("Обновить тренды"):
        st.info("Сбор трендов… (заглушка)")
        st.markdown("- #AI2026 — рост +420%\n- #Продуктивність — 2.1M просмотров")

with tab5:
    st.subheader("Аналитика постов")
    st.dataframe(pd.DataFrame({
        "Дата": ["2026-02-10", "2026-02-12"],
        "Платформа": ["Instagram", "TikTok"],
        "Views": [45000, 120000],
        "Engagement": ["1.2%", "3.4%"]
    }))

if __name__ == "__main__":
    st.caption("Outrank Personal v1.0 • 2026 • Anton • Kyiv")