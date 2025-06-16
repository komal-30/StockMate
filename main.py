from PySide6.QtWidgets import QApplication
from login_window import LoginWindow
from main_menu import MainMenu
from product_master import ProductMaster
from database import setup_database
from goods_form import GoodsForm
from sales_form import SalesForm

import sys

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.login_window = LoginWindow(self.show_main_menu)
        self.main_menu = None
        self.goods_form = GoodsForm()
        self.sales_form = SalesForm()
        self.product_form = ProductMaster()

    def show_main_menu(self):
        self.main_menu = MainMenu(self.goods_form.show, self.sales_form.show, self.product_form.show)
        self.main_menu.show()

    def run(self):
        setup_database()
        self.login_window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    setup_database()
    app = App()
    app.run()
