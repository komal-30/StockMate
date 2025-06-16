from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QComboBox, QMessageBox
)
from database import create_connection

class GoodsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goods Receiving Form")

        layout = QFormLayout()

        # Product selection combo box (load product names from DB)
        self.product_combo = QComboBox()
        self.load_products()

        self.supplier_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.rate_input = QLineEdit()
        self.total_label = QLabel("0.0")
        self.tax_input = QLineEdit()

        # Calculate total when quantity or rate changes
        self.quantity_input.textChanged.connect(self.calculate_total)
        self.rate_input.textChanged.connect(self.calculate_total)

        layout.addRow("Product:", self.product_combo)
        layout.addRow("Supplier Name:", self.supplier_input)
        layout.addRow("Quantity:", self.quantity_input)
        layout.addRow("Unit:", self.unit_input)
        layout.addRow("Rate per Unit:", self.rate_input)
        layout.addRow("Total Rate:", self.total_label)
        layout.addRow("Tax (%):", self.tax_input)

        save_btn = QPushButton("Save Goods Receiving")
        save_btn.clicked.connect(self.save_goods)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(save_btn)

        self.setLayout(main_layout)

    def load_products(self):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM products")
        self.products = cur.fetchall()  # List of tuples (id, name)
        conn.close()

        self.product_combo.clear()
        for _, name in self.products:
            self.product_combo.addItem(name)

    def calculate_total(self):
        try:
            qty = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            total = qty * rate
            self.total_label.setText(f"{total:.2f}")
        except ValueError:
            self.total_label.setText("0.0")

    def save_goods(self):
        idx = self.product_combo.currentIndex()
        if idx == -1:
            QMessageBox.warning(self, "Validation Error", "No product selected.")
            return
        product_id = self.products[idx][0]

        supplier = self.supplier_input.text()
        unit = self.unit_input.text()
        tax_text = self.tax_input.text()

        try:
            quantity = float(self.quantity_input.text())
            rate_per_unit = float(self.rate_input.text())
            tax = float(tax_text) if tax_text else 0.0
            total_rate = quantity * rate_per_unit
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Quantity, Rate, and Tax must be numbers.")
            return

        if not supplier or not unit:
            QMessageBox.warning(self, "Validation Error", "Please fill all required fields.")
            return

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO goods_receiving
        (product_id, supplier_name, quantity, unit, rate_per_unit, total_rate, tax)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (product_id, supplier, quantity, unit, rate_per_unit, total_rate, tax))

        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Goods receiving record saved successfully!")

        # Clear inputs
        self.supplier_input.clear()
        self.quantity_input.clear()
        self.unit_input.clear()
        self.rate_input.clear()
        self.tax_input.clear()
        self.total_label.setText("0.0")
