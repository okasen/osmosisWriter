
import os
from os import listdir
from os.path import isfile, join, expanduser

class fileAttributes:
    def __init__(self):
        #TODO: review these vars and ensure they're all still needed
        self.isNew = True #defines if we're loading a file or starting new
        self.isEdited = False #no file is edited before it is started!
        self.projectPath = ""
        self.projectTitle = "untitled"
        self.projectSet = False
        self.chapterFolder = ""
        self.saveLocale = os.path.expanduser('~')
        self.projectFolder = ""
        self.contents = "test"
        self.curChapterPath = ""
        self.windowCount = 0
        self.openWindows = dict() #the windows that hold writers, in the order they were created
        self.openWidgets = dict() #holds the widgets that hold the layouts....
        self.openLayouts = dict() #hold the layouts in each window that hold the writers"
        self.openLabels = dict()
        self.openCorrelation = dict() #just ensures that the keys in openWindows correlate to the correct keys in openWriters, and therefor, that the values are correct
        self.openWriters = dict() #used to hold the actual writers that correspond to writer windows, correlated to an int
        self.writerTabs = dict() #used to hold the actual tabs that correspond to writer windows, correlated to an int
        self.chapterList = dict() #holds the chapter paths in order of how the user has organised them, and is used to create the main OSM file's structure
        self.partName = "" #changes to hold the most recently added part's name
        self.partDescription = "" #holds the part name with any special chars or spaces
        self.chapterNames = dict() #chapter's path :: chapter's name, will not change with user input
        self.chapterPath = dict() #chapter's path linked to a number that correlates with the name, to ensure chapters do not become mislabeled or lost

        self.chapterNameValid = False
        self.themeChoice = ""
