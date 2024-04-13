import sys
import os
import threading
from time import strftime, localtime, sleep

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickWindow
from PyQt5.QtCore import QObject, pyqtSignal

# Backend object
class Backend(QObject):

    def __init__(self):
        QObject.__init__(self)
    
    updated = pyqtSignal(str, arguments=['updater'])

    # Sends signal to update time
    def updater(self, curr_time):
        self.updated.emit(curr_time)

    # Threading
    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()

    # Updates time every 0.1s
    def _bootUp(self):
        while True:
            curr_time = strftime("%H:%M", localtime())
            self.updater(curr_time)
            sleep(0.1)

# Launch application
QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./UI/main.qml')
back_end = Backend()
engine.rootObjects()[0].setProperty('backend', back_end)
back_end.bootUp()
sys.exit(app.exec())