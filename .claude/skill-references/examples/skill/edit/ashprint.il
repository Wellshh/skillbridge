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



;; ash_print_path - prints out a title for a path
(defun ash_print_path (path file)
    (pprint '_axlPath file)
) ; defun ash_print_path

;; ash_print_figure - prints out a figure's attributes
(defun ash_print_figure (figure file)
   (cond ((neq figure nil)
          (fprintf file "(")
          (foreach path figure
              (ash_print_path path file)
          ) ; foreach
          (fprintf file ")\n" ))
	  (t (println nil file)))
) ; defun ash_print_figure

;; ash_print_pad - prints out an AXL pad's attributes
(defun ash_print_pad (pad file)
    (fprintf file "Pad: %s %s\n" pad->layer pad->type)
    (fprintf file "\tShape: %s\n" pad->figureName)
    (fprintf file "\tFigure: ") (ash_print_figure pad->figure file)
    (foreach path pad->figure
	(fprintf file "\t\tPath: ") (ash_print_path path file)
	(foreach seg path->_pathList
	    (fprintf file "\t\t\tSegment: ") (pprint seg->?? file)
	    (fprintf file "\n")
	) ; foreach seg
    ) ; foreach path
) ; defun ash_print_pad


(setq objTypePrintTable 
      '((arc		(lambda (x) (sprintf nil "%s %L %L\n\t%L %L %L %s"
					     (cond 
						((equal x->parent->objType 
							"polygon")
						    "VOIDSEG")
						((equal x->parent->objType
							"shape")
						    "SHAPESEG")
						(x->parent->branch "CLINESEG")
						   (t "LINESEG"))
					     x->layer 
					     (cond (x->net x->net->name))
					     x->startEnd 
					     x->xy 
					     x->width
					     (cond (x->isClockwise "CW") 
						   (t "CCW")))))

	(component	(lambda (x) (sprintf nil "%L %L" 
					     x->name x->deviceType)))

	(design		(lambda (x) ""))

	(drc		(lambda (x) (sprintf nil "%L %L %L" 
					     x->layer x->type x->xy)))

	(line		(lambda (x) (sprintf nil "%s %L %L\n\t%L %L" 
					     (cond 
						((equal x->parent->objType 
							"polygon")
						   "VOIDSEG")
						((equal x->parent->objType
							"shape")
						    "SHAPESEG")
						(x->parent->branch 
						    "CLINESEG")
						(t "LINESEG"))
					     x->layer 
					     (cond (x->net x->net->name))
					     x->startEnd x->width)))

	(path		(lambda (x) (sprintf nil "%s %L %L %L" 
					     (cond (x->branch "CLINE")
						   (t "LINE"))
					     x->layer 
					     (cond (x->net x->net->name))
					     x->bBox)))

	(pin		(lambda (x) (sprintf nil "\"%s.%s\" %L %L"
			 		     (cond
						(x->parent->refdes 
						    x->parent->refdes)
						(t x->parent->name))
					     x->number
					     (cond (x->net x->net->name))
					     x->xy)))

	(net		(lambda (x) (sprintf nil "%L" x->name)))

	(polygon	(lambda (x) (sprintf nil "%s %L %L %L" 
					     (cond (x->isRect "RECT")
						   ((equal x->parent->objType 
							   "shape")
							   "VOID")
						   (t "SHAPE"))
					     x->layer
					     (cond (x->net x->net->name))
					     x->bBox)))

	(shape		(lambda (x) (sprintf nil "%s %L %L %L" 
					     (cond (x->isRect "FRECT") 
						   (t "SHAPE"))
					     x->layer
					     (cond (x->net x->net->name))
					     x->bBox)))

	(symbol		(lambda (x) (sprintf nil "%L %L %L %L %s" 
					     x->refdes x->name 
					     x->xy x->rotation
					     (cond (x->isMirrored "MIRRORED")
						   (t "")))))

	(text		(lambda (x) (sprintf nil "%L %L %L %s %s" 
					     x->text x->layer 
					     x->rotation 
					     x->justify
					     (cond (x->isMirrored "MIRRORED")
						   (t "")))))

	(via		(lambda (x) (sprintf nil "%L %L %L %L" 
					     x->name 
					     (cond (x->net x->net->name))
					     x->startEnd x->xy)))))

;; ashPrintObjData - prints short description of a database object
(defun ashPrintObjData (item)
    (let (tableEntry itemString)
	(cond 
	    ((null item->objType)
		(printf "<no objType> %L %L\n" item item->??))
	    ((setq tableEntry (assq (concat item->objType) objTypePrintTable))
		(sprintf itemString "<%s> %s" item->objType 
						(funcall (cadr tableEntry) item))
		(printf "%s\n" itemString)
		itemString)
	    (t nil))))

(defun ashPrintObjList (itemList)
    (mapc 'ashPrintObjData itemList)
    t)

(defun ashDiffObjList (listA listB)
    (let (shortList longList diffList shortL longL (shortCount 1) (longCount 1))
	(cond
	    ((greaterp (length listA) (length listB))
		(setq shortL "B")
		(setq longL "A")
		(setq longList listA)
		(setq shortList listB))
	    (t
		(setq shortL "A")
		(setq longL "B")
		(setq shortList listA)
		(setq longList listB)))
    
	(while longList
	    (cond
		((eq (car shortList) (car longList))
		    (setq shortCount (plus shortCount 1))
		    (setq shortList (cdr shortList)))
		((equal (car shortList) (car longList))
		    (printf "%s%L/%s%L \"equal\" but not \"eq\"\n\t"
			    shortL shortCount longL longCount)
		    (ashPrintObjData (car shortList))
		    (setq shortCount (plus shortCount 1))
		    (setq shortList (cdr shortList)))
		(t
		    (printf "%s%L/%s%L\t" shortL shortCount longL longCount)
		    (ashPrintObjData (car longList))))

	    (setq longList (cdr longList))
	    (setq longCount (plus longCount 1)))

	(when shortList
	    (printf "list%s Remainder\n" shortL)
	    (ashPrintObjList shortList))
	t))
