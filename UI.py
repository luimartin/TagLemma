from designUI import Ui_MainWindow
import sys
import TagLemma
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication, QSizePolicy, QFileDialog
import time
import webbrowser
import os
from pdf import pdf

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
            QTextEdit{ background: #FAF9F6; border: 2px solid black; border-radius: 10px}
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
        self.pdf_button.clicked.connect(self.pdf)
        self.preview_button.clicked.connect(self.preview)
        
        # to pdf method
    def pdf(self):
        # Open "Save As" dialog for user to choose save location
        file_path, _ = QFileDialog.getSaveFileName(None, "Save PDF", "", "PDF Files (*.pdf)")

        # Only proceed if a file path was chosen
        if file_path:
            # initiate pdf class
            page = pdf()
            # printing process
            page.add_list(self.result.toPlainText())
            # Generate and save the PDF at the chosen location
            page.output(file_path)
     
        
    # preview method
    def preview(self):
        # initiate pdf class
        page = pdf()
        # printing process
        page.add_list(self.result.toPlainText())
        # pdf generation
        page.output("file.pdf")
        # browser preview
        webbrowser.open("file.pdf")
        # so the file gets a chance to be previewed
        time.sleep(2)
        # volatile effect
        os.remove("file.pdf")

        self.result.setEnabled(False)
        

    def clear(self):
        self.input.setText("")
        self.result.setText("")
        print("Cleared")
    
    def lemmatize(self):
        start = time.perf_counter()
        self.result.setText(self.t.lemmatize_no_print(self.input.toPlainText()))
        end = time.perf_counter()
        print(f"Time Elapsed: {end - start}")

app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())