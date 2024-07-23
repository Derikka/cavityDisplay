import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout
from pydm import Display
from typing import List

print("Start of bar_chart_display.py-----------------------------------------")


class BarChart(Display):
    def __init__(self, x_vals: List[str], y_vals: List[int], parent=None, args=None):
        super().__init__(parent, args)

        self.setWindowTitle("Bar Chart")
        vertLayout_Form = QVBoxLayout()

        # Make plot window and add it to the vert layout
        self.plot_window = pg.plot()
        vertLayout_Form.addWidget(self.plot_window)

        self.setLayout(vertLayout_Form)

        # TODO Remove these hardcoded x_vals and y_vals
        # x_vals = ['OFF', 'PZO', 'MGT']
        # y_vals = [1, 6, 2]
        x_vals_ints = []

        ticks = []
        for idx, x_val in enumerate(x_vals):
            ticks.append((idx, x_val))
            x_vals_ints.append(idx)

        # Create pyqt5graph bar graph item with green bars
        bargraph = pg.BarGraphItem(x=x_vals_ints, height=y_vals, width=0.6, brush='g')

        ax = self.plot_window.getAxis('bottom')
        ax.setTicks([ticks])
        self.plot_window.showGrid(x=False, y=True, alpha=0.6)

        # Add bargraph to plot window
        self.plot_window.addItem(bargraph)
        print("End of bar_chart_display.py----------------------------------------")
