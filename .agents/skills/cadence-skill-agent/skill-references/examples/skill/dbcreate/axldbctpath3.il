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
;; axldbctpath3.il - axlDBCreatePath parent test driver
;;

(defun dbc_path3_print (return)
        ;(if return (foreach cln (car return)
                        ;(pprint (get cln '??))
                        ;(foreach seg (get cln 'segments)
                                ;(pprint (get seg '??)))))
        return)

(defun dbc_path3_t1 ()
    (let ((sym (car (axlDBCreateSymbol "r9" 0.7:6.3))))
	(axlMsgPut "**Starting dbc_path3_t1")
        ;; line attached to symbol instance
        (dbc_path3_print
	    (axlDBCreatePath
		(axlPathStart (list 0.9:6.7 0.9:6.5) .01)
		"PACKAGE GEOMETRY/ASSEMBLY_TOP" nil sym))

        ;; line attached to symbol defintion
        (dbc_path3_print
	    (axlDBCreatePath
		(axlPathStart (list -0.01:-.01 -0.01:.4) .005)
		"PACKAGE GEOMETRY/ASSEMBLY_TOP" nil (get sym 'definition)))
	(axlDBCreateSymbol "r8" 0.7:7.3)	;to see data now in definition
))

(defun dbc_path3_te_parent ()
	(axlMsgPut "**Starting dbc_path3_te_parent")
        ;; line attached to rectangle - illegal
	(axlDBCreateLine (list -0.01:-.01 -0.01:.4) nil
		"PACKAGE GEOMETRY/ASSEMBLY_TOP" nil
		(car (axlDBCreateRectangle (list 1:7 1.2:8))))
)

(defun dbc_path3_test ()
	(dbc_path3_t1)
	(dbc_path3_te_parent)
)
