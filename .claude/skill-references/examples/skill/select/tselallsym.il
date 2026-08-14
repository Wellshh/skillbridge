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



;; tselAllSyms - test if all symbols can be selected by various means
(defun tselAllSyms ()
    (let (drawing (testPass t))
	(axlClearSelSet)
	(axlCloseFindFilter)
	(axlSetFindFilter ?enabled "NOALL" ?onButtons "NOALL")

	(when (setq drawing (axlDBGetDesign))
	    (foreach symDBID drawing->symbols
		(cond 
		    ((null symDBID->refdes)
		       (printf "tselAllSyms: Unassigned symbol \"%s\" skipped\n"
				symDBID->name))
		(t
		    (when (null (tselSymByName symDBID)) (setq testPass nil))
		    (when (null (tselAllPins symDBID)) (setq testPass nil)))))

	    (when (null (tselAllSymsByArea drawing)) (setq testPass nil))
	)

	(axlClearSelSet)
	(tselEchoResults "Selset Symbol Selection Test" testPass)))


;; tselSymByName - test if a symbol can be selected by its refdes name
(defun tselSymByName (symDBID "o")
    (let (tselSet setCount setSymbol (testPass nil))
	(axlSetFindFilter ?enabled "SYMBOLS")
	(cond
	    ((null (axlSingleSelectName "SYMBOL" symDBID->refdes))
		(printf "tselSymByName: Failed to select symbol\n"))
	    ((nequal (setq setCount (axlGetSelSetCount)) 1)
		(printf "tselSymByName: Select count not 1: %d\n" setCount))
	    ((null (setq setSymbol (car (axlGetSelSet))))
		(printf "tselSymByName: Could not get symbol in Sel Set\n"))
	    ((nequal symDBID setSymbol)
		(printf "Selected symbol (%s) does not match original (%s)\n"
			setSymbol symDBID))

	    ((setq testPass t))
	)

	(when (null testPass)
	    (printf "tselSymByName: Failed for symbol %s - %s\n\n" 
		    symDBID symDBID->refdes))

	(axlSetFindFilter ?enabled "NOSYMBOLS")
	testPass
    )
)

; compare function for sorting unassigned symbol instances 
(defun tselUnassignedSymLessP (sym1 sym2)
    (let ((sym1Less nil) 
	 (x1 (car sym1->xy)) 
	 (x2 (car sym2->xy))
	 (y1 (cadr sym1->xy)) 
	 (y2 (cadr sym2->xy)))

	(cond
	    ((lessp x1 x2)
		(setq sym1Less t))
	    ((greaterp x1 x2)
		(setq sym1Less nil))
	    ((lessp y1 y2)
		(setq sym1Less t))
	    ((greaterp y1 y2)
		(setq sym1Less nil))
	    ((lessp sym1->rotation sym2->rotation)
		(setq sym1Less t))
	    ((greaterp sym1->rotation sym2->rotation)
		(setq sym1Less nil))
	    ((and (null s1->mirrored) s2->mirrored)
		(setq sym1Less t))
	    ((and s1->mirrored (null s2->mirrored))
		(setq sym1Less nil))
	    ((alphalessp sym1->name sym2->name)
		(setq sym1Less t))
	    ((alphalessp sym2->name sym1->name)
		(setq sym1Less nil))
	    ((alphalessp sym1->type sym2->type)
		(setq sym1Less t))
	    ((alphalessp sym2->type sym1->type)
		(setq sym1Less nil))
	    (t (setq sym1Less nil)))

    sym1Less)
)

; compare function for sorting symbol instances
(defun tselSymLessP (sym1 sym2 "oo")
  (let ((sym1Less nil))
    (cond
	(sym1->refdes
	    (cond 
		(sym2->refdes (setq sym1Less (alphalessp sym1->refdes 
							  sym2->refdes)))
		(t (setq sym1Less t))))
	(t (when (null sym2->refdes)
		 (setq sym1Less (tselUnassignedSymLessP sym1 sym2)))))

    sym1Less))


;; tselAllSymsByArea - test if we can select all symbols in the drawing by area
;;     compares against drawing symbol list
(defun tselAllSymsByArea (drawing "o")

    (let (selSet setCount setSymbol (testPass nil))
	(axlSetFindFilter ?enabled "SYMBOLS" ?onButtons "SYMBOLS")
	(cond
	    ((null (axlSingleSelectBox drawing->bBox))
		(printf "tselAllSymsByArea: Failed to select symbol\n"))
	    ((null (setq selSet (axlGetSelSet)))
		(printf "tselAllSymsByArea: Could not get Selection Set\n"))
	    ((null (tselListEqual selSet drawing->symbols 
				 "tselAllSymsByArea" 'tselSymLessP))
		(printf "tselAllSymsByArea:  Selected list != symbol list\n"))

	    ((setq testPass t))
	)

	(when (null testPass) (printf "tselAllSymsByArea: Failed \n\n" ))

	(axlSetFindFilter ?enabled "NOSYMBOLS" ?onButtons "NOSYMBOLS")
	testPass
    )
)


; compare function for sorting pins
(defun pinlessp (pin1 pin2 "oo")
    (alphalessp pin1->number  pin2->number )
)

;; tselAllPins - test if we can select pins of a symbol by name.
;;	compare with symbol pin list
(defun tselAllPins (symDBID "o")
    (let (selSet (testPass nil))
	(axlSetFindFilter ?enabled "PINS")
	(axlClearSelSet)
	(cond
	    ((null (tselectSymPinsByName (list symDBID)))
		(printf "tselAllPins:  Could not select pins for symbol %s\n"
			symDBID))
	    ((null (setq selSet (axlGetSelSet)))
		(printf "tselAllPins:  Could not get pin selSet\n"))
	    ((null (tselListEqual selSet symDBID->pins "tselAllPins" 'pinlessp))
		(printf "tselAllPins:  Selected list != pin list\n"))

	    ((setq testPass t))
	)

	(when (null testPass)
	    (printf "tselAllPins: Failed for symbol %s - %s\n\n" 
		    symDBID symDBID->refdes))

	(axlSetFindFilter ?enabled "NOPINS")
	testPass
    )
)

