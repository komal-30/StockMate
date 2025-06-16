from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog, QMessageBox, QFormLayout
)
from PySide6.QtGui import QPixmap
import os
import shutil
from database import create_connection

class ProductMaster(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master List")

        self.image_path = None  # To store image filepath

        form_layout = QFormLayout()

        self.barcode_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QLineEdit()
        self.subcategory_input = QLineEdit()
        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        self.tax_input = QLineEdit()
        self.price_input = QLineEdit()
        self.unit_input = QLineEdit()

        form_layout.addRow("Barcode:", self.barcode_input)
        form_layout.addRow("SKU:", self.sku_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Subcategory:", self.subcategory_input)
        form_layout.addRow("Product Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Tax (%):", self.tax_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Default Unit:", self.unit_input)

        # Image upload section
        self.img_label = QLabel("No Image Selected")
        self.img_label.setFixedSize(200, 200)
        self.img_label.setStyleSheet("border: 1px solid black;")

        img_btn = QPushButton("Upload Product Image")
        img_btn.clicked.connect(self.upload_image)

        # Save button
        save_btn = QPushButton("Save Product")
        save_btn.clicked.connect(self.save_product)

        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)
        vbox.addWidget(self.img_label)
        vbox.addWidget(img_btn)
        vbox.addWidget(save_btn)

        self.setLayout(vbox)

    def upload_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Product Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.img_label.setPixmap(pixmap.scaled(self.img_label.width(), self.img_label.height()))

    def save_product(self):
        barcode = self.barcode_input.text()
        sku = self.sku_input.text()
        category = self.category_input.text()
        subcategory = self.subcategory_input.text()
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        tax = self.tax_input.text()
        price = self.price_input.text()
        unit = self.unit_input.text()

        if not all([barcode, sku, category, name, price, unit]):
            QMessageBox.warning(self, "Validation Error", "Please fill all required fields (barcode, sku, category, name, price, unit).")
            return

        try:
            tax = float(tax) if tax else 0.0
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Tax and Price must be valid numbers.")
            return

        # Save image to local folder assets/
        saved_image_path = None
        if self.image_path:
            assets_dir = "assets"
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir)
            image_filename = os.path.basename(self.image_path)
            saved_image_path = os.path.join(assets_dir, image_filename)
            shutil.copy(self.image_path, saved_image_path)

        # Insert into DB
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO products
            (barcode, sku, category, subcategory, image_path, name, description, tax, price, unit)
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
        """, (barcode, sku, category, subcategory, saved_image_path, name, description, tax, price, unit))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Product '{name}' saved successfully!")

        # Clear fields
        self.barcode_input.clear()
        self.sku_input.clear()
        self.category_input.clear()
        self.subcategory_input.clear()
        self.name_input.clear()
        self.description_input.clear()
        self.tax_input.clear()
        self.price_input.clear()
        self.unit_input.clear()
        self.img_label.clear()
        self.img_label.setText("No Image Selected")
        self.image_path = None
