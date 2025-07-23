def BackupSensorReadings(dbManager, publisher):
    readings_dont_sent = dbManager.getSensorReadingsNotSent()
    if len(readings_dont_sent) > 0:
        for reading in readings_dont_sent:
            reading_to_send = [{
                "id": reading["id_sensor_reading"],
                "value": reading["value"],
                "timestamp": reading["timestamp"],
                "id_sensor": reading["id_sensor"]
            }]
            try:
                publisher.publishMessage(".measurements", reading_to_send)
                print("Datos respaldados:", reading_to_send)
                dbManager.markSensorReadingSent(reading_to_send["id"])
            except Exception as e:
                print("No fue posible respaldar los datos, intentar más tarde:", e)
    else:
        print("Sin datos qué respaldar")