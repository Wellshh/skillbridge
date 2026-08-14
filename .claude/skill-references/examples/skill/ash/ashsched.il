;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ; file.cc --
 ;
 ; Author --
 ;	Cadence Design Systems
 ;
 ; Function --
 ;	
 ; Copyright, 1993, Cadence Design Systems, Inc.
 ; No part of this file may be reproduced, stored in a retrieval system,
 ; or transmitted in any form or by any means --- electronic, mechanical,
 ; photocopying, recording, or otherwise --- without prior written permission
 ; of Cadence Design Systems, Inc.
 ;
 ; WARRANTY:
 ; NONE. NONE. NONE.
 ; Use all material in this code at your own risk.  Cadence Design Systems 
 ; makes no claims about any material in this archive.  These examples may
 ; not function or may only function in specific instances. We'd like to hear 
 ; what you think of our approach to this, and how we can improve it.
 ;
 ; RESTRICTIONS:
 ; All software contained within this archive is in the public domain or
 ; the author has given us permission for redistribution.  Some packages
 ; have explicit copyrights and notices concerning their redistribution.
 ; Please carefully read all documentation with any package on this tape.
 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



/* $Header: $*/
/*******************************************************************
 * ashsched.il
 *	Copyright 1993 Cadence Design Systems
 * Interactive command to schedule nets
 *	Don Morgan - 7/30/93
 *******************************************************************/

; Find filter setup for selecting a net

(defun initPinSelection ()
    (axlSetFindFilter ?enabled '("NOALL" "NETS" "PINS" "EQUIVLOGIC")
		      ?onButtons "All")
    (axlClearSelSet))


; Get a pick that results in a selection of a net.  Loop until the user picks to
; select or cancels.
; returns a point that results in a net selection

(defun _getNetPinPick ()
    (let (point (selectionDone nil))
	(initPinSelection)
	(while (null selectionDone)
	    (setq point (axlEnterPoint
	       ?prompts '("Pick to select a net pin.")
	       ?gridSnap nil))
	    (cond
		((null point) 
		    (setq selectionDone t))
		((null (axlSingleSelectPoint point))
		    (axlShell "echo No Net Pins Found at Pick."))
		(t (setq selectionDone t))))
	point))


; Write data for pins from ordered pin list to netin file.
; Recursive procedure processes car of list and calls itself with cdr.

(defun _writePinData (netinFile orderedPinList)
    (cond
	((null orderedPinList))
	((listp (car orderedPinList))
	    (_writePinData netinFile (car orderedPinList))
	    (_writePinData netinFile (cdr orderedPinList)))
	(t
	    (fprintf netinFile ",\n%s.%s" 
			       (car orderedPinList)->parent->refdes 
			       (car orderedPinList)->number)
	    (_writePinData netinFile (cdr orderedPinList)))))


; Write out netin file $SCHEDULE data for net schedule.  
; return name of netin file.

(defun _writeNetinFile (netName orderedPinList "tl")
    (let (netinFile (netinFileName "tmp_net_list_file.txt"))
	(cond
	    ((or (null orderedPinList) (null (car orderedPinList)))
		nil)
	    ((null (setq netinFile (outfile netinFileName)))
		(printf "Could not open netin file %s\n" netinFileName)
		nil)
	    (t
		(fprintf netinFile "$NETS\n")
		(fprintf netinFile "$SCHEDULE\n")
		(fprintf netinFile "%s ; " netName)
		(foreach subList orderedPinList
		    (_writePinData netinFile subList)
		    (fprintf netinFile " ;"))
		(fprintf netinFile "\n$END\n")
		(close netinFile)
		netinFileName))))

; Create a script which is replayed to process the netin $SCHEDULE file.
; Script will open netin param form and set data so netin will use our file.
; Then netin is executed to update the net's schedule.
; A script is used so the invisible form scriptmode will work.

(defun _createNetinScript (netinFile "t")
    (let (scriptFile (scriptFileName "tmp_netin.scr"))
	(cond
	    ((null (setq scriptFile (outfile scriptFileName)))
		(printf "Could not open netin script file %s\n" scriptFileName)
		nil)
	    (t 
		(fprintf scriptFile "setwindow pcb\n")
		(fprintf scriptFile "scriptmode +invisible\n")
		(fprintf scriptFile "scriptmode +noinfo\n")
		(fprintf scriptFile "netin param\n")
		(fprintf scriptFile "setwindow form.niparams\n")
		(fprintf scriptFile "FORM niparams filename %s\n" netinFile)
		(fprintf scriptFile "FORM niparams save_drawing NO\n")
		(fprintf scriptFile "FORM niparams syntax_check_only NO\n")
		(fprintf scriptFile "FORM niparams supercede NO\n")
		(fprintf scriptFile "FORM niparams append_device_log NO\n")
		(fprintf scriptFile "FORM niparams remove_etch NO\n")
		(fprintf scriptFile "FORM niparams place_never YES\n")
		(fprintf scriptFile "FORM niparams Done\n")
		(fprintf scriptFile "setwindow pcb\n")
		(fprintf scriptFile "netin execute\n")
		(fprintf scriptFile "scriptmode -invisible")
		(fprintf scriptFile "scriptmode -noinfo")
		(fprintf scriptFile "setwindow pcb\n")
		(close scriptFile)
		scriptFileName))))


; Update the schedule for net "netName" given an ordered pin list.
;  Create netin input file.
;  Create script to setup and run netin (use script for invisible forms).
;  Replay script.
;  Delete both files.

(defun _updateNetSched (netName orderedPinList "tl")
    (let (netinFile netinScript)
	(cond
	    ((null (setq netinFile (_writeNetinFile netName orderedPinList))))
	    ((null (setq netinScript (_createNetinScript netinFile))))
	    (t
		(axlShell (buildString (list "echo Updating Schedule for net \""
					     netName
					     "\".")
				       ""))
		(axlShell (buildString (list "replay" netinScript) " "))
		(deleteFile netinFile)
		(deleteFile netinScript)
		t))))


; Figure out which pin was just deselected.  This is the next pin which is
; to be added to the ordered pin list.
; Tests the previous pins selected list against the currenly selected pins by
; testing each item of the previous list against the current list.
; Returns the first pin that is in the old list and not in the new list.
; Uses recursion to process the old list,   testing the car of the list for
; being a member of the new list.  If the car pin is a member,  calls itself
; with the cdr of the old list so the next pin can be tested.

(defun _getLastPin (lastPinList curPinList "ll")
    (cond
	((null lastPinList)
	    nil)
	((null curPinList)
	    (car lastPinList))
	((member (car lastPinList) curPinList)
	    (_getLastPin (cdr lastPinList) curPinList))
	(t (car lastPinList))))



; Set up rubberbanding from cursor to all pins left to be scheduled.  Also
; rubberbands to last pin selected so user has an idea of where he came from.

(defun _setRbandDynamics (curPin otherPinList)
    (when curPin
	(axlAddSimpleRbandDynamics curPin->xy "directline" ?origin curPin->xy)
	(foreach pin otherPinList
	    (axlAddSimpleRbandDynamics pin->xy "directline" ?origin pin->xy))))

; Set up fixed line between pins already selected.

(defun _setSelectedPinPath (pinList lastPin)
    (cond
	((null pinList))
	((null (car pinList)))
	((listp (car pinList))
	    (_setSelectedPinPath (car pinList) nil)
	    (_setSelectedPinPath (cdr pinList) nil))
	((null lastPin)
	    (_setSelectedPinPath (cdr pinList) (car pinList)))
	(t
	    (axlAddSimpleRbandDynamics lastPin->xy 
				       "fixedline" 
				       ?origin (car pinList)->xy)
	    (_setSelectedPinPath (cdr pinList) (car pinList)))))


; Find a pin that has not been added to the ordered pin list yet.
; These pins are still selected and therefore are found with axlSubSelectPoint.
; Return a list of new pins and old pins with new pin being first.

(defun _findNewPin (point curPinList "l")
    (let (newPinList lastPin)
	(cond
	    ((null (axlSubSelectPoint point))
		nil)
	    (t
		(setq newPinList (axlGetSelSet))
		(setq lastPin (_getLastPin curPinList newPinList))
		(cond
		    (lastPin
			(cons lastPin newPinList))
		    (t nil))))))
; Get the pin in the new list that did not exist in the old list.
; Return that pin.

(defun _getNewPin (lastPinList curSelSet)
    (cond
	((null curSelSet)
	    nil)
	((null lastPinList)
	    (car curSelSet))
	((member (car curSelSet) lastPinList)
	    (_getNewPin lastPinList (cdr curSelSet)))
	(t
	    (car curSelSet))))


; Find a pin that has already been added to the ordered pin list.
; Use axlAddSelectPoint to find it.
; Use _getNewPin to determine which pin is new in the sel set.
; Return the new pin.

(defun _findOldPin (point curPinList allPinList "ll")
    (let (newPin)
	(cond
	    ((null (axlAddSelectPoint point))
	        nil)
	    ((null (setq newPin (_getNewPin curPinList (axlGetSelSet))))
	        (axlShell "echo _findOldPin selection error."))
	    (t
		(axlSubSelectObject newPin)
		(cond
		    ((null (member newPin allPinList))
			(setq newPin nil))
		    (t 
			(axlFlushDisplay)
			(axlHighlightObject newPin)))
	        newPin))))


; Create an ordered list of pins on selected net.
; Starts with a pin list an a first point.  The first point is used to find 
; the start pin (if the user picked close to a pin on the net.
; At first all pins on the net are selected (and appear to be highlighted).
; Each user pick is used to deselect a pin.  We figure out which pin was
; deselected and add it to the ordered pin list.  Since only pins on this
; net are selected,  we are guaranteed that we will only deselect pins on this
; net.  When there is only one pin left,  add it to the end of the ordered list.
; Uses tconc list for efficiency in appending to the list.

(defun _getOrderedPinList (netName pinList point "tll")
    (let (pickPrompt curPinList curPin newPin 
	 (compositePinList nil) (orderedPinList nil))

	(setq curPinList (copy pinList))
	(setq pickPrompt (buildString (list "Pick to select pin on net \""
					    netName
					    "\".")
				      ""))
	(axlSetFindFilter ?enabled "NONETS")

	(while curPinList
	    (when (null point)
		(axlClearDynamics)
		(_setRbandDynamics curPin curPinList)
		(_setSelectedPinPath (car compositePinList) nil)
		(_setSelectedPinPath (car orderedPinList) nil)
		(setq point (axlEnterPoint ?prompts (list pickPrompt))))

	    (cond
		((null point)
		    (setq orderedPinList nil)
		    (setq compositePinList nil)
		    (setq curPinList nil))
		((null (setq tmpPinList (_findNewPin point curPinList)))
		    (cond
			((setq newPin (_findOldPin point curPinList pinList))
			    (axlHighlightObject newPin)
			    (when (neq newPin curPin)
				(setq compositePinList 
				      (tconc compositePinList
					     (car orderedPinList)))
				(setq orderedPinList (tconc nil newPin))))
			(t
			    (axlShell "echo No Net Pins Found at Pick.")
			    (setq newPin curPin))))
		((null (setq newPin (car tmpPinList)))
		    (setq orderedPinList nil)
		    (setq compositePinList nil)
		    (setq curPinList nil)
		    (axlShell "echo ERROR in _findNewPin."))
		(t
		    (setq orderedPinList (tconc orderedPinList newPin))
		    (axlHighlightObject newPin)
		    (setq curPinList (cdr tmpPinList))))
	    (setq point nil)
	    (setq curPin newPin))

	(axlClearDynamics)
	(axlClearSelSet)
	(axlDehighlightObject pinList)
	(when orderedPinList
	   (setq compositePinList (tconc compositePinList 
					 (car orderedPinList))))
	(car compositePinList)))


; Get the net name.  This is a work around since v8m4 does not support access
; of the net from a pin.  Returns the net name string.

(defun _getNetName (pinList "l")
    (let (net netName)
	(cond
	    ((null pinList) nil)
	    ((null (setq net (car pinList)->net)) nil)
	    ((null (setq netName net->name)) nil)
	    ((equal netName "") nil)
	    (t 
		netName))))


; Main scheduling procedure for net scheduling called through skill evaluation.
; This command loops until the user cancels,  doing the following:
;	Get a pick which selects a net.
;	Get the name of the net.  Must not be "" or go back to get a new net.
;	Use the pick to reselect all of the pins on the net.
;	Create ordered list of picks by allowing user to interactively
;	    deselect pins in the order that they are to be scheduled.
;	Use ordered list to generate netin input file to update the net schedule.

(defun _ashDoNetSched ()
    (let ((schedDone nil) point netName pinList orderedPinList oldPopup popupId)
	(axlClearDynamics)
	(setq popupId (axlUIPopupDefine nil '(("Cancel" axlFinishEnterFun))))
	(setq oldPopup (axlUIPopupSet popupId))

	(while (null schedDone)
	    ; Workaround: popup gets cleared when we do axlShell interactive
	    ;  command (netin execute).  So reset it each time.
	    (axlUIPopupSet popupId)
	    (cond
	    	((null (setq point (_getNetPinPick)))
		    (setq schedDone t))

		((or (null (setq pinList (axlGetSelSet)))
		    (null (setq netName (_getNetName pinList))))
		    (axlShell "echo Please select pin which is on a net."))

		((null (setq orderedPinList (_getOrderedPinList netName 
								pinList 
								point)))
		    (setq schedDone t))

		((null (_updateNetSched netName orderedPinList))
		    (setq schedDone t))

		(t)))

	(axlUIPopupSet oldPopup)))


(setq netSchedActive nil)

(defun ashNetSched ()
"Interactive command to generate a user defined net schedule."
    (cond
	((and (null netSchedActive) (axlOKToProceed))
	    (setq netSchedActive t)
	    (errset (_ashDoNetSched) t)
	    (setq netSchedActive nil)
	    t)
	(t nil)))

; would like this to be interactive,  but it does a netin execute which is
; also interactive.
;(axlCmdRegister "netsched" 'ashNetSched ?cmdType "general")
