Osmosis Writer README:

Osmosis Writer is software for writing fiction novels chapter by chapter. 
It is licensed under the GNU GPL3 and created by Jennifer Black, AKA @JenniLBlack on Twitter, Okasen on Github, and OkasenLun on Reddit.

Currently, it contains the following features:
-create a new project (from start screen): Prompts for a project name and creates a folder with that name in your chosen directory. Also creates a .OSM file in that folder.
--you are then prompted to create your first chapter, which requires inputting a chapter name.

-load an existing project (from start screen): Prompts the user to pick a .OSM file from their computer, and load the chapters of that file.

-create new chapters from the "chapter" drop down menu. This adds a tab to the work tabs on the left hand side.

-reorder chapters by drag and drop: Users may drag and drop their chapters to change the chronological order in which they appear in any exported documents

-save your work: You can save your OSM file and any related OSMc files. All files are saved at the same time; scene-by-scene saving will be implemented later.

NEW IN PREALPHA 1.0.1:

-delete chapters
-shiny new GUI... kinda

KNOWN BUGS:
-If you ask Osmosis Writer to open a project and then cancel the file dialog, the program crashes.

-Choosing to make a new project will force you to either make the new file and folder, or close the program manually. Needs a cancel option.

-Choosing to load a file while one is already open will combine them in the work tabs and workspace.


BUGS FIXED IN PREALPHA 1.0.1

-you can now make a new project when one is open, and it will replace the tabs and writing interface
-fixed the broken formatting. However, formatting will not be applied to export due to... incompatibilities between docx exporter and HTML encoder

ABOUT THE FILE TYPES:
.OSM is the project file. It holds the locations of your chapters on your computer. 
-- If you find that a chapter has gone missing, you can open yourproject.OSM to see where the software is looking for that chapter (and edit the path if necessary)

.OSMc is chapter files. These files hold HTML containing the words you wrote and any formatting.

.doc is, of course, a word document file. It is, as of Pre-Alpha 1.0.1, the only export method possible. 
--A .doc from Osmosis Writer will be formatted with the current chapter names as headers and the contents listed below each chapter. No page breaks yet!



