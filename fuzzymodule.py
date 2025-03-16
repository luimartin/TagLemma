from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QFontMetricsF
from PyQt6.uic import loadUi

class Dialog(QMainWindow):
    def __init__(self, obj, parent):
        super().__init__(parent)
        self.t = obj
        loadUi("dialog.ui", self)  # Load the .ui file dynamically

        self.keys_list = list(self.t.source_to_target.keys())
        self.values_list = list(self.t.source_to_target.values())
        metrics = QFontMetricsF(self.output.font())

        # Adjust this multiplier to change tab size
        tab_width = metrics.horizontalAdvance(" ") * 5
        self.output.setTabStopDistance(tab_width)
        self.lemmatizable.addItems(self.keys_list)

        self.algo.addItems(["Cosine Similarity", "Levenshtein Distance"])
        self.lemmatizable.currentIndexChanged.connect(self.fuzzy_match)
        self.algo.currentTextChanged.connect(
            lambda: self.fuzzy_match(self.lemmatizable.currentIndex()))
        self.output.setPlainText(self.t.show_cosine_similarity(
            self.keys_list[self.lemmatizable.currentIndex()], self.values_list[self.lemmatizable.currentIndex()]))

    def fuzzy_match(self, index):
        if self.algo.currentText() == "Cosine Similarity":
            print(index)
            self.output.setPlainText(self.t.show_cosine_similarity(
                self.keys_list[index], self.values_list[index]))
        else:
            print(index)
            self.output.setPlainText(self.t.show_lev_distance(
                self.keys_list[index], self.values_list[index]))

