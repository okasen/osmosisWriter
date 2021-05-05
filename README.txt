Osmosis Writer ALPHA 1.0.2 README:

Osmosis Writer is software for writing fiction novels chapter by chapter. 
It is licensed under the GNU GPL3 and created by Jennifer Black, AKA @JenniLBlack on Twitter, Okasen on Github, and OkasenLun on Reddit.

Software is presented As-Is and offers no warranty.

If you are interested in contributing to Osmosis Writer, please read over our contributor code of conduct! If you just want to use Osmosis Writer, you can find the current installer via the releases page. 

Currently, Osmosis Writer contains the following features:
-create a new project (from start screen): Prompts for a project name and creates a folder with that name in your chosen directory. Also creates a .OSM file in that folder.
--you are then prompted to create your first chapter, which requires inputting a chapter name.

-load an existing project (from start screen): Prompts the user to pick a .OSM file from their computer, and load the chapters of that file.

-create new chapters from the "chapter" drop down menu (new in 1.0.1: from a toolbar button). This adds a tab to the work tabs on the left hand side.

-reorder chapters by drag and drop: Users may drag and drop their chapters to change the chronological order in which they appear in any exported documents

-save your work: You can save your OSM file and any related OSMc files. All files are saved at the same time; scene-by-scene saving will be implemented later.

-themes: You may set your UI to one of two themes on start and while the program is running. One theme is meant to be dyslexia friendly.

-deleting: you may delete chapters from the dropdown menu or from the toolbar button

-exporting: You may export to a docx file.

-image support: you can now drag and drop images into osmosis writer and export files with them inside.

NEW IN ALPHA 1.0.2:

-image support: you can now drag and drop images into osmosis writer and export files with them inside.
-program remembers your layout choice per-session. See TO DO for persisting layout choices information.
-bug fixes!
-SaveFileAs works! It does, I swear!

KNOWN BUGS:

...well, I don't /know/ any yet! Does that count?

BUGS FIXED IN ALPHA 1.0.1

(Hopefully) fixed the chapters of previous projects remaining in the sidebar and related saving issues
(Hopefully) solved the issue with small empty boxes appearing around the editor
fixed numerous issues with saving
removed the magic floating cancel button in certain dialogs
removed Herobrine

TODO:
Make a preferences window that appears on startup ONCE and lets you set preferences like layout, font type/size, theme, etc. These settings will persist throughout sessions until told to forget.
-there's a general need to optimize memory usage.

ABOUT THE FILE TYPES:
.OSM is the project file. It holds the locations of your chapters on your computer. 
-- If you find that a chapter has gone missing, you can open yourproject.OSM to see where the software is looking for that chapter (and edit the path if necessary)

.OSMc is chapter files. These files hold HTML containing the words you wrote and any formatting.

.doc is, of course, a word document file.
--A .doc from Osmosis Writer will be formatted with the current chapter names as headers and the contents listed below each chapter. No page breaks yet!

.html holds the raw formatting of your file. Should work with bolded/italicized/etc. text, as well as font choices (size and family)



