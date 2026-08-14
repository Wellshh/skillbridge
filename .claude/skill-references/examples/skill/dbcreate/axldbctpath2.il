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
;; axldbctpath2.il - second axlDBCreatePath test driver - cline merging
;;

; this function can be "uncommented" for some useful dump info
(defun dbc_path2_print (return)
	;(if return (foreach cln (car return)
			;(pprint (get cln '??))
			;(foreach seg (get cln 'segments)
				;(pprint (get seg '??)))))
	return)

(defun dbc_path2_t1 ()
	(axlMsgPut "**Starting dbc_path2_t1")
	;; cline that would completely merge into a previous - 1 segment
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.6:4 6.6:3.5) .012)
	        "ETCH/TOP" "sig2"))
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.6:4 6.6:3.5) .012)
	        "ETCH/TOP" "sig2")))

(defun dbc_path2_t2 ()
	(axlMsgPut "**Starting dbc_path2_t2")
	;; cline that would completely merge into a previous - multiseg
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.2:4 6.2:3.5 6.0:3.7) .012)
	        "ETCH/TOP" "sig2"))
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.2:4 6.2:3.5 6.0:3.7) .012)
	        "ETCH/TOP" "sig2")))

(defun dbc_path2_t3 ()
	(axlMsgPut "**Starting dbc_path2_t3")
	;; cline that subset of a previous - 1 segment
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.6:5 6.6:4.5) .012)
	        "ETCH/TOP" "sig2"))
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.6:4.8 6.6:4.5) .012)
	        "ETCH/TOP" "sig2")))

(defun dbc_path2_t4 ()
	(axlMsgPut "**Starting dbc_path2_t4")
	;; multiseg cline that has part a subset of a previous
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.8:5 6.8:4.5) .012)
	        "ETCH/TOP" "sig2"))
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.7:4.8 6.8:4.8 6.8:4.5 6.9:4.5) .012)
	        "ETCH/TOP" "sig2")))

(defun dbc_path2_t5 ()
	(axlMsgPut "**Starting dbc_path2_t5")
	;; cline that would completely merge into a previous - multiseg partial
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.2:3 6.2:2.5 6.0:2.7) .012)
	        "ETCH/TOP" "sig2"))
	(dbc_path2_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.2:2.8 6.2:2.5 6.1:2.6) .012)
	        "ETCH/TOP" "sig2")))

(defun dbc_path2_t6 ()
        (axlMsgPut "**Starting dbc_path2_t6")
        ;; stand alone etch - two segment arc and line previously a crash
        (dbc_path2_print
            (axlDBCreatePath 
                (axlPathLine 
                    (axlPathArcCenter 
                                (axlPathStart (list 8.155:4.842))
                        nil 7.856:4.842 nil 8.005:4.842)
                        ;nil 7.856:4.842 nil 8.006:4.842)
                    nil 7.856:4.632)
                "ETCH/TOP")))

(defun dbc_path2_t7 ()
        (axlMsgPut "**Starting dbc_path2_t7")
        ;; stand alone etch - two segment arc and line previously a crash
        (dbc_path2_print
            (axlDBCreatePath 
                    (axlPathArcCenter 
                        (axlPathLine 
                                (axlPathStart (list 8.155:4.642))
                        nil 8.066:4.642)
                    nil 7.856:4.432 nil 8.066:4.432)
                "ETCH/TOP")))

(defun dbc_path2_t8 ()
        (axlMsgPut "**Starting dbc_path2_t8")
        ;; crossing existing line at a segment end point - T created
        (dbc_path2_print
            (axlDBCreateLine (list 7.3:5.9 7.7:5.9 7.9:5.7) .012 "ETCH/TOP"))
        (dbc_path2_print
            (axlDBCreateLine (list 7.9:6.1 7.5:5.7) .012 "ETCH/TOP")))
(defun dbc_path2_t9 ()
        (axlMsgPut "**Starting dbc_path2_t9")
        ;; adding cline with a seg endpoint on an existing cline - T created
        (dbc_path2_print
            (axlDBCreateLine (list 8.7:6.1 8.3:5.7) .012 "ETCH/TOP"))
        (dbc_path2_print
            (axlDBCreateLine (list 8.1:5.9 8.5:5.9 8.7:5.7) .012 "ETCH/TOP"))
)
(defun dbc_path2_test ()
	(dbc_path2_t1)
	(dbc_path2_t2)
	(dbc_path2_t3)
	(dbc_path2_t4)
	(dbc_path2_t5)
	(dbc_path2_t6)
	(dbc_path2_t7)
	(dbc_path2_t8)
	(dbc_path2_t9)
	nil
)
