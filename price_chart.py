from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt # Import pyplot for event handling

# Chart Styling Configuration - Centralized styling (Vintage Newspaper Theme)
CHART_STYLE = {
    # Colors (matching vintage newspaper aesthetic from style.qss)
    'background_color': '#fdfbf7',  # Paper color
    'ink_color': '#1a1a1a',          # Ink color
    'grey_color': '#666666',          # Muted grey for placeholders
    
    # Line and marker styling
    'line_width': 2,
    'line_color': '#1a1a1a',
    'marker_style': 'o',
    'marker_size': 4,
    'marker_face_color': 'white',
    'marker_edge_color': '#1a1a1a',
    
    # Grid styling
    'grid_linestyle': '--',
    'grid_alpha': 0.3,
    'grid_color': '#1a1a1a',
    
    # Fonts
    'font_family': 'Noto Serif',
    'tick_font_size': 8,
    'annotation_font_size': 8,
    
    # Axis styling
    'y_tick_interval': 0.2,
    
    # Annotation styling
    'annotation_box_style': 'round,pad=0.5',
    'annotation_bg_color': 'white',
    'annotation_edge_color': 'k',
    'annotation_line_width': 1,
    'annotation_alpha': 0.7,
    'annotation_offset': 10,
}

class PriceChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Use the paper color for the figure background
        self.figure = Figure(dpi=100, facecolor=CHART_STYLE['background_color'])
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
        self.figure.clear() # Clear the figure
        self.annot = None  # Reset annotation when clearing to avoid orphaned axes reference
        self.ax = self.figure.add_subplot(111) # Re-assign ax after clearing the figure
        # Set facecolor again after clear
        self.figure.set_facecolor(CHART_STYLE['background_color'])
        self.ax.set_facecolor(CHART_STYLE['background_color'])
        
        # Remove top and right spines for a cleaner look
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_color(CHART_STYLE['ink_color'])
        self.ax.spines['bottom'].set_color(CHART_STYLE['ink_color'])

        if not self.df.empty:
            print("Plotting data...")
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df = self.df.sort_values(by='date')
            
            # Use 'step' plot with 'post' (equivalent to stepAfter)
            # Use ink-black for the line
            self.line, = self.ax.step(self.df['date'], self.df['price'], where='post', 
                                     color=CHART_STYLE['line_color'], 
                                     linewidth=CHART_STYLE['line_width'], 
                                     marker=CHART_STYLE['marker_style'], 
                                     markersize=CHART_STYLE['marker_size'], 
                                     markerfacecolor=CHART_STYLE['marker_face_color'], 
                                     markeredgecolor=CHART_STYLE['marker_edge_color'])
            
            # Set x-axis tick labels
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            self.ax.tick_params(axis='x', labelsize=CHART_STYLE['tick_font_size'], 
                              colors=CHART_STYLE['ink_color'], 
                              labelfontfamily=CHART_STYLE['font_family'])
            self.ax.tick_params(axis='y', labelsize=CHART_STYLE['tick_font_size'], 
                              colors=CHART_STYLE['ink_color'], 
                              labelfontfamily=CHART_STYLE['font_family'])
            
            # Set y-axis interval
            self.ax.yaxis.set_major_locator(mticker.MultipleLocator(CHART_STYLE['y_tick_interval']))
            
            # Add grid lines (horizontal only, dashed)
            self.ax.yaxis.grid(True, linestyle=CHART_STYLE['grid_linestyle'], 
                             alpha=CHART_STYLE['grid_alpha'], 
                             color=CHART_STYLE['grid_color'])
            self.ax.xaxis.grid(False)

            self.figure.tight_layout()

        else:
            self.ax.text(0.5, 0.5, "Awaiting data points...",
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=self.ax.transAxes,
                    fontfamily='serif',
                    fontstyle='italic',
                    color=CHART_STYLE['grey_color'])
            
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
                x_offset, y_offset = CHART_STYLE['annotation_offset'], CHART_STYLE['annotation_offset']
                ha = 'left'
                va = 'bottom'

                text = f"Price: {price:.2f}€\nSupermarket: {supermarket}"

                if self.annot is None:
                    self.annot = self.ax.annotate(text, xy=(xdata, ydata), xytext=(x_offset, y_offset),
                                                textcoords="offset points",
                                                bbox=dict(boxstyle=CHART_STYLE['annotation_box_style'], 
                                                         fc=CHART_STYLE['annotation_bg_color'], 
                                                         ec=CHART_STYLE['annotation_edge_color'], 
                                                         lw=CHART_STYLE['annotation_line_width'], 
                                                         alpha=CHART_STYLE['annotation_alpha']),
                                                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"),
                                                ha=ha, va=va, 
                                                fontsize=CHART_STYLE['annotation_font_size'], 
                                                color=CHART_STYLE['ink_color'])
                else:
                    self.annot.xy = (xdata, ydata)
                    self.annot.set_text(text)
                    self.annot.set_bbox(dict(boxstyle=CHART_STYLE['annotation_box_style'], 
                                            fc=CHART_STYLE['annotation_bg_color'], 
                                            ec=CHART_STYLE['annotation_edge_color'], 
                                            lw=CHART_STYLE['annotation_line_width'], 
                                            alpha=CHART_STYLE['annotation_alpha']))
                    self.annot.set_fontsize(CHART_STYLE['annotation_font_size'])
                    self.annot.set_color(CHART_STYLE['ink_color'])

                # Get the renderer to calculate text extent
                renderer = self.canvas.get_renderer()
                self.annot.set_visible(True) # Temporarily make visible to get extent
                self.canvas.draw() # Draw to update extent
                
                # Safety check: ensure annotation has valid axes before getting extent
                if self.annot.axes is not None:
                    bbox_ann = self.annot.get_window_extent(renderer)
                    bbox_ax = self.ax.bbox

                # Safety check: ensure annotation has valid axes before getting extent
                if self.annot.axes is not None:
                    bbox_ann = self.annot.get_window_extent(renderer)
                    bbox_ax = self.ax.bbox

                    # Check for overlap and adjust position
                    # 10% overlap threshold
                    overlap_threshold_x = bbox_ann.width * 0.1
                    overlap_threshold_y = bbox_ann.height * 0.1

                    # Check right boundary
                    if bbox_ann.x1 > bbox_ax.x1 - overlap_threshold_x:
                        ha = 'right'
                        x_offset = -CHART_STYLE['annotation_offset']
                    # Check left boundary
                    elif bbox_ann.x0 < bbox_ax.x0 + overlap_threshold_x:
                        ha = 'left'
                        x_offset = CHART_STYLE['annotation_offset']
                    else:
                        ha = 'left'
                        x_offset = CHART_STYLE['annotation_offset']

                    # Check top boundary
                    if bbox_ann.y1 > bbox_ax.y1 - overlap_threshold_y:
                        va = 'top'
                        y_offset = -CHART_STYLE['annotation_offset']
                    # Check bottom boundary
                    elif bbox_ann.y0 < bbox_ax.y0 + overlap_threshold_y:
                        va = 'bottom'
                        y_offset = CHART_STYLE['annotation_offset']
                    else:
                        va = 'bottom'
                        y_offset = CHART_STYLE['annotation_offset']

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
