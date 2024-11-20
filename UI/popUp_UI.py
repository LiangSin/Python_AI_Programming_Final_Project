from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


class PopupWindow(QDialog):
    def __init__(self, message=""):
        super().__init__()
        self.setWindowTitle("Warning")
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        # Add message label
        self.message_label = QLabel(message, self)
        # self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        # Add OK button
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.center()
    
    def center(self):
        """Center the dialog on the parent or the screen."""
        parent = self.parent()
        if parent:
            # Center on parent window
            parent_geometry = parent.frameGeometry()
            parent_center = parent_geometry.center()
            self_geometry = self.frameGeometry()
            self_geometry.moveCenter(parent_center)
            self.move(self_geometry.topLeft())
        else:
            # Center on the screen
            screen_center = self.screen().geometry().center()
            self_geometry = self.frameGeometry()
            self_geometry.moveCenter(screen_center)
            self.move(self_geometry.topLeft())

class PopupWindowHelp(QDialog):
    def __init__(self, message=""):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()

        # Add message label
        self.message_label = QLabel(message, self)
        # self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        # Add OK button
        ok_button = QPushButton("Thank You !", self)
        ok_button.clicked.connect(self.close)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.center()
    
    def center(self):
        """Center the dialog on the parent or the screen."""
        parent = self.parent()
        if parent:
            # Center on parent window
            parent_geometry = parent.frameGeometry()
            parent_center = parent_geometry.center()
            self_geometry = self.frameGeometry()
            self_geometry.moveCenter(parent_center)
            self.move(self_geometry.topLeft())
        else:
            # Center on the screen
            screen_center = self.screen().geometry().center()
            self_geometry = self.frameGeometry()
            self_geometry.moveCenter(screen_center)
            self.move(self_geometry.topLeft())