from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QLabel

class CharacterCounter(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.text_edit = QPlainTextEdit()
        self.text_edit.textChanged.connect(self.update_label)

        self.label = QLabel("Characters: 0")

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def update_label(self):
        text_length = len(self.text_edit.toPlainText())
        self.label.setText(f"Characters: {text_length}")

if __name__ == "__main__":
    app = QApplication([])
    window = CharacterCounter()
    window.show()
    app.exec()