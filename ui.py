from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1078, 571)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayout_main = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setObjectName("verticalLayout_main")
        
        self.headerWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.headerWidget.setStyleSheet("background-color:rgb(0, 255, 127)")
        self.headerWidget.setObjectName("headerWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.headerWidget)
        self.horizontalLayout_3.setContentsMargins(12, 0, 12, 0)
        self.horizontalLayout_3.setSpacing(21)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.titleLabel = QtWidgets.QLabel(parent=self.headerWidget)
        self.titleLabel.setObjectName("titleLabel")
        self.horizontalLayout_3.addWidget(self.titleLabel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.featureBtn = QtWidgets.QPushButton(parent=self.headerWidget)
        self.featureBtn.setObjectName("featureBtn")
        self.horizontalLayout_3.addWidget(self.featureBtn)
        self.verticalLayout_main.addWidget(self.headerWidget)
        
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout_main.addWidget(self.stackedWidget)
        
        self.featurePage = QtWidgets.QWidget()
        self.featurePage.setObjectName("featurePage")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.featurePage)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lemmaBtn = QtWidgets.QPushButton(parent=self.featurePage)
        self.lemmaBtn.setObjectName("lemmaBtn")
        self.horizontalLayout_4.addWidget(self.lemmaBtn)
        self.validationBtn = QtWidgets.QPushButton(parent=self.featurePage)
        self.validationBtn.setObjectName("validationBtn")
        self.horizontalLayout_4.addWidget(self.validationBtn)
        self.processBtn = QtWidgets.QPushButton(parent=self.featurePage)
        self.processBtn.setObjectName("processBtn")
        self.horizontalLayout_4.addWidget(self.processBtn)
        self.annotationBtn = QtWidgets.QPushButton(parent=self.featurePage)
        self.annotationBtn.setObjectName("annotationBtn")
        self.horizontalLayout_4.addWidget(self.annotationBtn)
        self.stackedWidget.addWidget(self.featurePage)
        
        self.lemmaPage = QtWidgets.QWidget()
        self.lemmaPage.setObjectName("lemmaPage")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.lemmaPage)
        self.verticalLayout_3.setSpacing(14)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(25)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.inputLabel = QtWidgets.QLabel(parent=self.lemmaPage)
        self.inputLabel.setObjectName("inputLabel")
        self.verticalLayout.addWidget(self.inputLabel)
        self.inputText = QtWidgets.QPlainTextEdit(parent=self.lemmaPage)
        self.inputText.setObjectName("inputText")
        self.verticalLayout.addWidget(self.inputText)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.resulLabel = QtWidgets.QLabel(parent=self.lemmaPage)
        self.resulLabel.setObjectName("resulLabel")
        self.verticalLayout_2.addWidget(self.resulLabel)
        self.resultText = QtWidgets.QPlainTextEdit(parent=self.lemmaPage)
        self.resultText.setObjectName("resultText")
        self.verticalLayout_2.addWidget(self.resultText)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.importBtn = QtWidgets.QPushButton(parent=self.lemmaPage)
        self.importBtn.setObjectName("importBtn")
        self.horizontalLayout_2.addWidget(self.importBtn)
        self.exportBtn = QtWidgets.QPushButton(parent=self.lemmaPage)
        self.exportBtn.setObjectName("exportBtn")
        self.horizontalLayout_2.addWidget(self.exportBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.lemmatizeBtn = QtWidgets.QPushButton(parent=self.lemmaPage)
        self.lemmatizeBtn.setObjectName("lemmatizeBtn")
        self.horizontalLayout_2.addWidget(self.lemmatizeBtn)
        self.clearBtn = QtWidgets.QPushButton(parent=self.lemmaPage)
        self.clearBtn.setObjectName("clearBtn")
        self.horizontalLayout_2.addWidget(self.clearBtn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.stackedWidget.addWidget(self.lemmaPage)
        
        self.validationPage = QtWidgets.QWidget()
        self.validationPage.setObjectName("validationPage")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.validationPage)
        self.verticalLayout_4.setContentsMargins(6, 4, 0, 9)
        self.verticalLayout_4.setSpacing(11)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(parent=self.validationPage)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.validText = QtWidgets.QPlainTextEdit(parent=self.validationPage)
        self.validText.setObjectName("validText")
        self.verticalLayout_4.addWidget(self.validText)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(18)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.validTokenBtn = QtWidgets.QPushButton(parent=self.validationPage)
        self.validTokenBtn.setObjectName("validTokenBtn")
        self.horizontalLayout_5.addWidget(self.validTokenBtn)
        self.invalidTokenBtn = QtWidgets.QPushButton(parent=self.validationPage)
        self.invalidTokenBtn.setObjectName("invalidTokenBtn")
        self.horizontalLayout_5.addWidget(self.invalidTokenBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.stackedWidget.addWidget(self.validationPage)
        
        self.processPage = QtWidgets.QWidget()
        self.processPage.setObjectName("processPage")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.processPage)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_2 = QtWidgets.QLabel(parent=self.processPage)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.processText = QtWidgets.QPlainTextEdit(parent=self.processPage)
        self.processText.setObjectName("processText")
        self.verticalLayout_7.addWidget(self.processText)
        self.horizontalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(parent=self.processPage)
        self.label_5.setScaledContents(False)
        self.label_5.setIndent(0)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.tokenizationBtn = QtWidgets.QPushButton(parent=self.processPage)
        self.tokenizationBtn.setObjectName("tokenizationBtn")
        self.verticalLayout_5.addWidget(self.tokenizationBtn)
        self.morphemeBtn = QtWidgets.QPushButton(parent=self.processPage)
        self.morphemeBtn.setObjectName("morphemeBtn")
        self.verticalLayout_5.addWidget(self.morphemeBtn)
        self.potentialLemmaBtn = QtWidgets.QPushButton(parent=self.processPage)
        self.potentialLemmaBtn.setObjectName("potentialLemmaBtn")
        self.verticalLayout_5.addWidget(self.potentialLemmaBtn)
        self.morphBtn = QtWidgets.QPushButton(parent=self.processPage)
        self.morphBtn.setObjectName("morphBtn")
        self.verticalLayout_5.addWidget(self.morphBtn)
        self.lemmaRankingBtn = QtWidgets.QPushButton(parent=self.processPage)
        self.lemmaRankingBtn.setObjectName("lemmaRankingBtn")
        self.verticalLayout_5.addWidget(self.lemmaRankingBtn)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.stackedWidget.addWidget(self.processPage)
        
        self.annotationPage = QtWidgets.QWidget()
        self.annotationPage.setObjectName("annotationPage")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.annotationPage)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 15)
        self.verticalLayout_6.setSpacing(20)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtWidgets.QLabel(parent=self.annotationPage)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.annotationTable = QtWidgets.QTableWidget(parent=self.annotationPage)
        self.annotationTable.setObjectName("annotationTable")
        self.annotationTable.setColumnCount(2)
        self.annotationTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.annotationTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.annotationTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout_6.addWidget(self.annotationTable)
        self.label_4 = QtWidgets.QLabel(parent=self.annotationPage)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.stackedWidget.addWidget(self.annotationPage)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lemmaBtn.setText(_translate("MainWindow", "Lemmatization"))
        self.validationBtn.setText(_translate("MainWindow", "Validation"))
        self.processBtn.setText(_translate("MainWindow", "Process"))
        self.annotationBtn.setText(_translate("MainWindow", "Annotation"))
        self.inputLabel.setText(_translate("MainWindow", "Input Tagalog Text"))
        self.resulLabel.setText(_translate("MainWindow", "Result"))
        self.importBtn.setText(_translate("MainWindow", "Import"))
        self.exportBtn.setText(_translate("MainWindow", "Export"))
        self.lemmatizeBtn.setText(_translate("MainWindow", "Lemmatize"))
        self.clearBtn.setText(_translate("MainWindow", "Clear"))
        self.label.setText(_translate("MainWindow", "Validation"))
        self.validTokenBtn.setText(_translate("MainWindow", "Valid Tokens"))
        self.invalidTokenBtn.setText(_translate("MainWindow", "Invalid Tokens"))
        self.label_2.setText(_translate("MainWindow", "Process"))
        self.label_5.setText(_translate("MainWindow", "Display"))
        self.tokenizationBtn.setText(_translate("MainWindow", "Tokenization"))
        self.morphemeBtn.setText(_translate("MainWindow", "Morphemes"))
        self.potentialLemmaBtn.setText(_translate("MainWindow", "Potential Lemma"))
        self.morphBtn.setText(_translate("MainWindow", "Morphological Stripping"))
        self.lemmaRankingBtn.setText(_translate("MainWindow", "Lemma Ranking"))
        self.label_3.setText(_translate("MainWindow", "Annotation"))
        item = self.annotationTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.annotationTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        self.label_4.setText(_translate("MainWindow", "Tagalog Input and Lemma Output will be annotated here       "))
        self.titleLabel.setText(_translate("MainWindow", "Lemmatization of Formal Tagalog Words"))
        self.featureBtn.setText(_translate("MainWindow", "Features"))