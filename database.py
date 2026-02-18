import sqlite3

def init_db():
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS content_plan
                 (id INTEGER PRIMARY KEY, keyword TEXT, date TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY, keyword TEXT, content TEXT, meta_desc TEXT, images TEXT, lang TEXT)''')
    conn.commit()
    conn.close()

def add_to_plan(keyword, date):
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO content_plan (keyword, date, status) VALUES (?, ?, 'pending')", (keyword, date))
    conn.commit()
    conn.close()

# Add similar functions for get_plan, update_status, store_article, etc.