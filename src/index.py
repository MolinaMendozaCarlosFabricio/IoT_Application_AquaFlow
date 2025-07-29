from src.services.ReadAllData import GetSensorsData
from src.services.uploadBackedData import BackupSensorReadings
from src.services.ShowActivities import CalculateWaterActivities
import time

# Método loop
def Loop(analogicSensors, digitalSensors, dbManager, publisher, mainView):
    BackupSensorReadings(dbManager, publisher)
    valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor = GetSensorsData(
        analogicSensors, digitalSensors, dbManager, publisher
    )
    mainView.showMeasurements(valueTurbiditySensor, valueTdsSensor, valuepHSensor, valueTempSensor)

    activities = CalculateWaterActivities(valuepHSensor, valueTdsSensor, valueTurbiditySensor, publisher, dbManager)
    mainView.showActivities(activities)
    # Lo último que se debe de ejecutar
    time.sleep(4)