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



(defun _transformSymbol (sym destXY destMirrored destRotation)
    (let (mirror rotation startRotation)
	(setq mirror (neq sym->mirrored destMirrored))

    	(cond
	    (mirror (setq startRotation (difference 360 sym->rotation)))
	    (t (setq startRotation sym->rotation)))

	(setq rotation (difference destRotation startRotation))

	(cond 
	    ((null (_axlTransformObject sym sym->xy destXY mirror rotation))
		(println "could not move symbol"))
	    ((null (axlDBRefreshId sym))
		(println "could not refresh symbol"))
	    (t))))


(defun ashSwapSymbols (swapList)
    (let (sym1 sym2 xy1 xy2 mirrored1 rotation1 (success nil))
	(setq sym1 (car swapList))
	(setq sym2 (cadr swapList))
	(setq xy1 (copy sym1->xy))
	(setq xy2 (copy sym2->xy))
	(setq mirrored1 sym1->mirrored)
	(setq rotation1 sym1->rotation)

	(cond
	    ((null swapList)
		(setq success t))
	    ((null (_transformSymbol sym1 xy2 sym2->mirrored sym2->rotation))
		(println "symbol 1 move failed"))
	    ((null (_transformSymbol sym2 xy1 mirrored1 rotation1))
		(println "symbol 2 move failed")
		(_transformSymbol sym1 xy1 mirrored1 rotation1))
	    (t (setq success t)))

	success))
