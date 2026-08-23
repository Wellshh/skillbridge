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



;; tselAreaSelect - Interactive Area Selection Single, Add and Sub select for
;;	point and box.   Tests for each selectable object type.
;   Run in conjunction with tselarea.scr which provides interactive input
(defun tselAreaSelect ()
    (let (testPass)
	(axlSetFindFilter ?enabled '("NOALL" "ALLTYPES") ?onButtons "NOALL")
	(axlOpenFindFilter)

	(cond
	    ((null (apply 'and (mapcar 'tselAreaTestType 
				       (tselGetObjectTypeData))))
		nil)

	    (t (setq testPass t)))

	(axlCloseFindFilter)
	(axlClearSelSet)
	(tselEchoResults "Selset Interactive Area Test" testPass)))

; tselAreaTestType - Do area selection test for a particular type
(defun tselAreaTestType (objTypeData)
    (let (testPass findType objTypeList)
	(setq findType (car objTypeData))
	(setq objTypeList (cadr objTypeData))

	(axlClearSelSet)
	(axlSetFindFilter ?onButtons (list "NOALL" findType))

	(cond
	    ((null (tselSingleSelectPoint objTypeData))
		nil)
	    ((null (tselAddSelectPoint objTypeData))
		nil)
	    ((null (tselSubSelectPoint objTypeData))
		nil)
	    ((null (tselSingleSelectBox objTypeData))
		nil)
	    ((null (tselAddSelectBox objTypeData))
		nil)
	    ((null (tselSubSelectBox objTypeData))
		nil)
	    (t (setq testPass t)))
	testPass))

; tselSingleSelectPoint - Single mode selection points provided in script
(defun tselSingleSelectPoint (objTypeData)
    (let ((testPass t) count selSet)
	(axlClearSelSet)
	(printf "\"%s\" Single Select Point Interactive Test" (car objTypeData))

	(while (axlSingleSelectPoint)
	    (cond
		((neq (setq count (axlGetSelSetCount)) 1)
		    (printf "tselSingleSelectPoint: Select count [%d]  != 1\n"
			    count)
		    (setq testPass nil))
		((null (setq selSet (axlGetSelSet)))
		    (printf "tselSingleSelectPoint: Nil Sel Set\n")
		    (setq testPass nil))
		((null (tselTestObjType "tselSingleSelectPoint"
					selSet
					objTypeData))
		    (setq testPass nil))
		(t t))

	    (mapc 'ashPrintObjData (axlGetSelSet)))

	testPass))

; tselAddSelectPoint - Add mode selection for points provided in script.
(defun tselAddSelectPoint (objTypeData)
   (let ((testPass t) count (oldCount 0) selSet)
	(axlClearSelSet)
	
	(printf "\"%s\" Add Select Point Interactive Test" (car objTypeData))

	(while (axlAddSelectPoint)
	    (when (neq (setq count (axlGetSelSetCount)) (plus oldCount 1))
		(printf "tselAddSelectPoint: count [%d] != oldCount [%d] + 1\n"
			count oldCount)
		(setq testPass nil))
	    (setq oldCount count))
		
	(cond
	    ((null (setq selSet (axlGetSelSet)))
		(printf "tselAddSelectPoint: Nil Selection Set\n")
		(setq testPass nil))
	    ((null (tselTestObjType "tselAddSelectPoint" selSet objTypeData))
		(setq testPass nil)))

	(printf "tselAddSelectPoint:  Selected %d \"%s\"\n"
		(axlGetSelSetCount) (car objTypeData))

	(mapc 'ashPrintObjData (axlGetSelSet))

	testPass))


; tselSubSelectPoint - Sub mode selection for points provided in script.
(defun tselSubSelectPoint (objTypeData)
   (let ((testPass t) count (oldCount (axlGetSelSetCount)) selSet)
	
	(printf "\"%s\" Sub Select Point Interactive Test" (car objTypeData))

	(while (axlSubSelectPoint)
	    (when (neq oldCount (plus (setq count (axlGetSelSetCount)) 1))
		(printf "tselSubSelectPoint: count [%d] != oldCount [%d] - 1\n"
			count oldCount)
		(setq testPass nil))
	    (setq oldCount count))
		
	(cond
	    ((setq selSet (axlGetSelSet))
		(printf "tselSubSelectPoint: Selection Set Not Nil\n")
		(mapc 'ashPrintObjData selSet)
		(setq testPass nil))
	    ((neq (setq count (axlGetSelSetCount)) 0)
		(printf "tselSubSelectPoint: Sel Set Count [%d] != 0\n" count)))

	testPass))


; tselSingleSelectBox - Single mode selection in areas provided in script
(defun tselSingleSelectBox (objTypeData)
   (let ((testPass t) count selSet)
	(axlClearSelSet)
	
	(printf "\"%s\" Single Select Box Interactive Test" (car objTypeData))

	(while (axlSingleSelectBox)
	    (cond 
		((leqp (setq count (axlGetSelSetCount)) 0)
		    (printf "tselSingleSelectBox: count [%d] <= 0\n" count)
		    (setq testPass nil))
		((null (setq selSet (axlGetSelSet)))
		    (printf "tselSingleSelectBox: Nil Selection Set\n")
		    (setq testPass nil))
		((null (tselTestObjType "tselSingleSelectBox" 
					selSet objTypeData))
		    (setq testPass nil))
		(t
		    (printf "tselSingleSelectBox:  Selected %d \"%s\"\n"
			    (axlGetSelSetCount) (car objTypeData))
		    (mapc 'ashPrintObjData (axlGetSelSet)))))

	testPass))


; tselAddSelectBox - Add mode selection in areas provided in script
(defun tselAddSelectBox (objTypeData)
   (let ((testPass t) count (oldCount 0) selSet)
	(axlClearSelSet)
	
	(printf "\"%s\" Add Select Box Interactive Test" (car objTypeData))

	(while (axlAddSelectBox)
	    (when (leqp (setq count (axlGetSelSetCount)) oldCount)
		(printf "tselAddSelectBox: count [%d] <= oldCount [%d]\n"
			count oldCount)
		(setq testPass nil))
	    (setq oldCount count))
		
	(cond
	    ((null (setq selSet (axlGetSelSet)))
		(printf "tselAddSelectBox: Nil Selection Set\n")
		(setq testPass nil))
	    ((null (tselTestObjType "tselAddSelectBox" selSet objTypeData))
		(setq testPass nil)))

	(printf "tselAddSelectBox:  Selected %d \"%s\"\n"
		(axlGetSelSetCount) (car objTypeData))

	(mapc 'ashPrintObjData (axlGetSelSet))

	testPass))


; tselSubSelectBox - Sub mode selection in areas provided in script
(defun tselSubSelectBox (objTypeData)
   (let ((testPass t) count (oldCount (axlGetSelSetCount)) selSet)
	
	(printf "\"%s\" Sub Select Box Interactive Test" (car objTypeData))

	(while (axlSubSelectBox)
	    (when (geqp (setq count (axlGetSelSetCount)) oldCount)
		(printf "tselSubSelectBox: count [%d] >= oldCount [%d]\n"
			count oldCount)
		(setq testPass nil))
	    (setq oldCount count))
		
	(cond
	    ((setq selSet (axlGetSelSet))
		(printf "tselSubSelectBox: Selection Set Not Nil\n")
		(mapc 'ashPrintObjData selSet)
		(setq testPass nil))
	    ((neq (setq count (axlGetSelSetCount)) 0)
		(printf "tselSubSelectBox: Sel Set Count [%d] != 0\n" count)))

	testPass))
