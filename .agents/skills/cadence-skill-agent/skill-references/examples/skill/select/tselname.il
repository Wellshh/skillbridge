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



;; tselNameSelect - Test that selection by name works
(defun tselNameSelect ()
   (let (testPass)
	(cond
	    ((null (tselAllDevTypeName))
		nil)
	    ((null (tselAllSymTypeName))
		nil)
	    ((null (tselAllNetName))
		nil)
	    ((null (tselAllPropName))
		nil)
	    (t (setq testPass t)))
		
	(tselEchoResults "Select By Name Test" testPass)))

;; tselAllDevTypeName - Select Components by device type
(defun tselAllDevTypeName ()
    (let (testPass comps devTypeList)
	(axlClearSelSet)
	(cond
	    ((null (setq comps (ashFindAllComponents)))
		(printf "tselAllDevTypeName: No Components Found\n")
		nil)
	    ((null (axlSetFindFilter ?enabled '("NOALL" "COMPONENTS")))
		(printf "tselAllDevTypeName: Find Filter Set Failed\n")
		nil)
	    ((null (setq devTypeList (tselMakeObjTypeList comps 
							  'tselDeviceType)))
		(printf "tselAllDevTypeName: Failed to Get Devtype List\n")
		nil)
	    ((null (apply 'and (mapcar 'tselDevTypeName devTypeList)))
		nil)
	    (t (setq testPass t)))
	testPass))

; tselDevTypeName - Select components with given device type
(defun tselDevTypeName (devTypeData)
    (let (testPass devType compList foundItems leftOver)
	(cond
	    ((null (setq devType (car devTypeData)))
		(printf "tselDevTypeName: Null devType Name\n")
		nil)
	    ((null (setq compList (cadr devTypeData)))
		(printf "tselDevTypeName: Null Comp List\n")
		nil)
	    ((null (axlSingleSelectName "DEVTYPE" devType))
		(printf "tselDevTypeName: Select Failed for %L\n" devType)
		nil)
	    ((null (setq foundItems (axlGetSelSet)))
		(printf "tselDevTypeName: Nil Sel Set\n")
		nil)
	    ((null (tselListEqual foundItems compList "tselDevTypeName"
				  '(lambda (obj1 obj2) 
					(alphalessp obj1->name obj2->name))))
		(printf "tselDevTypeName: Compare Failed for %L\n" devType)
		nil)
	    ((null (axlSubSelectName "DEVTYPE" devType))
		(printf "tselDevTypeName: Deselect Failed for %L\n" devType)
		(printf " %L\n" (axlGetSelSet))
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselDevTypeName: Sel Set Not Nil after Deselect\n")
		(printf " %L\n" leftOver)
		(axlClearSelSet)
		nil)
	    (t (setq testPass t)))
	testPass))

;; tselAllSymTypeName - Select symbols by symbol type
(defun tselAllSymTypeName ()
    (let (testPass syms symTypeList)
	(axlClearSelSet)
	(cond
	    ((null (setq syms (axlDBGetDesign)->symbols))
		(printf "tselAllSymTypeName: No Symbols Found\n")
		nil)
	    ((null (axlSetFindFilter ?enabled '("NOALL" "SYMBOLS")))
		(printf "tselAllSymTypeName: Find Filter Set Failed\n")
		nil)
	    ((null (setq symTypeList (tselMakeObjTypeList syms))) 
		(printf "tselAllSymTypeName: Failed to Get Symtype List\n")
		nil)
	    ((null (apply 'and (mapcar 'tselSymTypeName symTypeList)))
		nil)
	    (t (setq testPass t)))
	testPass))


; tselSymTypeName - Select symbols with a given symbol type
(defun tselSymTypeName (symTypeData)
    (let (testPass symName symList foundItems)
	(cond
	    ((null (setq symName (car symTypeData)))
		(printf "tselSymTypeName: Null symName Name\n")
		nil)
	    ((null (setq symList (cadr symTypeData)))
		(printf "tselSymTypeName: Null Comp List\n")
		nil)
	    ((null (axlAddSelectName "SYMTYPE" symName))
		(printf "tselSymTypeName: Select Failed for %L\n" symName)
		nil)
	    ((null (setq foundItems (axlGetSelSet)))
		(printf "tselSymTypeName: Nil Sel Set\n")
		nil)
	    ((null (tselListEqual foundItems symList "tselSymTypeName"
				  'tselSymLessP))
		(printf "tselSymTypeName: Compare Failed for %L\n" symName)
		nil)
	    ((null (axlSubSelectName "SYMTYPE" symName))
		(printf "tselSymTypeName: Deselect Failed for %L\n" symName)
		(printf " %L\n" (axlGetSelSet))
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselSymTypeName: Sel Set Not Nil after Deselect\n")
		(printf " %L\n" leftOver)
		(axlClearSelSet)
		nil)
	    (t (setq testPass t)))
	testPass))


;; tselAllNetName - Select nets by net name
(defun tselAllNetName ()
    (let (testPass nets)
	(axlClearSelSet)
	(cond
	    ((null (setq nets (ashFindAllNets)))
		(printf "tselAllNetName: No Components Found\n")
		nil)
	    ((null (axlSetFindFilter ?enabled '("NOALL" "NETS")))
		(printf "tselAllNetName: Find Filter Set Failed\n")
		nil)
	    ((null (apply 'and (mapcar 'tselNetName nets)))
		nil)
	    (t (setq testPass t)))
	testPass))

; tselNetName - select a net by its name and verify 
(defun tselNetName (net)
    (let (testPass foundItems leftOver)
	(cond
	    ((equal net->name "")
		(setq testPass t))
	    ((null (axlAddSelectName "NET" net->name))
		(printf "tselNetName: Select Failed for %L\n" net->name)
		nil)
	    ((null (setq foundItems (axlGetSelSet)))
		(printf "tselNetName: Nil Sel Set\n")
		nil)
	    ((null (tselListEqual foundItems (list net) "tselNetName"
				  '(lambda (obj1 obj2) 
					(alphalessp obj1->name obj2->name))))
		(printf "tselNetName: Compare Failed for %L\n" net->name)
		nil)
	    ((null (axlSubSelectName "NET" net->name))
		(printf "tselNetName: Deselect Failed for %L\n" net->name)
		(printf " %L\n" (axlGetSelSet))
		nil)
	    ((setq leftOver (axlGetSelSet))
		(printf "tselNetName: Sel Set Not Nil after Deselect\n")
		(printf " %L\n" leftOver)
		(axlClearSelSet)
		nil)
	    (t (setq testPass t)))
	testPass))


;; tselAllPropName - Select objects by property name (and sometimes value)
(defun tselAllPropName ()
    (let (testPass)
	(axlSetFindFilter ?enabled '("NOALL" "NETS"))
	(axlClearSelSet)

	(cond
	    ((null (tselPropName '(("BUS_NAME" "MEM"))))
		nil)
	    ((null (tselPropName "FIXED"))
		nil)
	    ((null (tselPropName '("FIXED")))
		nil)
	    (t (setq testPass t)))

	testPass))


; tselPropName - Select objects with a given property print out object
;	data.  Verification is in .jrl compare
(defun tselPropName (propData)
    (let (testPass nets foundItems sortedItems)
	(cond
	    ((null (axlSingleSelectName "PROPERTY" propData))
		(printf "tselPropName: Failed To Select %L\n" propData)
		nil)
	    ((null (setq foundItems (axlGetSelSet)))
		(printf "tselPropName: Failed To Get Sel Set - %L\n" propData)
		nil)
	    (t (setq testPass t)))

	(when foundItems
	    (setq sortedItems (tselCopyList foundItems 
			'(lambda (obj1 obj2)
				(cond 
				    ((lessp (strlen obj1->name) 
					    (strlen obj2->name))
					t)
				    ((eq (strlen obj1->name)
					 (strlen obj2->name))
					(alphalessp obj1->name obj2->name))
				    (t nil)))))

	    (printf "tselPropName: Found Items With Property %L\n" propData)
	    (mapc 'ashPrintObjData sortedItems))
	
	testPass))
