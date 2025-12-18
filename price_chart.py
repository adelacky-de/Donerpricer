from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt # Import pyplot for event handling

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
        self.ax = self.figure.add_subplot(111) # Store ax as instance variable
        self.annot = None # Initialize annotation
        self.df = pd.DataFrame() # Store dataframe
        self.plot(pd.DataFrame()) # Initial empty plot

        # Connect hover event
        self.canvas.mpl_connect('motion_notify_event', self.on_hover)

    def plot(self, df):
        print(f"PriceChart.plot called with {len(df)} records")
        self.df = df # Store the dataframe
        self.ax.clear() # Clear the stored ax
        # Set facecolor again after clear
        self.figure.set_facecolor('#fdfbf7')
        self.ax.set_facecolor('#fdfbf7')
        
        # Remove top and right spines for a cleaner look
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color('#1a1a1a')
        self.ax.spines['bottom'].set_color('#1a1a1a')

        if not self.df.empty:
            print("Plotting data...")
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df = self.df.sort_values(by='date')
            
            # Use 'step' plot with 'post' (equivalent to stepAfter)
            # Use ink-black for the line
            self.line, = self.ax.step(self.df['date'], self.df['price'], where='post', color='#1a1a1a', linewidth=2, marker='o', markersize=4, markerfacecolor='white', markeredgecolor='#1a1a1a')
            
            # Set x-axis tick labels
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            self.ax.tick_params(axis='x', labelsize=8, colors='#1a1a1a', labelfontfamily='Noto Serif')
            self.ax.tick_params(axis='y', labelsize=8, colors='#1a1a1a', labelfontfamily='Noto Serif')
            
            # Set y-axis interval
            self.ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
            
            # Add grid lines (horizontal only, dashed)
            self.ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#1a1a1a')
            self.ax.xaxis.grid(False)

            self.figure.tight_layout()

        else:
            self.ax.text(0.5, 0.5, "Awaiting data points...",
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=self.ax.transAxes,
                    fontfamily='serif',
                    fontstyle='italic',
                    color='#666666')
            
            # Hide axes for empty state
            self.ax.set_axis_off()

        self.canvas.draw()

    def on_hover(self, event):
        if event.inaxes == self.ax and not self.df.empty:
            cont, ind = self.line.contains(event)
            if cont:
                # Get the index of the hovered point
                data_index = ind['ind'][0]
                
                # Get data for the hovered point
                date = self.df['date'].iloc[data_index]
                price = self.df['price'].iloc[data_index]
                supermarket = self.df['supermarket'].iloc[data_index]

                # Update annotation text and position
                if self.annot is None:
                    self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),
                                                textcoords="offset points",
                                                bbox=dict(boxstyle="round,pad=0.5", fc="yellow", ec="k", lw=1, alpha=0.8),
                                                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"))
                
                self.annot.xy = (mdates.date2num(date), price)
                text = f"Price: {price:.2f}€\nSupermarket: {supermarket}"
                self.annot.set_text(text)
                self.annot.set_visible(True)
                self.canvas.draw_idle()
            else:
                if self.annot is not None:
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()
        else:
            if self.annot is not None:
                self.annot.set_visible(False)
                self.canvas.draw_idle()
