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
;; axldbctvia.il - axlDBCreateVia test driver
;;

(defun dbc_via_print (return)
        ;(if return (pprint (get (car return) '??)))
        return)

(defun dbc_via_t1 ()
	(axlMsgPut "**Starting dbc_via_t1")
	;; simple via
	(dbc_via_print
	    (axlDBCreateVia "via" 2.0:7.0))
	
	(dbc_via_print
	;; rectangular via
	    (axlDBCreateVia "via_rect" 2.2:7.0))

	;; mirrored via
	(dbc_via_print
	    (axlDBCreateVia "via_rect" 2.4:7.0 nil t))

	;; rotated via
	(dbc_via_print
	    (axlDBCreateVia "via_rect" 2.6:7.0 nil nil 22.5))

	;; mirror & rotated via
	(dbc_via_print
	    (axlDBCreateVia "via_rect" 2.8:7.0 nil t 270))
)

(defun dbc_via_t2 ()
	(axlMsgPut "**Starting dbc_via_t2")
	;; connect to a cline - no net specified
	(dbc_via_print
	    (axlDBCreateVia "via" 6.6:3.0 nil))

	;; connect to a cline - net specified - connection made
	(dbc_via_print
	    (axlDBCreateVia "via" 6.8:3.0 "sig2"))

	;; connect to a cline - net specified - no connection made
	(dbc_via_print
	    (axlDBCreateVia "via" 6.8:3.2 "SIG2"))

	;; connect to a cline - different net specified
	(dbc_via_print
	    (axlDBCreateVia "via" 7.0:3.0 "sig1"))
)

(defun dbc_via_te_args ()
	(axlMsgPut "**Starting dbc_via_te_args")

	;; padstack not found
	(axlDBCreateVia "via_nope" 1.0:5.0)

	;; bad location
	(axlDBCreateVia "via" (list "abc"))

	;; location out of drawing
	(axlDBCreateVia "via" 1111.0:5.0)

	;; extents out of drawing
	(axlDBCreateVia "via" .005:5.0)

	;; net not found
	(axlDBCreateVia "via" 1:5 "notmynet")

	;; bad mirror
	(axlDBCreateVia "via" 1:5 nil "mirror")

	;; bad rotate
	(axlDBCreateVia "via" 1:5 nil nil "badrot")

	;; bad parent - (another via)
	(axlDBCreateVia "via" 1:5 nil nil 0.0
		(car (axlDBCreateVia "via" 8:1.5)))

)

(defun dbc_via_te_args2 ()
	(axlMsgPut "**Starting dbc_via_te_args2")
	;; padstack not a string - caught by Skill
	(errset (axlDBCreateVia 777 1.0:5.0) t)
)

(defun dbc_via_tparent ()
    (let ((sym (car (axlDBCreateSymbol "r9" 0.7:6.3))))
	(axlMsgPut "**Starting dbc_via_tparent")
        ;; attached to symbol instance
	(axlDBCreateLine (list 0.7:6.3 0.9:6.3) .012 "ETCH/TOP" nil sym)
        (dbc_via_print
	    (axlDBCreateVia "via" 0.9:6.3 nil nil 0.0 sym))


        ;; attached to symbol defintion - is now illegal so will be error
	(axlDBCreateLine (list 0:0 0:.2) .012 "ETCH/TOP" nil
	    (get sym 'definition))
        (dbc_via_print
	    (axlDBCreateVia "via" 0:0.2 nil nil 0.0 (get sym 'definition)))
	(axlDBCreateSymbol "r8" 0.7:7.3)	;to see data now in definition
))

(defun dbc_via_te_parent ()
	(axlMsgPut "**Starting dbc_via_te_parent")
        ;; via attached to rectangle - illegal
	(axlDBCreateVia "via" 0:0.2 nil nil 0.0
		(car (axlDBCreateRectangle (list 1:7 1.2:8))))
)

(defun dbc_via_test ()
	(dbc_via_t1)
	(dbc_via_t2)
	(dbc_via_te_args)
	(dbc_via_te_args2)
	(dbc_via_tparent)
	(dbc_via_te_parent)
)

