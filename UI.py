from designUI import Ui_MainWindow
import sys
import TagLemma
from PyQt6.QtWidgets import QMainWindow, QApplication, QSizePolicy, QFileDialog
from PyQt6.QtCore import QThread, pyqtSignal
import time
import webbrowser
import os
from pdf import pdf

# pyuic5 xyz.ui -o xyz.py

# async functionality for lemmas if ever the process takes to long...
class LemmatizeThread(QThread):
    finished = pyqtSignal(str, list, list)  # Signal to send the result back to the main thread

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        start = time.perf_counter()
        self.t = TagLemma.TagLemma()
        self.t.load_lemma_to_dfame('tagalog_lemmas.txt')
        self.t.load_formal_tagalog('formal_tagalog.txt')
        result, lemmas = self.t.lemmatize_no_print(self.text)
        valid_tokens = self.t.valid_tokens
        end = time.perf_counter()
        print(f"Time Elapsed: {end - start}")

        self.finished.emit(result,valid_tokens, lemmas) # To be send to the main UI sadhkjasdhas

class MainMenu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        label_height = 70
        self.label.setFixedHeight(label_height)
        self.label_2.setFixedHeight(label_height)
        self.valid_tokens = None
        self.lemmas = None
        self.input.setPlaceholderText(
            'Enter Formal Tagalog Text to Lemmatize...')
        self.result.setPlaceholderText("Lemmatize Tagalog Words Here")
        self.result.setReadOnly(True)
        self.buttons_state(False)
        # CSS for MainWindow
        self.setStyleSheet("""
				QWidget{ background: #FDFDFD; font-family: 'Sans-serif';} 
				QPlainTextEdit{ background: #FAF9F6; border: 2px solid black; border-radius: 10px; font-size: 18px; }
				QPushButton { border: 2px solid black; background: #FAF9F6 ;border-radius: 10px;  font-size: 15px;}\
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

        # click handler for buttons...
        self.clear_button.clicked.connect(self.clear)
        self.lemmatize_button.clicked.connect(self.lemmatize)
        self.pdf_button.clicked.connect(self.pdf)
        self.token_button.clicked.connect(self.token)
        self.lemma_button.clicked.connect(self.lemma)
        # self.preview_button.clicked.connect(self.preview)

    def lemmatize(self):
        
        text = self.input.toPlainText()
        if not text.strip():
            return  # handols empty strings nyork

        self.result.setPlainText("Please Wait, Currently Lemmatizing.....")
        # Starts the lemmatization sa ibang thread.
        self.thread = LemmatizeThread(text)
        self.thread.finished.connect(self.on_lemmatization_complete)  # Connect signal to UI update
        self.thread.start()  

    def on_lemmatization_complete(self, result, valid_tokens, lemmas):
        """Updates the UI with the lemmatized text after processing."""
        self.valid_tokens = valid_tokens
        self.lemmas = lemmas
        self.result.setPlainText(result)  # Update UI from another thread
        self.thread = None 
        self.buttons_state(True) 

    def token(self):
        print(self.valid_tokens)
        result_str = ", ".join(self.valid_tokens)
        self.result.setPlainText(result_str)

    def lemma(self):    
        print(self.lemmas)
        result_str = ", ".join(self.lemmas)
        self.result.setPlainText(result_str)

    def buttons_state(self, state):
        self.lemma_button.setEnabled(state)
        self.token_button.setEnabled(state)
        self.pdf_button.setEnabled(state)
        self.process_button.setEnabled(state)

# to pdf method
    def pdf(self):

        if self.result.toPlainText():
            # Open "Save As" dialog for user to choose save location
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save PDF", "", "PDF Files (*.pdf)")

            # Only proceed if a file path was chosen
            if file_path:
                # initiate pdf class
                page = pdf()
                # printing process
                page.add_list(self.result.toPlainText())
                # Generate and save the PDF at the chosen location
                page.output(file_path)
        else:
            print("No text to save")

    """    
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
            """

    def clear(self):
        self.input.clear()
        self.result.clear()
        self.buttons_state(False)
        print("Cleared")



app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())
