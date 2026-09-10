#資料寫入

import sqlite3 #SQL
import requests #取資料
import urllib3 #導入連結

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #關閉憑證警告

api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"
url = f"https://cwa.gov.tw{api_key}&locationName=臺北市"

response = requests.get(url, verify=False) #關閉憑證
data = response.json() #轉json

taipei_data = data["records"]["location"][0]
city = taipei_data["locationName"]  # 取city

elements = taipei_data["weatherElement"]
wx_value = elements[0]["time"][0]["parameter"]["parameterName"]  # 取wx_value

conn = sqlite3.connect("weather.db") #連資料庫
cursor = conn.cursor() #選儲存格

cursor.execute(
    """
    INSERT INTO weather_table (location, wx)
    VALUES (?, ?)
""",
    (city, wx_value),
)

# ⚠️ 最關鍵的一步：存檔確認！ (Commit)
# 資料庫跟一般檔案不同，寫完指令只是草稿，必須下 commit 才會真正寫入硬碟！
conn.commit()

# 關閉連線
conn.close()

print(f"成功將【{city}】的【{wx_value}】寫入 weather.db 資料庫！")
