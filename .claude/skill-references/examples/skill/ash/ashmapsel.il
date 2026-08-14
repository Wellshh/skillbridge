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
;   (ashMapSelect func UserArg)
;    executes func. over list of object(s) found after each pick, also
;    passing in an optional UserArg from SKILL.  
;    
;    func = (func SelectObj @optional UserArg)
;


(defun ashMapSelect (func @optional __UserArg__)
  (let (points selSet selList)
    (and func
	 (axlSetFindFilter ?enabled "ALL" ?onButtons "ALL")
	 (axlShell "alias ~[ skill axlCancelEnterFun")
	 (axlMsgPut "Press <ESC> to terminate command")
         ; Set up picks, and then objects under picks.
	 (while (setq points
		      (axlEnterPoint
		       ?prompts
		       '("Pick to select object or <ESC> to finish")))
		(if (axlSingleSelectPoint points)
		    (push (car (axlGetSelSet)) selList)))
	 (axlClearSelSet)
	 (mapcar (lambda (x) 
		   (apply func (list x __UserArg__)))
		 selList))))

   




