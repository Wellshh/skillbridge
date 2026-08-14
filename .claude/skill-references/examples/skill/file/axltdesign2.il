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
;; axltdesign2.il - axl Design family tests - symbol commands
;;

(defun dsgn2_t1 ()
	(axlMsgPut "**Starting dsgn2_t1")
	(axlDBCreateText "U*" -200:100 "2" "REF DES/ASSEMBLY_TOP")

	(axlMsgPut "*compile, no args")
	(axlCompileSymbol)

	(axlMsgPut "*compile, ?symbol only - enter tsym")
	(axlCompileSymbol ?symbol nil)

	(axlMsgPut "*compile, ?symbol provided")
	(axlCompileSymbol ?symbol "tsym2")

	(axlMsgPut "*compile, ?type provided")
	(axlCompileSymbol ?type (axlDesignType t))

)

(defun dsgn2_test ()
	(dsgn2_t1)
)
