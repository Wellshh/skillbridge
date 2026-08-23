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

;;
;; Uses Allegro axlSelect to find all elements of a particular type
;;

(defun _saveFindFilter ()
    (let (oldElements oldOnButtons)
	(setq oldElements (axlGetFindFilter nil))
	(setq oldOnButtons (axlGetFindFilter t))

	(list oldElements oldOnButtons)))


(defun _restoreFindFilter (OldFilter "l")
    (let (oldElements oldOnButtons)
	(axlSetFindFilter ?enabled "NOALL" ?onButtons "NOALL")

	(when (setq oldElements (car OldFilter))
	    (axlSetFindFilter ?enabled oldElements))

	(when (setq oldOnButtons (cadr OldFilter))
	    (axlSetFindFilter ?onButtons oldOnButtons))
	t))


(defun findAllOfType (findType "t")
    (let (oldFilter newFilter selSet oldSet)
	(setq oldSet (axlGetSelSet))
	(setq oldFilter (_saveFindFilter))
	(axlClearSelSet)

	(setq newFilter (list "NOALL" findType "INVISIBLE"))
	(axlSetFindFilter ?enabled newFilter ?onButtons newFilter)

	(axlAddSelectAll)
	(setq selSet (axlGetSelSet))

	; restore old selections
	(axlClearSelSet)
	(when oldSet 
	    (axlSetFindFilter ?enabled '("NOALL" "ALLTYPES")
			      ?onButtons '("ALL"))
	    (axlAddSelectObject oldSet))

	(_restoreFindFilter oldFilter)
	selSet))


(defun ashFindAllPins ()
    (findAllOfType "PINS"))

(defun ashFindAllVias ()
    (findAllOfType "VIAS"))

(defun ashFindAllClines ()
    (findAllOfType "CLINES"))

(defun ashFindAllClinesegs ()
    (findAllOfType "CLINESEGS"))

(defun ashFindAllLines ()
    (findAllOfType "LINES"))

(defun ashFindAllLinesegs ()
    (findAllOfType "LINESEGS"))

(defun ashFindAllDrcs ()
    (findAllOfType "DRCS"))

(defun ashFindAllText ()
    (findAllOfType "TEXT"))

(defun ashFindAllShapes ()
    (findAllOfType "SHAPES"))

(defun ashFindAllShapesegs ()
    (findAllOfType "SHAPESEGS"))

(defun ashFindAllVoids ()
    (findAllOfType "VOIDS"))

(defun ashFindAllVoidsegs ()
    (findAllOfType "VOIDSEGS"))

(defun ashFindAllSymbols ()
    (findAllOfType "SYMBOLS"))

(defun ashFindAllComponents ()
    (findAllOfType "COMPONENTS"))

(defun ashFindAllNets ()
    (findAllOfType "NETS"))

