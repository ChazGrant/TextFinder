from PyQt5.QtWidgets import QMessageBox


def showInfo(text: str) -> None:
    msg = QMessageBox()

    msg.setIcon(QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Информация")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()

def showError(text: str) -> None:
    msg = QMessageBox()

    msg.setIcon(QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle("Ошибка")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()

def log(error_text: str) -> None:
    with open("errors.log", "a") as error_file:
        error_file.write(error_text)

def logFunction(func):
    def exceptionCatcher():
        try:
            func()
        except Exception as e:
            #showError("Возникла ошибка")
            return log(str(e))
    
    return exceptionCatcher()