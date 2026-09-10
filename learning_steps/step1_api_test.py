#確認連線

import requests

api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"

url = (
    "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    f"?Authorization={api_key}"
)

response = requests.get(url, verify=False)

print("狀態碼:", response.status_code)
print("資料內容:", response.text[:200])


