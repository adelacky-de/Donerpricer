import os
import sys
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QCompleter, QHeaderView, QScrollArea, QFrame)
from PySide6.QtGui import QFont, QFontDatabase, Qt
import database
import ml_model
from price_chart import PriceChart
from map import VintageMap # Added this line
import matplotlib.font_manager as fm
# from vertical_double_line import VerticalDoubleLine # Removed import

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
        main_layout.setSpacing(5) # Adjust spacing

        # --- Masthead ---
        masthead = QWidget()
        masthead.setObjectName("masthead")
        masthead_layout = QVBoxLayout(masthead)

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
        
        # Separator line
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.HLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        separator_line.setLineWidth(2)
        masthead_layout.addWidget(separator_line)
        
        title = QLabel("The Dönerprice")
        title.setObjectName("masthead-title")
        title.setAlignment(Qt.AlignCenter)
        masthead_layout.addWidget(title)

        # Sub Header Bar (bottom bar with double line)
        sub_header = QWidget()
        sub_header.setObjectName("sub-header-bar")
        sub_layout = QHBoxLayout(sub_header)
        sub_layout.setContentsMargins(10, 10, 10, 10)
        sub_layout.addWidget(QLabel("Grocery Intelligence"))
        sub_layout.addStretch()
        date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        sub_layout.addWidget(date_label)
        sub_layout.addStretch()
        berlin_label = QLabel("Muenster Edition")
        sub_layout.addWidget(berlin_label)
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
        search_panel = QWidget()
        search_panel.setObjectName("search-panel")
        search_panel_layout = QVBoxLayout(search_panel)
        search_panel_layout.setContentsMargins(15, 15, 15, 15)
        
        search_inner = QWidget()
        search_inner.setObjectName("search-panel-inner")
        search_inner_layout = QVBoxLayout(search_inner)
        search_inner_layout.setContentsMargins(15, 15, 15, 15)
        search_inner_layout.setSpacing(5)
        
        search_title_container = QWidget()
        search_title_layout = QVBoxLayout(search_title_container)
        search_title_layout.setContentsMargins(0, 0, 0, 0)
        
        search_title = QLabel("Search Archives")
        search_title.setProperty("class", "panel-title")
        search_title_layout.addWidget(search_title)
        search_inner_layout.addWidget(search_title_container)
        
        self.search_input = QComboBox()
        self.search_input.setEditable(True)
        self.search_input.setPlaceholderText("Product Name")
        self.search_input.setInsertPolicy(QComboBox.NoInsert)
        self.search_input.completer().setCompletionMode(QCompleter.PopupCompletion)
        
        item_names = database.get_all_item_names()
        self.search_input.addItems(item_names)
        self.search_input.currentTextChanged.connect(self.update_supermarket_input)
        
        search_inner_layout.addWidget(self.search_input, 0, Qt.AlignCenter)
        
        self.supermarket_input = QComboBox()
        self.supermarket_input.setEditable(True)
        self.supermarket_input.setPlaceholderText("Supermarket (Optional)")
        self.supermarket_input.setInsertPolicy(QComboBox.NoInsert)
        self.supermarket_input.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.supermarket_input.setVisible(True)
        
        search_inner_layout.addWidget(self.supermarket_input, 0, Qt.AlignCenter)

        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("search-button")
        self.search_button.clicked.connect(self.search_item)
        search_inner_layout.addWidget(self.search_button, 0, Qt.AlignCenter)
        
        search_panel_layout.addWidget(search_inner)
        main_layout.addWidget(search_panel, 0)

        # 2. Recommendation Panel
        recommendation_panel = QWidget()
        recommendation_panel.setObjectName("recommendation-panel")
        recommendation_panel_layout = QVBoxLayout(recommendation_panel)
        recommendation_panel_layout.setContentsMargins(15, 15, 15, 15)
        
        recommendation_inner = QWidget()
        recommendation_inner.setObjectName("recommendation-panel-inner")
        recommendation_inner_layout = QVBoxLayout(recommendation_inner)
        recommendation_inner_layout.setContentsMargins(5, 5, 5, 5)
        recommendation_inner_layout.setSpacing(2)

        verdict_badge_container = QHBoxLayout()
        self.verdict_badge = QLabel("Prediction")
        self.verdict_badge.setObjectName("verdict-badge")
        verdict_badge_container.addWidget(self.verdict_badge, 0, Qt.AlignCenter)
        recommendation_inner_layout.addLayout(verdict_badge_container)

        self.recommendation_header = QLabel("Awaiting Query")
        self.recommendation_header.setObjectName("recommendation-header")
        self.recommendation_header.setAlignment(Qt.AlignCenter)
        self.recommendation_header.setWordWrap(True)
        recommendation_inner_layout.addWidget(self.recommendation_header)

        # Stats Grid
        stats_widget = QWidget()
        stats_layout = QGridLayout(stats_widget)
        stats_layout.setContentsMargins(0, 5, 0, 5)

        price_label = QLabel("Forecasted Price")
        price_label.setProperty("class", "stat-label")
        self.price_value = QLabel("€ -")
        self.price_value.setProperty("class", "stat-value")
        self.price_value.setProperty("class", "prediction-value")

        day_label = QLabel("Target Day")
        day_label.setProperty("class", "stat-label")
        self.day_value = QLabel("-")
        self.day_value.setProperty("class", "stat-value")
        self.day_value.setProperty("class", "prediction-value")

        stats_layout.addWidget(price_label, 0, 0, Qt.AlignCenter)
        stats_layout.addWidget(self.price_value, 1, 0, Qt.AlignCenter)
        stats_layout.addWidget(day_label, 0, 1, Qt.AlignCenter)
        stats_layout.addWidget(self.day_value, 1, 1, Qt.AlignCenter)
        recommendation_inner_layout.addWidget(stats_widget)

        self.confidence_label = QLabel("Confidence Index: -")
        self.confidence_label.setProperty("class", "stat-label")
        self.confidence_label.setAlignment(Qt.AlignRight)
        recommendation_inner_layout.addWidget(self.confidence_label)

        recommendation_panel_layout.addWidget(recommendation_inner)
        main_layout.addWidget(recommendation_panel, 0)

        table_panel = QWidget()
        table_panel.setObjectName("table-panel")
        table_panel_layout = QVBoxLayout(table_panel)
        table_panel_layout.setContentsMargins(15, 15, 15, 15)
        
        table_inner = QWidget()
        table_inner.setObjectName("table-panel-inner")
        table_inner_layout = QVBoxLayout(table_inner)
        
        table_header_layout = QHBoxLayout()
        table_title = QLabel("Recent Transactions")
        table_title.setProperty("class", "panel-title")
        self.record_count_label = QLabel("REC: 0")
        self.record_count_label.setProperty("class", "panel-subtitle")
        self.record_count_label.setProperty("class", "panel-record-count") # Added this line
        table_header_layout.addWidget(table_title)
        table_header_layout.addStretch()
        table_header_layout.addWidget(self.record_count_label)
        table_inner_layout.addLayout(table_header_layout)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["DATE", "PRICE", "avgPrice/g or /ml", "SUPERMARKET", "LOCATION"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().sectionClicked.connect(self.sort_table)
        table_inner_layout.addWidget(self.history_table)
        
        table_panel_layout.addWidget(table_inner)
        main_layout.addWidget(table_panel, 0) # Fit to content

        # 4. Historical Chart
        chart_panel = QWidget()
        chart_panel.setObjectName("chart-panel")
        chart_panel_layout = QVBoxLayout(chart_panel)
        chart_panel_layout.setContentsMargins(15, 15, 15, 15)
        
        chart_inner = QWidget()
        chart_inner.setObjectName("chart-panel-inner")
        chart_inner_layout = QVBoxLayout(chart_inner)
        chart_inner_layout.setSpacing(2)
        
        chart_title_container = QWidget()
        chart_title_layout = QVBoxLayout(chart_title_container)
        chart_title_layout.setContentsMargins(0, 0, 0, 0)

        chart_title = QLabel("Market Fluctuations")
        chart_title.setProperty("class", "panel-title")
        chart_title.setAlignment(Qt.AlignCenter)
        chart_title_layout.addWidget(chart_title)
        chart_inner_layout.addWidget(chart_title_container)
        
        chart_subtitle = QLabel("Price History Analysis")
        chart_subtitle.setProperty("class", "panel-subtitle")
        chart_subtitle.setAlignment(Qt.AlignCenter)
        chart_inner_layout.addWidget(chart_subtitle)

        self.price_chart = PriceChart()
        chart_inner_layout.addWidget(self.price_chart)
        
        chart_panel_layout.addWidget(chart_inner)
        main_layout.addWidget(chart_panel, 2)

        # 5. Vintage Map
        map_panel = QWidget()
        map_panel.setObjectName("map-panel")
        map_panel_layout = QVBoxLayout(map_panel)
        map_panel_layout.setContentsMargins(15, 15, 15, 15)
        
        map_inner = QWidget()
        map_inner.setObjectName("map-panel-inner")
        map_inner_layout = QVBoxLayout(map_inner)
        
        map_title = QLabel("Geographic Distribution")
        map_title.setProperty("class", "panel-title")
        map_title.setAlignment(Qt.AlignCenter)
        map_inner_layout.addWidget(map_title)
        
        map_subtitle = QLabel("Supermarket Locations")
        map_subtitle.setProperty("class", "panel-subtitle")
        map_subtitle.setAlignment(Qt.AlignCenter)
        map_inner_layout.addWidget(map_subtitle)

        self.vintage_map = VintageMap()
        map_inner_layout.addWidget(self.vintage_map)
        
        map_panel_layout.addWidget(map_inner)
        main_layout.addWidget(map_panel, 1)

        main_layout.addStretch()

        self.current_sort_column = -1
        self.sort_order = Qt.AscendingOrder

    def search_item(self):
        item_name = self.search_input.currentText() # Get text from QComboBox
        supermarket_name = self.supermarket_input.currentText()
        print(f"Searching for: {item_name}, Supermarket: {supermarket_name}")
        if item_name:
            df = database.get_prices_by_item_and_supermarket(item_name, supermarket_name if supermarket_name and self.supermarket_input.isVisible() else None)
            print(f"Found {len(df)} records")
            self.current_df = df # Store DataFrame for sorting
            self.populate_table(df)
            ml_result = ml_model.get_recommendation(df) # Get dict result
            
            # Update Recommendation Panel
            # Parse the recommendation string from ml_model.py
            lines = ml_result["recommendation"].split("\n")
            if len(lines) >= 3 and ": " in lines[0]:
                best_day = lines[0].split(": ")[1]
                best_price = lines[1].split(": ")[1]
                confidence = float(lines[2].split(": ")[1].replace('%', ''))
            else:
                best_day = "-"
                best_price = "- (Not enough data)"
                confidence = 0.0
            
            # Only "BUY IT NOW!" if the best day is today
            today_name = datetime.now().strftime("%A")
            
            if confidence < 70.0:
                self.recommendation_header.setText("Confidence too low for a reliable recommendation.")
                self.day_value.setText("-")
                self.price_value.setText("€ -")
                self.confidence_label.setText(f"Confidence Index: {confidence:.2f}%")
            else:
                if best_day == today_name:
                    self.recommendation_header.setText("BUY IT NOW!")
                else:
                    self.recommendation_header.setText("HOLD YOUR WALLET!")
                    
                self.day_value.setText(best_day)
                self.price_value.setText(best_price)
                self.confidence_label.setText(f"Confidence Index: {confidence:.2f}%")
            
            self.price_chart.plot(df)
            self.vintage_map.update_map(df)
            self.record_count_label.setText(f"REC: {len(df)}")

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

    def update_supermarket_input(self, text):
        supermarkets = database.get_supermarkets_for_item(text)
        if supermarkets:
            self.supermarket_input.clear()
            self.supermarket_input.addItems(supermarkets)
            self.supermarket_input.setVisible(True)
        else:
            self.supermarket_input.clear()
            # self.supermarket_input.setVisible(False) # Removed to keep it always visible
            self.supermarket_input.setVisible(True) # Ensure it's visible even if no supermarkets


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load custom fonts
    font_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "fonts"))
    for f in os.listdir(font_dir):
        if f.endswith('.ttf'):
            font_path = os.path.join(font_dir, f)
            # Register with Qt
            QFontDatabase.addApplicationFont(font_path)
            # Register with Matplotlib
            try:
                fm.fontManager.addfont(font_path)
            except Exception as e:
                print(f"Could not register font {f} with Matplotlib: {e}")

    # Load and apply stylesheet
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())