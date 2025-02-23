# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(920, 490)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setSpacing(10)

        # Left-side Layout (Input & Result)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)

        self.input = QtWidgets.QTextEdit(self.centralwidget)
        self.input.setObjectName("input")
        self.input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addWidget(self.input)

        self.result = QtWidgets.QTextEdit(self.centralwidget)
        self.result.setObjectName("result")
        self.result.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addWidget(self.result)

        self.horizontalLayout.addLayout(self.verticalLayout_2, 3)  # Takes 3 parts of space

        # Right-side Layout (Buttons)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.lemmatize_button = QtWidgets.QPushButton(self.centralwidget)
        self.lemmatize_button.setObjectName("lemmatize_button")
        self.lemmatize_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addWidget(self.lemmatize_button)
        
        self.clear_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addWidget(self.clear_button)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.token_button = QtWidgets.QPushButton(self.centralwidget)
        self.token_button.setObjectName("token_button")
        self.token_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addWidget(self.token_button)

        self.process_button = QtWidgets.QPushButton(self.centralwidget)
        self.process_button.setObjectName("process_button")
        self.process_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addWidget(self.process_button)

        self.lemma_button = QtWidgets.QPushButton(self.centralwidget)
        self.lemma_button.setObjectName("lemma_button")
        self.lemma_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addWidget(self.lemma_button)
        
        self.pdf_button = QtWidgets.QPushButton(self.centralwidget)
        self.pdf_button.setObjectName("pdf_button")
        self.pdf_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addWidget(self.pdf_button)
        
        self.preview_button = QtWidgets.QPushButton(self.centralwidget)
        self.preview_button.setObjectName("preview_button")
        self.preview_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addWidget(self.preview_button)

        self.horizontalLayout.addLayout(self.verticalLayout, 1)  # Takes 1 part of space

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)


    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Action</span></p></body></html>"))
            self.lemmatize_button.setText(_translate("MainWindow", "Lemmatize"))
            self.clear_button.setText(_translate("MainWindow", "Clear"))
            self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Display</span></p></body></html>"))
            self.token_button.setText(_translate("MainWindow", "Token"))
            self.process_button.setText(_translate("MainWindow", "Process"))
            self.lemma_button.setText(_translate("MainWindow", "Lemma"))
            self.pdf_button.setText(_translate("MainWindow", "PDF"))
            self.preview_button.setText(_translate("MainWindow", "Preview"))