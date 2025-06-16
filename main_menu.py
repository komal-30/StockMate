from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class MainMenu(QWidget):
    def __init__(self, open_goods_form, open_sales_form, open_product_form):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.resize(300, 300)

        layout = QVBoxLayout()

        btn_goods = QPushButton("Goods Receiving Form")
        btn_sales = QPushButton("Sales Form")
        btn_products = QPushButton("Product Master List")

        btn_goods.clicked.connect(open_goods_form)
        btn_sales.clicked.connect(open_sales_form)
        btn_products.clicked.connect(open_product_form)

        layout.addWidget(btn_goods)
        layout.addWidget(btn_sales)
        layout.addWidget(btn_products)

        self.setLayout(layout)
