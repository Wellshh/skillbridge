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



;; tselObjectTest - test selection by DBID
(defun tselObjectTest ()
   (let (testPass findTypes)
	(cond
	    ((null (setq findTypes (tselGetObjectTypes)))
		(printf "tselObjectTest: (tselGetObjectTypes) failed\n"))
	    ((null (apply 'and (mapcar 'tselAllOfObjectDBID findTypes)))
		nil)
	    ((null (tselBadDBIDTest))
		nil)
	    (t (setq testPass t)))

	(axlClearSelSet)
	(tselEchoResults "Selset Object By DBID Test" testPass)))


;; tselAllOfObjectDBID - test all modes of selection bu object DBID
(defun tselAllOfObjectDBID (findType)
    (let (testPass foundItems leftOver newItems)
	(axlClearSelSet)
	(axlSetFindFilter ?enabled (list "NOALL" findType)
			  ?onButtons "ALL")
	(printf "DBID Select test for %L\n" findType)
	(axlFlushDisplay)

	(cond
	    ; find all of item type
	    ((null (axlAddSelectAll))
		(printf "tselAllOfObjectDBID: No \"%s\" to select\n" findType)
		nil)
	    ((null (setq foundItems (tselGetSelectedObjects)))
		(printf "tselAllOfObjectDBID: (axlGetSelSet) failed\n")
		nil)

	    ; clear onButtons because they should not affect select by dbid
	    ((null (axlSetFindFilter ?onButtons "NOALL"))
		(printf "tselAllOfObjectDBID: Failed to clear onButtons\n")
		nil)

	    ; sub select individual items of  a type by DBID
	    ((null (apply 'and (mapcar 'tselSubObject foundItems)))
		(printf "tselAllOfObjectDBID: Sub select Failed for \"%s\"\n"
			findType)
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselAllOfObjectDBID: \"%s\" Items not deselected %L\n"
			findType leftOver)
		nil)

	    ; single select individual items of a type by DBID
	    ((null (apply 'and (mapcar 'tselSingleObject foundItems)))
		(printf "tselAllOfObjectDBID: Single select Failed for \"%s\"\n" 
			findType)

		nil)

	    ; add select individual items of a type by DBID
	    ((null (axlClearSelSet))
		(printf "tselAllOfObjectDBID: Failed to Clear SelSet\n")
		nil)
	    ((null (apply 'and (mapcar 'tselAddObject foundItems)))
		(printf "tselAllOfObjectDBID: Add select Failed for \"%s\"\n" 
			findType)
		nil)
	    ((nequal foundItems (setq newItems (axlGetSelSet)))
		(printf "tselAllOfObjectDBID:  Selset Wrong After Add Select\n")
		(printf "    Was: %L\n" newItems)
		(printf "    Expected: %L\n" (axlGetSelSet))
		nil)

	    ; sub select all of a type with one call to axlSubSelectObject
	    ((null (axlSubSelectObject foundItems))
		(printf "tselAllOfObjectDBID: Failed to SubSelect All\n")
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselAllOfObjectDBID: \"%s\" items not deselected %L\n"
			findType leftOver)
		nil)

	    ; test that ?enabled does not affect selection by dbid
	    ((null (axlSetFindFilter ?enabled "NOALL"))
		(printf "tselAllOfObjectDBID:  axlSetFindFilter Failed\n")
		nil)
	    ((null (axlAddSelectObject foundItems))
		(printf "tselAllOfObjectDBID: ?enabled Disabled Add Select\n")
		nil)
	    ((nequal foundItems (setq newItems (axlGetSelSet)))
		(printf "tselAllOfObjectDBID Selset Wrong After Add Select\n")
		(printf "    Was: %L\n" newItems)
		(printf "    Expected: %L\n" foundItems)
		nil)
	    ((null (axlSingleSelectObject foundItems))
		(printf "tselAllOfObjectDBID: ?enabled Disabled Single Select\n")
		nil)
	    ((nequal foundItems (setq newItems (axlGetSelSet)))
		(printf "tselAllOfObjectDBID Selset Wrong After Single Select\n")
		(printf "    Was: %L\n" newItems)
		(printf "    Expected: %L\n" foundItems)
		nil)
	    ((null (axlSubSelectObject foundItems))
		(printf "tselAllOfObjectDBID: ?enabled Disabled Sub Select\n")
		nil)
	    ((setq newItems (axlGetSelSet))
		(printf "tselAllOfObjectDBID Selset Wrong After Sub Select\n")
		(printf "    Was: %L\n" newItems)
		(printf "    Expected: %L\n" nil)
		nil)

	    (t (setq testPass t)))
	testPass))

;
(defun _tselTruncateList (inputList curCount)
    (cond
	((or (null inputList) (greaterp curCount 20))
	    nil)
	(t
	    (cons (car inputList) (_tselTruncateList (cdr inputList) 
						     (plus curCount 1))))))
	    


;tselGetSelectedObjects - gets sel set,  but trucates list if it is too big
(defun tselGetSelectedObjects ()
    (let (foundItems (itemCount 0))
	(when (and (setq foundItems (axlGetSelSet)) 
		   (greaterp (axlGetSelSetCount) 20))
	    (setq foundItems (_tselTruncateList foundItems 1))
	    (axlSingleSelectObject foundItems))
	foundItems))


; tselSubObject - Sub select an object and verify that it was deselected
(defun tselSubObject (item)
    (cond
	((null (axlSubSelectObject item))
	    (printf "tselSubObject: Failed to Deselect %L\n%L" 
		    item item->??)
	    nil)
	((member item (axlGetSelSet))
	    (printf "tselSubObject: Item [%L] in Selset after Deselection\n"
		    item)
	    nil)
	(t t)))

; tselSingleObject - Single select an object and verify that it is the only
;	object in selection set
(defun tselSingleObject (item)
    (let (count foundItem)
	(cond
	    ((null (axlSingleSelectObject item))
		(printf "tselSingleObject: Failed to Select %L\n%L" 
			item item->??)
		nil)
	    ((nequal (setq count (axlGetSelSetCount)) 1)
		(printf "tselSingleObject: Select count [%d] != 1\n" count)
		nil)
	    ((nequal item (setq foundItem (car (axlGetSelSet))))
		(printf "tselSingleObject: Selected Item [%L] != exp'd [%L]\n"
			foundItem item)
		nil)
	    (t t))))

; tselAddObject - Add Select an object an verify that count increased by 1
(defun tselAddObject (item)
    (let (count foundItem oldCount)
	(setq oldCount (axlGetSelSetCount))
	(cond
	    ((null (axlAddSelectObject item))
		(printf "tselAddObject: Failed to Select %L\n%L" 
			item item->??)
		nil)
	    ((nequal (setq count (axlGetSelSetCount)) (plus oldCount 1))
		(printf "tselAddObject: Sel count [%d] != oldCount [%d] + 1\n" 
			count oldCount)
		nil)
	    (t t))))

;; Test that axlXXXSelectObject does not accept bad DBID's
(defun tselBadDBIDTest ()
    (axlClearSelSet)
    (printf "Select with Bad DBID's should Result in Warnings\n")

    (cond
	; Test that we do not get a selection with nil list
	((axlSingleSelectObject nil)
	    (printf "tselBadDBIDTest: Got Selection from Nil Object List\n")
	    nil)

	; Test that we do not get a selection with nil in list
	((axlAddSelectObject '(nil))
	    (printf "tselBadDBIDTest: Got Selection from Nil Object in List\n")
	    nil)

	; Test that we do not get a selection with a symbol in list
	((axlAddSelectObject '(5))
	    (printf "tselBadDBIDTest: Got Selection from 5 in List\n")
	    nil)

	; Test that we do not get a selection with list in list
	((axlAddSelectObject '((junk)))
	    (printf "tselBadDBIDTest: Got Selection from List in List\n")
	    nil)

	; Make sure that we can select the design
	((axlAddSelectObject (axlDBGetDesign))
	    (printf "tselBadDBIDTest: Selected the Design\n")
	    nil)

	((axlGetSelSet)
	    (printf "tselBadDBIDTest: Ended with Selections\n")
	    nil)
	(t t)))
