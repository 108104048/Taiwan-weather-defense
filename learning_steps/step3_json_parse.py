#資料清洗

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"
url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName=臺北市"

response = requests.get(url, verify=False)
data = response.json()

taipei_data = data["records"]["location"][0]
print("1. 成功鎖定城市:", taipei_data["locationName"])

elements = taipei_data["weatherElement"]

first_element_name = elements[0]["elementName"]
first_element_value = elements[0]["time"][0]["parameter"]["parameterName"]

print(f"2. 找到標籤名稱: {first_element_name}")
print(f"3. 該標籤接下來8小時的預報內容: {first_element_value}")

