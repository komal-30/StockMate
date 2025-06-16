# goods_form.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class GoodsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goods Receiving")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Goods Receiving Form (To Be Implemented)"))
        self.setLayout(layout)
