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



;; tselDeleteTest - Test that deleted objects which were in the selection 
;;	set no longer are returned by axlGetSelSet
(defun tselDeleteTest ()
    (let (testPass foundItems leftOver)
	(axlDBRefreshId (axlDBGetDesign))
	(axlSetFindFilter ?enabled '("NOALL" "SYMBOLS")
			  ?onButtons "ALL")

	(cond
	    ((null (axlSingleSelectObject (car (axlDBGetDesign)->symbols)))
		(printf "tselDeleteTest: Failed to Select Symbol\n")
		nil)
	    ((null (setq foundItems (axlGetSelSet)))
		(printf "tselDeleteTest: Nil Select Set\n")
		nil)
	    ((null (axlDeleteObject foundItems))
		(printf "tselDeleteTest: Failed to Delete Object\n")
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselDeleteTest: Sel Set No Nil After Delete %L\n"
			leftOver)
		nil)
	    ((tselReselectDeletedObject foundItems)
		(printf "tselDeleteTest: Selected Deleted Object %L\n"
			foundItems)
		nil)
	    (t (setq testPass t)))

	(tselEchoResults "Selset Delete Test" testPass)))

;; tselReselectDeletedObject - Test that deleted objects will not be selected
(defun tselReselectDeletedObject (foundItems)
    (printf "Select of Deleted Object Should Give Warning\n")
    (axlSingleSelectObject foundItems))
