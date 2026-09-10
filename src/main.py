import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
import scraper

def run_interactive_menu(cursor):
    while True:
        print("\n請選擇查詢功能：")
        print("1. 依縣市查詢")
        print("2. 篩選高降雨機率縣市")
        print("3. 離開系統")
        
        choice = input("請輸入選項 (1/2/3): ").strip()
        
        if choice == "1":
            city_input = input("請輸入想查詢的縣市名稱: ").strip()
            results = database.query_by_city(cursor, city_input)
            if results:
                for row in results:
                    print(f"📍 縣市: {row} | 天氣狀況: {row} | 降雨機率: {row}% | 溫度: {row}°C ~ {row}°C")
            else:
                print(f"❌ 找不到有關「{city_input}」的氣象資料。")
                
        elif choice == "2":
            pop_input = input("請輸入降雨機率門檻: ").strip()
            results = database.query_by_pop(cursor, pop_input)
            
            if results is None:
                print("🚨 輸入錯誤！請輸入純數字。")
                continue
                
            if results:
                for row in results:
                    print(f"📍 縣市: {row} | 天氣狀況: {row} | 降雨機率: {row}%")
            else:
                print(f"☀️ 沒有任何縣市的降雨機率大於或等於 {pop_input}%。")
                
        elif choice == "3":
            print("👋 感謝使用，系統已關閉！")
            break
        else:
            print("🚨 無效選項，請重新輸入。")

def main():
    conn, cursor = database.init_database()
    
    if scraper.fetch_and_save_weather(cursor, conn):
        run_interactive_menu(cursor)
        
    conn.close()

if __name__ == "__main__":
    main()
