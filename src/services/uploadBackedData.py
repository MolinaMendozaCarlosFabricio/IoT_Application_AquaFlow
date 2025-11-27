import time

def BackupSensorReadings(dbManager, publisher):
    # Obtiene lecturas no respaldadas
    readings_dont_sent = dbManager.getSensorReadingsNotSent()
    if len(readings_dont_sent) > 0:
        for reading in readings_dont_sent:
            # Arma diccionario
            reading_to_send = [{
                "id": reading["id_sensor_reading"],
                "value": reading["value"],
                "timestamp": reading["timestamp"],
                "id_sensor": reading["id_sensor"]
            }]
            # Envía por AMQP las lecturas a la BD en la nube
            try:
                publisher.publishMessage(".measurements", reading_to_send)
                print("Datos respaldados:", reading_to_send)
                # Marca las lecturas como respaldadas
                dbManager.markSensorReadingSent(reading_to_send[0]["id"])
            except Exception as e:
                print("No fue posible respaldar los datos, intentar más tarde:", e)
            time.sleep(3)
    else:
        print("Sin datos qué respaldar")