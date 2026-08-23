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
;; axldbctpath4.il - axlDBCreatePath test driver - test axlPathArcAngle/Radius
;;
 
; this function can be "uncommented" for some useful dump info
(defun dbc_path4_print (return)
        ;(if return (foreach cln (car return)
                        ;(pprint (get cln '??))
                        ;(foreach seg (get cln 'segments)
                                ;(pprint (get seg '??)))))
        return)

(defun dbc_path4_t1 ()
	(axlMsgPut "**Starting dbc_path4_t1")
	;; axlPathArcAngle - clockwise, 270 and 90
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
		(axlPathArcAngle
			(axlPathStart (list 6:6))
		    nil 7:6 t 270)
		    nil 6:6 t 90)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcAngle - clockwise, 180 and 180
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
		(axlPathArcAngle
			(axlPathStart (list 5:6))
		    nil 6:6 t 180)
		    nil 5:6 t 180)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcAngle - clockwise, 22.5, and 337.5
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
		(axlPathArcAngle
			(axlPathStart (list 5:5))
		    nil 4.8:5.2 t 22.5)
		    nil 5:5 t 337.5)
	        "BOARD GEOMETRY/DIMENSION"))
)
(defun dbc_path4_t2 ()
	(axlMsgPut "**Starting dbc_path4_t2")
	;; axlPathArcAngle - counter clockwise 90, center low/left
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
			(axlPathStart (list 4:5))
		    nil 3:6 nil 90)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcAngle - counter clockwise 90, center up/right
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
			(axlPathStart (list 3:6))
		    nil 4:5 nil 90)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcAngle - counter clockwise 22.5
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
			(axlPathStart (list 2.5:6))
		    nil 2:5.5 nil 22.5)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcAngle - counter clockwise 22.5
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
			(axlPathStart (list 2:5.5))
		    nil 2.5:6 nil 22.5)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcAngle - counter clockwise 292.5
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
			(axlPathStart (list 2.5:6))
		    nil 2:5.5 nil 292.5)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcAngle - counter clockwise 292.5
	(dbc_path4_print
	    (axlDBCreatePath
		(axlPathArcAngle
			(axlPathStart (list 2.1:5.5))
		    nil 2.6:6 nil 292.5)
	        "BOARD GEOMETRY/DIMENSION"))
)
(defun dbc_path4_t3 ()
	(axlMsgPut "**Starting dbc_path4_t3")
	;; axlPathArcRadius - clockwise, little then big, (90+270 deg)
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    (axlPathArcRadius 
		    		(axlPathStart (list 3:5))
		    nil 2:4 t nil 1.0)
		    nil 3:5 t t 1.0)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - counter clockwise, little then big, (90+270 deg)
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    (axlPathArcRadius 
		    		(axlPathStart (list 3.2:5.2))
		    nil 2.2:4.2 nil nil 1.0)
		    nil 3.2:5.2 nil t 1.0)
	        "BOARD GEOMETRY/DIMENSION"))
)
(defun dbc_path4_t4 ()
	(axlMsgPut "**Starting dbc_path4_t4")
	;; axlPathArcRadius - counter clockwise, little, (180 deg)
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 1.9:5))
		    nil 1.9:4 nil nil .5)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - clockwise, little, (180 deg)
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 2:5))
		    nil 2:4 t nil .5)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - counter clockwise, big, (180 deg)
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 2.1:5))
		    nil 2.1:4 nil t .5)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - clockwise, big, (180 deg)
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 2.2:5))
		    nil 2.2:4 t t .5)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - counter clockwise, big,
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 2.1:4.7))
		    nil 2.1:3.7 nil t .7)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - clockwise, big,
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 2.2:4.7))
		    nil 2.2:3.7 t t .7)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - counter clockwise, little,
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 2.1:4.2))
		    nil 2.1:3.2 nil nil .7)
	        "BOARD GEOMETRY/DIMENSION"))
	;; axlPathArcRadius - clockwise, little,
	(dbc_path4_print
	    (axlDBCreatePath 
		    (axlPathArcRadius 
		    		(axlPathStart (list 2.2:4.2))
		    nil 2.2:3.2 t nil .7)
	        "BOARD GEOMETRY/DIMENSION"))
)
(defun dbc_path4_te_circle ()
	(axlMsgPut "**Starting dbc_path4_te_circle")
	;; axlPathArcAngle - circle
		(axlPathArcAngle
			(axlPathStart (list 4.5:5.5))
		    nil 4.5:5.5 nil 360)
	;; axlPathArcRadius - circle
		    (axlPathArcRadius 
		    		(axlPathStart (list 4.5:5.5))
		    nil 4.5:5.5 nil t .5)
)
(defun dbc_path4_test ()
    (dbc_path4_t1)
    (dbc_path4_t2)
    (dbc_path4_t3)
    (dbc_path4_t4)
    (dbc_path4_te_circle)
    nil
)
