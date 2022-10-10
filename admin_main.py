from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from functions import showError, showInfo

import AdminFormUI


class MainForm(QtWidgets.QWidget, AdminFormUI.Ui_Form):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)

        self.text = ""
        self.pattern = ""

        self.outputResult.setText("Результат поиска...")

        self.acceptSearchButton.pressed.connect(self.searchInText)
        self.importCriteriaButton.pressed.connect(self.importCriteriaFromFile)
        self.importTextButton.pressed.connect(self.importTextFromFile)

        self.setLayout(self.verticalLayout)
        # self.Form.setLayout(self.verticalLayout)
        self.show()

    def searchInText(self):
        if pattern:=self.criteria.toPlainText():
            self.pattern = pattern
            self.importCriteriaButton.setText("Импортировать критерии из файла")
        if not (self.text and self.pattern):
            return
        
        print("PASSED")
        
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
            new_str += self.text[current_index:found_word_index] + "<span style='color: red;'>" + self.text[found_word_index:found_word_index + len(self.pattern)] + "</span>"

            # Нужен для поиска не с 0 элемента
            current_index = found_word_index + len(self.pattern)

        # Добавляем последние символы в строку
        new_str += self.text[found_word_index + len(self.pattern):]
        
        print("NEW_STR")
        print(new_str)

        if self.resultInFile.isChecked():
            with open("output.html", "w") as output_file:
                output_file.write(new_str)
            showInfo("Текст был записан в файл")
        elif self.resultOnDisplay.isChecked():
            self.outputResult.setText(new_str)

    def importCriteriaFromFile(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)

        if self.fileExtensions.toPlainText():
            extensions = " ".join\
                ([f"*.{ext}" for ext in self.fileExtensions.toPlainText().split(" ")])
            try:
                print(f"Text files ({extensions})")
                dialog.setNameFilter(f"Text files ({extensions})")
            except Exception as e:
                return showError(str(e))
        else:
            dialog.setNameFilter("Text files (*.txt)")


        if (dialog.exec()):
            file_name = dialog.selectedFiles()[0]
            with open(file_name, "r") as pattern_file:
                self.pattern = pattern_file.readline()

            self.importCriteriaButton.setText(self.importCriteriaButton.text() + f"({file_name.split('/')[-1]})")

    def importTextFromFile(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)

        dialog.setNameFilter("Text files (*.txt)")

        if (dialog.exec()):
            file_name = dialog.selectedFiles()[0]
            with open(file_name, "r") as pattern_file:
                self.text = " ".join(pattern_file.readlines())
            
            self.importTextButton.setText(self.importTextButton.text() + f"({file_name.split('/')[-1]})")


app = QtWidgets.QApplication([])
window = MainForm()
app.exec()