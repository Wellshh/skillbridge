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
;; axldbctdrc.il - axlDBCreateExternalDRC test driver
;;

; uncomment for print information
(defun dbc_drc_print (return)
        ;(if return (pprint (get (car return) '??)))
        return)

(defun dbc_drc_t1 ()
	(axlMsgPut "**Starting dbc_drc_t1")
	;; simple drc - no value
	(dbc_drc_print (axlDBCreateExternalDRC "Speed less than 13"
	    	5.0:3.2 "DRC/ALL"))
	;; simple drc - with value
	(dbc_drc_print (axlDBCreateExternalDRC "Speed less than 13"
	    	5.2:3.2 "DRC/TOP" nil nil "14.73 seconds/furlong"))
	;; simple drc - with empty string value
	(dbc_drc_print (axlDBCreateExternalDRC "Speed less than 13"
	    	5.4:3.2 "DRC/BOTTOM" nil nil ""))
)
(defun dbc_drc_t2 ()
	(axlMsgPut "**Starting dbc_drc_t2")
    (let ( (r1 (caar (axlDBCreateLine (list 5:2 5.6:3.2) nil "ETCH/TOP")))
    	   (r2 (caar (axlDBCreateLine (list 6:3.4 6.2:3.6) nil "ETCH/TOP"))))
	;; point to objects, include a second point
	(dbc_drc_print (axlDBCreateExternalDRC "My line-line < 13 feet"
	    	5.6:3.2 "DRC/ALL" (list r1 r2) 6:3.4 "15 feet"))
	;; only one object in list, include a second point
	(dbc_drc_print (axlDBCreateExternalDRC "My line-line < 13 feet"
	    	5.8:3.2 "DRC/INTERNAL_1" (list r1) 6:3.4 "15 feet"))
	;; duplicates in object list, include a second point
	(dbc_drc_print (axlDBCreateExternalDRC "My line-line < 13 feet"
	    	6.0:3.2 "DRC/PACKAGE_TOP" (list r1 r2 r2 r1) 6:3.4 "15 feet"))
	;; nil in object list, nil second point
	(dbc_drc_print (axlDBCreateExternalDRC "My line-line < 13 feet"
	    	6.2:3.2 "DRC/PACKAGE_BOTTOM" (list nil r1) nil "15 feet"))
	;; only one object - not in a list, include a second point
	(dbc_drc_print (axlDBCreateExternalDRC "My line-line < 13 feet"
	    	6.4:3.2 "DRC/INTERNAL_1" r1 6:3.4 "15 feet"))
))
(defun dbc_drc_te_args ()
    (let ( (r1 (caar (axlDBCreateLine (list 7:2 7.6:3.2) nil
				"BOARD GEOMETRY/DIMENSION")))
    	   (r2 (caar (axlDBCreateLine (list 8:3.4 8.2:3.6) nil
				"BOARD GEOMETRY/DIMENSION")))
    	   (r3 (caar (axlDBCreateLine (list 9:3.4 9.2:3.6) nil
				"BOARD GEOMETRY/DIMENSION"))))

	(axlMsgPut "**Starting dbc_drc_te_args")
	;; bad location
	(axlDBCreateExternalDRC "args" (list "5:3") "DRC/ALL")

	;; too many dbids
	(axlDBCreateExternalDRC "args" 5.1:3 "DRC/ALL" (list r1 r2 r3))

	;; bad layer
	(axlDBCreateExternalDRC "args" 5.2:3 "DRC/able")

	;; bad second location
	(axlDBCreateExternalDRC "args" 5.3:3 "DRC/ALL" nil (list "loc"))

	;; actual value not a string
	(axlDBCreateExternalDRC "args" 5.4:3 "DRC/ALL" nil nil 773)
))
(defun dbc_drc_te_layer ()
	(axlMsgPut "**Starting dbc_drc_te_layer")
	;; illegal class
	(axlDBCreateExternalDRC "Speed less than 13" 5.0:3.6 "ETCH/TOP")
)

(defun dbc_drc_te_list ()
	(axlMsgPut "**Starting dbc_drc_te_list")
	;; only nil in object list
	(axlDBCreateExternalDRC "My line-line < 13 feet"
	    	6.2:3.2 "DRC/ALL" (list nil) 6:3.4 "15 feet")
)

(defun dbc_drc_test ()
	(dbc_drc_t1)
	(dbc_drc_t2)
	(dbc_drc_te_args)
	(dbc_drc_te_layer)
	(dbc_drc_te_list)
)
