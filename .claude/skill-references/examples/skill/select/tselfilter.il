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



;; tselFilterTest - Test that find filter interface functions work correctly
(defun tselFilterTest ()
    (let ((success t))
	(when (null (ffReturnTest)) (setq success nil))
	(when (null (ffAllSetTest)) (setq success nil))
	(when (null (ffSetTest)) (setq success nil))
	(when (null (ffFormTest)) (setq success nil))

	(tselEchoResults "Selset Findfilter Set Test" success)))

; ffTestFilter - test that axlGetFindFilter returns expected filter list
(defun ffTestFilter (enableList onButtonList funcName "llt")
    (let (curList (success t))
	(setq curList (axlGetFindFilter nil))
	(when !(tselListEqual curList enableList funcName) 
	    (setq success nil))


	(setq curList (axlGetFindFilter t))
	(when !(tselListEqual curList onButtonList funcName) 
	    (setq success nil))
	
	success))


;; ffAllSetTest - Test that find filter set/get works for all object types
(defun ffAllSetTest ()
   (let (allList (success t))
	; sorted list of all filter items
	(setq allList (sort (copy (tselGetObjectTypes)) 'alphalessp))

	; turn off all find filter items and test result
	(axlSetFindFilter ?enabled (list "NOALL") ?onButtons (list "NOALL"))
	(when !(ffTestFilter nil nil "ffAllSetTest NOALL Test")
	    (setq success nil))
		
	; turn on all find filter items and test result
	(axlSetFindFilter ?enabled (list "ALL") ?onButtons (list "ALL"))
	(when !(ffTestFilter (append allList '("AUTOFORM" "EQUIVLOGIC" 
					       "INVISIBLE" "NAMEFORM")) 
			     allList "ffAllSetTest ALL Test")
	    (setq success nil))
		
	; clearing enabled should clear onButtons
	(axlSetFindFilter ?enabled (list "NOALL"))
	(when !(ffTestFilter nil nil 
			     "ffAllSetTest enabled clears onButton Test")
	    (setq success nil))
		
	success
   )
)


;; ffSetTest - Test that find filter can be set and cleared for all types
(defun ffSetTest ()
   (let (setList clearList item (success t))
	(axlSetFindFilter ?enabled (list "NOALL") ?onButtons (list "NOALL"))

	(foreach item (tselGetObjectTypes)
	    (setq setList (list item))
	    (setq clearList (list (buildString (list "NO" item) "")))

	    ; set item in enabled and onButton
	    (axlSetFindFilter ?enabled setList ?onButtons setList)
	    (when !(ffTestFilter setList setList "ffSetTest on Test")
		(setq success nil))

	    ; clear onButton.  enabled should not be affected
	    (axlSetFindFilter ?onButtons clearList)
	    (when !(ffTestFilter setList nil "ffSetTest onButton Off Test")
		(setq success nil))

	    ; turn both on then turn off enabled.  should also clear onButton
	    (axlSetFindFilter ?enabled setList ?onButtons setList)
	    (axlSetFindFilter ?enabled clearList)
	    (when !(ffTestFilter nil nil "ffSetTest enabled Off Test")
		(setq success nil))

	    ; turn on onButton should do nothing 
	    (axlSetFindFilter ?onButtons setList)
	    (when !(ffTestFilter nil nil "ffSetTest onButton w/o enabled Test")
		(setq success nil))
	)

	success
   )
)


;; ffReturnTest - Test return values for axlSetFindFilter
(defun ffReturnTest ()
    (let ((success nil))
	(cond
	    ((axlSetFindFilter)
		(println "(axlSetFindFilter) did not return nil"))
	    ((axlSetFindFilter ?enabled (list "JUNK") ?onButtons (list "JUNK"))
		(println "axlSetFindFilter with JUNK lists did not return nil"))
	    ((axlSetFindFilter ?enabled "JUNK" ?onButtons "JUNK")
		(println "axlSetFindFilter with JUNK did not return nil"))
	    ((null (axlSetFindFilter ?enabled "PINS"))
		(println "(axlSetFindFilter ?enabled PINS) returned nil"))
	    ((null (axlSetFindFilter ?enabled "NOALL" ?onButtons "NOALL"))
		(println "(axlSetFindFilter ?enabled NOALL) returns nil"))
	    ((setq success t)))))


;; ffFormTest - Test that find filter form can be opened
(defun ffFormTest ()
    (axlSetFindFilter ?enabled (list "ALL") ?onButtons (list "ALL"))
    (axlOpenFindFilter)
    (axlCloseFindFilter)
    t
)

