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
                data_index = ind['ind'][0]
                
                date = self.df['date'].iloc[data_index]
                price = self.df['price'].iloc[data_index]
                supermarket = self.df['supermarket'].iloc[data_index]

                # Determine annotation position dynamically
                xdata = mdates.date2num(date)
                ydata = price
                
                # Default text offset and alignment
                x_offset, y_offset = 10, 10 # Reduced initial offset
                ha = 'left'
                va = 'bottom'

                text = f"Price: {price:.2f}€\nSupermarket: {supermarket}"

                if self.annot is None:
                    self.annot = self.ax.annotate(text, xy=(xdata, ydata), xytext=(x_offset, y_offset),
                                                textcoords="offset points",
                                                bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="k", lw=1, alpha=0.7), # Changed alpha
                                                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"),
                                                ha=ha, va=va, fontsize=8, color='#1a1a1a') # Added fontsize and color
                else:
                    self.annot.xy = (xdata, ydata)
                    self.annot.set_text(text)
                    self.annot.set_bbox(dict(boxstyle="round,pad=0.5", fc="white", ec="k", lw=1, alpha=0.7)) # Changed alpha
                    self.annot.set_fontsize(8) # Set fontsize
                    self.annot.set_color('#1a1a1a') # Set color

                # Get the renderer to calculate text extent
                renderer = self.canvas.get_renderer()
                self.annot.set_visible(True) # Temporarily make visible to get extent
                self.canvas.draw() # Draw to update extent
                bbox_ann = self.annot.get_window_extent(renderer)
                bbox_ax = self.ax.bbox

                # Check for overlap and adjust position
                # 10% overlap threshold
                overlap_threshold_x = bbox_ann.width * 0.1
                overlap_threshold_y = bbox_ann.height * 0.1

                # Check right boundary
                if bbox_ann.x1 > bbox_ax.x1 - overlap_threshold_x:
                    ha = 'right'
                    x_offset = -10 # Adjust offset for right alignment
                # Check left boundary
                elif bbox_ann.x0 < bbox_ax.x0 + overlap_threshold_x:
                    ha = 'left'
                    x_offset = 10 # Adjust offset for left alignment
                else:
                    ha = 'left'
                    x_offset = 10

                # Check top boundary
                if bbox_ann.y1 > bbox_ax.y1 - overlap_threshold_y:
                    va = 'top'
                    y_offset = -10 # Adjust offset for top alignment
                # Check bottom boundary
                elif bbox_ann.y0 < bbox_ax.y0 + overlap_threshold_y:
                    va = 'bottom'
                    y_offset = 10 # Adjust offset for bottom alignment
                else:
                    va = 'bottom'
                    y_offset = 10

                self.annot.set_position((x_offset, y_offset))
                self.annot.set_ha(ha)
                self.annot.set_va(va)
                
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
