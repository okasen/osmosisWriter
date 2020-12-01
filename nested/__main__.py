'''
Created on 21 Nov 2020

coded with help from guides by 
Martin Fitzpatrick (Megasolid Idiom rich text word processor) 


@author: Jennifer Black
'''
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import re
from functools import partial
from htmldocx import HtmlToDocx
from pathlib import Path

def main():
    class fileAttributes:
        def __init__(self):
            self.isNew = True #defines if we're loading a file or starting new
            self.isEdited = False #no file is edited before it is started!
            self.projectPath = 'C:/untitled.txt'
            self.projectTitle = "untitled"
            self.projectSet = False
            self.chapterFolder = ""
            self.saveLocale = ""
            self.projectFolder = ""
            self.isNamed = False
            self.contents = "test"
            self.windowCount = 0
            self.fileRequest = list() #might be defunct
            self.openWindows = dict() #the windows that hold writers, in the order they were created
            self.openCorrelation = dict() #just ensures that the keys in openWindows correlate to the correct keys in openWriters, and therefor, that the values are correct
            self.openWriters = dict() #used to hold the actual writers that correspond to writer windows, correlated to an int
            self.writerTabs = dict() #used to hold the actual tabs that correspond to writer windows, correlated to an int
            self.chapterList = dict() #holds the chapter paths in order of how the user has organised them, and is used to create the main OSM file's structure
            self.partName = "" #changes to hold the most recently added part's name
            self.partDescription = "" #holds the part name with any special chars or spaces
            self.chapterNames = dict() #chapter's path :: chapter's name, will not change with user input
            self.chapterPath = dict() #chapter's path linked to a number that correlates with the name, to ensure chapters do not become mislabeled or lost
            self.chapterOrder = dict() #stores the order on the user end
    
    fileAtts = fileAttributes()
    
    class workTab(QPushButton):
        
        rearranged = pyqtSignal()
            
        
        def __init__(self, label):
            super().__init__()
            #self.show()
            self.setAcceptDrops(True)
            #self.setGeometry(QRect(0,0,100,100))
            self.setText(label)
            self.text = label
            
        
            
        
            
        
        def mousePressEvent(self, e):
                
            super().mousePressEvent(e)
                
            if e.button() == Qt.RightButton:
                print('press')
                
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
            print(e.pos)
            e.accept()
                
        def dropEvent(self, e):
            
            
            #sourceText = str(e.mimeData().text())
            location = e.source()
            if isinstance(location, workTab):
                l = self.text #location
                p = self #place
                st = e.mimeData().text()
                localeOfSource = list(fileAtts.chapterNames.keys())[list(fileAtts.chapterNames.values()).index(st)]
                numOfSource = list(fileAtts.chapterPath.keys())[list(fileAtts.chapterPath.values()).index(localeOfSource)]
                
                numOfDrop = list(fileAtts.writerTabs.keys())[list(fileAtts.writerTabs.values()).index(p)] #find num of writerTab dropped on
                #frex, you drop #1 at #3, pos:holding, 1:2, 2:3, 3:1, 4:4
                #frex, you drop #4 at #2, pos:holding, 1:1, 2:4, 3:2, 4:3
                switcher = dict()
                x = 0
                y = 0
                z = 0
                run = False
                 #checks if a specific method has run
                sourceSlot = 0 #the slot the tab came from
                
                print("dropped", numOfSource, "in", numOfDrop)
                #example of two sequences that cause issues, moving a number back into its original slot
                #1111 2222 333 4444
                #four one two three
                #four two one three
                for i in fileAtts.writerTabs:
                    z = z + 1
                        
                    if fileAtts.chapterList[z] == localeOfSource:
                            sourceSlot = z
                            print("source slot", sourceSlot)
                            
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
                        print("x, y", x, y)
                        if x == numOfDrop:
                            switcher[x] = fileAtts.chapterList[sourceSlot]
                            y = y - 1 #we want to grab what was in the numOfDrop now
                        elif x == sourceSlot:
                            switcher[x] = fileAtts.chapterList[y]
                            y = y + 1 #realign x and y
                        else:
                            switcher[x] = fileAtts.chapterList[y]
                        print("new", x, y)
                        
                elif sourceSlot < numOfDrop:
                    for i in fileAtts.writerTabs:
                        x = x + 1 #determines where is slotted
                        y = y + 1 #determines what is slotted
                        print("x, y", x, y)
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
                        print("new", x, y)
                        
                print("Dogbean")
                print(switcher)
                q = 0
                for i in switcher:
                    q = q + 1
                    print(q)
                    fileAtts.chapterList[q] = switcher[q]
                self.rearranged.emit()
            else:
                e.ignore
        
        
            
    class workspaceTemplate(QTextEdit):
        def __init__(self, *args, **kwargs):
            super(workspaceTemplate, self).__init__(*args, **kwargs)
            #self.workspace.selectionChanged.connect(self.update_format) #Getting the QTextEdit basics in
            self.font = QFont('Courier', 18)
            self.setFont(self.font)
            self.setFontPointSize(14)
            self.setPlaceholderText("Blank pages are intimidating, so we put these words here.")
            #self.setAutoFormatting(QTextEdit.AutoAll)
            
            
    class doStart(QDialog):
        def __init__(self, *args, **kwargs):
            super(doStart, self).__init__(*args, **kwargs)
            layout = QVBoxLayout()
            self.setGeometry(QRect(200,200,400,200))
            self.setLayout(layout)
            #self.addLayout(layout)
            self.isModal()
            projectNamer = QLineEdit()
            projectNamer.setPlaceholderText("enter your project title here")
            button = QPushButton("confirm title and choose project folder")
            button.setEnabled(False)
            def getTitle():
                fileAtts.projectTitle = projectNamer.text()
            def buttonToggle():
                button.setEnabled(True)
            def makeNew():    
                
                dialog = QFileDialog(self)
                dialog.setFileMode(QFileDialog.Directory)
                fileAtts.saveLocale = dialog.getExistingDirectory()
                if True:                    
                    fileAtts.projectFolder = fileAtts.saveLocale + "/" + fileAtts.projectTitle + "/"       
                    if os.path.exists(fileAtts.projectFolder):
                        print("This project already exists in this directory. Open the existing project, or create something new?")
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
            projectNamer.textChanged.connect(buttonToggle)
            layout.addWidget(projectNamer)
            layout.addWidget(button)
            button.clicked.connect(getTitle)
            button.clicked.connect(makeNew)
            button.clicked.connect(self.accept)
            #self.addWidget(button)
                    
            self.exec()         
        
        
    class titleGiver(QDialog):
        def __init__(self, *args, **kwargs):
            super(titleGiver, self).__init__(*args, **kwargs)
            layout = QVBoxLayout()
            self.setGeometry(QRect(200,200,400,200))
            self.setLayout(layout)
            #self.addLayout(layout)
            self.isModal()
            partNamer = QLineEdit()
            partNamer.setPlaceholderText("enter a brief chapter title here")
            button = QPushButton("confirm")
            button.setEnabled(False)
            def getTitle():
                fileAtts.partDescription = partNamer.text()
                cleanName = re.sub('[^A-Za-z0-9 ]+', '', fileAtts.partDescription)
                print("Squeaky clean", cleanName)
                fileAtts.partName = cleanName
            def buttonToggle():
                button.setEnabled(True)
            def makeNewPart():                
                fileAtts.chapterPath[fileAtts.windowCount] = fileAtts.chapterFolder + fileAtts.partName + ".osm"
                print(fileAtts.chapterPath)
                if os.path.exists(fileAtts.chapterPath[fileAtts.windowCount]):
                    print("This chapter title already exists in this directory. Please choose a new title")
                    errorNote = QMessageBox(self)
                    errorNote.setWindowTitle("Error")
                    errorNote.setText("This chapter title already exists in this directory. Please choose a new title")
                    errorNote.setStandardButtons(QMessageBox.Ok)
                    errorNote.exec()
                else:
                    print("making a scene for", fileAtts.windowCount)
                    with open(fileAtts.chapterPath[fileAtts.windowCount], 'w+') as f: #creating the main OSM file
                        f.write("")
            partNamer.textChanged.connect(buttonToggle)
            layout.addWidget(partNamer)
            layout.addWidget(button)
            button.clicked.connect(getTitle)
            button.clicked.connect(makeNewPart)
            button.clicked.connect(self.accept)
            #self.addWidget(button)
                    
            self.exec()         
    
     
    class osmosisWriter(QMainWindow):
        
        resetting = QtCore.pyqtSignal()     
           
        def __init__(self, *args, **kwargs):
            super(osmosisWriter, self).__init__(*args, **kwargs)
            
            
            self.mainScreen = QWidget()
            self.mainLayout = QGridLayout()
            self.setGeometry(QRect(100, 100, 800, 600))
            self.workTabs = QGridLayout()
            self.mdiLayout = QMdiArea()
            #self.mdiLayout.setOption()
            self.mainScreen.setLayout(self.mainLayout)
            
            self.mainLayout.addLayout(self.workTabs, 1,0, Qt.AlignTop)
            self.mainLayout.addWidget(self.mdiLayout, 1,1, Qt.AlignRight)
            self.setCentralWidget(self.mainScreen)    
           
            self.mainScreen.show()
            
            
            self.workspace = workspaceTemplate()
            
            def reTriggerTabs():
                for i in fileAtts.writerTabs:
                    print(i)
                    fileAtts.writerTabs[i].rearranged.connect(self.resetTabs)
            
            self.resetting.connect(reTriggerTabs)
            
            '''
            for i in fileAtts.writerTabs:
                reset = self.resetTabs
                print("ba")
                fileAtts.writerTabs[i].rearranged.connect(lambda: self.resetTabs())
                print("near")
               '''
        
           
            
            #resetter = self.resetTabs()        
            
            
            
            
            #starting config
            
            
            def onStart():
                self.newButton = QPushButton("Start a new project")
                self.openButton = QPushButton("Open an existing Osmosis project")
         
                self.newButton.clicked.connect(partial(startupHandler,value=1))
                self.openButton.clicked.connect(partial(startupHandler,value=2))
       
                self.workTabs.addWidget(self.newButton)
                self.workTabs.addWidget(self.openButton)
                self.newButton.show()
                self.openButton.show()
      
                        
            def startNew():
                self.newButton.setParent(None)
                self.openButton.setParent(None)
                fileAtts.isNew = True
                while fileAtts.projectSet == False:
                    doStart()
                self.mdiLayout.show()
                self.newChapter()
                
            def startOpen():
                self.newButton.setParent(None)
                self.openButton.setParent(None)
                fileAtts.isNew = False
                self.mdiLayout.show()
                self.openFile()
            
            def startupHandler(self, value):
                print("got it")
                if value == 1:
                    print("new")
                    startNew()
                    #fileAtts.isNew = True
                    #self.mdiLayout.show()
                    #self.newChapter()
                    
                    
                else:
                    print("existing")
                    startOpen()
    
                    
                    
            onStart()
        
        
        
        
            
             #we start with no windows
            
            
            #mdiLayout.addSubWindow(self.workspaceWindow) #put the workspace in the layout
            
            #begin File toolbar
            
            mainMenu = QToolBar("File")
            fileMenu = self.menuBar().addMenu("&File")
            
            newAction = QAction("New Project", self)
            newAction.triggered.connect(self.newProject)
            fileMenu.addAction(newAction)
            
            saveAction = QAction("Save", self)
            saveAction.triggered.connect(self.saveFile)
            fileMenu.addAction(saveAction)
            
            saveAsAction = QAction("Save As", self)
            saveAsAction.triggered.connect(self.saveFileAs)
            fileMenu.addAction(saveAction)
            
            openAction = QAction("Open", self)
            openAction.triggered.connect(self.loadCheck)
            fileMenu.addAction(openAction)
            
            exportAction = QAction("Export", self)
            exportAction.triggered.connect(self.exportFile)
            fileMenu.addAction(exportAction)
            
            #begin edit toolbar
        
            editMenu = QToolBar("Edit")
            editMenu = self.menuBar().addMenu("&Edit")
            
            undoAction = QAction("Undo", self)
            undoAction.triggered.connect(self.workspace.undo)
            editMenu.addAction(undoAction)
            
            redoAction = QAction("Redo", self)
            redoAction.triggered.connect(self.workspace.redo)
            editMenu.addAction(redoAction)
            
            cutAction = QAction("Cut", self)
            cutAction.triggered.connect(self.workspace.cut)
            editMenu.addAction(cutAction)
            
            copyAction = QAction("Copy", self)
            copyAction.triggered.connect(self.workspace.copy)
            editMenu.addAction(copyAction)
            
            pasteAction = QAction("Paste", self)
            pasteAction.triggered.connect(self.workspace.paste)
            editMenu.addAction(pasteAction)
            
            #begin formatting options + menu
            
            self.makeBold = QAction("Bold", self)
            self.makeBold.setShortcut(QKeySequence.Bold)
            self.makeBold.setCheckable(True)
            self.makeBold.toggled.connect(lambda x: self.workspace.setFontWeight(QFont.Bold if x else QFont.Normal))
            
            self.makeIta = QAction("Italic", self)
            self.makeIta.setShortcut(QKeySequence.Italic)
            self.makeIta.setCheckable(True)
            self.makeIta.toggled.connect(self.workspace.setFontItalic)
            
            self.makeUL = QAction("Underline", self)
            self.makeUL.setShortcut(QKeySequence.Underline)
            self.makeUL.setCheckable(True)
            self.makeUL.toggled.connect(self.workspace.setFontUnderline)
            
            formatMenu = QToolBar("Format")
            formatMenu = self.menuBar().addMenu("&Format")
            formatMenu.addAction(self.makeBold)
            formatMenu.addAction(self.makeIta)
            formatMenu.addAction(self.makeUL)
            
            #begin the chapter toolbar
            chapterMenu = QToolBar("Chapters")
            chapterMenu = self.menuBar().addMenu("&Chapters")
            newAction = QAction("New chapter", self)
            newAction.triggered.connect(self.newChapter)
            chapterMenu.addAction(newAction)
            
            #begin the section for laying out docs
            self.casWindows = QAction("Cascading", self)
            self.casWindows.triggered.connect(self.mdiLayout.cascadeSubWindows)
            
            self.tileWindows = QAction("Tiled", self)
            self.tileWindows.triggered.connect(self.mdiLayout.tileSubWindows)
            
            layoutMenu = QToolBar("Layout")
            layoutMenu = self.menuBar().addMenu("&Layout")
            layoutMenu.addAction(self.casWindows)
            layoutMenu.addAction(self.tileWindows)
            
            #begin font section
            
            fontToolbar = QToolBar("Font Choices")
            self.addToolBar(fontToolbar)
            self.fonts = QFontComboBox()
            self.fonts.currentFontChanged.connect(self.workspace.setFont)
            fontToolbar.addWidget(self.fonts)
            
            self.fontsize = QComboBox()
            self.fontsize.addItems(["14", "18", "24"])
            self.fontsize.currentIndexChanged[str].connect(lambda s: self.workspace.setFontPointSize(float(s)) )
            fontToolbar.addWidget(self.fontsize)
            
            self.show()
     
            
        
    
    
        def resetTabs(self):
            for i in fileAtts.writerTabs:
                fileAtts.writerTabs[i].setParent(None)
            for i in fileAtts.chapterList:
                fileAtts.writerTabs[i] = workTab(fileAtts.chapterNames[fileAtts.chapterList[i]])
                tabRow = i - 1
                self.workTabs.addWidget(fileAtts.writerTabs[i],tabRow,0)
                fileAtts.writerTabs[i].clicked.connect(partial(self.updateActiveWindow, fileAtts.chapterNames[fileAtts.chapterList[i]]))
                
                print("resetting")
                
                self.resetting.emit()
                
    
        
        def closeEvent(self, event):
            if fileAtts.isEdited:
                event.ignore()
                self.savePopup("closeAttempt")
    
        
        def checkWindowActive(self):
            currentlyOpen = 0
            for currentlyOpen in fileAtts.openWindows:
                if fileAtts.openWindows[currentlyOpen] == self.mdiLayout.activeSubWindow():
                    print(fileAtts.openWindows[currentlyOpen])
                    print(currentlyOpen)
                    break
            return currentlyOpen
                
        def goHereToSaveFirst(self, endResult):
            if endResult == "saveThenLoad":
                self.saveThenLoad()
            if endResult == "newProject":
                self.saveFile()
                fileAtts.isNew = True
                fileAtts.projectSet = False
                while fileAtts.projectSet == False:
                    print("here?")
                    doStart()
                self.mdiLayout.closeAllSubWindows()
                self.newChapter()
            elif endResult == "closeAttempt":
                self.saveFile()
                sys.exit()
                    #return True 
                
        def goHereToContinue(self, endResult):
            if endResult == "saveThenLoad":
                self.openFile()
            if endResult == "newProject":
                fileAtts.isEdited = False #set here to tell newChapter not to prompt again
                fileAtts.isNew = True
                fileAtts.projectSet = False
                while fileAtts.projectSet == False:
                    self.doStart()
                self.mdiLayout.show()
                self.newChapter()
            if endResult == "closeAttempt":
                fileAtts.isEdited = False
                sys.exit()
                
        def savePopup(self, source):
            saveAsk = QDialog()
            layout  = QGridLayout()
            layout.setColumnStretch(1,3)
            yesSave = QPushButton("Yes, save", saveAsk)
            #yesSave.move(10,50)
            noSave = QPushButton("No, do not save", saveAsk)
            #noSave.move(210,50)
            nevermindSave = QPushButton("Cancel", saveAsk)
            #nevermindSave.move(110,50)
            yesSave.clicked.connect(lambda: main.osmosisWriter.goHereToSaveFirst(self, source))
            yesSave.clicked.connect(saveAsk.close)
            noSave.clicked.connect(lambda: main.osmosisWriter.goHereToContinue(self, source))
            noSave.clicked.connect(saveAsk.close)
            nevermindSave.clicked.connect(saveAsk.close)
            saveAsk.setWindowTitle("Save your work?")
            saveAsk.setWindowModality(Qt.ApplicationModal)
            
            saveAsk.setLayout(layout)
            layout.addWidget(yesSave,0,0)
            layout.addWidget(noSave,0,1)
            layout.addWidget(nevermindSave,0,2)
            saveAsk.exec()
            
            def keyPressEvent(self, *args, **kwargs):
                if fileAtts.isEdited == False: #prevents isEdited from being changed when already true
                    fileAtts.isEdited = True
                return QTextEdit.keyPressEvent(self, *args, **kwargs)
        
        def newProject(self):
            print("new project")
            self.savePopup("newProject")
        
        def newChapter(self):
            fileAtts.windowCount = fileAtts.windowCount + 1
            count = fileAtts.windowCount
            print("gonna")
            titleGiver() #get the chapter title
            fileAtts.chapterList[count] = fileAtts.chapterPath[count] #chapters with corresponding urls by the order they were created, to be reordered by the user
            fileAtts.chapterNames[fileAtts.chapterList[count]] = str(fileAtts.partName) ##chapterlist refers to the number of each chapter, while chapter name is the user given title
            print(fileAtts.partName)
            fileAtts.openCorrelation[count] = fileAtts.chapterList[count] #they start out the same but chapterList changes with user input
            print(fileAtts.openCorrelation)
            fileAtts.openWriters[count] = workspaceTemplate()
            fileAtts.openWindows[fileAtts.partName] = QMdiSubWindow()
            fileAtts.openWindows[fileAtts.partName].setWidget(fileAtts.openWriters[count])
        
            self.mdiLayout.addSubWindow(fileAtts.openWindows[fileAtts.partName])
            
            fileAtts.openWindows[fileAtts.partName].setWindowTitle(fileAtts.partDescription)
            fileAtts.writerTabs[count] = workTab(str(fileAtts.partName))
            
            tabRow = count - 1
            self.workTabs.addWidget(fileAtts.writerTabs[count], tabRow, 1)
            
            fileAtts.writerTabs[count].clicked.connect(partial(self.updateActiveWindow, fileAtts.chapterNames[fileAtts.openCorrelation[count]]))
            fileAtts.writerTabs[count].rearranged.connect(self.resetTabs)
            
            #self.mdiLayout.cascadeSubWindows() #later on, set a toggle of if the user wants tile or cascades
            fileAtts.openWindows[fileAtts.partName].show()
            
        def saveThenLoad(self): #The function called when clicking the saveButton
            fileAtts.projectPath, _ = QFileDialog.getSaveFileName(self, "Save file", "", "OSM documents (*.osm)")
            print(fileAtts.projectPath)
            self.openFile()
        
        def saveFileAs(self): #The function called when clicking the saveButton
            fileAtts.projectPath, _ = QFileDialog.getSaveFileName(self, "Save file", "", "OSM documents (*.osm)")
            print(fileAtts.projectPath)
            try:
                with open(fileAtts.projectPath, 'w+') as f:
                    f.write(self.workspace.toHtml())
    
            except Exception as e:
                print("oops, something went wrong")
                self.dialog_critical(str(e))
            fileAtts.isEdited = False
        
        def saveFile(self): #The function called when clicking the saveButton
            try:
                count = 0
                for i in fileAtts.openWriters: #writes down the chapters
                    count = count + 1
                    print(i, ",", count)
                    #fileAtts.chapterPath = fileAtts.chapterFolder +  str(i) + ".osmc"
                    print("checking correlation")
                    #openCorrelation[count] should give you the path that correlates with that writer. To check:
                    print(fileAtts.openCorrelation[count])
                    with open(fileAtts.openCorrelation[count], 'w+') as f:
                        print("ready to write from", i)
                        f.write(fileAtts.openWriters[i].toHtml())
            except Exception as e:
                print("oops, something went wrong")
                self.dialog_critical(str(e))
                
            with open(fileAtts.projectPath, 'w+') as f: #writing the chapter list in the main OSM file
                for i in fileAtts.chapterList:
                    if i == 1: #if this is the first of the for loop iterations
                        self.projectString = fileAtts.chapterList[i]
                    else:
                        self.projectString = self.projectString + "<***ChapterBreak***>" + fileAtts.chapterList[i]
                    print("proj", self.projectString)
                print("ready to write", fileAtts.chapterList)
                f.write(self.projectString)
            fileAtts.isEdited = False
            print(fileAtts.projectPath)
            self.projectString = ""
            x = 0
    
    
        def openFile(self): 
            fileAtts.projectPath, _ = QFileDialog.getOpenFileName(self, "Open file", "", "OSM documents (*.osm)")
            currentPath = fileAtts.projectPath
            projectPathList = currentPath.split("/")
            projectFullName = projectPathList[-1]
            print(projectFullName)
            try:
                projectName = re.search('(.+?)\.osm', projectFullName).group(1)
            except:
                projectName = "oops, no project name..."
            #for i in self.openWriters:
            #    print(i)
            try:
                with open(fileAtts.projectPath, 'r') as f:
                    
                    fileAtts.isEdited = False #newly opened files have not been edited
                    fileAtts.isNew = False
                    print("about to split")
                    #fileAtts.openWriters[1] = workspaceTemplate()
                    chapterRaw = f.read()
                    print(chapterRaw)
                    chapterListMaker = list()
                    chapterListMaker = chapterRaw.split("<***ChapterBreak***>")
                    x = 0
                    for i in chapterListMaker:
                        x = x + 1
                        fileAtts.chapterList[x] =  i
                        print("printing i", i)
                    print(fileAtts.chapterList)
                    for i in chapterListMaker:
                        fileAtts.windowCount = fileAtts.windowCount + 1
                        current = fileAtts.windowCount
                        fileAtts.chapterPath[current] = i
                        print("the chapter path is", i)
                        chapterPathList = i.split("/")
                        chapterFullName = chapterPathList[-1]
                        print(chapterFullName)
                        print("Chapter folder")
                        del chapterPathList[-1]
                        fileAtts.chapterFolder = "/".join(chapterPathList) + "/"
                        
                        print(fileAtts.chapterFolder)
                        
                        try:
                            chapterName = re.search('(.+?)\.osm', chapterFullName).group(1)
                        except:
                            chapterName = "unnamed"
                        fileAtts.fileRequest.append(fileAtts.windowCount) #what is this for and can it leave
                        fileAtts.openCorrelation[fileAtts.windowCount] = i
                        fileAtts.chapterNames[i] = chapterName #to get the correlated text with this later, ask for fileAtts.chapterNames[openCorrelation[fileAtts.windowCount]]
                        #which along with fileAtts.openWriters[fileAtts.windowCount] will get you the correct chapter and text for the requisite window
                        
                        #writerPath = str(currentPath) + str(current)
                        
                        with open(i) as f:
                            contents = f.read()
                        
                        fileAtts.openWriters[current] = workspaceTemplate()
                    
                        fileAtts.openWindows[chapterName] = QMdiSubWindow()
                        
                        fileAtts.openWindows[chapterName].setWidget(fileAtts.openWriters[current])
                        print("are we in")
                        self.mdiLayout.addSubWindow(fileAtts.openWindows[chapterName])
                        self.mdiLayout.cascadeSubWindows() #later on, set a toggle of if the user wants tile or cascades
                        fileAtts.openWindows[chapterName].show()
                        
                        fileAtts.openWindows[chapterName].setWindowTitle(chapterName)
                        
                        fileAtts.openWriters[current].setHtml(contents)
                        
                        print("CURRENTLY", current)
                        
                        fileAtts.writerTabs[current] = workTab(chapterName)
                        
    
                        fileAtts.writerTabs[current].clicked.connect(partial(self.updateActiveWindow, fileAtts.chapterNames[fileAtts.openCorrelation[current]]))
                        
                        
                        fileAtts.writerTabs[current].rearranged.connect(self.resetTabs)
                        tabRow = current - 1
                        self.workTabs.addWidget(fileAtts.writerTabs[current], tabRow, 1)
                        
            #tabName = fileAtts.writerTabs[currentCount]
                        print("printing correlation")
                        print(fileAtts.openWindows)
                        print("writers")
                        print(fileAtts.openWriters)
                        print(fileAtts.writerTabs)
                        
                        print("Still", fileAtts.windowCount)
                        #when a button of a certain count is pressed, grabs the count number of that button and sends to a method
                        print("just set to", current)
                        print(fileAtts.writerTabs)
                        
                self.checkWindowActive()
                    
            except Exception as e:
                print("oops, something went wrong")
                
            self.updateWindowTitle()
            
        def exportFile(self):
            print("preparing to export")
            self.saveFile()
            chapterNamesForExport = list()
            try:
                with open(fileAtts.projectPath, 'r') as f:
                    chapterRaw = f.read()
                print(chapterRaw)
                chapterListMaker = list()
                chapterListMaker = chapterRaw.split("<***ChapterBreak***>")
                x = 0
                y = 0
                z = 0 
                for i in chapterListMaker:
                    x = x + 1
                    fileAtts.chapterList[x] =  i
                    print("printing i", i)
                for i in chapterListMaker:
                    z = z + 1 #tabbing through windows
                    print(z)
                    writingFrom = fileAtts.chapterList[z]
                    print("we are writing from", writingFrom)
                    writingFromList = writingFrom.split("/")
                    chapterFullName = writingFromList[-1]
                    print(chapterFullName)
                    try:
                        chapterName = re.search('(.+?)\.osm', chapterFullName).group(1)
                    except:
                        chapterName = "unnamed"
                    
                    chapterTitleHTML = "<p><h2>" + chapterName + "</h2><p>"
                    chapterNamesForExport.append(chapterTitleHTML)
                    print(chapterNamesForExport)
                
                exportPath, _ = QFileDialog.getSaveFileName(self, "Save file", "", "")
                docPath = Path(exportPath + ".doc")
                print("exporting to", exportPath)
                with open(exportPath, 'a+') as f:
                    for i in chapterListMaker:
                        print("printing chapter #", i)
                        f.write(chapterNamesForExport[y])
                        y = y + 1
                        print("name printed")
                        writingFrom = fileAtts.chapterList[y]
                        print("we are writing from", writingFrom)
                        writingFromList = writingFrom.split("/")
                        chapterFullName = writingFromList[-1]
                        print(chapterFullName)
                        try:
                            chapterName = re.search('(.+?)\.osm', chapterFullName).group(1)
                        except:
                            chapterName = "unnamed"
                        chapterID = list(fileAtts.openCorrelation.keys())[list(fileAtts.openCorrelation.values()).index(fileAtts.chapterList[y])]
                        #chapterID = list(fileAtts.chapterPath.keys())[list(fileAtts.chapterPath.values()).index(localeOfSource)]
                        print(chapterID)
                        print(fileAtts.openCorrelation)
                        print(fileAtts.openWindows)
                        print(fileAtts.openWriters)
                        f.write(fileAtts.openWriters[chapterID].toHtml())
                
                docParser = HtmlToDocx()
                docParser.parse_html_file(exportPath, docPath)
                print(docPath)
                
                       
                print("exported")
            except:
                print("oops, couldn't export")
            
            if os.path.exists(str(exportPath)):
                print("removal")
                os.remove(str(exportPath))
        def saveCheck(self): #asks if you want to save. Differs from loadCheck in that this one is a user choice prompt, but loadCheck checks if changes have been made
            #def saveAndLoad():
            self.savePopup()
            
        def loadCheck(self): #check if saving is necessary when asked to load a new file, and if not, load new file
            if fileAtts.isEdited == True:  #if you've started writing (made keystrokes), eg have work to save
                self.savePopup("saveThenLoad")
                
                '''
                if self.savePopup.cancelPopup == False and self.savePopup.buttonPressed == True:
                    self.openFile()
                '''
            elif fileAtts.isEdited == False:
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
            print(type(windowName))
            print("pressed", str(windowName))
            print(windowName)
            self.mdiLayout.setActiveSubWindow(fileAtts.openWindows[windowName])
                    
            
                
      
    app = QApplication(sys.argv)
    app.setApplicationName("Osmosis Writer")
            
    window = osmosisWriter()
    window.show()
    app.exec_() 
if __name__ == '__main__':       
    main()
    