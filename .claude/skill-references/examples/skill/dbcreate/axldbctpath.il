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
;; axldbctpath.il - axlDBCreatePath test driver
;;

; note - currently assumes that active layer is BOARD GEOMETRY/DIMENSION

; TODO
;	various etch merging stuff

; this function can be "uncommented" for some useful dump info
(defun dbc_path_print (return)
	;(if return (foreach cln (car return)
			;(pprint (get cln '??))
			;(foreach seg (get cln 'segments)
				;(pprint (get seg '??)))))
	return)

(defun dbc_path_t1 ()
	(axlMsgPut "**Starting dbc_path_t1")
	;; single segment, etch, net provided, default width provided, DRC
	(dbc_path_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.4:2.6 8.3:2.6) .012)
	        "ETCH/TOP" "sig2")))

(defun dbc_path_t2 ()
	(axlMsgPut "**Starting dbc_path_t2")
	;; multisegment, arcs and lines
	(dbc_path_print
	    (axlDBCreatePath 
	        (axlPathLine 
		    (axlPathLine 
		    (axlPathLine 
		    (axlPathArcCenter 
		    (axlPathArcCenter 
		    (axlPathArcCenter 
		    		(axlPathStart (list 6.4:4.7))
		    .012 6.7:4.5 t 6.4:4.375)
		    .02 7.025:4.3 nil 7.001:4.625)
		    .012 7.2:4.137 t 7.037:4.137)
		    nil 7.2:3.7)
		    .020 7.4:3.5)
		    .012 7.4:3.0)
	        "ETCH/TOP")))

(defun dbc_path_t3 ()
	(axlMsgPut "**Starting dbc_path_t3")
	;; default layer, some segs use default width
        (dbc_path_print
	    (axlDBCreatePath
                (axlPathLine
                (axlPathLine
                (axlPathLine
                (axlPathLine (axlPathStart (list 5.1:4) .25)
                    nil 5.7:4)
                    .0 5.7:3.8)
                    .1 5.9:3.8)
                    .1 5.9:3.3))))

(defun dbc_path_t4 ()
	(axlMsgPut "**Starting dbc_path_t4")
	;; odd diameter 180 deg. arc - center rounded to DB accuracy
	(axlDBCreatePath 
		(axlPathArcCenter (axlPathStart (list 1.0:1.0))
		    .01 1.011:1.0 nil 1.0055:1.0)
		"BOARD GEOMETRY/DIMENSION")

	;; width to edge of drawing
        (dbc_path_print
	    (axlDBCreatePath 
                (axlPathLine (axlPathStart (list 0.0:0.0))
                    .000 0.0:.4)
	        "BOARD GEOMETRY/DIMENSION"))
        (dbc_path_print
	    (axlDBCreatePath 
                (axlPathLine (axlPathStart (list 10.999:0.5))
                    .002 10.999:1.0)
		"BOARD GEOMETRY/DIMENSION"))
        (dbc_path_print
	    (axlDBCreatePath 
                (axlPathLine (axlPathStart (list 0.010:1.5))
                    .020 0.010:2.0)
		"BOARD GEOMETRY/DIMENSION")))

(defun dbc_path_t5 ()
	(axlMsgPut "**Starting dbc_path_t5")
	;; various legal combinations of specifying layer
        (axlDBCreateLine (list 3.8:4 5:5 6:4) .012 "BOARD GEOMETRY/DIMENSION")
        (axlDBCreateLine (list 4:4 5:5 6:4) .012 "board geometry/DIMENSION")
        (axlDBCreateLine (list 4.2:4 5:5 6:4) .012 "BOARD GEOMETRY/dimension")
        (axlDBCreateLine (list 4.4:4 5:5 6:4) .012 "")
        (axlDBCreateLine (list 4.6:4 5:5 6:4) .012)
        (axlDBCreateLine (list 4.8:4 5:5 6:4) .012 nil)
        (axlDBCreateLine (list 5:4 5:5 6:4) .012 "DIMENSION")
        (axlDBCreateLine (list 5.2:4 5:5 6:4) .012 "/dimension")
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "Bo/dim"))

(defun dbc_path_te_segs1 ()
	(axlMsgPut "**Starting dbc_path_te_segs1")
	;; no start point
	(axlDBCreatePath 
                (errset (axlPathLine (axlPathStart) .02 5.7:4) t)
			    "BOARD GEOMETRY/DIMENSION"))

(defun dbc_path_te_segs2 ()
	(axlMsgPut "**Starting dbc_path_te_segs2")
	;; start point out of drawing
	(axlDBCreatePath 
                (axlPathLine (axlPathStart (list 20.0:10.0)) .02 5.7:4)
		"BOARD GEOMETRY/DIMENSION"))

(defun dbc_path_te_segs3 ()
	(axlMsgPut "**Starting dbc_path_te_segs3")
	;; end point out of drawing
	(axlDBCreatePath 
                (axlPathLine (axlPathStart (list 2.0:1.0)) .02 25.7:4)
		"BOARD GEOMETRY/DIMENSION"))

(defun dbc_path_te_segs4 ()
	(axlMsgPut "**Starting dbc_path_te_segs4")
	;; zero length segment
	(axlDBCreatePath 
                (axlPathLine (axlPathStart (list 2.0:2.0 2.0:1.0) .02)
                    .02 2.0:1.0)
		"BOARD GEOMETRY/DIMENSION"))

(defun dbc_path_te_segs5 ()
	(axlMsgPut "**Starting dbc_path_te_segs5")
	;; width wider than drawing
	(axlDBCreatePath 
                (axlPathLine (axlPathStart (list 2.0:1.0)) 15.0 5.7:4)
		"BOARD GEOMETRY/DIMENSION"))

(defun dbc_path_te_segs6 ()
	(axlMsgPut "**Starting dbc_path_te_segs6")
	;; width past edge of drawing
	(axlDBCreatePath 
                (axlPathLine (axlPathStart (list 0.001:2.5)) .003 0.001:3.0)
		"BOARD GEOMETRY/DIMENSION"))

(defun dbc_path_te_segs7 ()
	(axlMsgPut "**Starting dbc_path_te_segs7")
	;; negative width
	(axlDBCreatePath 
                (axlPathLine (axlPathStart (list 0.010:1.5)) -0.020 0.010:2.0)
		"BOARD GEOMETRY/DIMENSION"))
		
(defun dbc_path_te_segs ()
	(dbc_path_te_segs1)
	(dbc_path_te_segs2)
	(dbc_path_te_segs3)
	(dbc_path_te_segs4)
	(dbc_path_te_segs5)
	(dbc_path_te_segs6)
	(dbc_path_te_segs7)
)

(defun dbc_path_te_arc ()	
	(axlMsgPut "**Starting dbc_path_te_arc")
	;; center same as start point
	(axlDBCreatePath 
		(axlPathArcCenter (axlPathStart (list 1.0:1.0))
		    .01 1.5:0.5 nil 1.0:1.0)
		"BOARD GEOMETRY/DIMENSION")

	;; center same as end point
	(axlDBCreatePath 
		(axlPathArcCenter (axlPathStart (list 1.0:1.0))
		    .01 1.5:0.5 nil 1.5:0.5)
		"BOARD GEOMETRY/DIMENSION")

	;; center 2 DB unit increase in x
	(axlDBCreatePath 
		(axlPathArcCenter (axlPathStart (list 8.0:2.0))
		    .01 8.5:1.5 nil 8.002:1.5)
		"BOARD GEOMETRY/DIMENSION")

	;; center 2 DB unit decrease in y
	(axlDBCreatePath 
		(axlPathArcCenter (axlPathStart (list 8.0:2.0))
		    .01 8.5:1.5 nil 8.:1.498)
		"BOARD GEOMETRY/DIMENSION")

	;; segment extents
	(axlDBCreatePath 
		(axlPathArcCenter (axlPathStart (list 1.0:1.0))
		    .01 1.5:0.5 nil 1.0:0.5)
		"BOARD GEOMETRY/DIMENSION"))
	

(defun dbc_path_te_layer ()
	(axlMsgPut "**Starting dbc_path_te_layer")
	;; illegal layer specifications
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 22.5)
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "P/")
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "Bo/")
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "foo/baz")
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "pin/baz")
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "Pin/top"))

(defun dbc_path_te_net ()
	(axlMsgPut "**Starting dbc_path_te_net")
	;; bad parent (a via)
	(axlDBCreatePath 
		(axlPathStart (list 6:2 8:2)) nil nil 
			(car (axlDBCreateVia "via" 9:1)))
	;; net not a string
	(axlDBCreatePath 
		(axlPathStart (list 6.4:2.4 8.3:2.4) .01) "etch/top" 77)
	;; net not in database
	(axlDBCreatePath 
		(axlPathStart (list 6.4:2.4 8.3:2.4) .01) "etch/top" "nonet"))

(defun dbc_path_te_path ()
	(axlMsgPut "**Starting dbc_path_te_path")
	;; not an r_path
	(axlDBCreatePath (make_axlFill))

	;; bad default width
	(axlDBCreatePath (axlPathStart (list 6:2 8:2) -.10) nil)

	;; bad start point
	(axlDBCreatePath (axlPathStart (list (list "6:2") 8:2) 0) nil)

	;; bad segment point
	(axlDBCreatePath (axlPathStart (list 8:2 (list "6:2")) 0) nil)

	;; bad arc center
	(axlDBCreatePath (axlPathArcCenter (axlPathStart (list 1:1))
		    .01 1.5:.5 nil (list "a")))

	;; bad arc direction
	(axlDBCreatePath (axlPathArcCenter (axlPathStart (list 1:1))
		    .01 1.5:.5 "bub" 1.75:.5))
)


; Line fonts
(defun dbc_path_font ()
	let( (layer)
	(axlMsgPut "**Starting dbc_path_font")

	layer = "BOARD GEOMETRY/DIMENSION"
	;; single segment, etch, net provided, default width provided, DRC
	(dbc_path_print
           axlDBCreateLine( (list 6.4:3.6 12:3) .2 layer nil nil 'HIDDEN ))

	(dbc_path_print
	    (axlDBCreatePath 
	        (axlPathStart (list 6.4:4.6 18.3:4.6) 0.2)
	        layer nil nil nil 'DOTTED))
))

(defun dbc_path_test ()
	(dbc_path_t1)
	(dbc_path_t2)
	(dbc_path_t3)
	(dbc_path_t4)
	(dbc_path_t5)
	(dbc_path_te_arc)
	(dbc_path_te_layer)
	(dbc_path_te_net)
	(dbc_path_te_path)
	(dbc_path_te_segs)
	dbc_path_font()
	)
