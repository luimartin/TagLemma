from sampleUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication,QMessageBox , QSizePolicy, QFileDialog, QProgressDialog, QLabel, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal, Qt
import sys
import pdf
import TagLemma

"""
page indexing
0 featurepage
1 lemmapage
2 validationpage
3 processPage
4 annotaitonPage
"""
# async functionality for lemmas if ever the process takes to long...
class LemmatizeThread(QThread):
    # Signal to send the result back to the main thread
    #update this shit if u want to add the variable to be send to the UI
    finished = pyqtSignal(str, list, list, list)

    def __init__(self, text):
        super().__init__()
        self.text = text
    
    def run(self):
        self.t = TagLemma.TagLemma()
        self.t.load_lemma_to_dfame('tagalog_lemmas.txt')
        self.t.load_formal_tagalog('formal_tagalog.txt')
        result, lemmas = self.t.lemmatize_no_print(self.text)
        valid_tokens = self.t.valid_tokens
        invalid_tokens = self.t.invalid_tokens

        # To be send to the main UI sadhkjasdhas
        self.finished.emit(result, valid_tokens, lemmas, invalid_tokens)


class MainMenu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.headerWidget.setMinimumHeight(100)
        # set the size for the btns in landing page
        self.lemmaBtn.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.validationBtn.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.annotationBtn.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.processBtn.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
    

        #labels for character count in text edits 
        #this shit is added in the UI
        self.inputLabelChar = QLabel(parent=self.lemmaPage)
        self.inputLabelChar.setObjectName("inputLabelChar")
        self.inputLabelChar.setText("Character: 0")
        self.verticalLayout.addWidget(self.inputLabelChar)
    
        self.resultLabelChar = QLabel(parent=self.lemmaPage)
        self.resultLabelChar.setObjectName("resultLabelChar")
        self.resultLabelChar.setText("Character: 0")
        self.verticalLayout_2.addWidget(self.resultLabelChar)
        
        #updates label for char count
        self.inputText.textChanged.connect(self.update_input_label)
        self.resultText.textChanged.connect(self.update_result_label)


        # stacked widget pages connectoers
        self.featureBtn.clicked.connect(self.switch_to_feature)
        self.lemmaBtn.clicked.connect(self.switch_to_lemma)
        self.validationBtn.clicked.connect(self.switch_to_validation)
        self.processBtn.clicked.connect(self.switch_to_process)
        self.annotationBtn.clicked.connect(self.switch_to_annotation)

        self.exportBtn.clicked.connect(self.pdf)

        # lemmaPage button connectors
        self.clearBtn.clicked.connect(self.clear)
        self.resultText.setReadOnly(True)
        self.lemmatizeBtn.clicked.connect(self.lemmatize)

        # validationPage button connectors
        self.validTokenBtn.clicked.connect(self.valid_tokens_function)
        self.invalidTokenBtn.clicked.connect(self.invalid_tokens_function)

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

    def clear(self):
        self.inputText.clear()
        self.resultText.clear()
        print("Cleared")

    def lemmatize(self):

        text = self.inputText.toPlainText()
        if not text.strip():
            # # handols empty inputs nyork
            self.message_dialog(QMessageBox.Icon.Warning,"Please Input...", "Warning")
            return  

        self.resultText.setPlainText("Please Wait, Currently Lemmatizing.....")
        
        """
        self.progressDialog = QProgressDialog(
            "Lemmatizing...", "Cancel", 0, 0, self)
        # self.progressDialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.progressDialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.progressDialog.setWindowTitle("Loading")
        self.progressDialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progressDialog.setCancelButton(None)
        self.progressDialog.show()
        """
        # Starts the lemmatization sa ibang thread
        self.thread = LemmatizeThread(text)
        # Connects signal to UI update
        self.thread.finished.connect(self.on_lemmatization_complete)
        self.thread.start()

    # update UI from another threadsasdasd
    def on_lemmatization_complete(self, result, valid_tokens, lemmas, invalid_tokens):
        #Updates the UI with the lemmatized text after processing
        self.valid_tokens = valid_tokens
        self.lemmas = lemmas
        self.invalid_tokens = invalid_tokens
        self.resultText.setPlainText(result)
        self.thread = None
        #self.progressDialog.close()

    def valid_tokens_function(self):
        print(self.valid_tokens)
        result_str = ", ".join(self.valid_tokens)
        self.validText.setPlainText(result_str) 

    def invalid_tokens_function(self):
        print(self.invalid_tokens)
        result_str = ", ".join(self.invalid_tokens)
        self.validText.setPlainText(result_str) 
    
    def pdf(self):
        if self.resultText.toPlainText():
            # Open "Save As" dialog for user to choose save location
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save PDF", "", "PDF Files (*.pdf)")

            # Only proceed if a file path was chosen
            if file_path:
                # initiate pdf class
                page = pdf.pdf()
                # printing process
                page.add_list("Input:")
                page.add_list(self.inputText.toPlainText())
                
                page.add_list("")
                page.add_list("")
                page.add_list("Output:")
                page.add_list(self.resultText.toPlainText())
                # Generate and save the PDF at the chosen location
                page.output(file_path)
        else:
            print("No text to save")

    #qmessagedialog for DRY blahvlahblah...
    def message_dialog(self, icon, message, title):
        msgBox = QMessageBox()
        msgBox.setIcon(icon)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()
    
    # function to see changes in the mfing textedits
    def update_input_label(self):
        x = len(self.inputText.toPlainText())
        self.inputLabelChar.setText(f"Characters: {x}")
    
    def update_result_label(self):
        x = len(self.resultText.toPlainText())
        self.resultLabelChar.setText(f"Characters: {x}")



app = QApplication(sys.argv)
window = MainMenu()
window.show()
sys.exit(app.exec())
