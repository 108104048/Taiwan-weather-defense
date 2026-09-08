# Taiwan Weather ETL Pipeline \& Anti-Crash Defense
 
 基於 Python 與 SQLite 建立的自動化氣象數據管線（ETL）專案。
 本專案專為後台腳本與自動化測試工程師架構設計，著重於「數據清洗流暢度」與「四重安全防禦機制（Anti-Crash）」。


<br>
# 專案核心特點

 * 1\. 穩定 API 數據管線 (ETL)：
 
       串接中央氣象署結構穩定的 JSON 數據流。
       
       精準過濾全台 22 縣市之 Wx、PoP、MinT、MaxT 等多維度氣象標籤。
 
 * 2\. 輕量化本地存儲：
 
       利用 Python 內建之 SQLite 自動初始化資料庫與表格，確保環境零依賴、快速佈署。
 
 * 3\. 高階防禦性例外處理 (Exception Handling)：
 
       網路防禦：攔截斷網、逾時、404/500 等外部伺服器異常。
       
       格式防禦：預防 API 資料結構突變或突發性 HTML 錯誤畫面解析失敗。
       
       資料庫防禦：捕捉 SQL 寫入衝突與資料夾檔案鎖死風險。
       
       數據預設值防禦：利用連等初始值，徹底消滅漏給欄位時引發的 `NameError`。


<br>
# 系統架構流向

準備環境/初始化 SQLite 表格 ➔ 網路安全請求 (Requests) ➔ 多層級 JSON 數據清洗 (for-loop) ➔ 批次安全防禦寫入 (SQL ?) ➔ 存檔確認 (Commit) ➔ 連線關閉 (Finally)


<br>
 # 開發環境與套件

 Python 3.14+

 Requests (網路請求)

 SQLite3 (內建資料庫)



