from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

class PriceChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Use the paper color for the figure background
        self.figure = Figure(dpi=100, facecolor='#fdfbf7')
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot(pd.DataFrame()) # Initial empty plot

    def plot(self, df):
        print(f"PriceChart.plot called with {len(df)} records")
        self.figure.clear()
        # Set facecolor again after clear
        self.figure.set_facecolor('#fdfbf7')
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#fdfbf7')
        
        # Remove top and right spines for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#1a1a1a')
        ax.spines['bottom'].set_color('#1a1a1a')

        if not df.empty:
            print("Plotting data...")
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date')
            
            # Use 'step' plot with 'post' (equivalent to stepAfter)
            # Use ink-black for the line
            ax.step(df['date'], df['price'], where='post', color='#1a1a1a', linewidth=2, marker='o', markersize=4, markerfacecolor='white', markeredgecolor='#1a1a1a')
            
            # Set x-axis tick labels
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax.tick_params(axis='x', labelsize=8, colors='#1a1a1a', family='Courier Prime')
            ax.tick_params(axis='y', labelsize=8, colors='#1a1a1a', family='Courier Prime')
            
            # Set y-axis interval
            ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
            
            # Add grid lines (horizontal only, dashed)
            ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#1a1a1a')
            ax.xaxis.grid(False)

            self.figure.tight_layout()

        else:
            ax.text(0.5, 0.5, "Awaiting data points...",
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax.transAxes,
                    fontfamily='serif',
                    fontstyle='italic',
                    color='#666666')
            
            # Hide axes for empty state
            ax.set_axis_off()

        self.canvas.draw()
