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



;
; ashdump.il
;

;
; straight line same width
;
(defun ashSegmentsToList (seglist)
	(if seglist			; else terminate recurse w/ nil
    	    (let (ptlist start end pts)
	        (if (null (setq ptlist (ashSegmentsToList (cdr seglist))))
		    (get (car seglist) 'startEnd)
		    (progn
		        (setq pts (get (car seglist) 'startEnd))
		        (setq start (car pts))
		        (setq end (cadr pts))
		        (cond
		            ((equal start (car ptlist)) (cons end ptlist))
		            ((equal end (car ptlist)) (cons start ptlist))
		            (t (cons
			        (if (equal start (cadr ptlist)) end start)
			        (reverse ptlist)))))))))

(defun ashSegmentsToPath (seglist)
	(if seglist
    	    (let (path start end prevpt
		    (firstpts (get (car seglist) 'startEnd))
		    (slist (cdr seglist)))

		; look to second seg to determine start point
		(setq start (car firstpts))
		(setq end (cadr firstpts))
		(setq path
		    (axlPathStart (list (setq prevpt
			(if (and slist
			        (or (equal end (car (get slist 'startEnd)))
			            (equal end (cadr (get slist 'startEnd)))))
		    	    start
		    	    end)))))

		; path (and start) established - now all segs (including first)
		(foreach seg seglist
		    (setq start (car (get seg 'startEnd)))
		    (setq prevpt
		        (setq end (if (equal start prevpt) end start)))
		    (if (get seg 'radius)	; to see if is an arc
			(axlPathArcCenter path (get seg 'width) end
			    ; may need to reverse the arc
			    (if (equal start end)
				(null (get seg 'isClockwise))
				(get seg 'isClockwise))
			    (get seg 'xy))
			(axlPathLine path (get seg 'width) end)))
		path))
)

(defun ashDumpMapParent (dbid)
    nil
)

(defun ashDumpPutLine  ( points width layer netName parent)
	(fprintf ashDumpFile "(axlDBCreatePath (axlPathStart (list")
	(foreach pt points (fprintf ashDumpFile "\n  '%L" pt))
	(fprintf ashDumpFile ") %L)" width)
	(if layer
	    (fprintf ashDumpFile " \"%s\"" layer)
	    (fprintf ashDumpFile " %L" nil))
	(if netName
	    (fprintf ashDumpFile "\n    \"%s\"" netName)
	    (fprintf ashDumpFile " %L" nil))
	(if (ashDumpMapParent parent)
	    (fprintf ashDumpFile " \"%s\"" parent)
	    (fprintf ashDumpFile " %L" nil))
	(fprintf ashDumpFile ")\n")
)
(defun ashDumpPutPathSeg  ( pathSeg pathString)
	(fprintf ashDumpFile
            (if (axlPathSegGetArcCenter pathSeg)
		"  (axlPathArcCenter"
		"  (axlPathLine"))
	(fprintf ashDumpFile " %s %L '%L" pathString
	    (axlPathSegGetWidth pathSeg)
	    (axlPathSegGetEndPoint pathSeg))

	(if (axlPathSegGetArcCenter pathSeg)
	    (fprintf ashDumpFile "\n    %L '%L"
		(axlPathSegGetArcClockwise pathSeg)
		(axlPathSegGetArcCenter pathSeg)))
		
	(fprintf ashDumpFile ")\n")
)
(defun ashDumpPutPath  ( path layer netName parent)
    (let ( (segments (axlPathGetPathSegs path)) )
	(fprintf ashDumpFile "(let ((path (axlPathStart %L %L)))\n"
	    (axlPathSegGetEndPoint (car segments))	; start point
	    (axlPathGetWidth path))

	(foreach seg (cdr segments) (ashDumpPutPathSeg seg "path"))

	(fprintf ashDumpFile "  (axlDBCreatePath path")
	(if layer
	    (fprintf ashDumpFile " \"%s\"" layer)
	    (fprintf ashDumpFile " %L" nil))
	(if netName
	    (fprintf ashDumpFile "\n    \"%s\"" netName)
	    (fprintf ashDumpFile " %L" nil))
	(if (ashDumpMapParent parent)
	    (fprintf ashDumpFile " \"%s\"" parent)
	    (fprintf ashDumpFile " %L" nil))
	(fprintf ashDumpFile "))\n")
))
(defun ashDumpPutVia  ( padstack location netName mirror rotation parent)
	(fprintf ashDumpFile "(axlDBCreateVia \"%s\" '%L" padstack location)
	(if netName
	    (fprintf ashDumpFile " \"%s\"" netName)
	    (fprintf ashDumpFile " %L" nil))
	(fprintf ashDumpFile " %L %L" mirror rotation)
	(if (ashDumpMapParent parent)
	    (fprintf ashDumpFile " \"%s\"" parent)
	    (fprintf ashDumpFile " %L" nil))
	(fprintf ashDumpFile ")\n")
)
(defun ashDumpPath1 (path)
	(ashDumpPutLine
	    (ashSegmentsToList (get path 'segments))
	    (get (car (get path 'segments)) 'width)
	    (get path 'layer)
	    (get (get path 'net) 'name)
	    (get path 'parent))
)
(defun ashDumpPath2 (path)
	(ashDumpPutPath
	    (ashSegmentsToPath (get path 'segments))
	    (get path 'layer)
	    (get (get path 'net) 'name)
	    (get path 'parent))
)
(defun ashDumpPath (path)
	(if (and (get path 'isSameWidth) (null (get path 'hasArcs)))
	    (ashDumpPath1 path)
	    (ashDumpPath2 path))
)
(defun ashDumpVia (via)
	(ashDumpPutVia
	    (get via 'name)
	    (get via 'xy)
	    (get (get via 'net) 'name)
	    (get via 'mirrored)
	    (get via 'rotation)
	    (get via 'parent))
)
(defun ashDumpMain (filename)
	(setq ashDumpFile (outfile filename))
	;(foreach l (ashFindAllLines) (ashDumpPath l))
	(foreach l (ashFindAllClines) (ashDumpPath l))
	(foreach l (ashFindAllVias) (ashDumpVia l))
	(close ashDumpFile)
)

(defun ashDumpAddLine ()
	(axlDBCreateLine (list 2:3 2:4 3:4 3:5)))

(defun ashDumpAddPath ()
	;; multisegment, arcs and lines
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
	        "ETCH/TOP"))
