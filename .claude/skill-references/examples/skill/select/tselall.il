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



;; tselSelectAll - Crosscheck found objects against expected objType for all
;;	types that can be selected.  Uses axlAddSelectAll
(defun tselSelectAll ()
    (let (testPass)

	(axlSetFindFilter ?enabled '("NOALL" "ALLTYPES") ?onButtons "NOALL")

	(cond
	    ((null (apply 'and (mapcar 'tselSelectAllOf 
				       (tselGetObjectTypeData))))
		nil)

	    (t (setq testPass t)))

	(tselEchoResults "Selset Select All Test" testPass)))


; tselSelectAllOf - Crosscheck found objects of a particular type
(defun tselSelectAllOf (objTypeData)
    (let (testPass foundItems leftOver findType objTypeList)
	(setq findType (car objTypeData))
	(setq objTypeList (cadr objTypeData))

	(axlClearSelSet)
	(axlSetFindFilter ?onButtons (list "NOALL" findType))

	(cond
	    ; select all of the type
	    ((null (axlAddSelectAll))
		(printf "tselSelectAllOf: No \"%s\" to select\n" findType)
		nil)
	    ((null (setq foundItems (axlGetSelSet)))
		(printf "tselSelectAllOf: (axlGetSelSet) failed\n")
		nil)
	    
	    ; test that all are correct objType
	    ((null (tselTestObjType "tselSelectAllOf"
				    foundItems
				    objTypeData))
		nil)


	    ; test that axlSubSelectAll is dependent on onButtons
	    ((null (axlSetFindFilter ?onButtons (list 
						 "ALLTYPES"
						 (buildString (list "NO"
								    findType)
							      ""))))
		(printf "tselSelectAllOf: ?onButton Control Failed for Sub\n")
		nil)
	    ((axlSubSelectAll)
		(printf "tselSelectAllOf: Nil onButton, Sub Selected Items\n")
		(printf "   %L\n" (axlGetSelSet))
		nil)
	    ((null (equal foundItems (setq nteItems (axlGetSelSet))))
		(printf "tselSelectAllOf: Selset Changed by Sub Select\n")
		(printf "    Was: %L\n" newItems)
		(printf "    Expected: %L\n" (axlGetSelSet))
		nil)

	    ; test that axlSubSelectAll will deselect all of specified type
	    ((null (axlSetFindFilter ?onButtons (list "NOALL" findType)))
		(printf "tselSelectAllOf: Failed to set find filter\n")
		nil)
	    ((null (axlSubSelectAll))
		(printf "tselSelectAllOf: Sub select failed for \"%s\"\n"
			findType)
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselSelectAllOf: \"%s\" Items not deselected %L\n"
			findType leftOver)
		nil)

	    ; test that axlAddSelectAll is dependent on onButtons
	    ((null (axlSetFindFilter ?onButtons "NOALLTYPES"))
		(printf "tselSelectAllOf: ?onButton Control Failed for Add\n")
		nil)
	    ((axlAddSelectAll)
		(printf "tselSelectAllOf: ?onButton Control Failed for Add\n")
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselSelectAllOf: Nil onButton, Add Selected Items\n")
		(printf "    %L\n" leftOver)
		nil)

	    (t (setq testPass t)))
	testPass))

