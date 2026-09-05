#🥊 第二關：多元素清洗（熟悉多欄位寫入）
#取 PoP（降雨機率）、MinT（最低溫）、MaxT（最高溫）匯入資料庫。

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

api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}"
response = requests.get(url, verify=False)
data = response.json()

location = data["records"]["location"]
for city in location:
    element0 = city["locationName"]
    print("1. 成功鎖定城市:", element0)

    elements = city["weatherElement"]
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