import sqlite3
import time
import threading

class LocalDB:
    def __init__(self):
        # Inicializa la base de datos con SQLite
        self.conn = sqlite3.connect('sensores.db', check_same_thread=False)
        # Permite obtener los registros como diccionarios
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.lock = threading.Lock()

        print("Conexión con la db establecida")

        # Permite usar las claves foráneas
        self.conn.execute("PRAGMA foreign_keys = ON")

        # Tabla de información del dispositivo (Se espera que solo tenga un registro)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_info (
                id_device TEXT PRIMARY KEY,
                id_user TEXT DEFAULT(null),
                model TEXT,
                created_at DATE DEFAULT CURRENT_TIMESTAMP,
                initialized BOOLEAN DEFAULT(false),
                synchronized BOOLEAN DEFAULT(false)
            );
        ''')

        print("Tabla de dispositivo creada")

        # Tabla de información de los sensores (Se espera que solo estén registrados los sensores del dispositivo)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensors (
                id_sensor TEXT PRIMARY KEY,
                id_device TEXT,
                sensor_name_model TEXT,
                unit_measurement TEXT,
                FOREIGN KEY (id_device) REFERENCES device_info(id_device) ON DELETE CASCADE
            );
        ''')

        print("Tabla de sensores creada")

        # Tabla de lecturas de sensor (El atributo "backed" permite saber si una lectura está respaldada o no, primitivamente)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id_sensor_reading INTEGER PRIMARY KEY AUTOINCREMENT,
                value REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                id_sensor TEXT,
                backed BOOLEAN,
                FOREIGN KEY (id_sensor) REFERENCES sensors(id_sensor) ON DELETE CASCADE
            )
        ''')

        print("Tabla de mediciones creada")

        self.conn.commit()

    # Método para insertar información del dispositivo (No empleado)
    def initDevice(self, id_device, model):
        with self.lock:
            self.cursor.execute(
                '''INSERT INTO device_info (id_device, model, initialized) VALUES (?, ?, ?)''', 
                (id_device, model, True)
            )
            print("Datos de fábrica del dispositivo añadidos")
            self.conn.commit()
    
    # Método para insertar información del sensor (No empleado)
    def initSensor(self, id_sensor, sensor_name_model, unit_measurement):
        with self.lock:
            self.cursor.execute(
                '''INSERT INTO sensors (id_sensor, sensor_name_model, unit_measurement) VALUES (?, ?, ?)''', 
                (id_sensor, sensor_name_model, unit_measurement)
            )
            print(f"Datos de fábrica del sensor '{sensor_name_model}' añadidos")
            self.conn.commit()
    
    # Método para obtener información del dispositivo
    def getDeviceInfo(self):
        with self.lock:
            self.cursor.execute('''SELECT * FROM device_info''')
            data = self.cursor.fetchall()
            print(f"Datos del dispositivo obtenidos: {data[0]}")
            return dict(data[0]) if data else None
    
    # Método para obtener información del sensor
    def getSensor(self, sensor_name_model):
        with self.lock:
            self.cursor.execute(
                '''SELECT * FROM sensors WHERE sensor_name_model = ?''', (sensor_name_model,)
            )
            data = self.cursor.fetchall()
            print(f"Datos del sensor obtenidos: {data[0]}")
            return dict(data[0]) if data else None
    
    # Método para ingresar ID de usuario
    def sinchronizeDevice(self, id_device, id_user):
        with self.lock:
            self.cursor.execute(
                '''UPDATE device_info SET id_user = ?, synchronized = true WHERE id_device = ?''', 
                (id_user, id_device)
            )
            print(f"Dispositivo sincronizado con el usuario: {id_user}")
            self.conn.commit()

    # Método para guardar una lectura de sensor
    def createSensorReading(self, value, id_sensor, backed):
        with self.lock:
            self.cursor.execute(
                '''INSERT INTO sensor_readings (value, id_sensor, backed) VALUES (?, ?, ?)''', (value, id_sensor, backed)
            )
            print(f"Medición del sensor '{id_sensor}' registrado: {value}")
            self.conn.commit()
    
    # Método para obtener lecturas
    def getSensorReadingsNotSent(self):
        with self.lock:
            self.cursor.execute(
                '''SELECT * FROM sensor_readings WHERE backed = false'''
            )
            data = self.cursor.fetchall()
            print(f"Mediciones sin enviar: {data}")
            return [dict(row) for row in data]
    
    # Método para marcar lecturas como respaldadas
    def markSensorReadingSent(self, id):
        with self.lock:
            self.cursor.execute(
                '''UPDATE sensor_readings SET backed = true WHERE id_sensor_reading = ?''', (id,)
            )
            print(f"Medición marcada como respaldada: {id}")
            self.conn.commit()

    # Método para cerrar la base de datos
    def closeDB(self):
        with self.lock:
            print("Cerrando conexión con la bd")
            self.conn.close()