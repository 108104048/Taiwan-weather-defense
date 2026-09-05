#🥊 第一關：擴大管線（熟悉 Python 字典提取）
#用 for 迴圈把全台灣 22 個縣市的天氣現象（Wx）通通印出來

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
conn.close()
print("【步驟二】資料庫與表格建立成功！")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}"
response = requests.get(url, verify=False)
data = response.json()

location = data["records"]["location"]
for city in location:
    print("1. 成功鎖定城市:", city["locationName"])

    elements = city["weatherElement"]
    for element in elements:
        if element["elementName"] == "Wx":
            first_element_name = element["elementName"]
            first_element_value = element["time"][0]["parameter"]["parameterName"]

            print(f"2. 找到標籤名稱: {first_element_name}")
            print(f"3. 該標籤接下來8小時的預報內容: {first_element_value}")