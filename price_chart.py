from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.dates as mdates

import matplotlib.ticker as mticker

class PriceChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6), dpi=100) # Increased figsize
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot(pd.DataFrame()) # Initial empty plot

    def plot(self, df):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Price History")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (€)")

        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date')
            
            # Color-code by supermarket
            lines = []
            for supermarket, group in df.groupby('supermarket'):
                line, = ax.plot(group['date'], group['price'], marker='o', linestyle='-', label=supermarket)
                lines.append(line)
            
            # Set x-axis tick labels to show abbreviated weekday
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%a'))
            ax.tick_params(axis='x', labelsize=8)
            
            # Set y-axis interval
            ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))
            
            self.figure.tight_layout(rect=[0, 0.15, 0.85, 0.95]) # Adjusted rect for more margin
            
            # Add legend at the bottom
            self.figure.legend(lines, [l.get_label() for l in lines], loc='center left', bbox_to_anchor=(0.85, 0.5))

            # Hover functionality
            annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="w"),
                                arrowprops=dict(arrowstyle="->"))
            annot.set_visible(False)

            def update_annot(event):
                if event.inaxes == ax:
                    for line in lines:
                        cont, ind = line.contains(event)
                        if cont:
                            pos = line.get_xydata()[ind["ind"][0]]
                            annot.xy = pos
                            date_str = pd.to_datetime(pos[0], unit='D').strftime('%Y-%m-%d')
                            annot.set_text(f"Date: {date_str}\nPrice: {pos[1]:.2f} €")
                            annot.get_bbox_patch().set_alpha(0.4)
                            annot.set_visible(True)
                            self.canvas.draw_idle()
                            return
                if annot.get_visible():
                    annot.set_visible(False)
                    self.canvas.draw_idle()

            self.canvas.mpl_connect("motion_notify_event", update_annot)

        else:
            ax.text(0.5, 0.5, "No data to display",
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax.transAxes)

        self.canvas.draw()
