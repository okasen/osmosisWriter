from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import logging

import osmosis.fileAttributes as fileAttributes

fileAtts = fileAttributes.fileAttributes()

class workArea(QMdiSubWindow):
    def __init__(self, *args, **kwargs):
        super(workArea, self).__init__(*args, **kwargs)

        self.oldPos = self.pos()
        self.pressed = False

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.pressed = True

    def mouseMoveEvent(self, event):
        if self.pressed:
            logging.info(self.pressed)
            delta = QPoint (event.globalPos() - self.oldPos)
            logging.info(delta)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.pressed = False

class workspaceTemplate(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(workspaceTemplate, self).__init__(*args, **kwargs)
        #self.workspace.selectionChanged.connect(self.update_format) #Getting the QTextEdit basics in

        self.setFontPointSize(14)
        self.setPlaceholderText("Blank pages are intimidating, so we put these words here.")


class workTab(QPushButton):

    goIta = pyqtSignal()
    goUL = pyqtSignal()
    rearranged = pyqtSignal()

    def __init__(self, label):

        super().__init__()
        self.setAcceptDrops(True)
        self.setText(label)
        self.text = label
        self.setMinimumWidth(195)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.RightButton:
            drag = QDrag(self)
            mimeData = QMimeData()
            dragPixmap = self.grab()

            drag.setMimeData(mimeData)
            mimeData.setText(str(self.text))

            drag.setPixmap(dragPixmap)
            drag.setHotSpot(e.pos())

            #self.setParent(None)
            drag.exec_(Qt.CopyAction)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        location = e.source()
        if isinstance(location, workTab):
            l = self.text #location
            p = self #place
            st = e.mimeData().text()
            localeOfSource = list(fileAtts.chapterNames.keys())[list(fileAtts.chapterNames.values()).index(st)]
            numOfSource = list(fileAtts.chapterPath.keys())[list(fileAtts.chapterPath.values()).index(localeOfSource)]

            numOfDrop = list(fileAtts.writerTabs.keys())[list(fileAtts.writerTabs.values()).index(p)] #find num of writerTab dropped on
            switcher = dict()
            x = 0
            y = 0
            z = 0
            sourceSlot = 0 #the slot the tab came from

            logging.info("dropped", numOfSource, "in", numOfDrop)

            for i in fileAtts.writerTabs:
                z = z + 1
                if fileAtts.chapterList[z] == localeOfSource:
                        sourceSlot = z
                        logging.info("source slot", sourceSlot)

            if sourceSlot == numOfDrop:
                #do nothing
                for i in fileAtts.writerTabs:
                        x = x + 1
                        y = y + 1
                        switcher[x] = fileAtts.chapterList[y]

            elif sourceSlot > numOfDrop:
                for i in fileAtts.writerTabs:
                    x = x + 1 #determines where is slotted
                    y = y + 1 #determines what is slotted
                    if x == numOfDrop:
                        switcher[x] = fileAtts.chapterList[sourceSlot]
                        y = y - 1 #we want to grab what was in the numOfDrop now
                    elif x == sourceSlot:
                        switcher[x] = fileAtts.chapterList[y]
                        y = y + 1 #realign x and y
                    else:
                        switcher[x] = fileAtts.chapterList[y]

            elif sourceSlot < numOfDrop:
                for i in fileAtts.writerTabs:
                    x = x + 1 #determines where is slotted
                    y = y + 1 #determines what is slotted
                    if sourceSlot == numOfDrop - 1:
                        switcher[x] = fileAtts.chapterList[y] #if you're trying to drag a piece into itself, essentially
                    elif x == numOfDrop - 1: #you're placing ABOVE the drop num
                        switcher[x] = fileAtts.chapterList[sourceSlot]
                        y = y - 1 #realign x and y
                    elif x == sourceSlot:
                        y = y + 1
                        switcher[x] = fileAtts.chapterList[y]
                    else:
                        switcher[x] = fileAtts.chapterList[y]

            q = 0
            for i in switcher:
                q = q + 1
                fileAtts.chapterList[q] = switcher[q]
            self.rearranged.emit()
        else:
            e.ignore
