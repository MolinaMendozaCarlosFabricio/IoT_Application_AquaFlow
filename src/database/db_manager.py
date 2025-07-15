import sqlite3

conn = sqlite3.connect('sensores.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS lecturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_sensor TEXT,
        valor REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()