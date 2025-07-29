# Método para almacenar ID de usuario
def SynchronizeUser(dbManager, id_user):
    if len(id_user) == 36:
        deviceInfo = dbManager.getDeviceInfo()
        dbManager.sinchronizeDevice(deviceInfo["id_device"], id_user)
        return True
    else:
        return False