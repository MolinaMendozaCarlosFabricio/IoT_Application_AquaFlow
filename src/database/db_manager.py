import sqlite3
import time

class LocalDB:
    def __init__(self):
        self.conn = sqlite3.connect('sensores.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        print("Conexión con la db establecida")

        self.conn.execute("PRAGMA foreign_keys = ON")

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_info (
                id_device TEXT PRIMARY KEY,
                id_user INTEGER DEFAULT(null),
                model TEXT,
                created_at DATE DEFAULT CURRENT_TIMESTAMP,
                initialized BOOLEAN DEFAULT(false),
                synchronized BOOLEAN DEFAULT(false)
            );
        ''')

        print("Tabla de dispositivo creada")

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensors (
                id_sensor INTEGER PRIMARY KEY,
                id_device TEXT,
                sensor_name_model TEXT,
                unit_measurement TEXT,
                FOREIGN KEY (id_device) REFERENCES device_info(id_device) ON DELETE CASCADE
            );
        ''')

        print("Tabla de sensores creada")

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id_sensor_reading INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                id_sensor INTEGER,
                backed BOOLEAN,
                FOREIGN KEY (id_sensor) REFERENCES sensors(id_sensor) ON DELETE CASCADE
            )
        ''')

        print("Tabla de mediciones creada")

        self.conn.commit()

    def initDevice(self, id_device, model):
        self.cursor.execute(
            '''INSERT INTO device_info (id_device, model, initialized) VALUES (?, ?, ?)''', 
            (id_device, model, True)
        )
        print("Datos de fábrica del dispositivo añadidos")
        self.conn.commit()
    
    def initSensor(self, id_sensor, sensor_name_model, unit_measurement):
        self.cursor.execute(
            '''INSERT INTO sensors (id_sensor, sensor_name_model, unit_measurement) VALUES (?, ?, ?)''', 
            (id_sensor, sensor_name_model, unit_measurement)
        )
        print(f"Datos de fábrica del sensor '{sensor_name_model}' añadidos")
        self.conn.commit()
    
    def getDeviceInfo(self):
        self.cursor.execute('''SELECT * FROM device_info''')
        data = self.cursor.fetchall()
        print(f"Datos del dispositivo obtenidos: {data[0]}")
        return data[0] if data else None
    
    def getSensor(self, sensor_name_model):
        self.cursor.execute(
            '''SELECT * FROM sensors WHERE sensor_name_model = ?''', (sensor_name_model,)
        )
        data = self.cursor.fetchall()
        print(f"Datos del sensor obtenidos: {data[0]}")
        return data[0] if data else None
    
    def sinchronizeDevice(self, id_device, id_user):
        self.cursor.execute(
            '''UPDATE device_info SET id_user = ?, synchronized = true WHERE id_device = ?''', 
            (id_user, id_device)
        )
        print(f"Dispositivo sincronizado con el usuario: {id_user}")
        self.conn.commit()

    def createSensorReading(self, value, id_sensor, backed):
        self.cursor.execute(
            '''INSERT INTO sensor_readings (value, id_sensor, backed) VALUES (?, ?, ?)''', (value, id_sensor, backed)
        )
        print(f"Medición del sensor '{id_sensor}' registrado: {value}")
        self.conn.commit()
    
    def getSensorReadingsNotSent(self):
        self.cursor.execute(
            '''SELECT * FROM sensor_readings WHERE backed = false'''
        )
        data = self.cursor.fetchall()
        print(f"Mediciones sin enviar: {data}")
        return data

    def closeDB(self):
        print("Cerrando conexión con la bd")
        self.conn.close()