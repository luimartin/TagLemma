from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QFontMetricsF, QTextCursor, QTextBlockFormat 
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import PyQt6

class Dialog(QDialog):
    def __init__(self, obj, parent):
        super().__init__(parent)
        self.t = obj
        loadUi("dialog.ui", self)  # Load the .ui file dynamically
        self.setWindowTitle("Tagalog Lemmatizer Algorithm")
        self.design()
        self.setLayout(self.verticalLayout)
        self.setMinimumSize(935, 576)
        self.output.setReadOnly(True)
        self.keys_list = list(self.t.source_to_target.keys())
        self.values_list = list(self.t.source_to_target.values())
        metrics = QFontMetricsF(self.output.font())
        

        # Adjust this multiplier to change tab size
        tab_width = metrics.horizontalAdvance(" ") * 2
        self.output.setTabStopDistance(tab_width)
        self.lemmatizable.addItems(self.keys_list)

        self.algo.addItems(["Cosine Similarity", "Levenshtein Distance", "Longest Common Substring"])
        self.lemmatizable.currentIndexChanged.connect(self.fuzzy_match)
        self.algo.currentTextChanged.connect(
            lambda: self.fuzzy_match(self.lemmatizable.currentIndex()))
        self.output.setText(self.t.show_cosine_similarity(
            self.keys_list[self.lemmatizable.currentIndex()], self.values_list[self.lemmatizable.currentIndex()]))
        self.center_text()

    def fuzzy_match(self, index):
        if self.algo.currentText() == "Cosine Similarity":
            print(index)
            self.output.setText(self.t.show_cosine_similarity(
                self.keys_list[index], self.values_list[index]))
            self.center_text()
        elif self.algo.currentText() == "Levenshtein Distance":
            print(index)
            self.output.setText(self.t.show_lev_distance(
                self.keys_list[index], self.values_list[index]))
            self.center_text()
        else:
            print(index)
            self.output.setText(self.t.show_lcs(
                self.keys_list[index], self.values_list[index]))
            self.center_text()


    def center_text(self):
        #center ouput
        cursor = self.output.textCursor()
        block_format = QTextBlockFormat()
        block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeBlockFormat(block_format)


    def design(self):
        self.label_2Icon = f'<img src = "assets/algorithm.png" width = "20" height = "18">'
        self.label_2.setText(PyQt6.QtCore.QCoreApplication.translate("Dialog", f'{self.label_2Icon} Algorithm'))
        self.label_2.setStyleSheet("font-size: 14px;")
        
        
        self.label_3Icon = f'<img src = "assets/approve.png" width = "20" height = "18">'
        self.label_3.setText(PyQt6.QtCore.QCoreApplication.translate("Dialog", f'{self.label_3Icon} Lemmatizable Token/s'))
        self.label_3.setStyleSheet("font-size: 14px;")

        self.label.setStyleSheet("""
            color: white;
            padding-top: 10px;
            padding-bottom: 10px;
            background: #1f6663;
            border: 1px ridge white;
            border-radius: 5px;
            font-size: 30px;

        """)
        self.output.setStyleSheet("""
        QTextEdit {
            background: #ffffff;
            border: 2px solid black;
            border-radius: 5px;
            font-size: 18px;
            font-family: "Consolas";  
        }       
  
        QScrollBar:vertical {
            border: none;
            background: #ecf6f9;
            width: 6px;  /* Makes the vertical scrollbar slimmer */
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #1f6663;
            min-height: 20px;
            border-radius: 3px;  /* Keeps it rounded for a modern look */
        } 
        """)
        self.setStyleSheet("""
        
        QWidget{
            background: #ecf6f9;} 

        QComboBox {
            background: white;
            color: black;
            border: 2px solid black;
            padding: 5px;
            font-family: "Consolas";
            font-size: 18px;
        }
                           
        QLabel {
            background: rgb(0,0,0,0);
            font-family: "Consolas"; 
            font-size: 23px;
            font-weight: bold;
            color: black; 
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
        
        QScrollBar:vertical {
            border: none;
            background: #ecf6f9;
            width: 6px;  /* Makes the vertical scrollbar slimmer */
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background: #1f6663;
            min-height: 20px;
            border-radius: 3px;  /* Keeps it rounded for a modern look */
        }                
        """)
        