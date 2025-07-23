from src.services.ReadAllData import GetSensorsData
from src.services.uploadBackedData import BackupSensorReadings
import time

def Loop(analogicSensors, digitalSensors, dbManager, publisher, mainView):
    BackupSensorReadings(dbManager, publisher)
    valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor = GetSensorsData(
        analogicSensors, digitalSensors, dbManager, publisher
    )
    mainView.showMeasurements(valueTurbiditySensor, valueTdsSensor, valuepHSensor, valueTempSensor)
    
    # Lo último que se debe de ejecutar
    time.sleep(10)