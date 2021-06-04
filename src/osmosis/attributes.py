import os
from os import listdir
from os.path import isfile, join, expanduser
from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re


import logging
#Let's be real, these were always global variables.
#Making them more obvious so it's more pressing to
#implement them properly

isNew = True #defines if we're loading a file or starting new
isEdited = False #no file is edited before it is started!
saveLocale = os.path.expanduser('~')
contents = "test"
curChapterPath = ""
windowCount = 0
openWindows = dict() #the windows that hold writers, in the order they were created
openWidgets = dict() #holds the widgets that hold the layouts....
openLayouts = dict() #hold the layouts in each window that hold the writers"
openLabels = dict()
openCorrelation = dict() #just ensures that the keys in openWindows correlate to the correct keys in openWriters, and therefor, that the values are correct
openWriters = dict() #used to hold the actual writers that correspond to writer windows, correlated to an int
writerTabs = dict() #used to hold the actual tabs that correspond to writer windows, correlated to an int
chapterList = dict() #holds the chapter paths in order of how the user has organised them, and is used to create the main OSM file's structure
partDescription = "" #holds the part name with any special chars or spaces
chapterNames = dict() #chapter's path :: chapter's name, will not change with user input
chapterPath = dict() #chapter's path linked to a number that correlates with the name, to ensure chapters do not become mislabeled or lost

chapterNameValid = False
themeChoice = ""



class Project:
    set = False
    folder = "nofolder"
    path = "none"
    chapterFolder = projectFolder + "/chapters/"
    title = "untitled"

CurrentProject = Project()

class ProjectStarterLogic():

    def makeNew():
        CurrentProject = Project()
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        saveLocale = dialog.getExistingDirectory()
        CurrentProject.folder = saveLocale + "/" + CurrentProject.title + "/"
        CurrentProject.chapterFolder = CurrentProject.folder + "/chapters/"
        if os.path.exists(CurrentProject.folder):
            logging.info("This project " + CurrentProject.folder +" already exists in this directory. Open the existing project, or create something new?")
            errorNote = QMessageBox()
            errorNote.setWindowTitle("Error")
            errorNote.setText("A project with this title" + CurrentProject.folder + "already exists in this folder. Please enter a new title or select a different folder.")
            errorNote.setStandardButtons(QMessageBox.Ok)
            errorNote.exec()
        else:
            os.mkdir(CurrentProject.folder)
            CurrentProject.path = CurrentProject.folder + "/" + CurrentProject.title + ".osm"
            CurrentProject.set = True
            with open(CurrentProject.path, 'w+') as f: #creating the main OSM file
                f.write("")
            os.mkdir(CurrentProject.chapterFolder)
            print("chapter folder made")




class ProjectMakerGUI(QDialog):

    def __init__(self, *args, **kwargs):
        super(ProjectMakerGUI, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setGeometry(QRect(200,200,400,200))
        self.setLayout(layout)
        self.isModal()
        self.projectNamer = QLineEdit()
        self.projectNamer.setPlaceholderText("enter your project title here")
        button = QPushButton("confirm title and choose project folder")
        button.setEnabled(False)
        cancel = QPushButton("cancel")

        def buttonToggle():
            button.setEnabled(True)

        def cancelPrompt():
            logging.info("Oops! No new project created.")

        def cleanTitle():
            CurrentProject.title = re.sub('[^A-Za-z0-9 ]+', '', self.projectNamer.text())

        self.projectNamer.textChanged.connect(buttonToggle)

        layout.addWidget(self.projectNamer)
        layout.addWidget(button)
        layout.addWidget(cancel)

        button.clicked.connect(cleanTitle)
        button.clicked.connect(ProjectStarterLogic.makeNew)
        button.clicked.connect(self.accept)

        cancel.clicked.connect(cancelPrompt)
        cancel.clicked.connect(self.reject)

        self.exec()
