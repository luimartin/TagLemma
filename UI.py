from designUI import Ui_MainWindow
import sys
import TagLemma
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication, QSizePolicy

#pyuic5 xyz.ui -o xyz.py
class MainMenu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.t = TagLemma.TagLemma()
        self.t.load_lemma_to_dfame('tagalog_lemmas.txt')
        self.t.load_formal_tagalog('formal_tagalog.txt')
        
        
        label_height = 65
        self.label.setFixedHeight(label_height)
        self.label_2.setFixedHeight(label_height)
        self.input.setPlaceholderText('Enter Formal Tagalog Text to Lemmatize...')
        self.result.setPlaceholderText("Lemmatize Tagalog Words Here")
        # CSS for MainWindow
        self.setStyleSheet("""
            QWidget{ background: #FDFDFD; } 
            QTextEdit{ background: #FAF9F6; border: 2px solid black; border-radius: 10px; color: black}
            QPushButton { border: 2px solid black; background: #FAF9F6 ;border-radius: 10px;}\
            QPushButton:hover { background: #E0DED9;}
            QPushButton:pressed { background: #C0BEB8;  border-color: #5E5E5E}""")
        # CSS for lemmatize button
        self.lemmatize_button.setStyleSheet("""
            QPushButton { border: 2px solid black;background: #44F52D; border-radius: 10px;}
            QPushButton:hover { background: #3CC026; }
            QPushButton:pressed { background: #2A8E1D; border-color: #5E5E5E}""")
        # CSS for clear button
        self.clear_button.setStyleSheet("""
            QPushButton{ border: 2px solid black; background: #EB2121; border-radius: 10px; ;}
            QPushButton:hover{ background: #C91D1D;}
            QPushButton:pressed { background: #A51717; border-color: #5E5E5E}""")
        
        # click handler for clear button
        self.clear_button.clicked.connect(self.clear)
        self.lemmatize_button.clicked.connect(self.lemmatize)

        self.result.setEnabled(False)
        

    def clear(self):
        self.input.setText("")
        self.result.setText("")
        print("Cleared")
    
    def lemmatize(self):
        self.t.lemmatize(self.input.toPlainText())
        self.result.setText(self.t.result)

app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())