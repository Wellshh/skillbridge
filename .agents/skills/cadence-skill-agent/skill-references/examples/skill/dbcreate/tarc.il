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

(defun dbc_t1 ()
	(axlMsgPut "**Starting dbc_path_t2")
	;; multisegment, arcs and lines
	    (axlDBCreatePath 
		    (axlPathArcCenter 
		    		(axlPathStart (list 2.0559:-0.388))
		    .005 2.07:-0.3739 nil 2.0629:-0.3809)
	        "ETCH/TOP"))

(defun dbc_t2 ()
	(axlMsgPut "**Starting dbc_path_t2")
	;; multisegment, arcs and lines
	    (axlDBCreatePath 
		    (axlPathArcCenter 
		    		(axlPathStart (list 2.0559:0.612))
		    .005 2.07:.6261 nil 2.0628:.6194)
	        "ETCH/TOP"))
(defun dbc_t3 ()
	(axlMsgPut "**Starting dbc_path_t2")
	;; multisegment, arcs and lines
	    (axlDBCreatePath 
		    (axlPathArcCenter 
		    		(axlPathStart (list 2.0001:1.000))
		    .005 2.0100:1.0100 t 2.0100:1.000)
	        "ETCH/TOP"))

