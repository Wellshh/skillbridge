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


; requires file ../select/ashfindall.il

;;
;; print-path  - function for printing out path symbol to file
;;
(defun print_path (path file)
    (pprint '_axlPath file)
) ; defun print_path

(defun print_figure (figure file)
   (cond ((neq figure nil)
          (fprintf file "(")
          (foreach path figure
              (print_path path file)
          ) ; foreach
          (fprintf file ")\n" ))
	  (t (println nil file)))
) ; defun print_figure

;;
;; print_pad - print out basic description of pad
;;
(defun print_pad (pad file)
    (fprintf file "Pad: %s %s\n" pad->layer pad->type)
    (fprintf file "\tShape: %s\n" pad->figureName)
    (fprintf file "\tFigure: ") (print_figure pad->figure file)
    (foreach path pad->figure
	(fprintf file "\t\tPath: ") (print_path path file)
	(foreach seg path->_pathList
	    (fprintf file "\t\t\tSegment: ") (pprint seg->?? file)
	    (fprintf file "\n")
	) ; foreach seg
    ) ; foreach path
) ; defun print_pad

;;
;; general_test - test axlDBGetPad, illegal attribute, etc
;;
(defun general_test (file)
    (setq y (car (ashFindAllPins)))
    (setq x	 (axlDBGetPad y "ETCH/TOP" "REGULAR"))
    ; test illegal attribute retrieval
    (fprintf file "Illegal Attribute: ")
    (pprint x->illegal file)
    (fprintf file "\n")

    ; test eval
    (fprintf file "Eval x: ")
    (pprint (eval x) file)
    (fprintf file "\n")

    ; test eq
    (setq z (axlDBGetPad y "ETCH/BOTTOM" "ANTI"))
    (fprintf file "Eq x z?: ")
    (pprint (eq x z) file)
    (fprintf file "\n")

    ; test equal
    (fprintf file "Equal x y?: ")
    (pprint (equal x z) file)
    (fprintf file "\n")

    ; objtype
    (fprintf file "ObjType: ")
    (pprint x->objType file)
    (fprintf file "\n")

    ; ReadOnly
    (fprintf file "Read Only?: ")
    (pprint x->readOnly file)
    (fprintf file "\n")

) ; defun general_test

;;
;; fig_test2  - test all padstack pads
;;
(defun fig_test2 (file)
    (let (x)
    (foreach padstack (axlDBGetDesign)->padstacks
	(println padstack->name file)
	(println padstack->startEnd file)
        (foreach pad padstack->pads (print "path: " file) (println pad->type file) 
				    (print "layer: " file) (println pad->layer file)
				    (print "figureName: " file) (println pad->figureName file)
				    (print "Figure: " file) (print_figure pad->figure file)
				    (println "Figure Paths: " file)
				    (cond ((pad->figure)
					   (foreach path pad->figure
					       (print_path path file)
					       (println "" file)
					       (foreach seg path->_pathList
					       (pprint seg->?? file)
					       (println "" file))
					       )))
				    (fprintf file  "\n" ))
    ) ; foreach padstack
    x
    ) ; let
) ; defun
;;
;; fig_test3 - test all pin pads
;;
(defun fig_test3 (file)
    (let ()
    (fprintf file "\n\n->FigTest3\n\n")
    (foreach pin (ashFindAllPins)
	(fprintf file "\n\n\n")
	(print "Pin: " file) (print pin->parent->refdes file) (fprintf file ".") 
			(println pin->number file) (pprint pin->xy file)
	(foreach pad pin->pads
	    ;(fprintf file "\nSingleQuestion: ")
	    ;(pprint pad->? file)
	    (fprintf file "\nDoubleQuestion: \n");
	    (setq dq pad->??)
	    ; avoid printing out array[] for pad path defstruct
	    (foreach a dq
		(cond ((listp a)
		       (cond ((arrayp (car a))
			       (print_figure a file)
			       (fprintf file "\n"))
			      (t (println a file))
		       ) ; cond arrayp
		       )
		       (t (println a file))
		) ; cond listp
	    ) ; foreach
	    (fprintf file "\n\n");
	    (print_pad pad file)
	) ; foreach pad
    ) ; foreach pin
    ) ; let
) ; defun

;;
;; fig_test6 - test via pads
;;
(defun fig_test6 (file)
    (foreach via (ashFindAllVias)
	(fprintf file "\n\n\n")
	(print "Via: @" file) (print via->xy file) (fprintf file "\n")
	(foreach pad via->pads
	    (fprintf file "\nSingleQuestion: ")
	    (pprint pad->? file)
	    (fprintf file "\nDoubleQuestion: \n");
	    (setq dq pad->??)
	    ; avoid printing out array[] for pad path defstruct
	    (foreach a dq
		(cond ((listp a)
		       (cond ((arrayp (car a))
			       (print_figure a file)
			       (fprintf file "\n"))
			      (t (println a file))
		       ) ; cond arrayp
		       )
		       (t (println a file))
		) ; cond listp
	    ) ; foreach
	    (fprintf file "\n\n");
	    (print_pad pad file)
	) ; foreach pad
    ) ; foreach via
) ; defun

;;
;; fig_test4 - test pin outline by adding to the drawing
;;
(defun fig_test4 (file)
    (foreach pin (ashFindAllPins)
	(foreach pad pin->pads
	    ; filter out all etch regular pads
	    (setq strings (parseString pad->layer "/"))

	    ; if the first string is ETCH
	    (cond ( (eq (strcmp "ETCH" (car strings)) 0)

		    ; if this is a REGULAR pod
		    (cond ( (eq (strcmp "REGULAR" pad->type) 0)

			      ; set the subclass to MANUFACTURING/xxx-REGULAR
			      (setq new_subclass (strcat "MANUFACTURING/" (cadr strings) "-REGULAR"))
			      ; and add each path defining the shape to the layout
			      (foreach path pad->figure
				  (print_pad pad file)
			          (axlDBCreatePath path new_subclass nil nil)
			      ) ; foreach
			      ) ; is regular pad
		      ) ; cond
                  ) ; is etch
            ) ; cond 
	) ; foreach pad
    ) ; foreach pin
) ; defun

;;
;; fig_test5 - test via pad outline by adding to drawing
;;
(defun fig_test5 (file)
    (foreach pin (ashFindAllVias)
	(foreach pad pin->pads
	    ; filter out all etch regular pads
	    (setq strings (parseString pad->layer "/"))

	    ; if the first string is ETCH
	    (cond ( (eq (strcmp "ETCH" (car strings)) 0)

		    ; if this is a REGULAR pod
		    (cond ( (eq (strcmp "REGULAR" pad->type) 0)

			      ; set the subclass to MANUFACTURING/xxx-REGULAR
			      (setq new_subclass (strcat "MANUFACTURING/" (cadr strings) "-REGULAR"))
			      ; and add each path defining the shape to the layout
			      (foreach path pad->figure
				  (print_pad pad file)
			          (axlDBCreatePath path new_subclass nil nil)
			      ) ; foreach
			      ) ; is regular pad
		      ) ; cond
                  ) ; is etch
            ) ; cond 
	) ; foreach pad
    ) ; foreach pin
) ; defun


;;
;; fig_test - call all figure tests
;;
(defun fig_test ()
    (let ((file outfile("~/tests/axl/pads/bronze.txt", "w")))
	(setq _itemsperline 1)
	(general_test file)
 	(fig_test2 file)
	 (fig_test3 file)
	 (fig_test4 file)
	 (fig_test5 file)
	 ; (fig_test6 file)
	(close file)
    ) ; let
) ; defun
