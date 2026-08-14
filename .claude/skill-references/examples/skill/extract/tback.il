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



(defun tryit2 ()
    (let (glob2)

	(foreach dbid (axlExtractMap "t_view" nil)
	    (funcall
	        '(lambda (dbid)
			(setq glob2 (cons dbid glob2)))
		dbid))
))

(defun tryit3 ()
    (let (glob3)

        (defun cback (dbid) (setq glob3 (cons dbid glob3)))

        (axlExtractMap "t_view" 'cback)
	glob3
))

(defun tryit3a ()
    (let (glob3)

        (axlExtractMap "t_view"
	    '(lambda (dbid) (setq glob3 (cons dbid glob3))) )
	glob3
))

(defun old_get_netnames ()
    (let (nets)

	(axlExtractMap "net_empty_view"
	    '(lambda (dbid)
		(setq nets (cons (get dbid 'name) nets)))
	    "quiet")
	;(sort nets 'alphalessp)
	nets
))

(defun get_netnames ()
    (let ((netsByReference (list nil 'nets nil)))
	(axlExtractMap "net_empty_view"
	    (lambda (dbid netRef)
		(putprop netRef
		    (cons (get dbid 'name) (get netRef 'nets))
		    'nets))
	    netsByReference
	    "quiet")
	(get netsByReference 'nets)))
