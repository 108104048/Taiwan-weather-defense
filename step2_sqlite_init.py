#建表格

import sqlite3

# 讓 Python 在硬碟中生出一個獨立的 weather.db 資料庫檔案
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# 傳送 SQL 指令給資料庫，在裡面規劃好格子（表格與欄位）
cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        wx TEXT,
        pop TEXT,
        min_t TEXT,
        max_t TEXT
    )
""")

conn.close()
print("【步驟二】空白資料庫與表格建立成功！")
