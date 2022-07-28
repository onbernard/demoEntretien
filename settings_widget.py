import os 

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QPushButton, QGridLayout, QWidget, QSlider
from PySide2.QtGui import QIcon

from config import *

def makeSliderLabelPair(name, min, max):
    """
    Widget Factory
    """
    slider = QSlider(orientation=Qt.Orientation.Horizontal)
    slider.setTickPosition(QSlider.TicksBelow)
    slider.setTickInterval(10)
    slider.setMinimum(0)
    slider.setMaximum(100)
    slider.setValue(0)
    label = QLabel(name + " = " + str(min))
    def changedValue():
        t = slider.value()/100
        label.setText(name + " = " + str(min*(1-t) + max*t))
    slider.valueChanged.connect(changedValue)
    return({'slider':slider, 'label':label, 'min':min, 'max':max, 'name':name})


class SimSettings(QWidget):
    """
    Simulation settings window
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulation Settings")
        self.setWindowIcon(QIcon(os.path.join(IMG_DIRPATH, "equalizer.png")))
        self.setMinimumSize(600,300)
        layout = QGridLayout()
        self.rules = []
        rule1 = makeSliderLabelPair("COHESION COEF", 0, 1)
        rule2 = makeSliderLabelPair("SEPARATION COEF", 0, 1)
        rule3 = makeSliderLabelPair("ALIGNMENT COEF", 0, 1)
        self.rules.append(rule1)
        self.rules.append(rule2)
        self.rules.append(rule3)
        layout.addWidget(rule1['slider'], 0, 0)
        layout.addWidget(rule1['label'], 0, 1)
        layout.addWidget(rule2['slider'], 1, 0)
        layout.addWidget(rule2['label'], 1, 1)
        layout.addWidget(rule3['slider'], 2, 0)
        layout.addWidget(rule3['label'], 2, 1)
        self.resetHasBeenClicked = False
        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetClicked)
        layout.addWidget(self.resetButton, 3,0)
        self.setLayout(layout)
        self.resetSliders()
    
    def getSettingValue(self, index):
        t = self.rules[index]['slider'].value() / 100
        min = self.rules[index]['min']
        max = self.rules[index]['max']
        return min*(1-t) + max*t
    
    def resetClicked(self):
        self.resetSliders()
        self.resetHasBeenClicked = True
    
    def resetSliders(self):
        for r in self.rules:
            if(r['name']=="SEPARATION COEF"):
                r['slider'].setValue(5)
            elif(r['name']=="COHESION COEF"):
                r['slider'].setValue(10)
            else:
                r['slider'].setValue(80)