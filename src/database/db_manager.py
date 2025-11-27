import sqlite3
import time
import threading

class LocalDB:
    def __init__(self):
        self.conn = sqlite3.connect('sensores.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()

        print("Conexión con la db establecida")

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id_sensor_reading INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                id_sensor TEXT,
                backed BOOLEAN
            )
        ''')

        print("Tabla de mediciones creada")

        self.conn.commit()

    def createSensorReading(self, value, id_sensor, backed):
        with self.lock:
            self.cursor.execute(
                '''INSERT INTO sensor_readings (value, id_sensor, backed) VALUES (?, ?, ?)''', (value, id_sensor, backed)
            )
            print(f"Medición del sensor '{id_sensor}' registrado: {value}")
            self.conn.commit()
    
    def getSensorReadingsNotSent(self):
        with self.lock:
            self.cursor.execute(
                '''SELECT * FROM sensor_readings WHERE backed = false'''
            )
            data = self.cursor.fetchall()
            print(f"Mediciones sin enviar: {data}")
            return [dict(row) for row in data]
    
    def markSensorReadingSent(self, id):
        with self.lock:
            self.cursor.execute(
                '''UPDATE sensor_readings SET backed = true WHERE id_sensor_reading = ?''', (id,)
            )
            print(f"Medición marcada como respaldada: {id}")
            self.conn.commit()

    def closeDB(self):
        with self.lock:
            print("Cerrando conexión con la bd")
            self.conn.close()