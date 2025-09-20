from sys import exit, argv
from os import system, path
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication, QDialog, QFileDialog, QDialogButtonBox
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QRect, QMetaObject, QCoreApplication

class UiForm(object):
    def __init__(self):
        " Guid Program "
        self.ICON = QIcon('icon.png')
        self.font = QFont()
        self.Font_Label = QFont()
        self.Font_msg = QFont()
        self.msg = QMessageBox()
        self.BtnClose = QDialogButtonBox.StandardButton.Close
        self.BtnOK = QDialogButtonBox.StandardButton.Ok
        self.translate = QCoreApplication.translate

    def setupUi(self, Form:QDialog):
        " setup Ui Program and set Setting "
        Form.setObjectName("Form")
        Form.setWindowTitle("Ui to Python Converter")
        Form.setEnabled(True)
        Form.setFixedSize(500, 160)
        self.font.setPointSize(10)
        Form.setFont(self.font)
        Form.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        Form.setWindowIcon(self.ICON)
        self.buttonBox = QDialogButtonBox(parent=Form)
        self.buttonBox.setGeometry(QRect(170, 120, 160, 40))
        self.buttonBox.setStandardButtons(self.BtnClose|self.BtnOK)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QLabel(parent=Form)
        self.label.setGeometry(QRect(10, 0, 320, 40))
        self.Font_Label.setFamily("MS Shell Dlg 2")
        self.Font_Label.setPointSize(14)
        self.Font_Label.setBold(False)
        self.Font_Label.setWeight(50)
        self.label.setFont(self.Font_Label)
        self.label.setObjectName("label")
        self.textentry = QLineEdit(parent=Form)
        self.textentry.setGeometry(QRect(10, 40, 480, 30))
        self.textentry.setObjectName("textentry")
        self.browser = QPushButton(parent=Form)
        self.browser.setGeometry(QRect(10, 80, 480, 30))
        self.browser.setObjectName("browser")
        self.msg.setWindowIcon(self.ICON)
        self.Font_msg.setPointSize(10)
        self.msg.setFont(self.Font_msg)
        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form:QDialog):
        self.label.setText(self.translate("Form", "Enter File .ui to Convert Python Files:"))
        self.browser.setText(self.translate("Form", "Browse"))

class ApplicationClass(QDialog):
    def __init__(self):
        super().__init__()
        self.Ui = UiForm()
        self.Ui.setupUi(self)
        self.pathinput = ""
        self.Ui.browser.clicked.connect(self.askfile)
        self.Ui.buttonBox.rejected.connect(self.exitapplication)
        self.Ui.buttonBox.accepted.connect(self.Convert)

    def askfile(self):
        self.pathinput, filename = QFileDialog.getOpenFileName(
            parent=self, caption="Select .ui File",
            filter="ui files (*.ui)")
        if filename:
            self.Ui.textentry.setText(self.pathinput)

    def Convert(self):
        pathinput = self.Ui.textentry.text()
        if pathinput and path.exists(pathinput) and pathinput.endswith('.ui'):
            pahtoutput = pathinput[:-3] + ".py"
            try:
                system(f'pyuic6 "{pathinput}" -o "{pahtoutput}"')
                notifi = "✅ Python Files Create Successfuly."
                self.ShowError(notifi, success=True)
            except:
                notifi = "❌ Python Files not Created!!"
                self.ShowError(notifi, success=False)
        else:
            notifi = "❌ File Not Found!"
            self.ShowError(notifi, success=False)

    def ShowError(self, message:str, success:bool):
        icon = QMessageBox.Icon.Information if success else QMessageBox.Icon.Critical
        title = "Success" if success else "Error"
        self.Ui.msg.setIcon(icon)
        self.Ui.msg.setWindowTitle(title)
        self.Ui.msg.setText(message)
        self.Ui.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.Ui.msg.exec()

    def exitapplication(self):
        QApplication.quit()

app = QApplication(argv)
WINDOWS = ApplicationClass()
WINDOWS.show()
exit(app.exec())
