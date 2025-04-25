from PyQt6.QtWidgets import (
    QApplication, QTextEdit, QMainWindow, QLabel, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QTextCursor, QCursor, QColor
from PyQt6.QtCore import Qt, QUrl
import sys
import TagLemma
import re

class PopupWindow(QMainWindow):
    def __init__(self, parent, lemma, pos, definition):
        super().__init__(parent)
        self.setWindowTitle("Meaning")

        # Styled Lemma (green background)
        lemma_label = QLabel(f"Lemma: {lemma}")
        lemma_label.setStyleSheet("""
            background-color: #1f6663;
            color: white;
            font-weight: bold;
            font-size: 24px;
            padding: 10px;
            border-radius: 8px;
        """)

        # POS and Definition (white background)
        details_label = QLabel(f"Part of Speech: {pos}\nDefinition: {definition}")
        details_label.setStyleSheet("""
            background-color: white;
            color: black;
            font-size: 18px;
            padding: 10px;
            border-radius: 8px;
        """)

        layout = QVBoxLayout()
        layout.addWidget(lemma_label)
        layout.addWidget(details_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        

class ClickableTextEdit(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setHtml("")
        self.parser = None

    def mouseMoveEvent(self, event):
        cursor = self.cursorForPosition(event.position().toPoint())
        anchor = cursor.charFormat().anchorHref()
        if anchor:
            self.viewport().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            self.viewport().unsetCursor()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        cursor = self.cursorForPosition(event.pos())
        anchor_href = cursor.charFormat().anchorHref()  # Check if clicked text is a link

        if anchor_href:
            # Save the initial cursor position
            initial_pos = cursor.position()

            # Find the start of the clickable block (expand left until whitespace or start)
            while True:
                cursor.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor)
                prev_char = cursor.selectedText()[-1] if cursor.selectedText() else ""
                if prev_char.isspace() or cursor.position() == 0:
                    break

            start_pos = cursor.position()

            # Reset cursor to initial position
            cursor.setPosition(initial_pos)

            # Find the end of the clickable block (expand right until whitespace or end)
            while True:
                cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)
                next_char = cursor.selectedText()[-1] if cursor.selectedText() else ""
                if next_char.isspace() or cursor.position() == len(self.toPlainText()):
                    break

            end_pos = cursor.position()

            # Select the entire clickable span
            cursor.setPosition(start_pos)
            cursor.setPosition(end_pos, QTextCursor.MoveMode.KeepAnchor)

            # Extract and handle the link
            link_text = cursor.selectedText().strip()
            self.handle_link(link_text)
        else:
            # Default behavior (non-link clicks)
            super().mouseReleaseEvent(event)
        

    def handle_link(self, link_text):
        # Lemma
        # Part of Speech
        # Definition
      

        link_text = link_text.strip().split()[-1]
        
        truncate = link_text[:link_text.find("(")]
        content = self.find(truncate)
        
        
        # Pass the current window as the parent to the PopupWindow
        try:
            lemma = content['lemma']
            pos = content['part-of-speech']
            definition = content['definition']
            self.popup = PopupWindow(self, lemma, pos, definition)
            self.popup.show()
            frame_geometry = self.popup.frameGeometry()
            screen_center = QApplication.primaryScreen().availableGeometry().center()
            frame_geometry.moveCenter(screen_center)
            self.popup.move(frame_geometry.topLeft())
        except:
            print("uh oh")


    def find(self, text):
        for index, word in enumerate(self.parser):
            if word['lemma'] == text:
                return self.parser[index]
        return None

    def set_parser(self, set):
        self.parser = set

    def append_link(self, href, text):
        cursor = self.textCursor()
        
        if text.endswith("(NN)"):
            cursor.insertHtml(f"<p><a href='{href}' style='background: #fb6962; color: black; text-decoration: none;'>{text}</a> </p>")
        elif text.endswith("(VRB)"):
            cursor.insertHtml(f"<p><a href='{href}' style='background: #a9def9; color: black; text-decoration: none;'>{text}</a> </p>")
        elif text.endswith("(ADJ)"):
            cursor.insertHtml(f"<p><a href='{href}' style='background: #79de79; color: black; text-decoration: none;'>{text}</a> </p>")
        elif text.endswith("(ADV)"):
            cursor.insertHtml(f"<p><a href='{href}' style='background: #fcfc99; color: black; text-decoration: none;'>{text}</a> </p>")
        elif text.endswith("(UNK)"):
            cursor.insertHtml(f"<p><a href='{href}' style='background: gray; color: black; text-decoration: none;'>{text}</a> </p>")

        else:
            cursor.insertHtml(f"<p>{text} </p>")

