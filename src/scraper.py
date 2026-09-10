import sqlite3
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_and_save_weather(cursor, conn):
    try:
        api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"
        url = ("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"f"?Authorization={api_key}")
        response = requests.get(url, verify=False)
        data = response.json()

        cursor.execute("DELETE FROM weather_table")

        location = data["records"]["location"]        
        for city in location:
            element0 = city["locationName"]
            elements = city["weatherElement"]
            element1 = element2 = element3 = element4 = "無資料"
            
            for element in elements:
                if element["elementName"] == "Wx":
                    element1 = element["time"]["parameter"]["parameterName"]
                if element["elementName"] == "PoP":
                    element2 = element["time"]["parameter"]["parameterName"]
                if element["elementName"] == "MinT":
                    element3 = element["time"]["parameter"]["parameterName"]
                if element["elementName"] == "MaxT":
                    element4 = element["time"]["parameter"]["parameterName"]

            cursor.execute(
                """
                INSERT INTO weather_table 
                (location, wx, pop, min_t, max_t)
                VALUES (?, ?, ?, ?, ?)
                """,
                (element0, element1, element2, element3, element4),
            )    

        conn.commit()
        return True

    except requests.exceptions.RequestException as e:
        print(f"🚨【連線錯誤】API 連線失敗，原因: {e}")
    except (ValueError, KeyError) as e:
        print(f"🚨【格式錯誤】回傳資料格式無法解析: {e}")
    except sqlite3.Error as e:
        print(f"🚨【資料庫錯誤】SQL 寫入或連線失敗: {e}")
    except Exception as e:
        print(f"🚨【未知錯誤】系統未知錯誤: {e}")
    
    return False
