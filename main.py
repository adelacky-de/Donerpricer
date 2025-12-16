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
    QHeaderView, # Added QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
import database
import ml_model
from price_chart import PriceChart

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Dönerpricer")
        self.setFixedSize(800, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

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

        # --- Main Content ---
        content_widget = QWidget()
        grid_layout = QGridLayout(content_widget)
        main_layout.addWidget(content_widget)

        # Left-top: Search Bar
        search_widget = QWidget()
        search_widget.setObjectName("search-panel")
        search_layout = QVBoxLayout(search_widget)
        search_layout.setContentsMargins(10, 10, 10, 10) # Add some padding
        search_layout.setSpacing(10) # Adjust spacing
        search_title = QLabel("Search Archives")
        search_title.setObjectName("search-title")
        search_layout.addWidget(search_title)
        
        self.search_input = QComboBox() # Changed to QComboBox
        self.search_input.setEditable(True)
        self.search_input.setPlaceholderText("Product Name")
        self.search_input.setInsertPolicy(QComboBox.NoInsert)
        self.search_input.completer().setCompletionMode(QCompleter.PopupCompletion)
        
        # Populate with item names
        item_names = database.get_all_item_names()
        self.search_input.addItems(item_names)
        
        self.search_input.currentTextChanged.connect(self.update_brand_input) # Connect signal
        
        search_layout.addWidget(self.search_input)
        
        self.brand_input = QComboBox() # Changed to QComboBox
        self.brand_input.setEditable(True)
        self.brand_input.setPlaceholderText("Brand (Optional)")
        self.brand_input.setInsertPolicy(QComboBox.NoInsert)
        self.brand_input.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.brand_input.setVisible(False) # Initially hidden
        
        search_layout.addWidget(self.brand_input)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_item)
        # Connect QComboBox signal as well
        self.search_input.activated.connect(self.search_item) 
        search_layout.addWidget(self.search_button)
        grid_layout.addWidget(search_widget, 0, 0)

        # Left-bottom: Recommendation Panel
        recommendation_widget = QWidget()
        recommendation_widget.setObjectName("recommendation-panel")
        recommendation_layout = QVBoxLayout(recommendation_widget)
        self.recommendation_label = QLabel("Recommendation will be shown here.")
        self.recommendation_label.setWordWrap(True)
        recommendation_layout.addWidget(self.recommendation_label)
        self.confidence_label = QLabel("Confidence: N/A") # New confidence label
        recommendation_layout.addWidget(self.confidence_label)
        grid_layout.addWidget(recommendation_widget, 1, 0)

        # Right Panel
        right_panel = QWidget()
        right_panel_layout = QVBoxLayout(right_panel)
        grid_layout.addWidget(right_panel, 0, 1, 2, 1)

        # Right-top: Historical Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["DATE", "PRICE", "avgPrice/g or /ml", "SUPERMARKET", "LOCATION"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) # Resize columns to contents
        self.history_table.horizontalHeader().setStretchLastSection(True) # Stretch last section
        self.history_table.horizontalHeader().sectionClicked.connect(self.sort_table) # Connect sorting
        right_panel_layout.addWidget(self.history_table, 2) # Give more stretch to table

        # Right-bottom: Historical Chart
        self.price_chart = PriceChart()
        self.price_chart.setObjectName("chart-panel")
        right_panel_layout.addWidget(self.price_chart, 1) # Give less stretch to chart

        # Set column stretch
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 2)

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
            self.recommendation_label.setText(ml_result["recommendation"])
            self.confidence_label.setText(f"Confidence: {ml_result['confidence']}%") # Display confidence
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
            self.brand_input.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply stylesheet
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())