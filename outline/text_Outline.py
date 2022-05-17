import sys, math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pydm import Display
from PyQt5 import QtGui

sys.path.insert(0, '../cavityDisplay/frontend')
from cavityWidget import CavityWidget

print("beginning")


class OutlinedLabel(CavityWidget):

    def __init__(self, *args, **kwargs):
        super(OutlinedLabel, self).__init__(*args, **kwargs)
        self.w = 1 / 25
        self.mode = True        # True for outline
        self.setBrush(Qt.white)
        self.setPen(Qt.black)
        print("OutlinedLabel: ", self.cavityText)


    def scaledOutlineMode(self):
        return self.mode

    def setScaledOutlineMode(self, state):
        self.mode = state

    def outlineThickness(self):
        return self.w * self.font().pointSize() if self.mode else self.w

    def setOutlineThickness(self, value):
        self.w = value

    def setBrush(self, brush):
        if not isinstance(brush, QBrush):
            brush = QBrush(brush)
        self.brush = brush

    def setPen(self, pen):
        if not isinstance(pen, QPen):
            pen = QPen(pen)
        pen.setJoinStyle(Qt.RoundJoin)
        self.pen = pen

    def sizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super(OutlinedLabel, self).sizeHint() + QSize(w, w)

    def minimumSizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super(OutlinedLabel, self).minimumSizeHint() + QSize(w, w)

    def paintEvent(self, event):
        w = self.outlineThickness()
        rect = self.rect()
        metrics = QFontMetrics(self.font())

        tr = metrics.boundingRect(self.cavityText).adjusted(0, 0, w, w)
        '''
        if self.indent() == -1:
            if self.frameWidth():
                indent = (metrics.boundingRect('x').width() + w * 2) / 2
            else:
                indent = w
        else:
            indent = self.indent()
            '''

        x = (rect.width() - tr.width()) / 2
        y = (rect.height() + metrics.ascent() - metrics.descent()) / 2

        '''
        if self.alignment() & Qt.AlignLeft:
            x = rect.left() + indent - min(metrics.leftBearing(self.cavityText()[0]), 0)
        elif self.alignment() & Qt.AlignRight:
            x = rect.x() + rect.width() - indent - tr.width()
        else:
            x = (rect.width() - tr.width()) / 2
            '''

        '''
        if self.alignment() & Qt.AlignTop:
            y = rect.top() + indent + metrics.ascent()
        elif self.alignment() & Qt.AlignBottom:
            y = rect.y() + rect.height() - indent - metrics.descent()
        else:
            y = (rect.height() + metrics.ascent() - metrics.descent()) / 2
        '''

        path = QPainterPath()
        path.addText(x, y, self.font(), self.cavityText)
        print(self.cavityText)
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        self.pen.setWidthF(w * 2)
        qp.strokePath(path, self.pen)
        if 1 < self.brush.style() < 15:
            qp.fillPath(path, self.palette().window())
        qp.fillPath(path, self.brush)


class Example(Display):
    def __init__(self, parent=None, args=None):
        super().__init__(parent=parent, args=args, ui_filename="word.ui")

        cavity = self.ui.cavityWidget
        print("Example class:", cavity.cavityText)

        #outlinedWord = OutlinedLabel(cavity)
        #outlinedWord.setStyleSheet("background-color: rgb(255,255,10)")
        #outlinedWord.adjustSize()

        default = OutlinedLabel()
        default.adjustSize()

        vbox = self.ui.verticalLayout
        vbox.addWidget(default)


        '''
        letters = OutlinedLabel('test')
        letters.setStyleSheet('font-family: Helvetica; font-size: 30pt; font-weight: bold')
        letters.adjustSize()

        vbox = self.ui.verticalLayout
        vbox.addWidget(letters)
        '''
