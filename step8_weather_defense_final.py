#🥊 第三關：try...except...

import sqlite3
import requests
import urllib3

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()
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
print("【步驟二】資料庫與表格建立成功！")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}"
    response = requests.get(url, verify=False)
    data = response.json()

    location = data["records"]["location"]
    for city in location:
        element0 = city["locationName"]
        print("1. 成功鎖定城市:", element0)

        elements = city["weatherElement"]
        element1 = element2 = element3 = element4 = "無資料"
        for element in elements:
            if element["elementName"] == "Wx":
                element1 = element["time"][0]["parameter"]["parameterName"]
            if element["elementName"] == "PoP":
                element2 = element["time"][0]["parameter"]["parameterName"]
            if element["elementName"] == "MinT":
                element3 = element["time"][0]["parameter"]["parameterName"]
            if element["elementName"] == "MaxT":
                element4 = element["time"][0]["parameter"]["parameterName"]

        cursor.execute(
                """
                INSERT INTO weather_table 
                (location, wx, pop, min_t, max_t)
                VALUES (?, ?, ?, ?, ?)
                """,
                (element0, element1, element2, element3, element4),
            )    

    conn.commit()
    conn.close()

    print("寫入成功")

except requests.exceptions.RequestException as e:
  # 🎯 專門抓：任何網路、網址、斷線、逾時或 404/500 問題
  print(f"🚨【網路防禦】API 連線失敗，原因: {e}")

except (ValueError, KeyError) as e:
  # 🎯 專門抓：對方給的資料壞掉、不是 JSON、或是標籤改名
  print(f"🚨【格式防禦】對方回傳的氣象資料格式毀損，無法解析: {e}")

except sqlite3.Error as e:
  # 🎯 專門抓：資料庫鎖死、表格不存在等 SQL 問題
  print(f"🚨【資料庫防禦】SQL 寫入或連線失敗: {e}")

except Exception as e:
  # 🛡️【終極宇宙保險】萬一發生了任何人類沒想到的神祕錯誤（例如電腦記憶體爆掉）
  print(f"🚨【未知防禦】系統發生了神祕的未預期錯誤: {e}")
