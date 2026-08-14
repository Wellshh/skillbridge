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



; Table of selection keywords and object types
(setq tselectTypes  
	'(("COMPONENTS"	("component"))
	  ("SYMBOLS"	("symbol"))
	  ("NETS"	("net"))
	  ("PINS"	("pin"))
	  ("VIAS"	("via"))
	  ("CLINES"	("path"))
	  ("CLINESEGS"	("line" "arc"))
	  ("LINES"	("path"))
	  ("LINESEGS"	("line" "arc"))
	  ("SHAPES"	("polygon" "shape"))
	  ("SHAPESEGS"	("line" "arc"))
	  ("VOIDS"	("polygon"))
	  ("VOIDSEGS"	("line" "arc"))
	  ("FIGURES"	("figure"))
	  ("DRCS"	("drc"))
	  ("TEXT"	("text"))))

; tselGetObjectTypeData - returns selection type table
(defun tselGetObjectTypeData ()
    tselectTypes)

; tselGetObjectTypes - returns list of find filter keywords
(defun tselGetObjectTypes ()
    (mapcar 'car tselectTypes))

; tselCopyList - Copy a list of objects and sort it
(defun tselCopyList (inList @optional (cmpFunc 'alphalessp) "lg")
    (sort (copy inList) cmpFunc)
)


; tselListEqual - Test that two list have the same contents
(defun tselListEqual (wasList expList 
		     @optional (funcName nil) (cmpFunc 'alphalessp) "lltg")
    (let (sortedWasList sortedExpList (listEqual t))
	(setq sortedWasList (tselCopyList wasList cmpFunc))
	(setq sortedExpList (tselCopyList expList cmpFunc))
	(when (nequal sortedWasList sortedExpList)
	    (setq listEqual nil)
	    (when funcName
		(print "List Compare Error For ")
		(println funcName)
		(print "    Was: ")
		(println sortedWasList)
		(print "    Expected: ")
		(println sortedExpList)
	    )
	)

	listEqual
    )
)


; tselEchoResults - print a message which shows the results of a completed test 
(defun tselEchoResults (description testPass)
    (axlFlushDisplay)
    (printf "%s - " description)
    (cond
	(testPass (printf "PASSED\n")
	t)
	(t (printf "FAILED\n")
	nil)))


; tselObjName - returns an objects name
(defun tselObjName (obj) obj->name)

;tselDeviceType - returns a components device type
(defun tselDeviceType (obj) obj->deviceType)

; tselMakeObjTypeList - Make a list which contains object types and a list
;	of objects that are of that type.
;	(list objectType (list object1 object2 ...))
;	objectType is a string defined by the caller by nameFunc which
;		takes an object and returns a string that types it.
;	Example:
;		(deviceType	(list of components))
(defun tselMakeObjTypeList (objList @optional (nameFunc 'tselObjName))
    (let (sortObjs objTypeList objName curObjList)
	(setq sortObjs (tselCopyList objList 
				    '(lambda (obj1 obj2)
					 (alphalessp (funcall nameFunc obj1)
						     (funcall nameFunc obj2)))))
	(foreach obj sortObjs
	    (cond
		((nequal (funcall nameFunc obj) objName)
		    (when curObjList
			(setq objTypeList (cons (list objName curObjList) 
						objTypeList))
			(setq curObjList nil))
		    (setq objName (funcall nameFunc obj))))
		(setq curObjList (cons obj curObjList)))
	objTypeList))


; tselTestObjType - test that an object is correct type for given findfilter
;	keyword
(defun tselTestObjType (funcName foundItems objTypeData)
    (let ((testPass t) objTypeList findType)
	(setq findType (car objTypeData))
	(setq objTypeList (cadr objTypeData))

	(foreach item foundItems
	    (cond
		((null (member item->objType objTypeList))
		    (printf "%s: objType %L not in list [%L]\n"
			    funcName item->objType objTypeList)
		    (setq testPass nil))
		((null (tselTestShapeType item findType))
		    (printf "%s: Wrong shape type %L\n"
			    funcName findType)
		    (setq testPass nil))
		((null (tselTestPolygonType item findType))
		    (printf "%s: Wrong polygon type %L %L %L\n"
			    funcName findType item->isRect 
			    item->parent->objType)
		    (setq testPass nil))
		((null (tselTestPathType item findType))
		    (printf "%s: Wrong path type %L %L %L\n"
			    funcName findType item->branch)
		    (setq testPass nil))
		((null (tselTestSegType item findType))
		    (printf "%s: Wrong seg parent %L %L %L %L\n"
			    funcName findType 
			    item->parent->objType item->parent->branch)
		    (setq testPass nil))))

	testPass))

; tselTestShapeType - extra checks to make sure that the right kind of
;	shape was found
(defun tselTestShapeType (item findType)
    (cond
	; if not a shape, return t
	((nequal item->objType "shape")
	    t)
	(t (equal findType "SHAPES"))))

; tselTestPolygonType - extra checks to make sure that the right kind of
;	polygon was found
(defun tselTestPolygonType (item findType)
    (cond
	; if not a polygon, return t
	((nequal item->objType "polygon")
	    t)
	((equal findType "RECTANGLES")
	    item->isRect)
	((equal findType "VOIDS")
	    (equal item->parent->objType "shape"))
	((equal findType "SHAPES")
	    (nequal item->parent->objType "shape"))
	(t nil)))

; tselTestPathType - extra checks to make sure that the right kind of
;	path was found
(defun tselTestPathType (item findType)
    (cond
	; if not a path,  return t
	((nequal item->objType "path")
	    t)
	((equal findType "CLINES")
	    (cond (item->branch t) (t nil)))
	((equal findType "LINES")
	    (cond (item->branch nil) (t t)))
	(t nil)))


; tselTestSegType - extra checks to make sure that the right kind of
;	segment was found
(defun tselTestSegType (item findType)
    (cond
	; if not line or arc then not a segment.  return t
	((null (or (equal item->objType "line") (equal item->objType "arc")))
	    t)

	((equal findType "LINESEGS")
	    (and (null item->parent->branch) 
		 (equal item->parent->objType "path")))

	((equal findType "CLINESEGS")
	    (and item->parent->branch (equal item->parent->objType "path")))

	((equal findType "VOIDSEGS")
	    (equal item->parent->objType "polygon"))

	((equal findType "SHAPESEGS")
	    (equal item->parent->objType "shape"))
	(t 
	    (printf "tselTestSegType: Unknown segment type %L\n" findType)
	    nil)))

