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



(defun axlMyCompleteCB ()
        (setq userdata (axlUIGetUserData))
        (printf "myCompleteCB: userdata, %L\n" userdata->??))

(defun axlMyRotateCB ()
        (setq userdata (axlUIGetUserData))
        (printf "myRotateCB: userdata, %L\n" userdata->??))

(defun myFinishCB ()
        (setq userdata (axlUIGetUserData))
        (printf "myFinishCB: userdata, %L\n" userdata->??)
	(axlFinishEnterFun))

(defun myCancelCB ()
        (setq userdata (axlUIGetUserData))
        (printf "myCancelCB: userdata, %L\n" userdata->??)
	(axlCancelEnterFun))

(defun axlTestSubCmdCB ()
        (setq userdata (axlUIGetUserData))
        (printf "axlTestSubCmdCB: userdata, %L\n" userdata->??))

(defun axltest_args ()
	(taiEchoResults "registered cmd" t
	    (axlCmdRegister "cmd" 'axlTestArgs ?doneCmd 'myFinishCB ?cancelCmd 'myCancelCB))

	(taiEchoResults "registered cmdsub" t
	    (axlCmdRegister "cmdsub" 'axlTestSubCmdCB ?cmdType "sub_cmd"))

	(taiEchoResults "registered cmdimm" t
	    (axlCmdRegister "cmdimm" 'axlTestImmediates ?cmdType "general")))

(defun axlTestArgs (@rest args "t")
    (let (userdata popId oldPopId point)
        (printf "axlTestArgs: args, %L\n" args)
	(setq userdata (axlUIGetUserData))
        (printf "axlTestArgs: user data:%L\n" userdata->??)
	(setq popId (axlUIPopupDefine userdata->popupId
	             (list (list "Complete" 'axlMyCompleteCB)
	             (list "Rotate" 'axlMyRotateCB))))
	(setq oldPopId (axlUIPopupSet popId))
        (printf "axlTestArgs: user data:%L\n" userdata->??)

	(while (setq point (axlEnterPoint))
                (printf "axlTestArgs: user data:%L\n" userdata->??))
	(setq userdata (axlUIGetUserData))
        (printf "axlTestArgs: user data:%L\n" userdata->??)))

(defun axlTestImmediates (@rest args "t")
    (let (userdata popId oldPopId point)
        (printf "axlTestArgs: args, %L\n" args)
        (setq userdata (axlUIGetUserData))
        (printf "axlTestArgs: user data:%L\n" userdata->??)
	(setq popId (axlUIPopupDefine userdata->popupId
                     (list (list "Complete" 'axlMyCompleteCB)
                     (list "Rotate" 'axlMyRotateCB))))
        (setq oldPopId (axlUIPopupSet popId))
        (printf "axlTestArgs: user data:%L\n" userdata->??)))

(defun axlreg_test ()
	(axlCancelEnterFun)
	(taiEchoResults "registered cmd" t
		(axlCmdRegister "cmd" 'axlTestArgs ?cmdType "interactive"))
	(taiEchoResults "registered cmd1" t
		(axlCmdRegister "cmd1" 'axlTestArgs ?doneCmd 'myFinishCB ?cancelCmd 'myCancelCB))
	(taiEchoResults "registered cmd2" t
		(axlCmdRegister "cmd2" 'axlTestArgs ?doneCmd 'myFinishCB))
	(taiEchoResults "registered cmd3" t
		(axlCmdRegister "cmd3" 'axlTestArgs ?cancelCmd 'myCancelCB))
	(taiEchoResults "registered cmd4" t
		(axlCmdRegister "cmd4" 'axlTestArgs ?cancelCmd 'myCancelCB))
	(taiEchoResults "registered cmd5" t
		(axlCmdRegister "cmd5" 'axlTestArgs ?doneCmd 'myFinishCB))
	(taiEchoResults "registered cmd6" t
		(axlCmdRegister "cmd6" 'axlTestArgs ))
	(taiEchoResults "registered cmd7" t
		(axlCmdRegister "cmd7" 'axlTestArgs ?doneCmd 'myFinishCB))
	(taiEchoResults "registered cmd8" t
		(axlCmdRegister "cmd8" 'axlTestArgs))
	(taiEchoResults "registered cmdi" t
		(axlCmdRegister "cmdi" "axlTestImmediates" ?cmdType "general"))
	(taiEchoResults "registered cmdi1" t
		(axlCmdRegister "cmdi1" "axlTestImmediates" ?cmdType "general"))
	(taiEchoResults "registered cmdi2" t
		(axlCmdRegister "cmdi2" "axlTestImmediates" ?cmdType "general" ?doneCmd "myFinishCB"))
	(taiEchoResults "registered cmdi3" t
		(axlCmdRegister "cmdi3" "axlTestImmediates" ?cmdType "general"))
	(taiEchoResults "registered cmdi4" t
		(axlCmdRegister "cmdi4" "axlTestSubCmdCB" ?cmdType "sub_cmd" ?doneCmd "myFinishCB"))
	(taiEchoResults "registered cmdi5" t
		(axlCmdRegister "cmdi5" "axlTestSubCmdCB" ?cmdType "sub_cmd"))
	(taiEchoResults "registered cmdi6" t
		(axlCmdRegister "cmdi6" "axlTestSubCmdCB" ?cmdType "sub_cmd" ?doneCmd "myFinishCB"))
	(taiEchoResults "registered cmdi7" t
		(axlCmdRegister "cmdi7" "axlTestSubCmdCB" ?cmdType "sub_cmd")))

(defun axlunreg_test ()
	(axlCancelEnterFun)
	(taiEchoResults "unregistered cmd" t (axlCmdUnregister "cmd"))
	(taiEchoResults "unregistered cmd1" t (axlCmdUnregister "cmd1"))
	(taiEchoResults "unregistered cmd2" t (axlCmdUnregister "cmd2"))
	(taiEchoResults "unregistered cmd3" t (axlCmdUnregister "cmd3"))
	(taiEchoResults "unregistered cmd4" t (axlCmdUnregister "cmd4"))
	(taiEchoResults "unregistered cmd5" t (axlCmdUnregister "cmd5"))
	(taiEchoResults "unregistered cmd6" t (axlCmdUnregister "cmd6"))
	(taiEchoResults "unregistered cmd7" t (axlCmdUnregister "cmd7"))
	(taiEchoResults "unregistered cmd8" t (axlCmdUnregister "cmd8"))

	(taiEchoResults "unregistered cmdi" t (axlCmdUnregister "cmdi"))
	(taiEchoResults "unregistered cmdi1" t (axlCmdUnregister "cmdi1"))
	(taiEchoResults "unregistered cmdi2" t (axlCmdUnregister "cmdi2"))
	(taiEchoResults "unregistered cmdi3" t (axlCmdUnregister "cmdi3"))
	(taiEchoResults "unregistered cmdi4" t (axlCmdUnregister "cmdi4"))
	(taiEchoResults "unregistered cmdi5" t (axlCmdUnregister "cmdi5"))
	(taiEchoResults "unregistered cmdi6" t (axlCmdUnregister "cmdi6"))
	(taiEchoResults "unregistered cmdi7" t (axlCmdUnregister "cmdi7")))
