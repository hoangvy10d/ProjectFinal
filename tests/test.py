from PyQt6.QtWidgets import QApplication, QMainWindow

from Login.LogInExt import LogInExt

app=QApplication([])
MainWindow=QMainWindow()
myui=LogInExt()
myui.setupUi(MainWindow)
myui.showWindow()
app.exec()