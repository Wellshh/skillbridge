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
	(taiEchoResults "axlenter_t0" t
        	(axlEnterPoint ?prompts (list "Enter point.")
                      ?points (list '(198 300))
                      ?gridSnap t)))

(defun axlenter_t1 () ;no grdiSnap
	(axlMsgPut "**Starting axlenter_t1")
	(taiEchoResults "axlenter_t1" t
        	(axlEnterPoint ?prompts (list "Enter point.")
                      ?points (list '(200 300)))))

(defun axlenter_t2 () ;no points
       	(axlEnterPoint ?prompts (list "Enter point.") ?gridSnap t))

(defun axlenter_t3 () ; no prompts ist
	(axlMsgPut "**Starting axlenter_t3")
	(taiEchoResults "axlenter_t3" t
        	(axlEnterPoint ?points (list '(200 300)) ?gridSnap t)))

(defun axlenter_t4 () ; only gridSnap
	(axlMsgPut "**Starting axlenter_t4")
	(taiEchoResults "axlenter_t4" t (axlEnterPoint ?gridSnap t)))

(defun axlenter_t5 (); nothing
	(axlMsgPut "**Starting axlenter_t5")
	(taiEchoResults "axlenter_t5" t (axlEnterPoint)))

(defun axlenter_t6 () ; multiple stuff in each list
	(axlMsgPut "**Starting axlenter_t6")
	(taiEchoResults "axlenter_t6" t
        	(axlEnterPoint ?prompts (list "Enter point." "Enter Point1." "Enter Point 2")
                      ?points (list '(200 300) '(400 500) '(600 700))
                      ?gridSnap t)))

(defun axlenterstring_t0 ()
    (let (string)
	(axlMsgPut "**Starting axlenterstring_t0")
        (setq string (axlEnterString ?prompts (list "Enter String.")))
	(taiEchoResults "enter string test no prompt" t string)
	string))

(defun axlenterstring_t1 ()
    (let (string)
	(axlMsgPut "**Starting axlenterstring_t1")
       	(setq string (axlEnterString))
	(taiEchoResults "enter string test no prompt" t string)
	string))


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
        path))

(defun axlcbuf_t0 ()
    (axlMsgPut "**Starting axlcbuf_t0")
    (let ( (pick1 (axlenter_t2)) )
    	(taiEchoResults "Add Simple Move Dynamics, PATH" t
        	(axlAddSimpleMoveDynamics pick1 (getpath pick1) "path"))
        (axlenter_t2)
    	(taiEchoResults "Clear dynamics test" t (axlClearDynamics))))

(defun axlcbuf_t1 ()
    (axlMsgPut "**Starting axlcbuf_t1")
    (let (point path)
        (setq point (axlenter_t2))
    	(taiEchoResults "axlPathStart" t
        	(setq path  (axlPathStart (list point) 50.0)))
    	(taiEchoResults "axlPathLine" t
        	(setq path (axlPathLine path nil 1500:1500)))
    	(taiEchoResults "Add Simple Move Dynamics, BOX" t
        	(axlAddSimpleMoveDynamics point (getrectpath point) "box"))
        (axlenter_t2)
	(taiEchoResults "Clear dynamics test" t (axlClearDynamics))))

(defun axlcbuf_t2 ()
    (axlMsgPut "**Starting axlcbuf_t2")
    (let ( (pick1 (axlenter_t2)) )
    	(taiEchoResults "Add Simple Move Dynamics, CIRCLE" t
        	(axlAddSimpleMoveDynamics pick1
            		(axlPathStartCircle (list 100:100 400) 50) "circle"))
        (axlenter_t2)
	(taiEchoResults "Clear dynamics test" t (axlClearDynamics))))

(defun axlcbuf_t3 ()
    (axlMsgPut "**Starting axlcbuf_t3")
    (let ( (pick1 (axlenter_t2)) path recpath circpath)
        (setq path (getpath pick1))
        (setq recpath (getrectpath pick1))
    	(taiEchoResults "axlPathStartCircle" t
        	(setq circpath (axlPathStartCircle (list 100:100 400) 50)))

    	(taiEchoResults "Add Simple Move Dynamics, PATH" t
        	(axlAddSimpleMoveDynamics pick1 path "path"))
    	(taiEchoResults "Add Simple Move Dynamics, BOX" t
        	(axlAddSimpleMoveDynamics pick1 path "box"))
    	(taiEchoResults "Add Simple Move Dynamics, CIRCLE" nil
        	(axlAddSimpleMoveDynamics pick1 path "circle"))
    	(taiEchoResults "Add Simple Move Dynamics, PATH" t
        	(axlAddSimpleMoveDynamics pick1 recpath "path"))
    	(taiEchoResults "Add Simple Move Dynamics, BOX" t
        	(axlAddSimpleMoveDynamics pick1 recpath "box"))
    	(taiEchoResults "Add Simple Move Dynamics, CIRCLE" nil
        	(axlAddSimpleMoveDynamics pick1 recpath "circle"))
    	(taiEchoResults "Add Simple Move Dynamics, PATH" t
        	(axlAddSimpleMoveDynamics pick1 circpath "path"))
    	(taiEchoResults "Add Simple Move Dynamics, BOX" t
        	(axlAddSimpleMoveDynamics pick1 circpath "box"))
    	(taiEchoResults "Add Simple Move Dynamics, CIRCLE" t
        	(axlAddSimpleMoveDynamics pick1 circpath "circle"))

        (axlenter_t2)
	(taiEchoResults "Clear dynamics test" t (axlClearDynamics))))

(defun axlrband_t0 ()
    (axlMsgPut "**Starting axlrband_t0")
    (let ( (pick1 (axlenter_t2)) )
    	(taiEchoResults "Add Simple Rband Dynamics, BOX" t
        	(axlAddSimpleRbandDynamics pick1 "box" ?origin pick1))
        (axlenter_t2)
	(taiEchoResults "Clear dynamics test" t (axlClearDynamics))))

(defun axlrband_t1 ()
    (axlMsgPut "**Starting axlrband_t1")
    (let (pick1 path pick2)
        (setq pick1 (axlenter_t2))
    	(taiEchoResults "Add Simple Rband Dynamics, PATH" t
        	(axlAddSimpleRbandDynamics pick1 "path"))
        (setq pick2 (axlenter_t2))
    	(taiEchoResults "axl Get Dynamics Segs" t
        	(setq segs (axlGetDynamicsSegs pick1 pick2 nil)))
    	(taiEchoResults "axl Make Dynamics Segs" t
        	(setq path (axlMakeDynamicsPath segs)))
        (axlClearDynamics)
    	(taiEchoResults "Add Simple Move Dynamics, PATH" t
        	(axlAddSimpleMoveDynamics pick2 path "path" ?ref_point pick1))
        (axlenter_t2)
	(taiEchoResults "Clear dynamics test" t (axlClearDynamics))))

(defun axlangle_t0 ()
    (axlMsgPut "**Starting axlangle_t0")
    (let ((pick1 (axlenter_t2)) angle)
    	(taiEchoResults "Add Simple Rband Dynamics, PATH" t
        	(axlAddSimpleRbandDynamics pick1 "path" ?origin pick1))
    	(taiEchoResults "Add Simple Move Dynamics, BOX" t
        	(axlAddSimpleMoveDynamics pick1 (getrectpath pick1) "box"))
	;torigin prompts refPoint angle lockAngle
    	(taiEchoResults "Set Rotation Increment" t
		(axlSetRotateIncrement ?angular 45))
    	(taiEchoResults "axl Enter Angle" t
            (setq angle (axlEnterAngle pick1 ?lockAngle 45)))
        (axlClearDynamics)
	(printf "angle %L\n" angle)
        (setq angle (axlEnterAngle pick1 ?lockAngle 45 ?angle angle))
        angle))

(defun axlplacepath_t0 ()
    (axlMsgPut "**Starting axlplacepath_t0")
    (let (path)
    	(taiEchoResults "axlEnterPath" t
        	(setq path axlEnterPath()))
    	(taiEchoResults "axlDBCreatePath" t
        	(axlDBCreatePath path "ETCH/TOP"))))

(defun axlplacepath_t1 ()
    (axlMsgPut "**Starting axlplacepath_t1")
    (let (path path1 path2)
    	(taiEchoResults "axlEnterPath" t
        	(setq path axlEnterPath()))
    	(taiEchoResults "axlDBCreatePath" t
        	(axlDBCreatePath path "ETCH/TOP"))
    	(taiEchoResults "axlEnterPath" t
        	(setq path1 axlEnterPath(?lastPath path)))
    	(taiEchoResults "axlDBCreatePath" t
        	(axlDBCreatePath path1 "ETCH/TOP"))
    	(taiEchoResults "axlEnterPath" t
        	(setq path2 axlEnterPath(?lastPath path1)))
    	(taiEchoResults "axlDBCreatePath" t
        	(axlDBCreatePath path2 "ETCH/TOP"))))

(defun axlplacepath_t2 ()
   (axlMsgPut "**Starting axlplacepath_t2")
   (let (path)
   	(while (setq path (axlEnterPath ?lastPath path))
    	    (taiEchoResults "axlEnterPath" t path)
    	    (taiEchoResults "axlDBCreatePath" t
              	(axlDBCreatePath path "ETCH/TOP")))))

(defun axlplacepath_t3 ()
    (axlMsgPut "**Starting axlplacepath_t3")
    (let (path)
   	(taiEchoResults "axlSetLineLock" t (axlSetLineLock ?arcEnable t))
        (while (setq path
                (axlEnterPath ?lastPath path ?points (list 
                    (axlEnterPoint ?prompts (list "start point:")))))
    	    (taiEchoResults "axlEnterPath" t path)
            (cond ((null path) return (nil)))
            (axlDBCreatePath path "ETCH/TOP"))
   	(taiEchoResults "axlSetLineLock" t (axlSetLineLock ?arcEnable nil))))

(defun axllinelock_t0 ()
    (axlMsgPut "**Starting axllinelock_t0")
    (let ( (pick1 (axlenter_t2)) )
    	(taiEchoResults "axlSetLineLock, arcEnable" t (axlSetLineLock ?arcEnable t))
	(taiEchoResults "axlSetLineLock, lockAngle" t (axlSetLineLock ?lockAngle 45)) 
	(taiEchoResults "axlSetLineLock, minRadius" t (axlSetLineLock ?minRadius 50))
	(taiEchoResults "axlSetLineLock, length45" t (axlSetLineLock ?length45 50))
	(taiEchoResults "axlSetLineLock, fixed45" nil (axlSetLineLock ?fixed45 t))
	(taiEchoResults "axlSetLineLock, lengthRadius" t (axlSetLineLock ?lengthRadius 100))
 	(taiEchoResults "axlSetLineLock, fixedRadius" t (axlSetLineLock ?fixedRadius t))
	(taiEchoResults "axlSetLineLock, lockTangent" t (axlSetLineLock ?lockTangent t))
    	(taiEchoResults "axlAddSimpleRbandDynamics" t
        	(axlAddSimpleRbandDynamics pick1 "path" ?origin pick1))
        (axlenter_t2)
        (axlClearDynamics)))

(defun axlaitest ()
    (axlenter_t0)
    (axlenter_t1)
    (axlenter_t2)
    (axlenter_t3)
    (axlenter_t4)
    (axlenter_t5)
    (axlenter_t6)
    (axlenterstring_t0)
    (axlenterstring_t1)
    (axlcbuf_t0)
    (axlcbuf_t1)
    (axlcbuf_t2)
    (axlcbuf_t3)
    (axlrband_t0)
    (axlrband_t1)
    (axlangle_t0)
    (axlplacepath_t0)
    (axlplacepath_t1)
    (axlplacepath_t2)
    (axlCancelEnterFun)
    (axllinelock_t0)
    (axlCancelEnterFun))
