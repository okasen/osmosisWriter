Osmosis Writer ALPHA 1.0.1 README:

Osmosis Writer is software for writing fiction novels chapter by chapter. 
It is licensed under the GNU GPL3 and created by Jennifer Black, AKA @JenniLBlack on Twitter, Okasen on Github, and OkasenLun on Reddit.

Software is presented As-Is and offers no warranty.

Currently, it contains the following features:
-create a new project (from start screen): Prompts for a project name and creates a folder with that name in your chosen directory. Also creates a .OSM file in that folder.
--you are then prompted to create your first chapter, which requires inputting a chapter name.

-load an existing project (from start screen): Prompts the user to pick a .OSM file from their computer, and load the chapters of that file.

-create new chapters from the "chapter" drop down menu (new in 1.0.1: from a toolbar button). This adds a tab to the work tabs on the left hand side.

-reorder chapters by drag and drop: Users may drag and drop their chapters to change the chronological order in which they appear in any exported documents

-save your work: You can save your OSM file and any related OSMc files. All files are saved at the same time; scene-by-scene saving will be implemented later.

-themes: You may set your UI to one of two themes on start and while the program is running. One theme is meant to be dyslexia friendly.

-deleting: you may delete chapters from the dropdown menu or from the toolbar button

-exporting: You may export to a docx file.

NEW IN ALPHA 1.0.1:

-new chapter button
-delete chapter button
-SO MANY bug fixes. So many.
-chapter recovery: If your program crashes after making a chapter but before saving, it will recover the chapter files (sort of)
-the chapter tabs now scroll, and the writer windows loop better now

KNOWN BUGS:

"Save as" can be unpredictable and requires more testing.
Sometimes files seem to be saved outside the chapters directory, where they belong.

BUGS FIXED IN ALPHA 1.0.1

Opening corrupted projects shouldn't crash the program anymore.
loading an empty project only to start a new one will allow you to save without crashing
save as can be cancelled now
you aren't forced to pick a directory or name for a new project if you accidentally request to make one
fixed an issue with openFile not clearing the screen of the last project. Maybe.
Fixed font family choices resetting the text to itty bitty size.
made the chapter deleter delete the last chapter if none are selected (instead of crashing)
fixed "ghost chapters" preventing you from making new chapters of ones that didn't save
fixed the prompt about "this chapter already exists". Now it actually prevents said duplication
fixed projectPath not updating after a second load
fixed an issue with the chapter tabs not liking deleting the ultimate chapter
fixed a "no project found to export" bug
fixed a bug that popped up after fixing all of this, where you couldn't save after deleting final chapters

ABOUT THE FILE TYPES:
.OSM is the project file. It holds the locations of your chapters on your computer. 
-- If you find that a chapter has gone missing, you can open yourproject.OSM to see where the software is looking for that chapter (and edit the path if necessary)

.OSMc is chapter files. These files hold HTML containing the words you wrote and any formatting.

.doc is, of course, a word document file.
--A .doc from Osmosis Writer will be formatted with the current chapter names as headers and the contents listed below each chapter. No page breaks yet!

.html holds the raw formatting of your file. Should work with bolded/italicized/etc. text, as well as font choices (size and family)



