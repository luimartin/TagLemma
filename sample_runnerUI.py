from sampleUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QSizePolicy, QFileDialog, QProgressDialog, QLabel, QComboBox, QSpacerItem, QPushButton, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QCoreApplication, QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6 import QtGui, QtCore 
import sys
import pdf
import TagLemma
import fitz
import docx
import json
"""
page indexing
0 featurepage
1 lemmapage
2 validationpage
3 processPage
4 annotaitonPage
"""
# For The UI components, it uses : camelCase
# For The UI behavior and function, it uses snake-case


# async functionality for lemmas if ever the process takes to long...
class LemmatizeThread(QThread):
    # Signal to send the result back to the main thread
    # update this shit if u want to add the variable to be send to the UI
    finished = pyqtSignal(str, list, list, list, list,
                          list, list, list, dict, dict, object)

    def __init__(self, text):
        super().__init__()
        self.text = text
        self.lemma_object = None

    def run(self):
        self.t = TagLemma.TagLemma()
        self.t.load_lemma_to_dfame('tagalog_lemmas.txt')
        self.t.load_formal_tagalog('formal_tagalog.txt')
        result, lemmas, self.lemma_obj = self.t.lemmatize_no_print(self.text)
        valid_tokens = self.t.valid_tokens
        invalid_tokens = self.t.invalid_tokens
        tokenized = self.t.tokenized
        result_removed_sw = self.t.result_removed_sw
        morphemes = self.t.show_inflection_and_morpheme()
        exclude_invalid = self.t.exclude_invalid()
        annotation = self.t.show_annotation()
        source_to_target = self.t.source_to_target

        # To be send to the main UI sadhkjasdhas
        self.finished.emit(result, valid_tokens, lemmas,
            invalid_tokens, tokenized, morphemes, result_removed_sw, 
            exclude_invalid, annotation, source_to_target, self.lemma_obj)


class MainMenu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.t = TagLemma.TagLemma()
        self.t_thread = None
        #======================================================================

        self.setWindowTitle("TagLemma")
        self.setWindowIcon(QIcon("assets/logo.png"))
        
        self.centralwidget.setStyleSheet("""
            background: #ecf6f9;
                    
        """)
        self.headerWidget.setStyleSheet("""
            background: #1f6663;
            border-right: 1px ridge white;
            border-bottom: 1px ridge white;
            border-top: none;
            border-left: none;
            border-radius: 5px;
        """)
        self.titleLabel.setStyleSheet("""
            color: #ffffff;  
            padding: 0px 5px;
            font-size: 20px;
            font-family: "Georgia";
            font-weight: bold;
            border-left: none;
            border-right: none;  
            border-radius: 1px;                                             
        """)
        
        self.featureBtn.setStyleSheet("""
            QPushButton {
                color: white;
                font-family: "Poppins"; 
                border-radius: 2px;
                border: 2px solid rgba(0, 0, 0, 0);
            } 
            QPushButton:pressed {
                background-color: black;  
            }                      
        """) 
        self.stackedWidget.setStyleSheet("""  
            QLabel{
                background: rgb(0,0,0,0);
                font-family: "Georgia"; 
                font-size: 16px;
                font-weight: bold;
                color: black; 
            }       
            QPushButton {
                background: #FAF9F6;
                font-weight: bold;
                font-family: "Segoe UI";
                border-top: none;
                border-bottom: 2px solid black; 
                border-left: none;
                border-right: 2px solid black;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:pressed {
                background-color: #1f6663;
                color: white;  
            }
            QPlainTextEdit{
                background: #ffffff;
                border: 1px solid black;
            }
            QComboBox {
                background: white;
                color: black;
                border: 2px solid black;
                padding: 5px;
                font-family: "Segoe UI";
                font-size: 14px;
            }
            
            QComboBox QAbstractItemView {
                border: 2px solid black;
                selection-background-color: white; 
                selection-color: black; 
                outline: none;
            }
            
            QComboBox QAbstractItemView::item:selected {
                background: #1f6663;  
                color: white;
            }         
        """)
        
        self.featurePage.setStyleSheet(("""
            QPushButton {
                background: #ffffff;
                border: 1px solid #1f6663;
                border-radius: 4px;
            }
            QPushButton:Hover{
                background: #FAF9F6;
            }
            QPushButton:pressed {
                background: #1f6663;
            }
            
            QPushButton:disabled {
                background: #ececec;
            }  
        """))
        
        self.annotationPage.setStyleSheet(("""
            QTableWidget {
                background: #ffffff;
                border: 2px solid black;
            }

            QTableWidget::item {
                background: #ffffff;
                border: 1px solid #dcdcdc;
            }

            QHeaderView::section {
                background: #f0f0f0;
                border: 1px solid black;
                padding: 4px;
            }

            QTableWidget {
                gridline-color: black;
            }
        """))
        
        self.featureBtn.setIcon(QIcon("assets/feature-icon.png"))
        self.featureBtn.setIconSize(self.featureBtn.size()) 
        self.featureBtn.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.featureBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.importBtn.setIcon(QIcon("assets/import.png"))
        self.importBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.importBtn.setIconSize(QSize(20, 18)) 
        
        self.exportBtn.setIcon(QIcon("assets/export.png"))
        self.exportBtn.setIconSize(QSize(20, 18)) 
        self.exportBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.lemmatizeBtn.setIcon(QIcon("assets/lemmatize.png"))
        self.lemmatizeBtn.setIconSize(QSize(20, 18)) 
        self.lemmatizeBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.clearBtn.setIcon(QIcon("assets/trash.png"))
        self.clearBtn.setIconSize(QSize(20, 18)) 
        self.clearBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.validTokenBtn.setIcon(QIcon("assets/checked.png"))
        self.validTokenBtn.setIconSize(QSize(20, 18))
        self.validTokenBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.invalidTokenBtn.setIcon(QIcon("assets/cancel.png"))
        self.invalidTokenBtn.setIconSize(QSize(20, 18))
        self.invalidTokenBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.comboBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        _translate = QCoreApplication.translate
        inputIcon = f'<img src="assets/text.png" width="20" height="20">'
        self.inputLabel.setText(_translate("MainWindow", f'{inputIcon} Input Tagalog Text'))
        
        resultIcon = f'<img src="assets/results.png" width="20" height="20">'
        self.resulLabel.setText(_translate("MainWindow", f'{resultIcon} Result'))
        
        validationIcon = f'<img src="assets/shield.png" width="20" height="20">'
        self.label.setText(_translate("MainWindow", f'{validationIcon} Validation'))
        
        processIcon = f'<img src="assets/process.png" width="20" height="20">'
        self.label_2.setText(_translate("MainWindow", f'{processIcon} Process'))
        
        displayIcon = f'<img src="assets/display.png" width="15" height="15">'
        self.label_5.setText(_translate("MainWindow", f'{displayIcon} Display'))
        
        anonotationIcon = f'<img src="assets/writing.png" width="20" height="20">'
        self.label_3.setText(_translate("MainWindow", f'{anonotationIcon} Annotation'))
        
        self.lemmaBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.validationBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.processBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.annotationBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        
        self.tokenizationBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.morphemeBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.potentialLemmaBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.fuzzyBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.lemmaRankingBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        #======================================================================0

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

        # labels for character count in text edits
        # this shit is added in the UI
        self.inputLabelChar = QLabel(parent=self.lemmaPage)
        self.inputLabelChar.setObjectName("inputLabelChar")
        self.inputLabelChar.setText("Character: 0")
        self.verticalLayout.addWidget(self.inputLabelChar)

        self.resultLabelChar = QLabel(parent=self.lemmaPage)
        self.resultLabelChar.setObjectName("resultLabelChar")
        self.resultLabelChar.setText("Character: 0")
        self.verticalLayout_2.addWidget(self.resultLabelChar)

        self.disable_features(False)

        # updates label for char count
        self.inputText.textChanged.connect(self.update_input_label)
        self.resultText.textChanged.connect(self.update_result_label)
        self.inputText.textChanged.connect(self.max_char_count)

        # stacked widget pages connectoers
        self.featureBtn.clicked.connect(self.switch_to_feature)
        self.lemmaBtn.clicked.connect(self.switch_to_lemma)
        self.validationBtn.clicked.connect(self.switch_to_validation)
        self.processBtn.clicked.connect(self.switch_to_process)
        self.annotationBtn.clicked.connect(self.switch_to_annotation)

        # import file parse to textfield
        self.importBtn.clicked.connect(self.load_file)
        self.exportBtn.clicked.connect(self.pdf)

        # lemmaPage button connectors
        self.clearBtn.clicked.connect(self.clear)
        self.resultText.setReadOnly(True)
        self.lemmatizeBtn.clicked.connect(self.lemmatize)
        # combobox in the Lemmatization Page
        self.comboBox.currentIndexChanged.connect(self.combo_box_changed)

        # validationPage button connectors
        self.validTokenBtn.clicked.connect(self.valid_tokens_function)
        self.invalidTokenBtn.clicked.connect(self.invalid_tokens_function)
        self.comboBox.setEnabled(False)

        # processPage button connectors
        self.tokenizationBtn.clicked.connect(self.get_tokenized)
        self.morphemeBtn.clicked.connect(self.display_morphemes)

        # This create the combobox with out editing the whole code.....
        self.label_2 = QLabel(parent=self.processPage)
        self.label_2.setText(_translate("MainWindow", f'{processIcon} Process'))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.addWidget(self.label_2)
        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)
        self.process_dropdown = QComboBox(parent=self.processPage)
        self.process_dropdown.setObjectName(u"process_dropdown")
        self.horizontalLayout_7.addWidget(self.process_dropdown)
        self.verticalLayout_7.insertLayout(0, self.horizontalLayout_7)
        self.process_dropdown.hide()
        self.potentialLemmaBtn.setCheckable(True)
        self.potentialLemmaBtn.clicked.connect(self.potential_lemma_toggle)
        # annotationPage
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)
        self.export_annotation = QPushButton(parent=self.annotationPage)
        self.export_annotation.setObjectName(u"export_annotation")
        self.export_annotation.setText("Export Annotation")
        self.horizontalLayout_7.addWidget(self.export_annotation)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.annotationTable.setReadOnly(True)

        self.export_annotation.clicked.connect(self.save_json)

    def potential_lemma_toggle(self):
        if self.potentialLemmaBtn.isChecked():
            print(self.source_to_target)
            keys = list(self.source_to_target.keys())
            
            self.process_dropdown.addItems(keys)
            self.process_dropdown.show()
            #self.potential_lemma(0, keys)
            print(self.potential_lemma(0, keys))
            self.process_dropdown.currentIndexChanged.connect(
                lambda: self.potential_lemma(self.process_dropdown.currentIndex(), keys))
        else:
            self.process_dropdown.hide()
            self.processText.clear()

    def potential_lemma(self, index, token):
        print(token[index])
        text = (", ".join(self.t_thread.lemma_obj.show_potential_lemmas(token[index])))
        self.processText.setPlainText(text)
        
    # this set the behavior of the results using the combobox
    def combo_box_changed(self, i):
        if i == 0:
            self.resultText.setPlainText(self.result)
        elif i == 1:
            result_str = " ".join(self.exclude_invalid)
            self.resultText.setPlainText(result_str)
        else:
            result_str = " ".join(self.result_removed_sw)
            self.resultText.setPlainText(result_str)

    # sets the maximum char count for the input of words
    def max_char_count(self):
        text = self.inputText.toPlainText()
        max = 50000
        if len(text) > max:
            cursor = self.inputText.textCursor()
            pos = cursor.position()
            self.inputText.setPlainText(text[:max])
            # Restore cursor position (move it to the end if it was past the limit)
            if pos > max:
                pos = max
            cursor.setPosition(pos)
            self.inputText.setTextCursor(cursor)

    # this disable other features of the system when the no lemmatization occurs
    def disable_features(self, bol):
        self.validationBtn.setEnabled(bol)
        self.annotationBtn.setEnabled(bol)
        self.processBtn.setEnabled(bol)

    # clears the inputs
    def clear(self):
        self.comboBox.setCurrentIndex(0)
        self.comboBox.setEnabled(False)
        self.disable_features(False)
        self.inputText.clear()
        self.resultText.clear()
        print("Cleared")

    def lemmatize(self):

        text = self.inputText.toPlainText()
        if not text.strip():
            # # handols empty inputs nyork
            self.message_dialog(QMessageBox.Icon.Warning,
                                "Please Input...", "Warning")
            return

        self.resultText.setPlainText("Please Wait, Currently Lemmatizing.....")
        self.comboBox.setCurrentIndex(0)
        self.validText.setPlainText("")
        self.processText.setPlainText("")
        self.annotationTable.setPlainText("")

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
        self.t_thread =  LemmatizeThread(text)

        self.thread = self.t_thread
        # Connects signal to UI update
        self.thread.finished.connect(self.on_lemmatization_complete)
        self.thread.start()

    # update UI from another threadsasdasd
    def on_lemmatization_complete(self, result, valid_tokens, lemmas, invalid_tokens,
                                  tokenized, morphemes, result_removed_sw, exclude_invalid, annotation, source_to_target):
        # Updates the UI with the lemmatized text and other shits after processing
        self.valid_tokens = valid_tokens
        self.lemmas = lemmas
        self.invalid_tokens = invalid_tokens
        self.result = result  # store the lemma
        self.tokenized = tokenized
        self.morphemes = morphemes
        self.result_removed_sw = result_removed_sw
        self.exclude_invalid = exclude_invalid
        self.annotation = annotation
        self.resultText.setPlainText(self.result)
        self.source_to_target = source_to_target
        temp = json.dumps(annotation, indent=6)
        self.annotationTable.setPlainText(temp)
        self.thread = None
        self.comboBox.setEnabled(True)
        self.disable_features(True)
        # self.progressDialog.close()
        print(source_to_target)

    def valid_tokens_function(self):
        print(self.valid_tokens)
        result_str = ", ".join(self.valid_tokens)

        if not result_str.strip():
            # # handols empty inputs nyork
            self.message_dialog(QMessageBox.Icon.Information,
                                "There was no valid tokens", "Notice")
            return
        self.validText.setPlainText(result_str)

    def invalid_tokens_function(self):
        print(self.invalid_tokens)

        result_str = ", ".join(self.invalid_tokens)

        if not result_str.strip():
            # # handols empty inputs nyork
            self.message_dialog(QMessageBox.Icon.Information,
                                "There was no invalid tokens", "Notice")
            return

        self.validText.setPlainText(result_str)

    # Exclude invalid words on result & Exclude stop words on result
    def lemma(self):
        print(self.lemmas)
        result_str = " ".join(self.lemmas)
        self.resultText.setPlainText(result_str)

    def pdf(self):
        if not self.resultText.toPlainText():
            self.message_dialog(QMessageBox.Icon.Critical,
                                "No Text to Save", "Warning")
            return
            # Open "Save As" dialog for user to choose save location
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save PDF", "", "PDF Files (*.pdf)")

        # Only proceed if a file path was chosen
        if file_path:
            try:
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
                self.message_dialog(QMessageBox.Icon.Information,
                                    f"File saved successfully: {file_path}", "Success")
            except Exception as e:
                self.message_dialog(QMessageBox.Icon.Warning,
                                    f"Error saving file: {e}", "Warning")

    # qmessagedialog for DRY blahvlahblah...
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

    def get_tokenized(self):
        print("tokenzide")
        result_str = ", ".join(self.tokenized)
        self.processText.setPlainText(f'Tokens = [{result_str}]',)
        self.processText

    def display_morphemes(self):
        result_str = "\n".join(self.morphemes)
        self.processText.setPlainText(result_str)


# TODO: parse file to be refactored....

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "PDF Files (*.pdf);;Word Files (*.docx)")
        if file_path:
            text = self.parse_file(file_path)
            self.inputText.setPlainText(text)

    def parse_file(self, file_path):
        if file_path.endswith(".pdf"):
            return self.parse_pdf(file_path)
        elif file_path.endswith(".docx"):
            return self.parse_docx(file_path)
        return "Unsupported file format."

    def parse_pdf(self, file_path):
        doc = fitz.open(file_path)
        text = "".join([page.get_text("text") for page in doc])
        return text

    def parse_docx(self, file_path):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def save_json(self):
        # Open a file dialog to choose save location
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save JSON File", "", "JSON Files (*.json);;All Files (*)")

        if file_path:  # Check if the user selected a file
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    # Write JSON to file
                    json.dump(self.annotation, file, indent=4)
                print(f"File saved successfully: {file_path}")
                self.message_dialog(QMessageBox.Icon.Information,
                                    f"File saved successfully: {file_path}", "Success")
            except Exception as e:
                self.message_dialog(QMessageBox.Icon.Warning,
                                    f"Error saving file: {e}", "Warning")

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
