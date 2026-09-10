import sqlite3

# 1. 連接資料庫檔案
conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# 2. 執行查詢指令 (按下 Enter 查表)
cursor.execute("SELECT * FROM weather_table")

# 3. 💡 關鍵動作：把查到的結果「抓出來」 (fetchall)
# execute 只是讓游標鎖定資料，必須下 fetchall() 才會把所有整齊的資料打包成清單傳回 Python
rows = cursor.fetchall()

# 4. 用迴圈一列一列印出資料庫裡面的內容
print("----【資料庫查詢結果】----")
for row in rows:
  # row 會是一個元組，對應 (id, location, wx, pop, min_t, max_t)
  print(
      f"ID: {row[0]} | 城市: {row[1]} | 天氣: {row[2]} | 降雨機率: {row[3]}"
  )

# 5. 關閉連線
conn.close()
