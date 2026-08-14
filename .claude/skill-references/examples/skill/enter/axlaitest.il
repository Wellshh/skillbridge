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



(defun axlenter_t0 ()
	(axlMsgPut "**Starting axlenter_t0")
        (axlEnterPoint ?prompts (list "Enter point.")
                      ?points (list '(198 300))
                      ?gridSnap t))

(defun axlenter_t1 () ;no grdiSnap
	(axlMsgPut "**Starting axlenter_t1")
        (axlEnterPoint ?prompts (list "Enter point.")
                      ?points (list '(200 300))))

(defun axlenter_t2 () ;no points
	(axlMsgPut "**Starting axlenter_t2")
        (axlEnterPoint ?prompts (list "Enter point.") ?gridSnap t))

(defun axlenter_t3 () ; no prompts ist
	(axlMsgPut "**Starting axlenter_t3")
        (axlEnterPoint ?points (list '(200 300)) ?gridSnap t))

(defun axlenter_t4 () ; only gridSnap
	(axlMsgPut "**Starting axlenter_t4")
        (axlEnterPoint ?gridSnap t))

(defun axlenter_t5 (); nothing
	(axlMsgPut "**Starting axlenter_t5")
        (axlEnterPoint))

(defun axlenter_t6 () ; multiple stuff in each list
	(axlMsgPut "**Starting axlenter_t6")
        (axlEnterPoint ?prompts (list "Enter point." "Enter Point1." "Enter Point 2")
                      ?points (list '(200 300) '(400 500) '(600 700))
                      ?gridSnap t))


(defun getpath (start)
    (let (path)
        if( (start != 'nil) then 
            (setq path (axlPathStart (list start) 50.0))
        else
            (setq path (axlPathStart (list 1000:3000) 50.0)))

	(setq path (axlPathLine path nil 1000:3500))
	(setq path (axlPathArcCenter path nil 1500:3500 t 1250:3500))
	(setq path (axlPathArcCenter path nil 2000:3000 t 1750:3250))
	(setq path (axlPathLine path nil 2200:3600))
        path))

(defun getrectpath (start)
    (let (path)
        if( (start != 'nil) then path = (axlPathStart (list start) 50.0)
            else path = (axlPathStart (list 1000:3000) 50.0) )
        (setq path (axlPathLine path nil 1500:1500))
        ;(setq path (axlPathArcCenter path 10.5 30:25 t 15:15))
        ;(setq path (axlPathLine path nil 10:10))
        path))

(defun axlcbuf_t0 ()
    (axlMsgPut "**Starting axlcbuf_t0")
    (let ( (pick1 (axlenter_t2)) )
        (axlAddSimpleMoveDynamics pick1 (getpath pick1) "path")
        ;axlAddSimpleMoveDynamics(pick1 
        ;    (axlPathStartCircle (list 1000.0:1500.0 400.0) 50.0) "circle"); no width specified
        ;axlAddSimpleMoveDynamics(pick1 
        ;    (axlPathStartCircle (list pick1 400) 50.0) "circle")
        ;axlAddSimpleMoveDynamics(pick1 (getrectpath pick1) "box")
        (axlenter_t2)
        (axlClearDynamics)))

(defun axlcbuf_t1 ()
    (axlMsgPut "**Starting axlcbuf_t1")
    (let (point path)
        (setq point (axlenter_t2))
        (setq path  (axlPathStart (list point) 50.0))
        (setq path (axlPathLine path nil 1500:1500))
        ;axlAddSimpleMoveDynamics(point path "box")
        axlAddSimpleMoveDynamics(point (getrectpath point) "box")
        (axlenter_t2)
        (axlClearDynamics)))

(defun axlcbuf_t2 ()
    (axlMsgPut "**Starting axlcbuf_t2")
    (let ( (pick1 (axlenter_t2)) )
        (axlAddSimpleMoveDynamics pick1
            (axlPathStartCircle (list (100:100) 400) 50) "circle")
        (axlenter_t2)
        (axlClearDynamics)))

(defun axlrband_t0 ()
    (axlMsgPut "**Starting axlrband_t0")
    (let ( (pick1 (axlenter_t2)) )
        axlAddSimpleRbandDynamics(pick1 "box" ?origin pick1)
        (axlenter_t2)
        (axlClearDynamics)))

(defun axlrband_t1 ()
    (axlMsgPut "**Starting axlrband_t1")
    (let ( pick1 path pick2)
        (setq pick1 (axlenter_t2))
        axlAddSimpleRbandDynamics(pick1 "path")
        (setq pick2 (axlenter_t2))
        (setq segs axlGetDynamicsSegs(pick1 pick2 nil))
        (setq path axlMakeDynamicsPath(segs))
        (axlClearDynamics)
        axlAddSimpleMoveDynamics(pick2 path "path" ?ref_point pick1)
        (axlenter_t2)
        (axlClearDynamics)))

(defun axlangle_t0 ()
    (axlMsgPut "**Starting axlangle_t0")
    (let ((pick1 (axlenter_t2)) angle)
        (axlAddSimpleRbandDynamics pick1 "path" ?origin pick1)
        (axlAddSimpleMoveDynamics pick1 (getrectpath pick1) "box")
	;origin prompts refPoint angle lockAngle
        (setq angle (axlEnterAngle pick1 ?lockAngle 45))
        (axlClearDynamics)
(printf "angle %L\n" angle)
        (setq angle (axlEnterAngle pick1 ?lockAngle 45 ?angle angle))
        angle))

(defun axlplacepath_t0 ()
    (axlMsgPut "**Starting axlplacepath_t0")
    (let (path)
        (setq path axlEnterPath())
        (axlDBCreatePath path "ETCH/TOP")))

(defun axlplacepath_t1 ()
    (axlMsgPut "**Starting axlplacepath_t1")
    let(((path nil) (path1 nil) (path2 nil))
        (setq path axlEnterPath())
        (axlDBCreatePath path "ETCH/TOP")
        (setq path1 axlEnterPath(?lastPath path))
        (axlDBCreatePath path1 "ETCH/TOP")
        (setq path2 axlEnterPath(?lastPath path1))
        (axlDBCreatePath path2 "ETCH/TOP")))

(defun axlplacepath_t2 ()
    (axlMsgPut "**Starting axlplacepath_t2")
    (let ((path nil))
        (while (setq path 
            (axlEnterPath ?lastPath path))
                (axlDBCreatePath path "ETCH/TOP"))))

(defun axlplacepath_t3 ()
    (axlMsgPut "**Starting axlplacepath_t3")
    (let ((path nil))
        (while (setq path
                (axlEnterPath ?lastPath path ?points (list 
                    (axlEnterPoint ?prompts (list "start point:")))))
            (cond ((null path) return (nil)))
            (axlDBCreatePath path "ETCH/TOP"))))

(defun axlaitest ()
    (axlenter_t0)
    (axlenter_t1)
    (axlenter_t2)
    (axlenter_t3)
    (axlenter_t4)
    (axlenter_t5)
    (axlenter_t6)
    (axlcbuf_t0)
    (axlcbuf_t1)
    (axlcbuf_t2)
    (axlrband_t0)
    (axlrband_t1)
    (axlangle_t0)
    (axlplacepath_t0)
    (axlplacepath_t1)
    (axlplacepath_t2))
