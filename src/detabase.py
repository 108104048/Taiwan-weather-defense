import sqlite3

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

def clean_city_name(city_input):
    corrections = {"台":"臺"}
    name = city_input.strip()
    return corrections.get(name, name)

def query_by_city(cursor, city_input):
    search_name = clean_city_name(city_input)
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
