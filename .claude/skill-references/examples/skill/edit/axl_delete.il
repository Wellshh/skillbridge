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



(defun _makeCline (p1 p2)
    (let (cline)
	(setq cline 
	      (axlDBCreatePath (axlPathStart (list p1 p2) .012)
			       "ETCH/TOP" nil))
	(car (car cline))))

(defun deleteAndPrint (items message)
    (let (result)
	(unless (listp items) (setq items (list items)))
	(axlFlushDisplay)
	(axlMsgPut "")
	(axlMsgPut (sprintf nil "Deleting %L" message))
	(axlMsgPut "---------------------------------------")
	(axlFlushDisplay)
	(setq result (axlDeleteObject items))
	(axlFlushDisplay)
	(mapc 'ashPrintObjData items)
	(axlFlushDisplay)
	(axlMsgPut "")
	result))

;; Merge CLINES to make sure that axl dbid subsystem handles it correctly.
;    error shows up in .jrl diff
(defun mergeClines ()
    (let (clineList testPass)
	(setq clineList (cons (_makeCline 6.4:2.6 8.4:2.6) nil))
	(setq clineList (cons (_makeCline 2.4:2.6 4.4:2.6) clineList))
	(setq clineList (cons (_makeCline 4.4:2.6 6.4:2.6) clineList))

	(axlFlushDisplay)
	(axlMsgPut "")
	(axlMsgPut "Merging 3 Clines")
	(axlMsgPut "---------------------------------------")
	(axlFlushDisplay)

	(mapc 'ashPrintObjData clineList)

	(foreach cline clineList
	    (when cline->objType (axlDeleteObject cline)))
	(axlFlushDisplay)
	(axlMsgPut "")
	testPass))

;; Delete CLINES to make sure that axl dbid subsystem handles it correctly.
;    error shows up in .jrl diff
(defun deleteClines ()
    (let (clineList testPass)
	(setq clineList (cons (_makeCline 6.4:2.6 8.4:2.6) nil))
	(setq clineList (cons (_makeCline 2.4:2.6 4.4:2.6) clineList))
	(setq clineList (cons (_makeCline 4.4:2.6 6.4:2.6) clineList))

	(deleteAndPrint clineList "Clines")

	testPass))

(defun addShapeOutline ()
    (let (path)
	(setq path (axlPathStart (list 1:1)))
	(axlPathLine path 0 1:8)
	(axlPathLine path 0 5:4)
	(axlPathArcCenter path 0 5:1 t 5:2.5)
	(axlPathLine path 0 1:1)
	(axlDBCreateOpenShape path t "ETCH/TOP" nil)))

(defun addShapeVoid (shape)
    (let (path)
	(setq path (axlPathStart (list 2:2)))
	(axlPathLine path 0 2:4)
	(axlPathLine path 0 3:3)
	(axlPathArcCenter path 0 3:2 nil 3:2.5)
	(axlPathLine path 0 2:2)
	(axlDBCreateVoid shape path)))

(defun openTestShape ()
    (let (shape)
	(setq shape (addShapeOutline))
	(addShapeVoid shape)
	shape))

(defun closeTestShape (shape)
    (axlDBCreateCloseShape shape))

;; Delete a shape void segment.  Delete should report error. Seg should not be
;;   deleted.
;    error show up in .jrl diff
(defun deleteShapeVoidSeg (shape)
    (deleteAndPrint (car shape->voids)->segments "Void Segments"))


;; Delete a shape outline segment.  Delete should report error.  Seg should not
;;   be deleted.
;    error show up in .jrl diff
(defun deleteShapeSegment (shape)
   (null (deleteAndPrint shape->segments "Shape Segments")))


;; Delete a void from an open shape.  Should work.
;    error show up in .jrl diff
(defun deleteOpenShapeVoid (shape)
   (deleteAndPrint shape->voids "Open Shape Voids"))


;; Delete a void from an non-open shape.  Delete should report error.  Void
;;  should not be deleted.
;    error show up in .jrl diff
(defun deleteShapeVoids (shape)
   (null (deleteAndPrint shape->voids "Closed Shape Voids")))


;; Delete open shape.  Delete should report error.  Shape should not be deleted.
;    error show up in .jrl diff
(defun deleteOpenShape (shape)
   (null (deleteAndPrint shape "Open Shape")))


;; Delete close shape.  Should work.
;    error show up in .jrl diff
(defun deleteShape (shape)
   (null (deleteAndPrint shape "Closed Shape")))

(defun deleteOpenShapeTests ()
    (let (shape)
	(setq shape (openTestShape))
	(deleteShapeSegment shape)
	(deleteShapeVoidSeg shape)
	(deleteOpenShape shape)
	(deleteOpenShapeVoid shape)
	(closeTestShape shape)
	(deleteShape shape)
	t))

(defun addFixedProp (shape)
    (axlFlushDisplay)
    (axlMsgPut "")
    (axlMsgPut "Adding FIXED Prop To Shape")
    (axlMsgPut "---------------------------------------")
    (axlFlushDisplay)
    (axlShell (sprintf nil 
		       "replay %s/scripts/prop_on" (axlGetVariable "TEST_DIR")))
    t)


(defun deleteClosedShapeTests ()
    (let (shape)
	(setq shape (openTestShape))
	(closeTestShape shape)
	(deleteShapeVoids shape)

	; add fixed prop to shape and try to delete it
	(addFixedProp shape)
	(null (deleteShape (ashFindAllShapes)))
	t))

;; delete of DRC that was added by Allegro Constraints - should fail
(defun deleteAllegroDRC ()
    (let (drcs)
	(closeTestShape (openTestShape))
	(closeTestShape (openTestShape))
	(setq drcs (ashFindAllDrcs))
	(deleteAndPrint drcs "Allegro defined DRCs")
	(axlDeleteObject (ashFindAllShapes))
	t))

;; delete of DRC that was added by AXL
(defun deleteExternalDRC ()
   (let (drc_error)
	(setq drc_error 
	      (car (axlDBCreateExternalDRC "myconstraint" 2.0:2.0 "drc/all")))
	(deleteAndPrint (list drc_error) "AXL defined DRCs")
	t))

(defun deleteDRCTests ()
    (deleteExternalDRC)
    (deleteAllegroDRC)
    t)

(defun deleteShapeTests ()
    (deleteOpenShapeTests)
    (deleteClosedShapeTests)
    t)

(defun axlDeleteTest ()
    (mergeClines)
    (deleteDRCTests)
    (deleteClines)
    (deleteShapeTests)
    t)
