import _winapi as winAPI

class InterfaceConnectionManager(object):
    """description of class"""

    @staticmethod
    def initializeConnection():
        return winAPI.CreateFile("\\\\.\\pipe\\Demo", winAPI.GENERIC_READ | winAPI.GENERIC_WRITE, 0, 0, winAPI.OPEN_EXISTING, 0, 0)

    @staticmethod
    def sendMessage(fileHandle, message):
        winAPI.WriteFile(fileHandle, message, 0)

    @staticmethod
    def readMessage(fileHandle):
        return winAPI.ReadFile(fileHandle, 4096)



