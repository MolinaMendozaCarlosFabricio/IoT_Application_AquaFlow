from src.database.db_manager import LocalDB
from src.messaging.Publisher_RabbitMQ import PublisherAMQP
from src.sensors.digital import DigitalSensors
from src.sensors.analogic import AnalogicSensors
from src.ui.MainView import MainView
from config import Config
from src.index import Loop
import threading

# Iniciar configuración con dotenv
try:
    configManager = Config()
    print("Configuración Obtenida")
except Exception as e:
    print("Error al obtener configuración:", e)
    configManager = None

# Iniciar base de datos local
try:
    dbManager = LocalDB()
    print("Base de datos iniciada")
except Exception as e:
    print("Error al iniciar base de datos:", e)
    dbManager = None

# Conectar con RabbitMQ
try:
    amqpManager = PublisherAMQP(configManager)
    print("Conexión AMQP establecida")
except Exception as e:
    print("Error al conectarse con servidor AMQP:", e)
    amqpManager = None

# Conectar con sensores digitales
try:
    digitalSensorManager = DigitalSensors()
    print("Sensores Digitales inicializados")
except:
    print("Error al conectar con los sensores digitales:", e)
    digitalSensorManager = None

# Conectar con sensores analógicos
try:
    analogicSensorManager = AnalogicSensors()
    print("Sensores analógicos inicializados")
except Exception as e:
    print("Error al conectar con los sensores analógicos:", e)
    analogicSensorManager = None

# Iniciar vista principal
try:
    mainView = MainView()
    print("Vista inicializada")
except Exception as e:
    print("Error al iniciar vista:", e)

runing = True
hilo_ui = threading.Thread(target=mainView.mainloop)
hilo_ui.daemon = True
hilo_ui.start()

while runing:
    Loop(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView)
    runing = mainView.verifyRunning()
# Cerrar las conexiones con dependencias al finalizar
dbManager.closeDB()
amqpManager.closeConnection()