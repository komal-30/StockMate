from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from database import create_connection


class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.setWindowTitle("Operator Login")
        self.resize(300, 300)
        self.on_login_success = on_login_success

        # Username & Password inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)

        # Form layout (vertical stack)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(QLabel("Username:"))
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(QLabel("Password:"))
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(login_btn)

        # Container to center the form
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)

        # Optional: fixed size widget for form
        form_container = QWidget()
        form_container.setLayout(form_layout)
        form_container.setFixedWidth(300)  # Make form width consistent

        container_layout.addWidget(form_container)
        self.setLayout(container_layout)

    def handle_login(self):
        user = self.username_input.text()
        pwd = self.password_input.text()

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM operators WHERE username=%s AND password=%s", (user, pwd))
        result = cur.fetchone()
        conn.close()

        if result:
            self.on_login_success()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
