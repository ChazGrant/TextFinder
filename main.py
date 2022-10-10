from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from functions import showError, showInfo, log

import MainFormUI


class MainForm(QtWidgets.QWidget, MainFormUI.Ui_Form):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)

        self.text = ""
        self.pattern = ""

        self.outputResult.setText("Результат поиска...")

        self.importCriteriaButton.resize(321, 31)

        self.acceptSearchButton.pressed.connect(self.searchInText)
        self.importCriteriaButton.pressed.connect(self.importCriteriaFromFile)
        self.importTextButton.pressed.connect(self.importTextFromFile)

        self.setLayout(self.verticalLayout)
        self.show()

    def searchInText(self):
        if pattern:=self.criteria.toPlainText():
            self.pattern = pattern
            self.importCriteriaButton.setText("Импортировать критерии из файла")
        if not (self.text and self.pattern):
            return
        
        current_index = 0
        found_word_index = 0
        new_str = ""

        while True:
            try:
                # Находим начало слова, необходимое для поиска, начиная с current_index
                find_index = self.text[current_index:].lower().index(self.pattern.lower())
            except:
                # Выход из цикла если слова больше нет
                break
            # Находим индекс начала найденного слова
            found_word_index = current_index + find_index
            # Изменяем цвет найденного слова на красный
            new_str += self.text[current_index+len(self.pattern)-1:found_word_index] + "<span style='color: red;'>" + self.text[found_word_index:found_word_index + len(self.pattern)] + "</span>"

            # Нужен для поиска не с 0 элемента
            current_index = found_word_index + len(self.pattern)

        # Добавляем последние символы в строку
        new_str += self.text[found_word_index + len(self.pattern):]
        
        if self.resultInFile.isChecked():
            with open("output.html", "w") as output_file:
                output_file.write(new_str)
            showInfo("Текст был записан в файл")
        elif self.resultOnDisplay.isChecked():
            self.outputResult.setText(new_str)

    def importCriteriaFromFile(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)

        dialog.setNameFilter("Text files (*.txt)")

        if (dialog.exec()):
            file_name = dialog.selectedFiles()[0]
            with open(file_name, "r") as pattern_file:
                try:
                    self.pattern = pattern_file.readline()
                except Exception as e:
                    showError("Возникла ошибка")
                    return log(str(e))

            self.importCriteriaButton.setText(self.importCriteriaButton.text() + f"({file_name.split('/')[-1]})")

    def importTextFromFile(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)

        dialog.setNameFilter("Text files (*.txt)")

        if (dialog.exec()):
            file_name = dialog.selectedFiles()[0]
            with open(file_name, "r") as pattern_file:
                try:
                    self.text = " ".join(pattern_file.readlines())
                except Exception as e:
                    showError("Возникла ошибка")
                    return log(str(e))
            
            self.importTextButton.setText(self.importTextButton.text() + f"({file_name.split('/')[-1]})")


app = QtWidgets.QApplication([])
window = MainForm()
app.exec()