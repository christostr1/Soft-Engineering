# view/components/product_grid.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from functools import partial
from view.components.product_card import ProductCard

class ProductGrid(QWidget):
    """
    Displays products in a grid layout.
    Emits a signal with product details when any product card is clicked.
    """
    # Signal to emit a dictionary with product details.
    productClicked = pyqtSignal(dict)

    def __init__(self, products, parent=None):
        """
        :param products: A list of dictionaries containing product data.
        """
        super().__init__(parent)
        self.products = products
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)

        # Grid layout (2 columns) for the product cards.
        grid = QGridLayout()
        grid.setSpacing(10)

        for i, product in enumerate(self.products):
            # Create a product card for each product.
            card = ProductCard(**product)
            # Instead of lambda, use partial to capture the product dictionary.
            card.clicked.connect(partial(self.emit_product, product))
            row, col = divmod(i, 2)
            grid.addWidget(card, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(grid)
        self.setLayout(layout)

    def emit_product(self, product: dict):
        """
        Helper function to emit the productClicked signal with the provided product data.
        """
        self.productClicked.emit(product)
