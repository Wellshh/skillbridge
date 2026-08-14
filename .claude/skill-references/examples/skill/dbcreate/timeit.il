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



(defun axlu ()
	(axlTestDriver t 1.1 2 "abc" 1.0:2.0 .012 1.0:2.0 224466 "ETCH/BOTTOM")
	(axlTestDriver "a" 1.1 2 "def" 1.0:2.0 .012 1.0:2.0 224466 "ETCH/BOTTOM")
	(axlTestDriver nil 1.2 3 "ghi" 1:2 .2 1:3 22 "Etch/bot")
)

(defun tlayer ()
        (axlDBCreateLine (list 3.8:4 5:5 6:4) .012 "ETCH/TOP")
        (axlDBCreateLine (list 4:4 5:5 6:4) .012 "etch/TOP")
        (axlDBCreateLine (list 4.2:4 5:5 6:4) .012 "ETCH/bottom")
        (axlDBCreateLine (list 4.4:4 5:5 6:4) .012 "")
        (axlDBCreateLine (list 4.6:4 5:5 6:4) .012)
        (axlDBCreateLine (list 4.8:4 5:5 6:4) .012 nil)
        (axlDBCreateLine (list 5:4 5:5 6:4) .012 "ASSEMBLY_TOP")
        (axlDBCreateLine (list 5.2:4 5:5 6:4) .012 "/ASSEMBLY_TOP")
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "Etch/")
        (axlDBCreateLine (list 5.4:4 5:5 6:4) .012 "Et/bot")
)
(defun foo ()
        (axlDBCreateLine (list 1000:1000 1500:1000 1500:2500 2000:2000) 12.0
			"BOARD GEOMETRY/DIMENSION"))
(defun foo2 ()
        (axlDBCreateLine (list 2700:6075 1575:6075 1550:6100 1550:6150) 12.0
			"ETCH/TOP" "SIGCAP1"))
(defun baz ()
    (let ( (path (axlPathStart (list 1000:3000) 50.0)) )
	(putpropq path
		(list
		    (make_axlPathSeg ?endPoint 1000:3500)
		    (make_axlPathSeg ?endPoint 1500:3500 ?arcCenter 1250:3500)
		    (make_axlPathSeg ?endPoint 2000:3000 ?arcCenter 1750:3250
							?arcCounterClockwise t)
		    (make_axlPathSeg ?endPoint 2200:3600)) pathList)
	(axlDBCreatePath path)))

(defun timeit ()
    (let (x y start end)
	(axlPerformance)
	(for outer 1 3
	    (setq x 200)
	    (for xloop 1 200
		(setq y 200)
		(for yloop 1 100
		    (writeLine (list (list x y) (list (plus x 10)
							(plus y 10))) 10
						;"ETCH/TOP")
						"BOARD GEOMETRY/DIMENSION")
						;nil)
		    (setq y (plus y 50)))
		(setq x (plus x 50))))
))

(defun writeLine (
    points
    @optional
    width
    layer
    netName)
 
	(fprintf outFile "(L (list ")
	(foreach pt points (fprintf outFile " %d:%d"
				(car pt) (cadr pt)))
	(fprintf outFile ")")
	(fprintf outFile " %d" width)
	(fprintf outFile ")\n")
)

(defun timeit2 ()
    (let (x y start end)
	(axlPerformance)
	(for outer 1 3
	    (setq x 200)
	    (for xloop 1 200
		(setq y 200)
		(for yloop 1 100
		    (axlDBCreate1SegLine (list x y)
					(list (plus x 10) (plus y 10)) 10.0
						;"ETCH/TOP")
						"BOARD GEOMETRY/DIMENSION")
						;nil)
		    (setq y (plus y 50)))
		(setq x (plus x 50))))
))

(defun timeit2C ()
    (axlTestDriver 3 200 100 "BOARD GEOMETRY/DIMENSION"))
