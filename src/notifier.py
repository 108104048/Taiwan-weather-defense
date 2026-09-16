import requests

def send_line_notification(token, message):
    url = "https://line.me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "message": message
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            print("🚀 LINE Notify 警報發送成功！")
            return True
        else:
            print(f"🚨 LINE 發送失敗，狀態碼: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"🚨【網路防禦】LINE 通知發送異常: {e}")
    return False

def check_and_alert_rain(cursor, token):
    cursor.execute("SELECT location, pop FROM weather_table WHERE CAST(pop AS INTEGER) >= 60")
    results = cursor.fetchall()
    
    if not results:
        print("☀️ 今日全台縣市降雨機率皆未達 60%，不觸發 LINE 通報。")
        return
        
    alert_cities = []
    for row in results:
        alert_cities.append(f"{row[0]}({row[1]}%)")
        
    cities_str = "、".join(alert_cities)
    alert_message = f"\n🌧️【降雨防禦警報】\n今日以下縣市降雨機率高達 60% 以上，出門記得帶傘：\n📍 {cities_str}"
    
    send_line_notification(token, alert_message)
