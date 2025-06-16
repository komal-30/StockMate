from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QComboBox, QMessageBox
)
from database import create_connection

class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Form")

        layout = QFormLayout()

        self.product_combo = QComboBox()
        self.load_products()

        self.customer_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.rate_input = QLineEdit()
        self.total_label = QLabel("0.0")
        self.tax_input = QLineEdit()

        self.quantity_input.textChanged.connect(self.calculate_total)
        self.rate_input.textChanged.connect(self.calculate_total)

        layout.addRow("Product:", self.product_combo)
        layout.addRow("Customer Name:", self.customer_input)
        layout.addRow("Quantity:", self.quantity_input)
        layout.addRow("Unit:", self.unit_input)
        layout.addRow("Rate per Unit:", self.rate_input)
        layout.addRow("Total Rate:", self.total_label)
        layout.addRow("Tax (%):", self.tax_input)

        save_btn = QPushButton("Save Sale")
        save_btn.clicked.connect(self.save_sale)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(save_btn)

        self.setLayout(main_layout)

    def load_products(self):
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM products")
        self.products = cur.fetchall()
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

    def save_sale(self):
        idx = self.product_combo.currentIndex()
        if idx == -1:
            QMessageBox.warning(self, "Validation Error", "No product selected.")
            return
        product_id = self.products[idx][0]

        customer = self.customer_input.text()
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

        if not customer or not unit:
            QMessageBox.warning(self, "Validation Error", "Please fill all required fields.")
            return

        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sales
            (product_id, customer_name, quantity, unit, rate_per_unit, total_rate, tax)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (product_id, customer, quantity, unit, rate_per_unit, total_rate, tax))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Sale record saved successfully!")

        # Clear inputs
        self.customer_input.clear()
        self.quantity_input.clear()
        self.unit_input.clear()
        self.rate_input.clear()
        self.tax_input.clear()
        self.total_label.setText("0.0")
