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
;; axldbctsym.il - axlDBCreateSymbol test driver
;;

; TODO
;   symbols with shapes in it, pads as shapes, shape symbols
;   

(defun dbc_sym_t1 ()
	(axlMsgPut "**Starting dbc_sym_t1")
	;; simple refdes
	(axlDBCreateSymbol "r9" 0.7:6.3)

	;; simple refdes - DRC created
	(axlDBCreateSymbol "R8" 0.2:6.3)

	;; format symbol
	(axlDBCreateSymbol (list "target" "format") 1.5:7.0)

	;; mechanical symbol
	(axlDBCreateSymbol (list "mtg156" "Mechanical") 3.0:7.0)
)
(defun dbc_sym_t2 ()
	(axlMsgPut "**Starting dbc_sym_t2")
	;; package symbols - no refdes - various rotations and mirror
	(axlDBCreateSymbol (list "DIP14_3" nil) 2.8:6.1 nil 340)
	(axlDBCreateSymbol (list "DIP14_3") 3.6:6.1 nil 20)
	(axlDBCreateSymbol (list "DIP14_3" "package") 4.6:6.1 nil 110)
	(axlDBCreateSymbol (list "DIP14_3" "package") 6.0:5.8 nil 220)
	(axlDBCreateSymbol (list "DIP14_3" "package") 3:4.7 t 350)
	(axlDBCreateSymbol (list "DIP14_3" "package") 3.6:4.7 t 10)
	(axlDBCreateSymbol (list "DIP14_3" "package") 4.6:4.7 t 130)
	(axlDBCreateSymbol (list "DIP14_3" "package") 5.8:4.7 t 220)

	;; extents just in drawing
	(axlDBCreateSymbol (list "res400" "package") 0.052:8.059)
)
(defun dbc_sym_te_args ()
	(axlMsgPut "**Starting dbc_sym_te_args")

	;; illegal refdes or list
	(axlDBCreateSymbol 777 1:8.4)

	;; illegal location
	(axlDBCreateSymbol "r20" (list "8" "4"))

	;; illegal list contents
	(axlDBCreateSymbol nil 1:8.4)	; no error reported is OK
	(axlDBCreateSymbol (list 666) 1:8.4)
	(axlDBCreateSymbol (list "dip14" 555) 1:8.4)
	(axlDBCreateSymbol (list "able" "packadack") 1:8.4)

	;; illegal mirror
	(axlDBCreateSymbol "R20" 1:8.4 "mirror_error")
	(axlDBCreateSymbol "R20" 1:8.4 7)

	;; illegal rotate code
	(axlDBCreateSymbol "R20" 1:8.4 t "abc")

	;; illegal symbol name
	(axlDBCreateSymbol (list "dip#$%14") 1:8.4)
)
(defun dbc_sym_te_loc ()
	(axlMsgPut "**Starting dbc_sym_te_loc")

	;; coordinate out of drawing
	(axlDBCreateSymbol "R20" 1:9.0)

	;; extents not in drawing
	(axlDBCreateSymbol "R20" 1:8.4)

	;; extents out of drawing - text
	(axlDBCreateSymbol "R20" 0.052:8.059)
)
(defun dbc_sym_te_refdes ()
	(axlMsgPut "**Starting dbc_sym_te_refdes")

	;; already placed
	(axlDBCreateSymbol "r7" 1.7:6.3)
	;; refdes not in database
	(axlDBCreateSymbol "zoo" 0.7:6.3)
)
(defun dbc_sym_test ()
	(dbc_sym_t1)
	(dbc_sym_t2)
	(dbc_sym_te_args)
	(dbc_sym_te_loc)
	(dbc_sym_te_refdes)
)
