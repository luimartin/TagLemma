from sampleUI import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QSizePolicy, QFileDialog
import sys

"""
0 featurepage
1 lemmapage
2 validationpage
3 processPage
4 annotaitonPage
"""

class MainMenu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #set the size for the btns in landing page
        self.lemmaBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.validationBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.annotationBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.processBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        #stacked widget pages connectoers
        self.featureBtn.clicked.connect(self.switch_to_feature)
        self.lemmaBtn.clicked.connect(self.switch_to_lemma)
        self.validationBtn.clicked.connect(self.switch_to_validation)
        self.processBtn.clicked.connect(self.switch_to_process)
        self.annotationBtn.clicked.connect(self.switch_to_annotation)

    # function connectors for stacked widget
    def switch_to_feature(self):
        self.stackedWidget.setCurrentIndex(0)
 
    def switch_to_lemma(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_validation(self):
        self.stackedWidget.setCurrentIndex(2)
 
    def switch_to_process(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_annotation(self):
        self.stackedWidget.setCurrentIndex(4)
        
    

app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())