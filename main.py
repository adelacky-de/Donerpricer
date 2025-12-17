import os
import sys
from datetime import datetime
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
        masthead_layout.setContentsMargins(0, 0, 0, 0)
        masthead_layout.setSpacing(0)

        # Meta Header (top bar)
        meta_header = QWidget()
        meta_header.setObjectName("meta-header")
        meta_layout = QHBoxLayout(meta_header)
        meta_layout.setContentsMargins(0, 0, 0, 5)
        meta_layout.addWidget(QLabel("Vol. 01"))
        meta_layout.addStretch()
        meta_layout.addWidget(QLabel("Est. 2024"))
        meta_layout.addStretch()
        meta_layout.addWidget(QLabel("€ 0.50"))
        masthead_layout.addWidget(meta_header)
        
        title = QLabel("The Dönerprice")
        title.setObjectName("masthead-title")
        title.setAlignment(Qt.AlignCenter)
        masthead_layout.addWidget(title)

        # Sub Header Bar (bottom bar with double line)
        sub_header = QWidget()
        sub_header.setObjectName("sub-header-bar")
        sub_layout = QHBoxLayout(sub_header)
        sub_layout.setContentsMargins(10, 5, 10, 5)
        sub_layout.addWidget(QLabel("Grocery Intelligence"))
        sub_layout.addStretch()
        sub_layout.addWidget(QLabel(datetime.now().strftime("%A, %B %d, %Y")))
        sub_layout.addStretch()
        sub_layout.addWidget(QLabel("Berlin Edition"))
        masthead_layout.addWidget(sub_header)

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
        recommendation_layout = QVBoxLayout(recommendation_widget)
        recommendation_layout.setContentsMargins(1, 1, 1, 1)

        rec_content = QWidget()
        rec_content.setObjectName("recommendation-panel-inner")
        rec_content_layout = QVBoxLayout(rec_content)

        verdict_badge_container = QHBoxLayout()
        self.verdict_badge = QLabel("Official Verdict")
        self.verdict_badge.setObjectName("verdict-badge")
        verdict_badge_container.addWidget(self.verdict_badge, 0, Qt.AlignCenter)
        rec_content_layout.addLayout(verdict_badge_container)

        self.recommendation_header = QLabel("Awaiting Query")
        self.recommendation_header.setObjectName("recommendation-header")
        self.recommendation_header.setAlignment(Qt.AlignCenter)
        self.recommendation_header.setWordWrap(True)
        rec_content_layout.addWidget(self.recommendation_header)

        # Stats Grid
        stats_widget = QWidget()
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setContentsMargins(0, 10, 0, 10)

        price_label = QLabel("Forecasted Price")
        price_label.setProperty("class", "stat-label")
        self.price_value = QLabel("€ -")
        self.price_value.setProperty("class", "stat-value")

        day_label = QLabel("Target Day")
        day_label.setProperty("class", "stat-label")
        self.day_value = QLabel("-")
        self.day_value.setProperty("class", "stat-value")

        stats_layout.addWidget(price_label, 0, 0)
        stats_layout.addWidget(self.price_value, 1, 0)
        stats_layout.addWidget(day_label, 0, 1, Qt.AlignRight)
        stats_layout.addWidget(self.day_value, 1, 1, Qt.AlignRight)

        rec_content_layout.addWidget(stats_widget)

        self.recommendation_details = QLabel("Search an item to read the report.")
        self.recommendation_details.setObjectName("recommendation-details")
        self.recommendation_details.setWordWrap(True)
        rec_content_layout.addWidget(self.recommendation_details)

        self.confidence_label = QLabel("Confidence Index: -")
        self.confidence_label.setProperty("class", "stat-label")
        self.confidence_label.setAlignment(Qt.AlignRight)
        rec_content_layout.addWidget(self.confidence_label)

        recommendation_layout.addWidget(rec_content)
        main_layout.addWidget(recommendation_widget, 1)
        
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
            
            # Update Recommendation Panel
            # Parse the recommendation string from ml_model.py
            lines = ml_result["recommendation"].split("\n")
            best_day = lines[0].split(": ")[1] if len(lines) > 0 else "-"
            best_price = lines[1].split(": ")[1] if len(lines) > 1 else "-"
            confidence = lines[2].split(": ")[1] if len(lines) > 2 else "-"
            
            self.recommendation_header.setText("BUY IT NOW!" if "Best day to buy" in ml_result["recommendation"] else "HOLD YOUR WALLET!")
            self.day_value.setText(best_day)
            self.price_value.setText(best_price)
            self.confidence_label.setText(f"Confidence Index: {confidence}")
            self.recommendation_details.setText(f"Market analysis suggests that {best_day} is the optimal time for acquisition.")
            
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