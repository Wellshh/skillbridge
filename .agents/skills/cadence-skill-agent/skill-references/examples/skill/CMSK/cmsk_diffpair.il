;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Cadence Design Systems
;
; (C) COPYRIGHT, Cadence Design Systems, Inc. 2017
; All Rights Reserved
; Licensed Materials - Property of Cadence Design Systems
;
; No part of this file may be reproduced, stored in a retrieval system,
; or transmitted in any form or by any means --- electronic, mechanical,
; photocopying, recording, or otherwise --- without prior written permission
; of Cadence Design Systems, Inc.
;
; WARRANTY:
; Use all material in this file at your own risk.  Cadence Design Systems 
; makes no claims about any material contained in this file.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;================================================================
;                                                                
;  Skill code for creating Diff Pairs using Constraint Automation.                    
;                                                                
;================================================================
; Revised: 2017Feb01_DWP:  Created (code moved from cmsk_main.il).     
;================================================================


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Name:
;;    cmsk_createDiffPairs
;;
;; Purpose:
;;    Process Nets and create/update Diffpairs.
;; 
;; Parameters:
;;    design - CMXL ID of design being processed.
;;    dpMatchInfo - list of DP matching information (lists). Each list/info contains:
;;                   - DiffPair name prefix. E.g. "DP_"
;;                   - list containing positive name regular expression and suffix. E.g. (".*MEM.*CLK.*" "_P")
;;                   - list containing negative name regular expression and suffix. E.g.( ".*MEM.*CLK.*" "_N")
;;    reportFile - File opened for writing
;;    forceDPChanges - If set, nets that are already members of existing diffpairs may move (not yet implemented)
;;
;; Returns:
;;    None
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(cmsk_createDiffPairs(design dpMatchInfo reportFile forceDPChanges)
    let((allNets allXNets matchingInfo)
        when(CMSK_DEBUG>0
            println(list( "==>cmsk_createDiffPairs: " dpMatchInfo)))

        fprintf(reportFile "\n========================================================================\n")
        fprintf(reportFile "Updating Differential Pairs based upon Nets in the Design. Force mode(%d)\n", forceDPChanges)
        
        ; Process all nets in the design updating DiffPair objects based upon those nets that match suffix information.
        ;
        allNets = cmxlGetObjectNames(design REDS_NET_OBJ)
        allXNets = cmxlGetObjectNames(design REDS_XNET_OBJ)
        foreach(matchingInfo dpMatchInfo
            when(CMSK_DEBUG>0
                println(list("matchinfo..." matchingInfo)))
            
            ;; For each pair of sufixes, find matching Nets for the differential pairs.
            let((stop dpNamePrefix 
                 posMatchedNets posNameInfo posNameMatch posSuffix posBitNumber posBaseName posObj posObjInfo  
                 negMatchedNets negNameInfo negNameMatch negSuffix negBitNumber negBaseName negObj negObjInfo)
				 
                dpNamePrefix = car(matchingInfo)
              
                posNameInfo = cadr(matchingInfo)
                posNameMatch = car(posNameInfo)
                posSuffix = cadr(posNameInfo)
                
                negNameInfo = caddr(matchingInfo)
                negNameMatch = car(negNameInfo)
                negSuffix = cadr(negNameInfo)

                fprintf(reportFile "\nProcessing nets that contain \"%s\" and suffix \"%s\" with nets that contain \"%s\" and suffix \"%s\"...\n" posNameMatch posSuffix negNameMatch negSuffix)
                
                posMatchedNets = _getMatchObjects(design allNets allXNets posNameInfo)
                negMatchedNets = nil
                when(posMatchedNets
                    negMatchedNets = _getMatchObjects(design allNets allXNets negNameInfo)
                )

                when(posMatchedNets && negMatchedNets
                    foreach(posNetInfo posMatchedNets
                        posBaseName = car(posNetInfo)
                        posBitNumber = cadr(posNetInfo)
                        posObj = caddr(posNetInfo)
                        posObjInfo = cmxlGetObjInfo(posObj)
                        when(CMSK_DEBUG>0
                            println(list( "  Found positive (x)net, name/base/bit: " cadr(posObjInfo) posBaseName posBitNumber)))

                        stop = nil
                        negNets = negMatchedNets
                        while(negNets && !stop
                            negNetInfo = car(negNets)
                            negNets = cdr(negNets)

                            negBaseName = car(negNetInfo)
                            negBitNumber = cadr(negNetInfo)
                            negObj = caddr(negNetInfo)
                            negObjInfo = cmxlGetObjInfo(negObj)
                            if(negBitNumber == posBitNumber && (strcmp(negBaseName, posBaseName) == 0) then
                                when(CMSK_DEBUG>0
                                    println(list( "  Found matching negative (x)net/base/bit: " cadr(negObjInfo) negBaseName negBitNumber)))

                                when(posObj != negObj
                                    _createDiffPair(design dpNamePrefix posObj posObjInfo negObj negObjInfo negBaseName negBitNumber forceDPChanges reportFile)
                                    stop = t
                                )
                            )
                        )

                        if(!negNetInfo then
                            ; Could not find matching negative leg for positive leg.
                            fprintf(reportFile "  Could not find Negative leg for (X)Net %s. No DiffPair created.\n", cadr(posObjInfo))
                        )
                    )
                )
            )
        )

        ; FIXSOON: Iterate over all Differential Pairs and delete those that:
        ; - no longer contain two Nets.
        ; - do not contain two nets that match the naming conventions.
        ;
        ; Possible algorithm:
        ;   allDiffPairs = cmxlGetObjects(design REDS_DIFFPAIR_OBJ)
        ;   Iterate over each DiffPair
        ;     diffPairMembers = cmxlGetObjects(diffPair, REDS_NULL_OBJ) 
        ;     if diffPairMemberss is < 2 OR both members do NOT match anything in dpMatchInfo
        ;        Update report and delete DiffPair
        ;
        when(CMSK_DEBUG>0
            println(list( "<==cmsk_createDiffPairs\n")))
        fprintf(reportFile "\n=========================================================\n")
    )
)

;; Return information for all CM XNet and Net objects that match the regular expression.
procedure(_getMatchObjects(design allNets allXNets matchingInfo)
    let((matchedObjList nameInfo nameMatch matchedXNets matchedNets suffix objName obj objInfo xnet)
        when(CMSK_DEBUG>0
            println(list( "_getMatchObjects==>\n")))
            		
        matchedObjList = nil

        nameMatch = car(matchingInfo)
        suffix = cadr(matchingInfo)
        when(CMSK_DEBUG>0
                println(list("Finding objects that match:" nameMatch suffix)))

        ; Add all matching XNets.
        matchedXNets = pcreMatchList(nameMatch allXNets)
        foreach(objName matchedXNets
            objInfo = cmxlParseName(objName, suffix )
            when(objInfo
                obj = cmxlFindOrCreateObject(design, REDS_XNET_OBJ, objName)
                when(obj
                    when(CMSK_DEBUG>0
                        println(list("Adding Xnet to list:" objName)))

                    objInfo = append(objInfo list(obj))
                    matchedObjList = append(matchedObjList list(objInfo))
                )
            )
        )

        ; Add all matching nets that are not part of an XNet.
        matchedNets = pcreMatchList(nameMatch allNets)
        foreach(objName matchedNets
            objInfo = cmxlParseName(objName, suffix )
            when(objInfo
                obj = cmxlFindOrCreateObject(design, REDS_NET_OBJ, objName)
                when(obj
                    xnet = cmxlGetParents(obj REDS_XNET_OBJ)
                    if(!xnet then
                        when(CMSK_DEBUG>0
                            println(list("Adding Net to list:" objName)))

                        objInfo = append(objInfo list(obj))
                        matchedObjList = append(matchedObjList list(objInfo))
                    )
                )
            )
        )
        when(CMSK_DEBUG>0
            println(list( "<==_getMatchObjects\n")))

        matchedObjList
    )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Check if two nets are legal for a new/existing diffpair
;; 
;; Parameters;
;;   posNet/negNet - CMXL ID of the two nets.
;;
;; Returns:
;;  t - legal
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(_legalNetsForDiffPair(posNet negNet)
    let((xnet1 xnet2 pList)
        legal = list(posNet negNet)

        ; Determine if two Nets are part of the same XNet.
        pList = cmxlGetParents(posNet, REDS_XNET_OBJ)
        xnet1 = nil
        when(pList
            xnet1 = car(pList)
			legal = list(xnet1 negNet)
		)
                            
        pList = cmxlGetParents(negNet, REDS_XNET_OBJ)
        xnet2 = nil
        if(pList then
            xnet2 = car(pList)
			if(xnet1 then
				if(xnet1==xnet2 then
					legal = nil
				else
					legal = list(xnet1 xnet2)
				)
			else
				legal = list(posNet xnet2)
			)		
		)

        legal
    )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Create/Update the DiffPair for two Nets
;; 
;; Parameters;
;;   design - CMXL ID of design being processed.
;;   posObj - CMXL ID of the positive object.
;;   posObjInfo - Name of the positive object.
;;   negObj - CMXL ID of the negative object.
;;   negObjInfo - Name of the negative object.
;;   reportFileName - Report file to record changes.
;;
;; Returns:
;;  None.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(_createDiffPair(design dpNamePrefix posObj posObjInfo negObj negObjInfo baseName bitNumber forceDPChanges reportFile)
    let((dp dpName dp1 dp2 pList dpObjInfo pList ndx)
	
        ; Determine if two Nets are already members of Differential Pairs.
        dp1 = nil
        pList = cmxlGetParents(posObj, REDS_DIFFPAIR_OBJ, 1)
        when(pList
            dp1 = car(pList))
                            
        pList = cmxlGetParents(negObj, REDS_DIFFPAIR_OBJ, 1)
        dp2 = nil
        when(pList
            dp2 = car(pList))

        ; Create default name for this DiffPair.
        if(bitNumber == -1 then
            sprintf(dpName, "%s%s", dpNamePrefix baseName)
        else
            sprintf(dpName, "%s%s_%d", dpNamePrefix baseName bitNumber)
        )

        if(dp1 || dp2 then
            if(dp1==dp2 then
                ; DiffPair with these two members already exists.
                dpObjInfo = cmxlGetObjInfo(dp1)
                if((strcmp(cadr(dpObjInfo), dpName) == 0) || forceDPChanges == 0 then
                    fprintf(reportFile "  Using existing %s for members %s and %s\n" cadr(dpObjInfo), cadr(posObjInfo), cadr(negObjInfo))
                else
                    let((rc)
                        rc = cmxlRenameObject(dp1, dpName)
                        if(rc == REDS_OK then
                            fprintf(reportFile "  Renamed %s to %s for members %s and %s\n", cadr(dpObjInfo), dpName, cadr(posObjInfo), cadr(negObjInfo))
                        else
                            fprintf(reportFile "  WARNING: Failed to rename %s to %s. Using existing name for members %s and %s\n", cadr(dpObjInfo) dpName, cadr(posObjInfo), cadr(negObjInfo))
                        )
                    )
                )
            else
                if(forceDPChanges!=0 then
                    fprintf(reportFile "ERROR: Nets %s and %s are members of existing DiffPairs and FORCE is not yet implemented.\n", cadr(posObjInfo), cadr(negObjInfo))
                else
                    fprintf(reportFile "  Nets %s and %s are members of two different existing DiffPairs and will not be changed\n", cadr(posObjInfo), cadr(negObjInfo))
                )
            )
        else
            ; Create new DiffPair for these Nets.
            if(bitNumber == -1 then
                sprintf(dpName, "%s%s", dpNamePrefix baseName)
            else
                sprintf(dpName, "%s%s_%d", dpNamePrefix baseName bitNumber)
            )
            dp = cmxlFindObject(REDS_DIFFPAIR_OBJ, dpName, design)    
            let((ndx)
                ndx=1
                while(dp
                    sprintf(dpName, "%s_%d", posBaseName, ndx )
                    ndx++
                    dp = cmxlFindObject(REDS_DIFFPAIR_OBJ, dpName, design)
                )
                dp = cmxlFindOrCreateObject(design, REDS_DIFFPAIR_OBJ, dpName)
            )

            if(dp then
                cmxlReferenceObject(dp, posObj)
                cmxlReferenceObject(dp, negObj)
				cmxlPutAttribute(dp, "CDS_SKILL_DEFINED", REDS_BOOLEAN_TYPE, '(t))

                fprintf(reportFile "  Adding %s with members %s and %s\n", dpName, cadr(posObjInfo), cadr(negObjInfo))
            else
                fprintf(reportFile "ERROR: Could not create differential pair for members %s and %s\n", cadr(posObjInfo), cadr(negObjInfo))
            )
        )
    )
)
