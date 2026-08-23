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



;; tselEquivlogicTest - Test that the EQUIVLOGIC option works
(defun tselEquivlogicTest ()
    (let (testPass)
	(cond
	    ((null (tselComponentEquivlogic)) nil)
	    ((null (tselNetEquivlogic)) nil)
	    ((null (tselEquivlogicRemove)) nil)
	    ((null (tselNetNoEquivlogic)) nil)
	    ((null (tselCompNoEquivlogic)) nil)
	    (t (setq testPass t)))
		
	(tselEchoResults "Selset EQUIVLOGIC Test" testPass)))

;  tselComponentEquivlogic- Test EQUIVLOGIC for all components
(defun tselComponentEquivlogic ()
    (let (testPass components)
	(axlClearSelSet)
	(axlSetFindFilter ?enabled '("NOALL" "EQUIVLOGIC" "ALLTYPES")
			  ?onButtons '("NOALL"))
	(axlSetFindFilter ?onButtons '("NOALLTYPES" "COMPONENTS" "SYMBOLS"))
	(cond
	    ((null (setq components (ashFindAllComponents)))
		(printf "tselComponentEquivlogic: No Components Found.\n"))
	    ((axlGetSelSet)
		(printf "tselComponentEquivlogic: selset not nil after find\n"))
	    ((null (apply 'and (mapcar 'tselCompEquivlogic components)))
		nil)
	    (t (setq testPass t)))
	testPass))

; tselCompEquivlogic - Test EQUIVLOGIC for a component
(defun tselCompEquivlogic (component)
    (let (symbol testPass)
	(cond
	    ((null component)
		(printf "tselCompEquivlogic: Nil Component.\n"))
	    ((null (axlSingleSelectObject component))
		(printf "tselCompEquivlogic: No Symbol for Comp %L\n"
			component->name))
	    ((neq (axlGetSelSetCount) 1)
		(printf "tselCompEquivlogic: Select count [%d] != 1\n" 
			(axlGetSelSetCount)))
	    ((null (setq symbol (car (axlGetSelSet))))
		(printf "tselCompEquivlogic: Nil sel set\n"))
	    ((nequal symbol->objType "symbol")
		(printf "tselCompEquivlogic: Object %L) found not a symbol\n"
			symbol->objType))
	    ((nequal symbol->refdes component->name)
		(printf "tselCompEquivlogic: Sym %L != Comp %L\n"
			symbol->refdes component->name))
	    (t (setq testPass t)))
	testPass))


; tselNetEquivlogic - test EQUIVLOGIC for all nets
(defun tselNetEquivlogic ()
    (let (nets netItemData)
	(axlClearSelSet)
	(axlSetFindFilter ?enabled '("NOALL" "EQUIVLOGIC" "ALLTYPES")
			  ?onButtons '("NOALL"))
	(cond
	    ((null (setq netItemData (tselMakeNetItemDataList)))
		(printf "tselNetEquivlogic: Failed to make net item type list\n")
		nil)
	    ((null (setq nets (ashFindAllNets)))
		(printf "tselNetEquivlogic: No Nets Found.\n")
		nil)
	    ((null (tselAllNetsItems nets netItemData))
		(printf "tselAllNetsItems failed\n")
		nil)
	    (t t))))


; tselMakeNetItemDataList - make a list of object data for net EQUIVLOGIC
(defun tselMakeNetItemDataList ()
    (let (netItemData)
	(foreach findType (tselGetObjectTypeData)
	    (cond
		; remove "polygon" from "SHAPE" objTypes
		((equal (car findType) "SHAPES")
		    (setq netItemData (cons '("SHAPES" ("shape"))
					    netItemData)))
		((member (car findType) '("PINS" "CLINES" "CLINESEGS" 
					   "VIAS" "SHAPES" "SHAPESEGS" 
					   "VOIDS" "VOIDSEGS"))
		    (setq netItemData (cons findType netItemData)))))
	netItemData))

; tselAllNetsItems - for all nets, test that equivlogic selects the correct
;	object types and that objects are from the given net
(defun tselAllNetsItems (nets netItemData)
    (let (netItemsFound (testPass t))
	(foreach netItemType netItemData
	    ; want to find at least one of every type.
	    (setq netItemsFound nil)

	    (axlSetFindFilter ?onButtons (list "NOALLTYPES" 
					       "NETS" 
					       (car netItemType)))
	    (foreach net nets
		(when (axlSingleSelectObject net)
		    (setq netItemsFound t)

		    (when (null (tselTestNetItems net 
						  (axlGetSelSet) 
						  netItemType))
			(setq testPass nil))))

	    (when (null netItemsFound)
		(printf "tselAllNetsItems: No Net %L Found (at all)\n"
			(car netItemType))
		(setq testPass nil)))

	testPass))

;  tselTestNetItems - test EQUIVLOGIC for a given net
(defun tselTestNetItems (net foundItems netItemType)
    (cond
	((null (tselTestObjType "tselTestNetItems" foundItems netItemType))
	    (printf "tselTestNetItems: %L obj test failed for net %L\n" 
		    (car netItemType) net->name)
	    nil)
	((null (tselFindItemOnBranch foundItems net->branches net))
	    nil)
	((null (tsetTestItemsNet foundItems net))
	    (printf "tselTestNetItems: %L net test failed for net %L\n" 
		   (car netItemType) net->name)
	    nil)
	(t
	    t)))

; tsetTestItemsNet - test that all found items have net field that matches
;	with given net
(defun tsetTestItemsNet (foundItems net)
    (let ((testPass t))
	(foreach item foundItems
	    (when (nequal item->net net)
		(printf "tsetTestItemsNet failed\n")
		(printf "tsetTestItemsNet: item->net [%L] != exp'd [%L]\n"
			item->net net)
		(setq testPass nil)))
	testPass))

; tselFindItemOnBranch - Test if net item appears on one of the net's branches
(defun tselFindItemOnBranch (item branches net)
    (cond
	; end of list of found items
	((null item)
	    nil)

	; list of found items
	((listp item)
	    (cond
		((null (tselFindItemOnBranch (car item) branches net))
		    (tselFindItemOnBranch (cdr item) branches net))
		(t t)))

	; end of list of branches
	((null branches)
	   (printf "Object [%L] not found on net %L\n" item net->name)
	   nil)

	; line or arc segment could be from shape, cline on branch
	((or (equal item->objType "line") (equal item->objType "arc"))
	    (tselFindItemOnBranch item->parent branches net))
	; void
	((equal item->objType "polygon")
	    (tselFindItemOnBranch item->parent branches net))
	; pin, cline, via or shape should be on a branch
	((member item (car branches)->children)
	   t)
	(t
	    (tselFindItemOnBranch item (cdr branches) net))))


; tselEquivlogicRemove - Test if physical equivalents are deselected by 
;	using the logical object
(defun tselEquivlogicRemove ()
    (cond
	((null (tselEquivlogicRemoveType "NETS" "NET")) nil)
	((null (tselEquivlogicRemoveType "COMPONENTS" "COMPONENT")) nil)
	(t t)))

(defun tselEquivlogicRemoveType (findType findNameType)
    (axlSetFindFilter ?enabled '("NOALL" "EQUIVLOGIC" "ALLTYPES")
		      ?onButtons "ALL")
    (axlClearSelSet)
    (cond
	((null (axlAddSelectName findNameType  "*"))
	    (printf "tselEquivlogicRemove: axlAddSelectName failed for %L\n"
		    findType)
	    nil)
	((null (axlSetFindFilter ?enabled (list "NOALLTYPES" findType)
				 ?onButtons "ALL"))
	    (printf "tselEquivlogicRemove: set filter for %L failed\n"
		    findType)
	    nil)
	((null (axlSubSelectAll))
	    (printf "tselEquivlogicRemove: axlSubSelectAll failed for %L\n"
		    findType)
	    nil)
	((axlGetSelSet)
	    (printf "tselEquivlogicRemove: (axlGetSelSet) not nil for %L\n"
		    findType)
	    nil)
	(t t)))

; tselNetNoEquivlogic - Test that nothing is selected if onButtons have no
;	net EQUIVLOGIC types
(defun tselNetNoEquivlogic ()
    (axlClearSelSet)
    (axlSetFindFilter ?enabled '("NOALL" "EQUIVLOGIC" "NETS")
			  ?onButtons '("NOALL" "NETS"))

    (cond
	((axlSingleSelectName "NET" "*")
	    (printf "tselNoEquivlogic: Selected Something\n")
	    (printf "%L\n" (axlGetSelSet))
	    nil)
	(t t)))

; tselCompNoEquivlogic - Test that nothing is selected if onButtons have no
;	component EQUIVLOGIC types
(defun tselCompNoEquivlogic ()
    (let (testPass pin)
	(axlClearSelSet)
	(axlSetFindFilter ?enabled '("NOALL" "EQUIVLOGIC" "COMPONENTS")
			  ?onButtons '("NOALL" "COMPONENTS"))
	(setq pin (car (car (axlDBGetDesign)->components)->symbol->pins))
	(cond
	    ((null pin)
		(printf "tselCompNoEquivlogic:  Found No Pin\n")
		nil)
	    ((axlSingleSelectPoint pin->xy)
		(printf "tselCompNoEquivlogic: Found Something at %L\n"
			pin->xy)
		(mapc 'ashPrintObjData (axlGetSelSet))
		nil)
	    ((axlAddSelectPoint pin->xy)
		(printf "tselCompNoEquivlogic: Found Something at %L\n"
			pin->xy)
		(mapc 'ashPrintObjData (axlGetSelSet))
		nil)
	    (t (setq testPass t)))
	testPass))
