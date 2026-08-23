
This directory hierarchy contains documentation and examples for
the Allegro implementation of Skill. 

As of PSD15.1, cdsdoc contains a description of Allegro Skill functions 
(axl) that matches the code. The documentation contained in this 
directory is no longer required but is provided for reference purposes.
It will also be kept in sync with the content of the releases.

For the documenttation directory is structured as follows::
	DOC
		FUNCS - documentation, one text file per "axl" function
		also the list of files starting with "New" contain function
			that are added from release to release
		
There are several directories of example code. Items of interest are

The FAQ directory contains several tips and a document on how to
build Skill contextes. Contextes are a means of packaging your
Skill code to your users for faster loading.

Form (dialog programming) and capabilites:
     form/basic:  demostrates basic capability of the forms package.
		Shows all of the available controls with any options.
		Also shows a basic skill programming model for forms.

     form/grid:	Forms supports a spreadsheet like control (grids). This
		program demostrates its capabilities

     form/wizard: Programming in the Microsoft "Wizard" model. Not as 
		useful

     Also in the cmds directory the cns-design.il and acns_design.form
     show a real world form to Allegro database programming example. This
     is the Allegro Global Constraint Interface.

     To understand how the form user interface package functions it is best 
     to look at the examples shown below. The most import is the basic 
     example.  In any case to use the examples:
         - Copy all of the files from one of the directories to a local
           directory.
         - Start Allegro
         - Change it to the directory with the demoestration files
              "cd <directory>
           on Allegro command line
         - load the Skill file in the directory (it is the one with the
           "il" extension. Example on Allegro command line:
                skill load "<filename>"
        - start demo by typing on Allegro command line
           For basic demo
                skill formtest
           For grid demo
                skill gridtest
        - examine the Skill code and form file

The other directories show programming examples using axl functions.
The cmds, symchk and swap directories have actual Allegro extensions
written in Skill. Many more Skill extensions to Allegro exists at
the following link. Note this requires a sourcelink account.

	http://sourcelink.cadence.com/docs/files/PCB_library.html

