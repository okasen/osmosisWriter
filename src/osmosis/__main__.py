'''
Created on 21 Nov 2020

coded with help from guides by
Martin Fitzpatrick (Megasolid Idiom rich text word processor)


@author: Jennifer Black
'''
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *  # seems redundant
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * # seems redundatn
import os
from os import listdir
from os.path import isfile, join, expanduser
import sys
import re
import shutil
from functools import partial
from bs4 import *
from pathlib import Path
import logging

import osmosis.style as style
import osmosis.fileAttributes as fileAttributes
import osmosis.guiComponents as guiComponents

home = expanduser("~")
logLocation = os.path.join(home, "osmosisLog.log")
print(logLocation)
assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# having fileAtts instead of a Project-Class semms a bit odd TODO consider how to change this
fileAtts = fileAttributes.fileAttributes()

def styleChange():
    styleSet()

class workspaceTemplate(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(workspaceTemplate, self).__init__(*args, **kwargs)
        #self.workspace.selectionChanged.connect(self.update_format) #Getting the QTextEdit basics in

        self.setFontPointSize(14)
        self.setPlaceholderText("Blank pages are intimidating, so we put these words here.")
        self.setAutoFormatting(QTextEdit.AutoAll)

class newProjectAtStart(QDialog):
    def __init__(self, *args, **kwargs):
        super(newProjectAtStart, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setGeometry(QRect(200,200,400,200))
        self.setLayout(layout)
        #self.addLayout(layout)
        self.isModal()
        projectNamer = QLineEdit()
        projectNamer.setPlaceholderText("enter your project title here")
        button = QPushButton("confirm title and choose project folder")
        button.setEnabled(False)
        cancel = QPushButton("cancel")

        # if this would return projectTitle it could be passed to a class creating
        # projects
        def getTitle():
            fileAtts.projectTitle = projectNamer.text()
            cleanName = re.sub('[^A-Za-z0-9 ]+', '', fileAtts.projectTitle)
            fileAtts.projectTitle = cleanName

        def buttonToggle():
            button.setEnabled(True)

        # This is business logic, could be refactored into a ProjectFactory,
        # this way it would be easier to make changes to the ui
        def makeNew():
            logging.info("making a new project")
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            fileAtts.saveLocale = dialog.getExistingDirectory()

            fileAtts.projectFolder = fileAtts.saveLocale + "/" + fileAtts.projectTitle + "/"
            if os.path.exists(fileAtts.projectFolder):
                logging.info("This project already exists in this directory. Open the existing project, or create something new?")
                errorNote = QMessageBox(self)
                errorNote.setWindowTitle("Error")
                errorNote.setText("A project with this title already exists in this folder. Please enter a new title or select a different folder.")
                errorNote.setStandardButtons(QMessageBox.Ok)
                errorNote.exec()
            else:
                os.mkdir(fileAtts.projectFolder)
                fileAtts.projectPath = fileAtts.projectFolder + "/" + fileAtts.projectTitle + ".osm"
                fileAtts.projectSet = True
                with open(fileAtts.projectPath, 'w+') as f: #creating the main OSM file
                    f.write("")
                fileAtts.chapterFolder = fileAtts.projectFolder + "chapters/"
                os.mkdir(fileAtts.chapterFolder)
                logging.info("chapter folder made")

        def cancelPrompt():
            logging.info("Oops! No new project created.")

        projectNamer.textChanged.connect(buttonToggle)
        layout.addWidget(projectNamer)
        layout.addWidget(button)
        layout.addWidget(cancel)
        button.clicked.connect(getTitle)
        button.clicked.connect(makeNew)
        button.clicked.connect(self.accept)

        cancel.clicked.connect(cancelPrompt)
        cancel.clicked.connect(self.reject)

        self.exec()

class titleGiver(QDialog):
    def __init__(self, *args, **kwargs):
        super(titleGiver, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setGeometry(QRect(200,200,400,200))
        self.setLayout(layout)
        self.isModal()
        partNamer = QLineEdit()
        partNamer.setPlaceholderText("enter a brief chapter title here")
        button = QPushButton("confirm")
        button.setEnabled(False)
        def getTitle():
            fileAtts.partDescription = partNamer.text()
            logging.info(fileAtts.partDescription + " cleaned to")
            cleanName = re.sub('[^A-Za-z0-9 ]+', '', fileAtts.partDescription)
            fileAtts.partName = cleanName
            logging.info(fileAtts.partName)
            fileAtts.chapterPath[fileAtts.windowCount] = fileAtts.chapterFolder + fileAtts.partName + ".osmc"
            if os.path.exists(fileAtts.chapterPath[fileAtts.windowCount]):
                logging.info("This chapter title already exists in this directory. Please choose a new title")
                errorNote = QMessageBox(self)
                errorNote.setWindowTitle("Error")
                errorNote.setText("This chapter title already exists in this directory. Please choose a new title")
                errorNote.setStandardButtons(QMessageBox.Ok)
                errorNote.exec()
            else:
                fileAtts.chapterNameValid = True
        def buttonToggle():
            button.setEnabled(True)
        def makeNewPart():
            logging.info("making new chapter")
            with open(fileAtts.chapterPath[fileAtts.windowCount], 'w+') as f: #creating the main OSM file
                f.write("")
            self.accept()
        partNamer.textChanged.connect(buttonToggle)
        layout.addWidget(partNamer)
        layout.addWidget(button)
        button.clicked.connect(getTitle)
        button.clicked.connect(makeNewPart)

        self.exec()

class osmosisWriter(QMainWindow):


    resetting = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(osmosisWriter, self).__init__(*args, **kwargs)

        self.saveAsk = QDialog()

        self.startSplash = QWidget()

        self.mainScreen = QWidget()
        self.mainLayout = QGridLayout()
        self.setGeometry(QRect(50, 50, 1600, 800))
        scrollHolder = QVBoxLayout()
        self.workTabHolder = QWidget()
        self.workTabs = QGridLayout()
        self.mdiLayout = QMdiArea()
        self.mainScreen.setLayout(self.mainLayout)


        self.workTabs.setGeometry(QRect(0,0,400,800))

        self.workTabs.setSizeConstraint(QLayout.SetFixedSize)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.workTabHolder)
        self.scroll.setWidgetResizable(True)
        scrollHolder.addWidget(self.scroll)




        self.mainLayout.addLayout(scrollHolder, 1,0, Qt.AlignTop)
        self.mainLayout.addWidget(self.startSplash, 1,1, Qt.AlignRight)
        self.mainLayout.addWidget(self.mdiLayout, 1,1,Qt.AlignRight)
        self.setCentralWidget(self.mainScreen)

        self.workTabHolder.setLayout(self.workTabs)


        self.mainScreen.show()

        self.workspace = workspaceTemplate()


        self.newButton = QPushButton("Start a new project")
        self.openButton = QPushButton("Open an existing Osmosis project")


        def reTriggerTabs():
            for i in fileAtts.writerTabs:
                fileAtts.writerTabs[i].rearranged.connect(self.resetTabs)

        self.resetting.connect(reTriggerTabs)


        def startMenu():
            logging.info("start menu start!")
            self.newButton.clicked.connect(partial(startupHandler,value=1))
            self.openButton.clicked.connect(partial(startupHandler,value=2))

            self.workTabs.addWidget(self.newButton)
            self.workTabs.addWidget(self.openButton)
            self.newButton.show()
            self.openButton.show()
            self.openButton.adjustSize()
            logging.info(self.openButton.width())
            self.scroll.setMinimumWidth(self.openButton.width() + 86)

        def startNew():
            logging.info("starting a new project")
            fileAtts.isNew = True
            fileAtts.projectSet = False
            logging.info("About to newProjectAtStart")
            newProjectAtStart()
            if fileAtts.projectSet == True:
                self.newButton.setParent(None)
                self.openButton.setParent(None)
                self.newChapter()
                self.bigCascade()
                self.mdiLayout.show()
                chapterMenu.setEnabled(True)
                layoutMenu.setEnabled(True)
                formatMenu.setEnabled(True)
                editMenu.setEnabled(True)

        def startOpen():
            logging.info("about to open file")
            self.openFile()
            if fileAtts.projectSet == True:
                self.mdiLayout.show()
                self.newButton.setParent(None)
                self.openButton.setParent(None)
                chapterMenu.setEnabled(True)
                layoutMenu.setEnabled(True)
                formatMenu.setEnabled(True)
                editMenu.setEnabled(True)
            else:
                logging.info("project not set")
                return

        def startupHandler(self, value):
            if value == 1:
                startNew()
            else:
                startOpen()

        startMenu()

        mainMenu = QToolBar("File")
        fileMenu = self.menuBar().addMenu("&File")

        newAction = QAction("New Project", self)
        newAction.triggered.connect(self.newProject)
        fileMenu.addAction(newAction)

        saveAction = QAction("Save Project", self)
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)

        saveAsAction = QAction("Save As", self)
        saveAsAction.triggered.connect(self.saveFileAs)
        fileMenu.addAction(saveAsAction)

        openAction = QAction("Open Project", self)
        openAction.triggered.connect(lambda: self.savePopup("open"))
        fileMenu.addAction(openAction)

        exportAction = QAction("Export", self)
        exportAction.triggered.connect(self.exportFile)
        fileMenu.addAction(exportAction)

        #begin edit toolbar

        editMenu = QToolBar("Edit")
        editMenu = self.menuBar().addMenu("&Edit")

        undoAction = QAction("Undo", self)
        undoAction.triggered.connect(lambda: self.ctrlActions("undo"))
        editMenu.addAction(undoAction)

        redoAction = QAction("Redo", self)
        redoAction.triggered.connect(lambda: self.ctrlActions("redo"))
        editMenu.addAction(redoAction)

        cutAction = QAction("Cut", self)
        cutAction.triggered.connect(lambda: self.ctrlActions("cut"))
        editMenu.addAction(cutAction)

        copyAction = QAction("Copy", self)
        copyAction.triggered.connect(lambda: self.ctrlActions("copy"))
        editMenu.addAction(copyAction)

        pasteAction = QAction("Paste", self)
        pasteAction.triggered.connect(lambda: self.ctrlActions("paste"))
        editMenu.addAction(pasteAction)

        editMenu.setEnabled(False)

        #begin formatting options + menu

        self.bolded = False
        self.italic = False
        self.ul = False

        self.makeBold = QAction("Bold", self)
        self.makeBold.setShortcut(QKeySequence.Bold)
        self.makeBold.setCheckable(True)
        self.makeBold.toggled.connect(self.bold)

        self.makeIta = QAction("Italic", self)
        self.makeIta.setShortcut(QKeySequence.Italic)
        self.makeIta.setCheckable(True)
        self.makeIta.toggled.connect(self.setItalic)

        self.makeUL = QAction("Underline", self)
        self.makeUL.setShortcut(QKeySequence.Underline)
        self.makeUL.setCheckable(True)
        self.makeUL.toggled.connect(self.under)

        formatMenu = QToolBar("Format")
        formatMenu = self.menuBar().addMenu("&Format")
        formatMenu.addAction(self.makeBold)
        formatMenu.addAction(self.makeIta)
        formatMenu.addAction(self.makeUL)

        formatMenu.setEnabled(False)

        #begin the chapter toolbar

        chapterMenu = QToolBar("Chapters")
        chapterMenu = self.menuBar().addMenu("&Chapters")
        newAction = QAction("New chapter", self)
        newAction.triggered.connect(self.newChapter)
        chapterMenu.addAction(newAction)

        delAction = QAction("Delete current chapter", self)
        delAction.triggered.connect(self.deleteChapter)
        chapterMenu.addAction(delAction)

        chapterMenu.setEnabled(False)

        #begin the section for laying out docs

        self.casWindows = QAction("Smaller Cascading", self)
        self.casWindows.triggered.connect(self.mdiLayout.cascadeSubWindows)

        self.tileWindows = QAction("Tiled", self)
        self.tileWindows.triggered.connect(self.mdiLayout.tileSubWindows)

        self.bigWindows = QAction("Bigger Cascading", self)
        self.bigWindows.triggered.connect(self.bigCascade)

        self.maxWindows = QAction("Maximised", self)
        self.maxWindows.triggered.connect(self.maximizeMainWindow)

        layoutMenu = QToolBar("Layout")
        layoutMenu = self.menuBar().addMenu("&Layout")
        layoutMenu.addAction(self.casWindows)
        layoutMenu.addAction(self.tileWindows)
        layoutMenu.addAction(self.bigWindows)
        layoutMenu.addAction(self.maxWindows)

        layoutMenu.setEnabled(False)

        #begin font section

        fontToolbar = QToolBar("Font Choices")
        self.fontsize = QComboBox()
        self.fontsize.addItems(["14", "18", "24"])
        self.fontsize.currentIndexChanged[str].connect(lambda s: self.fontSize(float(s)))
        fontToolbar.addWidget(self.fontsize)

        self.addToolBar(fontToolbar)
        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.fontFamily)
        fontToolbar.addWidget(self.fonts)

        chapterToolbar = QToolBar("Chapter Tools")
        self.newChap = QPushButton("New Chapter")
        self.delChap = QPushButton("Delete Chapter")
        self.newChap.pressed.connect(self.newChapter)
        self.delChap.pressed.connect(self.deleteChapter)
        fontToolbar.addWidget(self.newChap)
        fontToolbar.addWidget(self.delChap)
        self.addToolBar(chapterToolbar)

        #begin theme section
        themeMenu = self.menuBar().addMenu("&Theme")
        self.themePicker = QAction("Pick a theme", self)
        self.themePicker.triggered.connect(self.styleChange)
        themeMenu.addAction(self.themePicker)

        self.show()


    def styleChange(self):
        style.styleSet()

    def bigCascade(self):
        #x and y here represent x and y coordinates.
        #might need renaming to not need this comment!
        y = 0
        x = 0
        xOffset = 0
        self.mdiLayout.cascadeSubWindows()
        for i in fileAtts.openWindows:
            xCascader = x * 40
            yCascader = y * 40
            fileAtts.openWindows[i].setGeometry(QRect(xCascader + xOffset, yCascader, 700, 500))
            x = x + 1
            y = y + 1
            if y == 11: #to prevent the tiles from going endlessly offscreen to the bottom right
                y = 0
                xOffset = xOffset + 40
                x = 0

    def resetTabs(self):
        logging.info(fileAtts.writerTabs)
        for i in fileAtts.writerTabs:
            fileAtts.writerTabs[i].setParent(None)
        for i in fileAtts.chapterList:
            fileAtts.writerTabs[i] = guiComponents.workTab(fileAtts.chapterNames[fileAtts.chapterList[i]])
            tabRow = i - 1
            self.workTabs.addWidget(fileAtts.writerTabs[i],tabRow,0)
            fileAtts.writerTabs[i].clicked.connect(partial(self.updateActiveWindow, fileAtts.chapterNames[fileAtts.chapterList[i]]))

            self.resetting.emit()
        self.scroll.setMinimumWidth(240)

    def closeEvent(self, event):
        if fileAtts.isEdited:
            event.ignore()
            self.savePopup("closeAttempt")

    def checkWindowActive(self):
        currentlyOpen = ""
        logging.info(fileAtts.openWindows)
        for i in fileAtts.openWindows:
            logging.info(i)
            if fileAtts.openWindows[i] == self.mdiLayout.activeSubWindow():
                logging.info(fileAtts.openWindows[i])
                logging.info(i)
                currentlyOpen = i
                break
            currentlyOpen = i
        logging.info(currentlyOpen, "is open")
        return currentlyOpen

    def checkWriterActive(self):
        window = self.checkWindowActive()
        winPath = list(fileAtts.chapterNames.keys())[list(fileAtts.chapterNames.values()).index(window)]
        writerNum = list(fileAtts.openCorrelation.keys())[list(fileAtts.openCorrelation.values()).index(winPath)]
        return writerNum

    def ctrlActions(self, source):
        writer = self.checkWriterActive()
        logging.info("ctrl Action pressed " + source)
        if source == "undo":
            logging.info("undo")
            fileAtts.openWriters[writer].undo()
        elif source == "redo":
            logging.info("redo")
            fileAtts.openWriters[writer].redo()
        elif source == "cut":
            fileAtts.openWriters[writer].cut()
        elif source == "copy":
            fileAtts.openWriters[writer].copy()
        elif source == "paste":
            fileAtts.openWriters[writer].paste()

    def fontSize(self, s):
        writer = self.checkWriterActive()
        fileAtts.openWriters[writer].setFontPointSize(s)

    def fontFamily(self):
        writer = self.checkWriterActive()
        fileAtts.openWriters[writer].setCurrentFont(self.fonts.currentFont())
        fileAtts.openWriters[writer].setFontPointSize(float(self.fontsize.currentText()))

    def bold(self):
        writer = self.checkWriterActive()
        if self.bolded == False:
            fileAtts.openWriters[writer].setFontWeight(QFont.Bold)
            self.bolded = True
        elif self.bolded == True:
            fileAtts.openWriters[writer].setFontWeight(QFont.Normal)
            self.bolded = False

    def setItalic(self):
        writer = self.checkWriterActive()
        if self.italic == False:
            fileAtts.openWriters[writer].setFontItalic(True)
            self.italic = True
        elif self.italic == True:
            fileAtts.openWriters[writer].setFontItalic(False)
            self.italic = False

    def under(self):
        writer = self.checkWriterActive()
        if self.ul == False:
            fileAtts.openWriters[writer].setFontUnderline(True)
            self.ul = True
        elif self.ul == True:
            fileAtts.openWriters[writer].setFontUnderline(False)
            self.ul = False


    def maximizeMainWindow(self):
        try:
            window = self.checkWindowActive()
            fileAtts.openWindows[window].showMaximized()
        except:
            logging.info("no window activated")

        def keyPressEvent(self, *args, **kwargs):
            if fileAtts.isEdited == False: #prevents isEdited from being changed when already true
                fileAtts.isEdited = True
            return QTextEdit.keyPressEvent(self, *args, **kwargs)

    def newProject(self):
        logging.info("new project")
        self.savePopup("newProject")

    def newChapter(self):
        for i in fileAtts.writerTabs:
            fileAtts.writerTabs[i].setParent(None)
        fileAtts.windowCount = fileAtts.windowCount + 1
        count = fileAtts.windowCount
        while fileAtts.chapterNameValid == False:
            titleGiver() #get the chapter title
        fileAtts.chapterNameValid = False
        fileAtts.chapterList[count] = fileAtts.chapterPath[count] #chapters with corresponding urls by the order they were created, to be reordered by the user
        fileAtts.chapterNames[fileAtts.chapterList[count]] = str(fileAtts.partName) #chapterlist refers to the number of each chapter, while chapter name is the user given title
        fileAtts.openCorrelation[count] = fileAtts.chapterList[count] #they start out the same but chapterList changes with user input

        fileAtts.openWidgets[count] = QWidget()
        fileAtts.openWindows[fileAtts.partName] = guiComponents.workArea()
        fileAtts.openWriters[count] = workspaceTemplate()
        fileAtts.openLayouts[count] = QVBoxLayout()

        fileAtts.openWindows[fileAtts.partName].setWidget(fileAtts.openWidgets[count])
        fileAtts.openWidgets[count].setLayout(fileAtts.openLayouts[count])

        fileAtts.openLabels[count] = QLabel()
        fileAtts.openLabels[count].setText(fileAtts.partName)
        fileAtts.openLayouts[count].addWidget(fileAtts.openLabels[count])

        fileAtts.openLayouts[count].addWidget(fileAtts.openWriters[count])

        self.mdiLayout.addSubWindow(fileAtts.openWindows[fileAtts.partName])

        fileAtts.openLabels[count] = QLabel()
        fileAtts.openLabels[count].setText(fileAtts.partDescription)
        fileAtts.writerTabs[count] = guiComponents.workTab(str(fileAtts.partName))


        tabRow = count
        self.workTabs.addWidget(fileAtts.writerTabs[count], tabRow, 1)

        fileAtts.writerTabs[count].clicked.connect(partial(self.updateActiveWindow, fileAtts.chapterNames[fileAtts.openCorrelation[count]]))
        fileAtts.writerTabs[count].rearranged.connect(self.resetTabs)

        #self.mdiLayout.cascadeSubWindows() #later on, set a toggle of if the user wants tile or cascades
        fileAtts.openWindows[fileAtts.partName].show()

        self.resetTabs()

    # business logic, a UI-Class might call a function like this,
    # but it should be defined elsewhere
    # TODO
    def saveFile(self): #The function called when clicking the saveButton
        print("Saving!")
        logging.info("saving!")
        try:
            count = 0
            for i in fileAtts.chapterList: #writes down the chapters, once for each in the list
                count = count + 1
                chapterID = list(fileAtts.openCorrelation.keys())[list(fileAtts.openCorrelation.values()).index(fileAtts.chapterList[count])]
                #openCorrelation[count] should give you the path that correlates with that writer. To check
                with open(fileAtts.chapterList[count], 'w+') as f:
                    f.write(fileAtts.openWriters[chapterID].toHtml())
        except Exception as e:
            logging.info("oops, something went wrong")
            self.dialog_critical(str(e))
        # This sounds like something we could use multiple times, so it should be in its
        # own method
        with open(fileAtts.projectPath, 'w+') as f: #writing the chapter list in the main OSM file
            for i in fileAtts.chapterList:
                if i == 1: #if this is the first of the for loop iterations
                    self.projectString = fileAtts.chapterList[i]
                else:
                    self.projectString = self.projectString + "<***ChapterBreak***>" + fileAtts.chapterList[i]
            f.write(self.projectString)
        fileAtts.isEdited = False
        self.projectString = ""
        x = 0

    def saveFileAs(self): #The function called when clicking the saveButton
        oldPath = fileAtts.projectPath
        fileAtts.projectPath, _ = QFileDialog.getSaveFileName(self, "Save file as", "", "OSM documents (*.osm)")
        logging.info(fileAtts.projectPath)
        logging.info("^^^")
        if oldPath == fileAtts.projectPath: #if the path has not changed
            logging.info("You seem to be saving as a project that already exists")
            self.saveFile()
        if fileAtts.projectPath == "":
            logging.info("no path chosen. Cancelling save as")
            fileAtts.projectPath = oldPath
            return #return without a return statement should never be needed

    def openFile(self):
        fileAtts.isNew = False
        currentPath = ""
        try:
            fileAtts.projectPath, _ = QFileDialog.getOpenFileName(self, "Open file", "", "OSM documents (*.osm)")
            currentPath = fileAtts.projectPath
            logging.info(currentPath)
            if currentPath != "": #If it's still blank Dave: this is currentPath == None
                fileAtts.projectSet = True
        except: # broad excepts are evil, catch the error you are actually expecting
            fileAtts.projectSet = False
            logging.info("project not set because path is empty")
            return
        if fileAtts.projectSet == True:
            projectPathList = currentPath.split("/")
            projectFullName = projectPathList[-1]
            logging.info("was:")
            for i in fileAtts.writerTabs:
                fileAtts.writerTabs[i].setParent(None)#remove writertabs
            logging.info("part one popped")
            for i in fileAtts.openWindows:
                fileAtts.openWindows[i].close()#remove windows
            logging.info("part two popped")
            logging.info("about to try creating")
            try:
                fileAtts.projectName = re.search('(.+?)\.osm', projectFullName).group(1)
            except:
                fileAtts.projectName = "untitled"
                logging.info("no project name found.")

            logging.info("projectName set for {}", fileAtts.projectPath)
            try:
                with open(fileAtts.projectPath, 'r') as f:
                    fileAtts.isEdited = False #newly opened files have not been edited
                    fileAtts.isNew = False
                    #fileAtts.openWriters[1] = workspaceTemplate()
                    chapterRaw = f.read()
                    chapterListMaker = list()
                    chapterListMaker = chapterRaw.split("<***ChapterBreak***>")
                    fileAtts.projectSet = True
            except:
                logging.info("oops, it looks like your .osm file is blank.")

                fileAtts.projectSet = False
                self.__init__()

            #getting chapter folder:
            for i in chapterListMaker:
                #os.path.split(path) does this already
                chapterPathList = i.split("/")
                del chapterPathList[-1]
                fileAtts.chapterFolder = "/".join(chapterPathList) + "/"

            # adding on lost files #putting this in its own function would increase
            # readability and should be easier to test TODO
            chapFiles = [f for f in listdir(fileAtts.chapterFolder) if isfile(join(fileAtts.chapterFolder, f))]
            logging.info(chapFiles)
            lostChapFiles = list()
            for i in chapFiles:
                match = False
                for n in chapterListMaker:
                    chapterNameList = n.split("/")
                    chapterName = chapterNameList[-1]
                    if i == chapterName:
                        match = True
                        break
                if match == False:
                    lostChapterName = fileAtts.chapterFolder + i
                    logging.info(lostChapterName)
                    lostChapFiles.append(lostChapterName)
            logging.info("these chapters were lost: {}", lostChapFiles)
            logging.info("adding these chapters at the end")
            chapterListMaker += (lostChapFiles)
            logging.info(chapterListMaker)
            #end additions


            try:
                x = 0
                for i in chapterListMaker:
                    if os.path.exists(i):
                        x = x + 1
                        fileAtts.chapterList[x] =  i
                logging.info("chapterList is {}", fileAtts.chapterList)
                for i in chapterListMaker:
                    if os.path.exists(i):
                        logging.info("we are currently working through CLM {}", i)
                        fileAtts.windowCount = fileAtts.windowCount + 1
                        current = fileAtts.windowCount
                        fileAtts.chapterPath[current] = i
                        chapterPathList = i.split("/")
                        chapterFullName = chapterPathList[-1]

                        try:
                            chapterName = re.search('(.+?)\.osmc', chapterFullName).group(1)
                        except:
                            chapterName = "unnamed"
                        fileAtts.openCorrelation[fileAtts.windowCount] = i
                        fileAtts.chapterNames[i] = chapterName #to get the correlated text with this later, ask for fileAtts.chapterNames[openCorrelation[fileAtts.windowCount]]
                        #which along with fileAtts.openWriters[fileAtts.windowCount] will get you the correct chapter and text for the requisite window
                        #TODO make this not require copy/paste or superhuman memory
                        try:
                            with open(i) as f:
                                contents = f.read()
                        except:
                            logging.info("looks like a chapter was deleted improperly")

                        fileAtts.openLayouts[current] = QVBoxLayout()

                        fileAtts.openWidgets[current] = QWidget()

                        fileAtts.openWriters[current] = workspaceTemplate()

                        fileAtts.openWindows[chapterName] = guiComponents.workArea()

                        fileAtts.openWidgets[current].setLayout(fileAtts.openLayouts[current])

                        fileAtts.openLabels[current] = QLabel()
                        fileAtts.openLabels[current].setText(chapterName)
                        fileAtts.openLayouts[current].addWidget(fileAtts.openLabels[current])

                        fileAtts.openLayouts[current].addWidget(fileAtts.openWriters[current])

                        fileAtts.openWindows[chapterName].setWidget(fileAtts.openWidgets[current])

                        self.mdiLayout.addSubWindow(fileAtts.openWindows[chapterName])
                        self.mdiLayout.cascadeSubWindows() #later on, set a toggle of if the user wants tile or cascades
                        fileAtts.openWindows[chapterName].show()

                        fileAtts.openWriters[current].setHtml(contents)

                        fileAtts.writerTabs[current] = guiComponents.workTab(chapterName)

                        fileAtts.writerTabs[current].clicked.connect(
                            partial(self.updateActiveWindow,
                                    fileAtts.chapterNames[fileAtts.openCorrelation[current]]
                                    )
                        )

                        fileAtts.writerTabs[current].rearranged.connect(self.resetTabs)
                        tabRow = current - 1
                        self.workTabs.addWidget(fileAtts.writerTabs[current], tabRow, 1)
                    else:
                        chapterListMaker.remove(i)

                self.checkWindowActive()
                self.updateWindowTitle()
                self.bigCascade()
                self.resetTabs()
                logging.info(fileAtts.writerTabs)

            except Exception as e:
                logging.info("oops, it looks like your .osm file is improperly formatted.")

    def deleteChapter(self): # this function mixes business logic and gui logic.
        chapterToDeleteWindow = self.checkWindowActive()
        chapterOriginalPath = list(fileAtts.chapterNames.keys())[list(fileAtts.chapterNames.values()).index(chapterToDeleteWindow)]
        logging.info("delete")
        delPath = fileAtts.chapterFolder + "deleted"
        chapterDeletePath = delPath + "/" + fileAtts.chapterNames[chapterOriginalPath] + ".osmc" #BIZ
        logging.info(chapterDeletePath)
        if not os.path.exists(delPath):
            os.mkdir(delPath)
        else:
            logging.info("preparing to delete")
        if not os.path.exists(chapterDeletePath):
            shutil.move(chapterOriginalPath, chapterDeletePath)
        else:
            logging.info("chapter already deleted")
            os.remove(chapterOriginalPath)
        logging.info("moved")

        #TODO: Above this line and below this line are Business and GUI logic respectively
        #Move them to separate functions

        totalTabs = len(fileAtts.chapterList)
        logging.info("there are x tabs: ")
        logging.info(totalTabs) #find the position of the last tab in the sequence

        switcher = dict()
        x = 0
        y = 0
        z = 0
        sourceSlot = 0 #the slot the tab came from

        for i in fileAtts.chapterList: #probably needs the single letter names cleaned
            z = z + 1
            logging.info(fileAtts.chapterList)
            logging.info(chapterOriginalPath)
            if fileAtts.chapterList[z] == chapterOriginalPath:
                    sourceSlot = z
                    logging.info("source slot {}", sourceSlot)

        if sourceSlot == totalTabs: #in this case, if it's last on the list
            #do nothing
            logging.info("final chapter tab removed, no reordering") #GUI!

        elif sourceSlot < totalTabs:
            logging.info("in")
            for i in fileAtts.chapterList:
                x = x + 1 #determines where is slotted, please rename this oh wow
                y = y + 1 #determines what is slotted, same, needs a better name
                if x == totalTabs: #you're placing ABOVE the drop num
                    logging.info("final slot")
                    switcher[totalTabs] = fileAtts.chapterList[sourceSlot]
                    logging.info("switched to back")
                    y = y - 1 #realign x and y
                elif x == sourceSlot:
                    logging.info("at source")
                    y = y + 1
                    switcher[x] = fileAtts.chapterList[y]
                else:
                    logging.info("before")
                    switcher[x] = fileAtts.chapterList[y]
        #just move everything up after the source slot
        q = 0
        for i in switcher:
            q = q + 1
            fileAtts.chapterList[q] = switcher[q]
        numLeft = len(fileAtts.chapterList)
        if numLeft > 1:
            del fileAtts.chapterList[numLeft]
            fileAtts.openWindows[chapterToDeleteWindow].close()
            fileAtts.openWindows.pop(chapterToDeleteWindow, None)
            fileAtts.windowCount = fileAtts.windowCount - 1
        else:
            logging.info("you can't remove the last tab from your project!")
        logging.info("about to rearrange")
        self.resetTabs() #majorly GUI
        logging.info(fileAtts.chapterList)

    def exportFile(self):
        if fileAtts.projectSet == True:
            logging.info("preparing to export")
            self.saveFile()
            chapterNamesForExport = list()
            try:
                with open(fileAtts.projectPath, 'r') as f:
                    chapterRaw = f.read()
                chapterListMaker = list()
                chapterListMaker = chapterRaw.split("<***ChapterBreak***>")
                x = 0
                y = 0
                z = 0

                for i in chapterListMaker:
                    x = x + 1
                    fileAtts.chapterList[x] =  i
                for i in chapterListMaker:
                    z = z + 1 #tabbing through windows
                    writingFrom = fileAtts.chapterList[z]
                    writingFromList = writingFrom.split("/")
                    chapterFullName = writingFromList[-1]
                    try:
                        chapterName = re.search('(.+?)\.osm', chapterFullName).group(1)
                    except:
                        chapterName = "unnamed"

                    chapterTitleHTML = "<p><h2>" + chapterName + "</h2><p>"
                    chapterNamesForExport.append(chapterTitleHTML)

                exportPath, _ = QFileDialog.getSaveFileName(self, "Save file", "", "")
                htmlPath = exportPath + ".html"
                docPath = Path(exportPath + ".doc")
                logging.info("exporting to {}", htmlPath)
                with open(htmlPath, 'a+') as f:
                    for i in chapterListMaker:
                        f.write(chapterNamesForExport[y])
                        logging.info("name written")
                        y = y + 1
                        chapterID = list(fileAtts.openCorrelation.keys())[
                            list(fileAtts.openCorrelation.values()).index(fileAtts.chapterList[y])
                        ]
                        logging.info("about to write contents")
                        f.write(fileAtts.openWriters[chapterID].toHtml())

                docParser = HtmlToDocx()
                docParser.parse_html_file(htmlPath, docPath)
                logging.info(docPath)
                logging.info("exported")
            except:
                logging.info("oops, couldn't export")

            if os.path.exists(str(exportPath)):
                os.remove(str(exportPath))
        else:
            logging.info("no project to export found")

    def goHereToContinue(self, endResult): #TODO: Review this function. It feels like it's doing more than one job
        if endResult == "closeAttempt":
            self.saveFile()
            sys.exit()
        elif endResult == "open":
            self.openFile()
        else: #if new file
            logging.info("getting ready for the new project")
            fileAtts.isNew = True
            fileAtts.projectSet = False
            self.saveAsk.close()
            newProjectAtStart()
            if fileAtts.projectSet == True:
                self.mdiLayout.closeAllSubWindows()
                x = 0
                for i in fileAtts.writerTabs:
                    x = x + 1
                    fileAtts.writerTabs[x].setParent(None)
                x = 0
                for i in fileAtts.openWriters:
                    x = x + 1
                    fileAtts.openWriters[x].setParent(None)
                fileAtts.windowCount = 0
                logging.info("window clear done")
                fileAtts.openWindows.clear() #the windows that hold writers, in the order they were created
                fileAtts.openCorrelation.clear() #just ensures that the keys in openWindows correlate to the correct keys in openWriters, and therefor, that the values are correct
                fileAtts.chapterList.clear() #holds the chapter paths in order of how the user has organised them, and is used to create the main OSM file's structure
                fileAtts.chapterNames.clear() #chapter's path :: chapter's name, will not change with user input
                fileAtts.writerTabs.clear()
                fileAtts.openWriters.clear()
                logging.info(fileAtts.chapterPath)
                fileAtts.chapterPath.clear()
                logging.info("cleared")
            else:
                fileAtts.projectSet == True #reset the projectSet

    def goHereToSaveFirst(self, endResult):
        logging.info("saving first")
        self.saveFile()
        self.goHereToContinue(endResult)
        self.saveAsk.close()

    def savePopup(self, sourceDia): #TODO: consider if this should be in guiComponenets?
        #What changes would this need?
        layout  = QGridLayout()
        layout.setColumnStretch(1,3)
        yesSave = QPushButton("Yes, save", self.saveAsk)
        noSave = QPushButton("No, do not save", self.saveAsk)
        nevermindSave = QPushButton("Cancel", self.saveAsk)

        yesSave.clicked.connect(lambda: self.goHereToSaveFirst(sourceDia))
        noSave.clicked.connect(lambda: self.goHereToContinue(sourceDia))
        nevermindSave.clicked.connect(self.saveAsk.close)
        self.saveAsk.setWindowTitle("Save your work?")
        self.saveAsk.setWindowModality(Qt.ApplicationModal)

        self.saveAsk.setLayout(layout)
        layout.addWidget(yesSave,0,0)
        layout.addWidget(noSave,0,1)
        layout.addWidget(nevermindSave,0,2)
        self.saveAsk.exec()

    def saveThenLoad(self): #The function called when clicking the saveButton
        self.saveFile()
        self.goHereToContinue("openProject")
        self.openFile()

    def updateWindowTitle(self):
        projectPathList = fileAtts.projectPath.split("/")
        projectFullName = projectPathList[-1]
        try:
            projectName = re.search('(.+?)\.osm', projectFullName).group(1)
        except:
            projectName = "untitled"
        self.setWindowTitle("Osmosis Writer - " + projectName)

    def updateActiveWindow(self, windowName):
        #set the active window to the one correlated with the button pressed
        logging.info(windowName)
        self.mdiLayout.setActiveSubWindow(fileAtts.openWindows[windowName])


app = QApplication(sys.argv)
app.setApplicationName("Osmosis Writer")
window = osmosisWriter()
window.show()
QFontDatabase.addApplicationFont("OpenDyslexic-Bold")
QFontDatabase.addApplicationFont("OpenDyslexic-BoldItalic")
QFontDatabase.addApplicationFont("OpenDyslexic-Italic")
QFontDatabase.addApplicationFont("OpenDyslexic-Regular")

def main():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=logLocation, filemode='w+', level=logging.INFO)

    app.style().unpolish(app)
    StyleSet = style.styleSet()
    app.setStyleSheet(StyleSet.styleChoice)
    app.style().polish(app)
    app.exec_()

if __name__ == '__main__':
    main()
