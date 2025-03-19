from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QApplication, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class CustomButton(QPushButton):
    def __init__(self, icon_path, title, description, parent=None):
        super().__init__(parent)

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # Spacing
        self.spacer_above_icon = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(self.spacer_above_icon)
        
        # Icon
        self.icon_label = QLabel()                         # width, height, image expander
        self.icon_label.setPixmap(QPixmap(icon_path).scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.icon_label)

        # Spacer in between
        self.spacer_above_text = QSpacerItem(20, 40)
        self.layout.addItem(self.spacer_above_text)

        # Container for title and description
        self.text_container = QWidget()
        self.text_container.setStyleSheet("background: rgb(0,, 0, 0, 0);") # Transparent background
        self.text_layout = QVBoxLayout(self.text_container)
        self.text_layout.setContentsMargins(0, 0, 0, 0)
        self.text_layout.setSpacing(2)

        # Title add margin to space description
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.title_label.setContentsMargins(0, 0, 0, 5)
        self.text_layout.addWidget(self.title_label)

        # Description add margin to space title
        self.desc_label = QLabel(description)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: gray; font-size: 10px;")
        self.text_layout.addWidget(self.desc_label)

        # Spacer below text
        spacer_below_text = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.text_layout.addItem(spacer_below_text)

        # Add container to the main layout
        self.layout.addWidget(self.text_container)
        
        # Button effects
        self.pressed.connect(self.on_press)
        self.released.connect(self.on_release)
        
    def on_press(self):
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #ffffff;")
   
    def on_release(self):
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: black;")
        



if __name__ == "__main__":
    app = QApplication([])
    window = CustomButton("C:/Users/maver/Pictures/Screenshots/Screenshot 2025-03-09 183004.png", "My Title", "This is a description.")
    window.clicked.connect(lambda: print("Button clicked!"))
    window.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    window.show()
    app.exec()