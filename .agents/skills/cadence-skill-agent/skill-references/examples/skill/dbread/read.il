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

;NOTE: requires files ../select/ashfindall.il and ../ash/ashprint.il

;;
;; print_title - function to print any string to the specified port
;;
(defun print_title (string port)
    (fprintf port "\n\n%s\n\n" string)
) ; defun print_title

;;
;; Local function my_print, which all test functions call, and
;; which may change the way items are printed out everywhere
;;
(defun my_print (list port)
    (pprint list port)
) ; my_print

;;
;; test_a_symdef - test symdef to evaluate special 'owner' type stuff
;;
(defun test_a_symdef (p)
    (let (dsn sdf child)
        (print_title "Symdef Test:" p)
	(foreach sdf (axlDBGetDesign)->symdefs
	    (fprintf p "\n\n Symdef: %s Children:\n\n", sdf->name)
	    (foreach child
	        sdf->children
	        (my_print child->?? p)
	    ) ; foreach sdf child
	) ; foreach sdf
    ) ; test_a_symdef
) ; defun test_a_symdef

;;
;; test_general - test eval, eq, is dbid, etc
;;
(defun test_general (p)
    (let (x y)
	(setq x (axlDBGetDesign))
        ; test the refresh function
        (axlDBRefreshId x)
        ; test the isDBIDType function
        (fprintf p "Is design dbid? %s\n", (axlIsDBIDType x))
        ; test the eval function
        (fprintf p "Eval of x: %s\n", (eval x))
	; test the eq function
	(setq y (car x->symdefs))
	(fprintf p "Eq x y?: %s\n", (cond ((equal x y)
					   ("t"))
					   ("nil")))
	; test the singlequestion attr retrieval
	(my_print x->? p)
	; test illegal attr retrieval
	(my_print x->dummy p)
    ) ; let
) ; defun test_general

;;
;; test_design - check out design attributes
;;
; retrieve the design    /* axlDBGetDesign */
;    print out all attributes of the design
;    for each symbol definition
;	print out the attributes of each symbol definition
;    for each padstack definition
;	print out all attributes of the padstack
;	for each padstack pad
;	    print out all attributes of the pad
(defun test_design (p)
    (let ((dsn (axlDBGetDesign))
	  (branches (axlDBGetLonelyBranches))
	  padstack pad symdef)
	(print_title "Design:" p)
	(my_print dsn->?? p)
	(print_title "Symbol Definitions:" p)
	(foreach symdef dsn->symdefs
	    (print_title "symdef:" p)
	    (my_print symdef->?? p)
	) ; foreach symdef
	(print_title "Padstacks:" p)
	(foreach padstack dsn->padstacks
	    (print_title "padstack:" p)
	    (my_print padstack->?? p)
	    (print_title "Pads:" p)
	    (foreach pad padstack->pads
	        (print_title "pad:" p)
		(ash_print_pad pad p)
	    ) ; foreach pad
	) ; foreach padstack
    ) ; let
) ; defun test_design

;;
;; test_branches - test branch attribute retrieval
;;
; retrieve the standalone branch list /* axlDBGetLonelyBranches */
;    print out all attributes of each branch
(defun test_branches (p)
    (let (branch)
	(print_title "Lonely Branches:" p)
        (foreach branch (axlDBGetLonelyBranches)
	    (print_title "branch:" p)
	    (my_print branch->?? p)
        ) ; foreach branch
    ) ; let
) ; defun test_branches

;;
;; test_nets - test net attribute retrieval
;;
;find all nets
;    print out all attributes of each net
;    for each net branch
;	for each branch child
;	    if the child is a "tee"
;		print out all attributes of the "tee"
(defun test_nets (p)
    (let ((nets (ashFindAllNets))
	   net branch branch_item)
        (foreach net
	    nets
	    (my_print net->?? p)
	    (foreach branch
	        net->branches
	        (foreach branch_item
	            branch->children
		    (cond ((eq branch_item->objType "tee")
		         (fprintf p "\n\n!! Found a T: !!\n\n")
			 (my_print branch_item->?? p))
		    ) ; cond
		) ; foreach branch_item
	    ) ; foreach branch
	) ; foreach net
    ) ; let
) ; defun test_nets

;;
;; test_comps - test component attribute retrieval
;;
;find all components 
;    print out all attributes of each component
(defun test_comps (p)
    (let ((comps (ashFindAllComponents))
	   comp)
	(foreach comp
	    comps
	    (my_print comp->?? p)
	) ; foreach
    ) ; let
) ; cond test_comps


;;
;; test_paths - test path attribute retrieval
;;
;find all paths
;    print out all attributes of each path
(defun test_paths (p)
    (let ((cpaths (ashFindAllClines))
	  (paths (ashFindAllLines))
	   path)
	(foreach path
	    cpaths
	    (my_print path->?? p)
	) ; foreach path cpaths
	(foreach path
	    paths
	    (my_print path->?? p)
	) ; foreach path paths
    ) ; let
) ; defun test_paths

;; 
;; test_segments - test line and arc segment attribute retrieval
;;
;find all lines (non-arc line segments)
;    print out all attributes of each line
;find all arcs (non-straight line segments)
;    print out all attributes of each arc
(defun test_segments (p)
    (let ((csegments (ashFindAllClinesegs))
          (segments (ashFindAllLinesegs))
	  segment)
	(foreach segment
		 csegments
		 (my_print segment->?? p)
        ) ; foreach
	(foreach segment
		 segments
		 (my_print segment->?? p)
        ) ; foreach
    ) ; let
) ; defun test_branches

;;
;; test_symbols - test attribute retrieval for symbols
;;
;find all symbols
;    print out all attributes of each symbol
(defun test_symbols (p)
    (let ((symbols (ashFindAllSymbols))
	   symbol)
	(foreach symbol
	    symbols
	    (my_print symbol->?? p)
	) ; foreach symbol
    ) ; let
) ; test_symbols

;;
;; test_vias - test attribute retrieval for vias
;;
;find all vias
;    print out all attributes of each via
(defun test_vias (p)
    (let ((vias (ashFindAllVias))
	   via)
	(foreach via
	    vias
	    (my_print via->?? p)
	) ; foreach via
    ) ; let
) ; defun test_vias

;;
;; test_drcs  - test attribute retrieval for all DRC errors
;;
;find all DRC errors
;    print out all attributes of each DRC
(defun test_drcs (p)
    (let ((drcs (ashFindAllDrcs))
	   drc)
        (foreach drc
	    drcs
	    (my_print drc->?? p)
	) ; foreach
    ) ; let
) ; defun test_drcs

;;
;; test_pins - test attribute retrieval for pins
;;
;find all pins
;    print out all attributes of each pin
(defun test_pins (p)
    (let ((pins (ashFindAllPins))
	   pin)
	(foreach pin
	    pins
	    (my_print pin->?? p)
	) ; foreach pin
    ) ; let
) ; defun test_pins

;;
;; test_shapes - test attribute retrieval for shapes
;;
;find all shapes and rectangles
;    print out all attributes of each shape
(defun test_shapes (p)
    (let ((shapes (ashFindAllShapes))
	   shape segment void)
	(foreach shape
	    shapes
	    (my_print shape->?? p)
	    (foreach segment
		shape->segments
		(my_print segment->?? p)
	    ) ; foreach shape segment
	    (fprintf p "\n\nShape Voids Start:\n\n")
	    (foreach void
		shape->voids
		(my_print void->?? p)
	    ) ; foreach void
	    (fprintf p "\n\nShape Voids End:\n\n")
	) ; foreach shape
    ) ; let
) ; defun test_shapes

;;
;; test_text - test attribute retrieval for text
;;
;find all text
;    print out all attributes of text
;
(defun test_text (p)
    (let ((all_text (ashFindAllText))
	   text)
	(foreach text
	    all_text
	    (my_print text->?? p)
	    (my_print text->parent->?? p)
	) ; foreach text
    ) ; let
) ; defun test_text

;;
;; axldbread_test - function to exercise the attribute retrieval for all db
;;
(defun axldbread_test ()
    (setq p outfile("~/tests/axl/dbid/bronze.txt", "w"))
    ; because initialization is not happening automatically yet, call manually
    ; (axlDBIDInit)
    (setq _itemsperline 1)
    (fprintf p "\n\ntest_general:\n\n")
    (test_general p)
    (fprintf p "\n\ntest_a_symdef:\n\n")
    (test_a_symdef p)
    (fprintf p "\n\ntest_design:\n\n")
    (test_design p)
    (fprintf p "\n\ntest_branches:\n\n")
    (test_branches p)
    (fprintf p "\n\ntest_segments:\n\n")
    (test_segments p)
    (fprintf p "\n\ntest_nets:\n\n")
    (test_nets p)
    (fprintf p "\n\ntest_comps:\n\n")
    (test_comps p)
    (fprintf p "\n\ntest_paths:\n\n")
    (test_paths p)
    (fprintf p "\n\ntest_symbols:\n\n")
    (test_symbols p)
    (fprintf p "\n\ntest_vias:\n\n")
    (test_vias p)
    (fprintf p "\n\ntest_drcs:\n\n")
    (test_drcs p)
    (fprintf p "\n\ntest_pins:\n\n")
    (test_pins p)
    (fprintf p "\n\ntest_shapes:\n\n")
    (test_shapes p)
    (fprintf p "\n\ntest_text:\n\n")
    (test_text p)
    ; because cleanup is not happening automatically yet, call manually
    ; (axlDBIDCleanup)
    (fprintf p "\n")
    (close p)
) ; defun axldbread_test
