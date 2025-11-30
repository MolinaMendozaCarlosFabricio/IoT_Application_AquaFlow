from src.services.ReadAllData import GetSensorsData
from src.services.uploadBackedData import BackupSensorReadings
from src.services.ShowActivities import CalculateWaterActivities
import time

# Método loop
def Loop(analogicSensors, digitalSensors, dbManager, publisher, mainView, userConfig):
    BackupSensorReadings(dbManager, publisher)
    valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor, taken = GetSensorsData(
        analogicSensors, digitalSensors, dbManager, publisher, userConfig
    )
    if taken:
        mainView.showMeasurements(valueTurbiditySensor, valueTdsSensor, valuepHSensor, valueTempSensor)

        activities = CalculateWaterActivities(valuepHSensor, valueTdsSensor, valueTurbiditySensor, publisher, userConfig)
        mainView.showActivities(activities)
    # Lo último que se debe de ejecutar
    time.sleep(4)