from src.database.db_manager import LocalDB
from src.messaging.Publisher_RabbitMQ import PublisherAMQP
from src.sensors.digital import DigitalSensors
from src.sensors.analogic import AnalogicSensors
from src.ui.MainView import MainView
from config import Config
from src.config.config_manager import ConfigUser
from src.index import Loop
import threading


def getDependencies(
        configManager, 
        userConfig, 
        dbManager, 
        amqpManager, 
        digitalSensorManager, 
        analogicSensorManager
    ):
    # Inicializa los módulos y dependencias
    # Variables de entorno
    if configManager == None:
        try:
            configManager = Config()
            print("Configuración Obtenida")
        except Exception as e:
            print("Error al obtener configuración:", e)
            configManager = None

    # Obtiene configuración de usuario
    if userConfig == None:
        try:
            userConfig = ConfigUser()
            print("Configuración de usuario obtenida")
        except Exception as e:
            print("Error al obtener configuración de usuario:", e)
            userConfig = None

    # DB
    if dbManager == None:
        try:
            dbManager = LocalDB()
            print("Base de datos iniciada")
        except Exception as e:
            print("Error al iniciar base de datos:", e)
            dbManager = None

    # Publicador RabbitMQ
    if amqpManager == None:
        try:
            amqpManager = PublisherAMQP(configManager)
            print("Conexión AMQP establecida")
        except Exception as e:
            print("Error al conectarse con servidor AMQP:", e)
            amqpManager = None

    # Sensores digitales
    if digitalSensorManager == None:
        try:
            digitalSensorManager = DigitalSensors()
            print("Sensores Digitales inicializados")
        except Exception as e:
            print("Error al conectar con los sensores digitales:", e)
            digitalSensorManager = None

    # Sensores analógicos
    if analogicSensorManager == None:
        try:
            analogicSensorManager = AnalogicSensors()
            print("Sensores analógicos inicializados")
        except Exception as e:
            print("Error al conectar con los sensores analógicos:", e)
            analogicSensorManager = None

def main():
    configManager = None
    userConfig = None
    dbManager = None
    amqpManager = None
    digitalSensorManager = None
    analogicSensorManager = None

    getDependencies(configManager, userConfig, dbManager, amqpManager, digitalSensorManager, analogicSensorManager)

    # Vista principal
    try:
        mainView = MainView(dbManager)
        print("Vista inicializada")
    except Exception as e:
        print("Error al iniciar vista:", e)
        return

    # Inicializa un hilo para los procesos relacionados con la bd y sensores
    hilo_loop = threading.Thread(target=system_loop, args=(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView, userConfig, configManager))
    hilo_loop.daemon = True
    hilo_loop.start()

    # En el hilo principal ejecuta una vista en Tkinter
    mainView.mainloop()

    dbManager.closeDB()
    amqpManager.closeConnection()

# Función para mantener ejecutando el tkinter
def system_loop(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView, userConfig, configManager):
    while mainView.verifyRunning():
        getDependencies(configManager, userConfig, dbManager, amqpManager, digitalSensorManager, analogicSensorManager)
        Loop(analogicSensorManager, digitalSensorManager, dbManager, amqpManager, mainView, userConfig)

if __name__ == "__main__":
    main()