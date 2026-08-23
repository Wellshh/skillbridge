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
;; axldbcttext.il - axlDBCreateText test driver
;;

; uncomment if want to see results from axlDBCreateText printed.
(defun dbc_text_print (return)
        ;(if return (foreach txt (car return) (pprint (get txt '??))))
        return)

(defun dbc_text_t1 ()
	(axlMsgPut "**Starting dbc_text_t1")
	;; text block provided instead of text orientation record
	(dbc_text_print
	    (axlDBCreateText "test text line" 3.7:0.6 "1"
		"BOARD GEOMETRY/DIMENSION")))

(defun dbc_text_t2 ()
	(axlMsgPut "**Starting dbc_text_t2")
	;; left justified, mirrored, rotated
	(dbc_text_print
	    (axlDBCreateText "FFFRRRBBB" 3.8:1.2
	        (make_axlTextOrientation ?textBlock "3" ?rotation 90
		    ?mirrored t ?justify "left")
		"BOARD GEOMETRY/DIMENSION"))
	;; right justified, not mirrored
	(dbc_text_print
	    (axlDBCreateText "FFFLLLEEE" 3.8:1.2
	        (make_axlTextOrientation ?textBlock "3" ?rotation 75
		    ?mirrored nil ?justify "right")
					"BOARD GEOMETRY/DIMENSION"))
	;; center justified
	(dbc_text_print
	    (axlDBCreateText "FFFCCCTTT" 3.8:1.2
	        (make_axlTextOrientation ?textBlock "3" ?rotation 180
		    ?mirrored t ?justify "center")
		"BOARD GEOMETRY/DIMENSION"))
	;; orientation specified, but textBlock only, others default
	(dbc_text_print
	    (axlDBCreateText "FFFRRRSSS" 3.8:1.2
	        (make_axlTextOrientation ?textBlock "3")
		"BOARD GEOMETRY/DIMENSION"))
)

(defun dbc_text_t3 ()
	(axlMsgPut "**Starting dbc_text_t3")
	;; multiline text - unrotated
	(dbc_text_print
	    (axlDBCreateText "Line 1\nLine 2\nLine 3 is a longer one"
		5.7:7.8 "1" "BOARD GEOMETRY/DIMENSION"))

	;; multiline - rotated -30
	(dbc_text_print
	    (axlDBCreateText "Line 1A\nLine 2A\nLine 3A is a longer one"
		5.7:7.6
	        (make_axlTextOrientation ?textBlock "1" ?rotation -30)
		"BOARD GEOMETRY/DIMENSION"))

	;; multiline - rotated 157.5
	(dbc_text_print
	    (axlDBCreateText "Line 1B\nLine 2B\nLine 3B is a longer one"
		5.5:7.2
	        (make_axlTextOrientation ?textBlock "1" ?rotation 157.5)
		"BOARD GEOMETRY/DIMENSION"))

	;; multiline - rotated 270
	(dbc_text_print
	    (axlDBCreateText "Line 1C\nLine 2C\nLine 3C is a longer one"
		5.8:7.3
	        (make_axlTextOrientation ?textBlock "1" ?rotation 270)
		"BOARD GEOMETRY/DIMENSION"))

	;; multiline - mirrored
	(dbc_text_print
	    (axlDBCreateText "Line 1D\nLine 2D\nLine 3D is a longer one"
		5.6:7.8
	        (make_axlTextOrientation ?textBlock "1" ?rotation 45
		    ?mirrored t)
		"BOARD GEOMETRY/DIMENSION"))
)

(defun dbc_text_te_args ()
	(axlMsgPut "**Starting dbc_text_te_args")
	;; bad location
	(axlDBCreateText "foo" (list "1:6") "1")

	;; bad layer
	(axlDBCreateText "foo" 1:6 "1" "etch/tipple")

	;; string takes it out of extents
	(axlDBCreateText "out of extents" 11.4:0.6 "1"
	    "BOARD GEOMETRY/DIMENSION")

	;; rotate it out of extents
	(axlDBCreateText "out of extents" 0.2:0.6
	    (make_axlTextOrientation ?textBlock "1" ?rotation 180)
	    "BOARD GEOMETRY/DIMENSION")

	;; orientation not a string 
	(axlDBCreateText "test text line" 3.7:0.6 777 "PIN/TOP")

	;; orientation an incorrect defstruct
	(axlDBCreateText "test text line" 3.7:0.6 
	    (make_axlFill) "PIN/TOP")
)

(defun dbc_text_te_text ()
	(axlMsgPut "**Starting dbc_text_te_text")

	;; textBlock out of range - textBlock not textOrientation
	(axlDBCreateText "foo" 1:6 "99")

	;; textBlock out of range
	(axlDBCreateText "foo" 1:6 (make_axlTextOrientation ?textBlock "98"))

	;; textBlock not a string
	(axlDBCreateText "foo" 1:6 (make_axlTextOrientation ?textBlock 19))

	;; bad rotation
	(axlDBCreateText "foo" 1:6
	        (make_axlTextOrientation ?textBlock "3" ?rotation "badrot"
		    ?mirrored nil ?justify "right"))

	;; bad mirror
	(axlDBCreateText "foo" 1:6
	        (make_axlTextOrientation ?textBlock "3" ?rotation 0
		    ?mirrored "badmir" ?justify "right"))

	;; bad justify
	(axlDBCreateText "foo" 1:6
	        (make_axlTextOrientation ?textBlock "3" ?rotation 0
		    ?mirrored nil ?justify "anywhere"))
)

(defun dbc_text_tparent ()
        ;; attached text
    (let ((sym (car (axlDBCreateSymbol "r6" 2.4:4.3))))
	(dbc_text_print
	    ; this is legal according to axl, even though Allegro would
	    ;  normally want this text attached to a PLACE_BOUND rectangle
            (axlDBCreateText "25" 2.5:4.5 "3"
	        "PACKAGE GEOMETRY/PLACE_BOUND_TOP" sym))
	(dbc_text_print
	    (axlDBCreateText "r666" 2.5:4.6 "2" "REF DES/ASSEMBLY_TOP" sym))
	(dbc_text_print
	    (axlDBCreateText "r666" 2.5:4.4 "2" "ETCH/TOP" sym))
))

(defun dbc_text_te_parent ()
        ;; attached to sym def - illegal
    (let ((sym (car (axlDBCreateSymbol "r9" 0.7:6.3))))
	(axlDBCreateText "25" 2.5:4.5 "3"
	    "PACKAGE GEOMETRY/PLACE_BOUND_TOP" (get sym 'definition))
))

(defun dbc_text_te_layer ()
	(axlMsgPut "**Starting dbc_text_te_layer")
	;; illegal class
	(axlDBCreateText "test text line" 3.7:0.6 "1" "PIN/TOP")
)

(defun dbc_text_test ()
	(dbc_text_t1)
	(dbc_text_t2)
	(dbc_text_t3)
	(dbc_text_te_args)
	(dbc_text_te_layer)
	(dbc_text_te_text)
	(dbc_text_tparent)
	(dbc_text_te_parent)
	nil
)
