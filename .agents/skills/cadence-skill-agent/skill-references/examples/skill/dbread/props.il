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

;NOTE: requires file ../select/ashfindall.il

;;
;; add_dicts_to_list - places each allegro property name into a unique list
;;
(defun add_dicts_to_list (list_of_names)
    (foreach item list_of_names
	(cond ((eq (memq item dict_list) nil)
	       (setq dict_list (cons item dict_list))))
    )
) ; add_dicts

;;
;; print_list_props - prints the ->? and ->?? retrievals on the propList
;;
(defun print_list_props (list p)
	(foreach item list 
	    (cond ((neq item->prop nil)
	           (pprint item->objType p)
	           (fprintf p ": prop: ")
	           (pprint item->prop p)
		   (fprintf p ":\n")
		   (fprintf p "->? :\n")
		   (pprint item->prop->? p)
		   (add_dicts_to_list item->prop->?)
		   (fprintf p "\n->?? :\n")
	           (pprint item->prop->?? p)
	           (fprintf p "\n\n")
                   ; remember at least on element that has an allegro property
                   (setq has_a_prop item))
	    ) ; cond
	) ; foreach item 
) ; print_list_props

;;
;; do_print - print header and call print_list_prop after applying 
;;            appropriate ash Find function
;;
(defun do_print (p description find_func)
    (let (list)
        (fprintf p "Properties on %s:\n" description)
	(setq list (apply find_func nil))
	(print_list_props list p)
	(fprintf p "\n\n")
    ) ; let
) ; do_print

;;
;; main_test - compile a list of used property definitions by retrieving the 
;;             list of attributes on all elements
;;
(defun main_test (p)
    (let (list)
	(do_print p "Nets" 'ashFindAllNets)
	(do_print p "Components" 'ashFindAllComponents)
	(do_print p "Clines" 'ashFindAllClines)
	(do_print p "Lines" 'ashFindAllLines)
	(do_print p "Clinesegs" 'ashFindAllClinesegs)
	(do_print p "Linesegs" 'ashFindAllLinesegs)
	(do_print p "Symbols" 'ashFindAllSymbols)
	(do_print p "Vias" 'ashFindAllVias)
	(do_print p "Drcs" 'ashFindAllDrcs)
	(do_print p "Pins" 'ashFindAllPins)
	(do_print p "Shapes" 'ashFindAllShapes)
	(do_print p "Text" 'ashFindAllText)
    ) ; let
) ; main_test

;;
;; dict_test - using compiled list of all attribute names, test the property
;;             dictionary attribute retrieval
;;
(defun dict_test (p)
    (fprintf p "Dict Test:\n\n")
    (pprint dict_list p)
    (foreach item dict_list
	(setq dict (axlDBGetPropDictEntry item))
	(pprint dict->? p)
	(pprint dict->?? p)
	(fprintf p "\n\n")
    ) ; foreach
) ; dict_test

;;
;; general_test - test eval, equal illegal attribute, etc
;;
(defun general_test (item file)
    (fprintf file "general test, y is property, z is prop dict\n")
    (setq y (item->prop))
    (setq z (axlDBGetPropDictEntry (car y->?)))
    (setq w (axlDBGetPropDictEntry (car y->?)))

    ; test illegal attribute retrieval
    (fprintf file "Illegal Property Attribute: ")
    (pprint y->illegal file)
    (fprintf file "\n")

    ; illegal propdict attribute
    (fprintf file "Illegal Prop Dict Attribute: ")
    (pprint z->illegal file)
    (fprintf file "\n")

    ; test eval y
    (fprintf file "Eval y: ")
    (pprint (eval y) file)
    (fprintf file "\n")

    ; test eval z
    (fprintf file "Eval z: ")
    (pprint (eval z) file)
    (fprintf file "\n")

    ; test equal y
    (setq x (axlDBGetDesign)->prop)
    (fprintf file "(setq x ((axlDBGetDesign)->prop)) : ")
    (pprint x file)
    (fprintf file "Equal x y?: ")
    (pprint (equal x y) file)
    (fprintf file "\n")

    ; test equal z
    (fprintf file "Equal x z?: ")
    (pprint (equal x z) file)
    (fprintf file "\n")
    (fprintf file "Equal w z?: ")
    (pprint (equal w z) file)
    (fprintf file "\n")

    ; objtype
    (fprintf file "y ObjType: ")
    (pprint y->objType file)
    (pprint y->? file)
    (fprintf file "\n")

    ; objtype
    (fprintf file "z ObjType: ")
    (pprint z->objType file)
    (fprintf file "\n")

    ; ReadOnly
    (fprintf file "Read Only?: ")
    (pprint x->readOnly file)
    (fprintf file "\n")

    ; Access a known property
    (fprintf file "Accessing a known - SCEMATIC_NAME\n")
    (pprint x->SCHEMATIC_NAME file)

    ; again - to test sequential gets of same property
    (fprintf file "Accessing a known - SCEMATIC_NAME\n")
    (pprint x->SCHEMATIC_NAME file)

    ; retrieve a property from the property dictionary
    (pprint w->?? p)
    (pprint w->dataType p)

) ; defun general_test

;;
;; axlpropread_test - main test function for allegro properties and property
;;                    definitions
;;
(defun axlpropread_test ()
    (setq dict_list nil)
    (setq has_a_prop nil)
    (setq p outfile("~/tests/axl/props/bronze.txt", "w"))
    (setq _itemsperline 1)
    (main_test p)
    (dict_test p)
    (general_test has_a_prop p)
    (fprintf p "\n")
    (close p)
) ; defun axlpropread_test

