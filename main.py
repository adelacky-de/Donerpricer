import os
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QCompleter,
    QHeaderView,
    QScrollArea,
    QFrame, # Added QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase
import database
import ml_model
from price_chart import PriceChart
# from vertical_double_line import VerticalDoubleLine # Removed import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

# Placeholder for VintageMap
class VintageMap(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("vintage-map-panel")
        layout = QVBoxLayout(self)
        label = QLabel("Vintage Map Placeholder")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setMinimumHeight(200) # Give it some initial height

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Dönerpricer")
        self.setMinimumSize(800, 600) # Allow resizing, but maintain minimum

        central_content_widget = QWidget() # Renamed to central_content_widget
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_content_widget)
        self.setCentralWidget(scroll_area)

        main_layout = QVBoxLayout(central_content_widget) # Layout for the scrollable content
        main_layout.setContentsMargins(10, 10, 10, 10) # Add some padding
        main_layout.setSpacing(10) # Adjust spacing

        # --- Masthead ---
        masthead = QWidget()
        masthead.setObjectName("masthead")
        masthead_layout = QVBoxLayout(masthead)
        masthead_layout.setAlignment(Qt.AlignCenter)

        subtitle_layout = QHBoxLayout()
        subtitle_layout.addWidget(QLabel("Vol. 01"))
        subtitle_layout.addStretch()
        subtitle_layout.addWidget(QLabel("Est. 2024"))
        subtitle_layout.addStretch()
        subtitle_layout.addWidget(QLabel("€ 0.50"))
        
        title = QLabel("The Dönerprice")
        title.setObjectName("masthead-title")
        title.setAlignment(Qt.AlignCenter)

        masthead_layout.addLayout(subtitle_layout)
        masthead_layout.addWidget(title)
        main_layout.addWidget(masthead)

        # Add horizontal double line under masthead
        masthead_separator = QFrame()
        masthead_separator.setFrameShape(QFrame.HLine)
        masthead_separator.setFrameShadow(QFrame.Sunken)
        masthead_separator.setLineWidth(2)
        main_layout.addWidget(masthead_separator)

        # --- Main Content (Vertical Stack) ---
        # 1. Search Bar
        search_widget = QWidget()
        search_widget.setObjectName("search-panel")
        search_layout = QVBoxLayout(search_widget)
        search_layout.setContentsMargins(10, 10, 10, 10) # Add some padding
        search_layout.setSpacing(15) # Adjust spacing to 15px
        search_title = QLabel("Search Archives")
        search_title.setObjectName("search-title")
        search_layout.addWidget(search_title)
        
        self.search_input = QComboBox()
        self.search_input.setEditable(True)
        self.search_input.setPlaceholderText("Product Name")
        self.search_input.setInsertPolicy(QComboBox.NoInsert)
        self.search_input.completer().setCompletionMode(QCompleter.PopupCompletion)
        
        item_names = database.get_all_item_names()
        self.search_input.addItems(item_names)
        self.search_input.currentTextChanged.connect(self.update_brand_input)
        
        search_layout.addWidget(self.search_input)
        
        self.brand_input = QComboBox()
        self.brand_input.setEditable(True)
        self.brand_input.setPlaceholderText("Brand (Optional)")
        self.brand_input.setInsertPolicy(QComboBox.NoInsert)
        self.brand_input.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.brand_input.setVisible(True) # Ensure it's initially visible
        
        search_layout.addWidget(self.brand_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_item)
        self.search_input.activated.connect(self.search_item) 
        search_layout.addWidget(self.search_button)
        main_layout.addWidget(search_widget, 1) # Give some stretch

        # 2. Recommendation Panel
        recommendation_widget = QWidget()
        recommendation_widget.setObjectName("recommendation-panel")
        recommendation_layout = QHBoxLayout(recommendation_widget) # Changed to QHBoxLayout

        # Left side: Recommendation Header
        header_container = QVBoxLayout()
        self.recommendation_header = QLabel("Prediction:")
        self.recommendation_header.setObjectName("recommendation-header")
        header_container.addWidget(self.recommendation_header, alignment=Qt.AlignCenter) # Vertically center
        recommendation_layout.addLayout(header_container, 3) # Set stretch factor to 3

        # Add a vertical double line separator (using QFrame)
        separator = QFrame()
        separator.setObjectName("recommendation-separator")
        separator.setFrameShape(QFrame.VLine)
        separator.setFixedWidth(4) # Set fixed width for the QFrame
        recommendation_layout.addWidget(separator)

        # Right side: Recommendation Label
        details_container = QVBoxLayout()
        self.recommendation_label = QLabel("Best day to buy: -\nBest Price: -\nConfidence: -")
        self.recommendation_label.setObjectName("recommendation-label")
        self.recommendation_label.setWordWrap(True)
        details_container.addWidget(self.recommendation_label, alignment=Qt.AlignCenter) # Vertically center
        recommendation_layout.addLayout(details_container, 7) # Set stretch factor to 7
        
        main_layout.addWidget(recommendation_widget, 1) # Give some stretch

        # 3. Historical Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["DATE", "PRICE", "avgPrice/g or /ml", "SUPERMARKET", "LOCATION"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.history_table.setMinimumHeight(200) # Set a minimum height
        main_layout.addWidget(self.history_table, 2) # Give more stretch

        # 4. Historical Chart
        self.price_chart = PriceChart()
        self.price_chart.setObjectName("chart-panel")
        self.price_chart.setMinimumHeight(200) # Set a minimum height
        main_layout.addWidget(self.price_chart, 2) # Give more stretch

        # 5. Vintage Map (Placeholder)
        vintage_map_widget = VintageMap()
        main_layout.addWidget(vintage_map_widget, 1) # Give some stretch

        self.current_sort_column = -1
        self.sort_order = Qt.AscendingOrder

    def search_item(self):
        item_name = self.search_input.currentText() # Get text from QComboBox
        brand_name = self.brand_input.currentText()
        if item_name:
            df = database.get_prices_by_item_and_brand(item_name, brand_name if brand_name and self.brand_input.isVisible() else None)
            self.current_df = df # Store DataFrame for sorting
            self.populate_table(df)
            ml_result = ml_model.get_recommendation(df) # Get dict result
            self.recommendation_header.setText(ml_result["recommendation_header"])
            self.recommendation_label.setText(ml_result["recommendation"])
            self.price_chart.plot(df)

    def populate_table(self, df):
        self.history_table.setRowCount(len(df))
        for i, row in df.iterrows():
            self.history_table.setItem(i, 0, QTableWidgetItem(row["date"]))
            self.history_table.setItem(i, 1, QTableWidgetItem(str(row["price"])))
            
            # Calculate avgPrice/g or /ml
            avg_price = ""
            if row["weight_grams"] and row["weight_grams"] > 0:
                avg_price = f"{row['price'] / row['weight_grams']:.4f} €/g"
            
            self.history_table.setItem(i, 2, QTableWidgetItem(avg_price))
            self.history_table.setItem(i, 3, QTableWidgetItem(row["supermarket"]))
            self.history_table.setItem(i, 4, QTableWidgetItem(row["location"]))
        # self.history_table.resizeColumnsToContents() # No longer needed

    def sort_table(self, column_index):
        if self.current_sort_column == column_index:
            self.sort_order = Qt.DescendingOrder if self.sort_order == Qt.AscendingOrder else Qt.AscendingOrder
        else:
            self.sort_order = Qt.AscendingOrder
        self.current_sort_column = column_index
        self.history_table.sortItems(column_index, self.sort_order)

    def update_brand_input(self, text):
        brands = database.get_brands_for_item(text)
        if brands:
            self.brand_input.clear()
            self.brand_input.addItems(brands)
            self.brand_input.setVisible(True)
        else:
            self.brand_input.clear()
            # self.brand_input.setVisible(False) # Removed to keep it always visible
            self.brand_input.setVisible(True) # Ensure it's visible even if no brands


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load custom fonts
    font_dir = os.path.join(os.path.dirname(__file__), "fonts")
    QFontDatabase.addApplicationFont(os.path.join(font_dir, "Tangerine-Bold.ttf"))
    QFontDatabase.addApplicationFont(os.path.join(font_dir, "Tangerine-Regular.ttf"))

    # Load and apply stylesheet
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())