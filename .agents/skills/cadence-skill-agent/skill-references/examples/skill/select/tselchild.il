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



;; tselChildTest - Test that objects and their parents or children do not
;;	coexist in the selection set.
(defun tselChildTest ()
    (let ((testPass nil))
	(axlSetFindFilter ?enabled '("ALL" "EQUIVLOGIC") ?onButtons "ALL")
	(cond
	    ((null (tselNotSymChildren "up3")))
	    ((null (tselSubSymChild "up3")))
	    ((null (tselNotNetChildren "sig101")))
	    ((null (tselSubNetChildren "sig101")))
	    ((null (tselNotPropChildren "mygroup" "*")))
	    ((setq testPass t))
	)

	(tselEchoResults "Selset Parent/Child Exclusion Test" testPass)))

;; tselNotSymChildren - Test that symbol children will not be selected if
;;	the symbol already is
(defun tselNotSymChildren (symName "t")
    (let (symSet (testPass nil))
	(axlClearSelSet)
	(cond
	    ((null (axlAddSelectName "SYMBOL" symName))
		(println "tselNotSymChildren - Could not select symbol"))
	    ((null (setq symSet (axlGetSelSet)))
		(println "tselNotSymChildren - nil selection set"))
	    ((tselectSymPinsByName symSet)
		(println "tselNotSymChildren - selected pins by name"))
	    ((tselectSymPinsByDBID symSet)
		(println "tselNotSymChildren - selected pins by DBID"))
	    ((tselectSymChildren symSet)
		(println "tselNotSymChildren - selected children by DBID"))
	    ((setq testPass t)))

	(when (null testPass)
	    (print "tselNotSymChildren - Failed for symbol: ")
	    (println symName))

	testPass))


;; tselSubSymChild - Test that previously selected children of a symbol will
;;	be replaced by the symbol (i.e. deselected) when the symbol is selected
(defun tselSubSymChild (symName "t")
    (let (symSet1 symSet2 (testPass nil))
	(axlClearSelSet)
	(cond
	    ; select symbols, get sel set and deselect symbols
	    ((null (axlAddSelectName "SYMBOL" symName))
		(println "tselSubSymChild - Could not select symbol"))
	    ((null (setq symSet1 (axlGetSelSet)))
		(println "tselSubSymChild - nil selection set 1"))
	    ((null (axlClearSelSet))
		(println "tselSubSymChild - could not clear selection set"))

	    ; select children
	    ((null (tselectSymPinsByDBID symSet1))
		(println "tselSubSymChild - could not select pins by DBID"))
	    ((null (tselectSymChildren symSet1))
		(println "tselSubSymChild - could not select children by DBID"))

	    ; selecting symbols again should deselect children
	    ((null (axlAddSelectName "SYMBOL" symName))
		(println "tselSubSymChild - Could not reselect symbol"))
	    ((null (setq symSet2 (axlGetSelSet)))
		(println "tselSubSymChild - nil selection set 2"))

	    ; compare two list (does sort) - prints out error
	    ((null (tselListEqual symSet1 symSet2 "tselSubSymChild")))

	    ((setq testPass t)))

	(when (null testPass)
	    (print "tselSubSymChild - Failed for symbol: ")
	    (println symName))

	testPass))

;; tselNotNetChildren - Test that children of a net are not selected when the
;;	Net already is selected
(defun tselNotNetChildren (netName "t")
    (let ((testPass nil))
	(axlClearSelSet)
	(cond
	    ((null (axlSetFindFilter ?enabled "NOEQUIVLOGIC"))
		(println "tselNotNetChildren - Could not clear EQUIVLOGIC"))
	    ((null (axlAddSelectName "NET" netName))
		(println "tselNotNetChildren - Could not select net"))

	    ; disable logic and select children
	    ((null (axlSetFindFilter ?enabled "EQUIVLOGIC"))
		(println "tselNotNetChildren - Could not set EQUIVLOGIC"))
	    ((axlAddSelectName "NET" netName)
		(println "tselNotNetChildren - Selected net children"))

	    ((setq testPass t)))

	(when (null testPass)
	    (print "tselNotNetChildren - Failed for symbol: ")
	    (println netName))

	testPass))

;; tselSubNetChildren - Test that previously selected children of a net will 
;; 	be replaced by the net (i.e. deselected) when the net is selected
(defun tselSubNetChildren (netName "t")
    (let (netSet1 netSet2 (testPass nil))
	(axlClearSelSet)
	(cond
	    ; set logic enable and select nets (remember sel set)
	    ((null (axlSetFindFilter ?enabled "NOEQUIVLOGIC"))
		(println "tselSubNetChildren - Could not clear EQUIVLOGIC"))
	    ((null (axlAddSelectName "NET" netName))
		(println "tselSubNetChildren - Could not select net"))
	    ((null (setq netSet1 (axlGetSelSet)))
		(println "tselSubNetChildren - nil selection set 1"))

	    ; clear sel set, disable logic and select children
	    ((null (axlClearSelSet))
		(println "tselSubNetChildren - Could not clear sel set"))
	    ((null (axlSetFindFilter ?enabled "EQUIVLOGIC"))
		(println "tselSubNetChildren - Could not set EQUIVLOGIC"))
	    ((null (axlAddSelectName "NET" netName))
		(println "tselSubNetChildren - Could not select net children"))


	    ; turn logic enable back on, reselect nets and compare with old set
	    ((null (axlSetFindFilter ?enabled "NOEQUIVLOGIC"))
		(println "tselSubNetChildren - Could not clear EQUIVLOGIC"))
	    ((null (axlAddSelectName "NET" netName))
		(println "tselSubNetChildren - Could not reselect net"))

	    ((null (setq netSet2 (axlGetSelSet)))
		(println "tselSubNetChildren - nil selection set 2"))

	    ; compare two list (does sort) - prints out error
	    ((null (tselListEqual netSet1 netSet2 "selSubNetChildren")))
	    ((setq testPass t)))

	(when (null testPass)
	    (print "tselSubNetChildren - Failed for symbol: ")
	    (println netName))

	testPass))

; tselFoundSymChildInSet - look for a symbol and any children of that symbol 
;	in the selection set
(defun tselFoundSymChildInSet (setSet "l")
    (let ((foundSymChild nil) (foundSymInst nil)) 
	(foreach symInst setSet
	    (when (equal (strcmp symInst->objType "symbol") 0)
		(setq foundSymInst t)

		(foreach child setSet
		    (when (member child symInst->pins)
			(setq foundSymChild t))
		    (when (member child symInst->children)
			(setq foundSymChild t)))))

	(when (null foundSymInst)
	    (println "tselFoundSymChildInSet - no symbols in sel set")
	    (setq foundSymChild t))

	foundSymChild))


;; tselNotPropChildren - Test that no parent/child combinations exist after
;;	doing a selction by a property name that is know to exist on 
;;	some parent and its children
(defun tselNotPropChildren (propName propValue "tt")
    (let (selSet (testPass nil))
	(axlClearSelSet)
	(axlSetFindFilter ?enabled '("ALL" "INVISIBLE"))
	(cond
	    ((null (axlAddSelectName "PROPERTY" 
				     (list (list propName propValue))))
		(println "tselNotPropChildren - Could not select by prop"))
	    ((null (setq selSet (axlGetSelSet)))
		(println "tselNotPropChildren - NULL sel set"))
	    ((tselFoundSymChildInSet selSet)
		(println "tselNotPropChildren - Children selected with parent"))
	    ((setq testPass t)))

	(when (null testPass)
	    (printf "tselNotPropChildren - Failed for prop \"%s\" \"%s\"\n"
		     propName propValue))

	testPass))
