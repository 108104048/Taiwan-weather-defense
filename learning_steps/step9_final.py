import sqlite3
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def init_database(db_path="weather.db"):
    conn = sqlite3.connect(db_path)
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
    conn.commit()
    return conn, cursor


def fetch_and_save_weather(cursor, conn):
    try:
        api_key = "CWA-D6DC001F-FBBC-4FF3-97E5-32546C42234E"
        url =(
    "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    f"?Authorization={api_key}"
)
        response = requests.get(url, verify=False)
        data = response.json()

        location = data["records"]["location"]
        
        cursor.execute("DELETE FROM weather_table")
        
        for city in location:
            element0 = city["locationName"]
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
        return True

    except requests.exceptions.RequestException as e:
        print(f"🚨【網路防禦】API 連線失敗，原因: {e}")
    except (ValueError, KeyError) as e:
        print(f"🚨【格式防禦】對方回傳的氣象資料格式毀損，無法解析: {e}")
    except sqlite3.Error as e:
        print(f"🚨【資料庫防禦】SQL 寫入或連線失敗: {e}")
    except Exception as e:
        print(f"🚨【未知防禦】系統發生了神祕的未預期錯誤: {e}")
    
    return False


def query_by_city(cursor, city_input):
    search_name = city_input.replace("台", "臺").strip()
    cursor.execute(
        "SELECT location, wx, pop, min_t, max_t FROM weather_table WHERE location LIKE ?", 
        (f"%{search_name}%",)
    )
    return cursor.fetchall()


def query_by_pop(cursor, pop_input):
    if not pop_input.isdigit():
        return None
    cursor.execute(
        "SELECT location, wx, pop FROM weather_table WHERE CAST(pop AS INTEGER) >= ?", 
        (int(pop_input),)
    )
    return cursor.fetchall()


def run_interactive_menu(cursor):
    while True:
        print("\n請選擇查詢功能：")
        print("1. 查詢指定縣市氣象")
        print("2. 篩選高降雨機率縣市")
        print("3. 離開系統")
        
        choice = input("請輸入選項 (1/2/3): ").strip()
        
        if choice == "1":
            city_input = input("請輸入想查詢的縣市名稱: ").strip()
            results = query_by_city(cursor, city_input)
            if results:
                for row in results:
                    print(f"📍 縣市: {row[0]} | 天氣狀況: {row[1]} | 降雨機率: {row[2]}% | 溫度: {row[3]}°C ~ {row[4]}°C")
            else:
                print(f"❌ 找不到有關「{city_input}」的氣象資料。")
                
        elif choice == "2":
            pop_input = input("請輸入降雨機率門檻: ").strip()
            results = query_by_pop(cursor, pop_input)
            
            if results is None:
                print("🚨 輸入錯誤！請輸入純數字。")
                continue
                
            if results:
                for row in results:
                    print(f"📍 縣市: {row[0]} | 天氣狀況: {row[1]} | 降雨機率: {row[2]}%")
            else:
                print(f"☀️ 沒有任何縣市的降雨機率大於或等於 {pop_input}%。")
                
        elif choice == "3":
            print("👋 感謝使用，系統已關閉！")
            break
        else:
            print("🚨 無效選項，請重新輸入。")


def main():
    conn, cursor = init_database()
    
    if fetch_and_save_weather(cursor, conn):
        run_interactive_menu(cursor)
        
    conn.close()


if __name__ == "__main__":
    main()
