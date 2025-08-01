from datetime import datetime

def GetSensorsData (analogicSensors, digitalSensors, dbManager, publisher):
    # Obtiene información del dispositivo y sensores
    deviceInfo = dbManager.getDeviceInfo()
    tempSensorInfo = dbManager.getSensor('ds18b20')
    tdsSensorInfo = dbManager.getSensor('tdsSensor')
    pHSensorInfo = dbManager.getSensor('phSensor')
    turbiditySensorInfor = dbManager.getSensor('turbiditySensor')

    # Obtiene lecturas de sensores
    valueTempSensor = digitalSensors.read_temp()
    valuepHSensor, valueTdsSensor, valueTurbiditySensor, e = analogicSensors.getAnalogicSensorReadings()

    if e != None or deviceInfo["synchronized"]:
        # Obtiene timestamp (Fecha y hora)
        now = datetime.now()
        iso_string = now.isoformat() + 'Z'
        # Hace un diccionario de las lecturas
        tempReading = {
            "id": 0,
            "value": valueTempSensor,
            "date": iso_string,
            "sensor_id": tempSensorInfo["id_sensor"]
        }
        tdsReading = {
            "id": 0,
            "value": valueTdsSensor,
            "date": iso_string,
            "sensor_id": tdsSensorInfo["id_sensor"]
        }
        pHReading = {
            "id": 0,
            "value": valuepHSensor,
            "date": iso_string,
            "sensor_id": pHSensorInfo["id_sensor"]
        }
        turbidityReading = {
            "id": 0,
            "value": valueTurbiditySensor,
            "date": iso_string,
            "sensor_id": turbiditySensorInfor["id_sensor"]
        }

        sensorReadingsList = [pHReading, tdsReading, tempReading, turbidityReading]
        messageSensorReadings = {
            "idUser": deviceInfo["id_user"],
            "idFiltrer": deviceInfo["id_device"],
            "sensorReadings": sensorReadingsList
        }

        # Intenta publicar las lecturas en los tópicos
        try:
            publisher.publishMessage("websocket_topic.many_readings", messageSensorReadings)
            print("Datos enviados al websocket")
            publisher.publishMessage(".measurements", sensorReadingsList)
            print("Datos enviados a la Base de datos")
            # Almacena en la bd local
            dbManager.createSensorReading(tempReading["value"], tempReading["sensor_id"], True)
            dbManager.createSensorReading(tdsReading["value"], tdsReading["sensor_id"], True)
            dbManager.createSensorReading(pHReading["value"], pHReading["sensor_id"], True)
            dbManager.createSensorReading(turbidityReading["value"], turbidityReading["sensor_id"], True)
            print("Lecturas guardadas de manera local")
        # Si no puede, almacena las lecturas locales como no respaldadas
        except Exception as e:
            print("Error al mandar datos por amqp:", e)
            dbManager.createSensorReading(tempReading["value"], tempReading["sensor_id"], False)
            dbManager.createSensorReading(tdsReading["value"], tdsReading["sensor_id"], False)
            dbManager.createSensorReading(pHReading["value"], pHReading["sensor_id"], False)
            dbManager.createSensorReading(turbidityReading["value"], turbidityReading["sensor_id"], False)
            print("Datos guardados de manera local")
        
        # Retorna los valores leídos
        return valueTempSensor, valueTdsSensor, valueTurbiditySensor, valuepHSensor
    else:
        print("Error en la toma de lecturas")
        return False