from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
from os import listdir
from os.path import isfile, join, expanduser
import logging

assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

class styleSet(QDialog):
    styleChoice = ""

    def choose(self):
        chosen = self.stylePicker.currentText()
        logging.info("we chose the following style:")
        logging.info(chosen)
        try:
            with open(os.path.join(assets, chosen), "r") as f:
                styleSet.styleChoice = f.read()
                logging.info("style set")
        except:
            styleSet.styleChoice = ""
            logging,info("Error: couldn't find a file by that name in the assets directory!")


    def __init__(self, *args, **kwargs):
        super(styleSet, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setGeometry(QRect(200,200,400,200))
        self.setLayout(layout)
        self.isModal()
        availableStyles = list()

        with open(os.path.join(assets,"OWthemes.txt"), 'r') as f:
            availableStylesRaw = f.read()
            logging.info(availableStylesRaw)

        availableStyles = availableStylesRaw.split()

        logging.info(availableStyles)

        self.stylePicker = QComboBox(self)

        x = 0
        for i in availableStyles:
            self.stylePicker.addItem(i, 0)
            x = x + 1

        button = QPushButton("confirm theme selection")
        cancel = QPushButton("cancel")
        layout.addWidget(self.stylePicker)
        layout.addWidget(button)
        layout.addWidget(cancel)

        button.clicked.connect(self.choose)
        button.clicked.connect(self.accept)
        cancel.clicked.connect(self.accept)
        self.exec()
