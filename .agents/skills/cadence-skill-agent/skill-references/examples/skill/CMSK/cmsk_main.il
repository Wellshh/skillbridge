;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;   Cadence Design Systems
;
; (C) COPYRIGHT, Cadence Design Systems, Inc. 2016
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
;  Skill code for Design Specific Constraint Automation.                    
;                                                                
;================================================================
; Revised: 2016Apr20_RPR:  Created.     
; 	     : 2016Jun03_RPR:  Added Rename support.      
;          2016Jun29_RPR:  Process XNets instead of Nets, when they exist.  
;          2016Feb01_DWP:  Diff Pair code moved to cmsk_diffpair.il.                     
;================================================================


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Name: cmsk_allegroNoCMLaunch
;;
;; Purpose:
;;    Main function that triggers all automation when running from Allegro and
;;    not launching CM.
;;
;; Parameters:
;;    reportFileName - Name of the report file.
;;    configFileName - Configuration Information.
;;
;; Returns:
;;  t if successful
;;  nil if error
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(cmsk_allegroNoCMLaunch(reportFileName configFileName)
    CMSK_DEBUG=0
    let((design reportFile res)
        reportFile = outfile(reportFileName)
        configInfo = _readCMSKConfigFile(configFileName)
        fprintf(reportFile "Allegro Constraint Automation Report\n")

        axlCMDBInit()
        design = cmxlFindObject(REDS_DESIGN_OBJ)
        when(design
            cmxlDBSkillInit(design)
            res = errset(cmsk_runAutomations(design configInfo reportFile))
			unless(res
				fprintf(reportFile "\n\n Error %L" errset.errset)
			)
        )
        fprintf(reportFile "\n\n*** End Report")

        axlCMDBExit()
        close(reportFile)
    )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Name: cmsk_afterCMLaunch
;;
;; Purpose:
;;    Main function that triggers all automation after launching CM.
;;
;; Parameters:
;;    reportFileName - Name of the report file.
;;    configFileName - Configuration Information.
;;
;; Returns:
;;  t if successful
;;  nil if error
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(cmsk_afterCMLaunch(reportFileName configFileName)
    CMSK_DEBUG=0
    let((retList design reportFile configInfo res)
        retList = nil
        reportFile = outfile(reportFileName)
        configInfo = _readCMSKConfigFile(configFileName)
        fprintf(reportFile "DEHDL Constraint Automation Report\n")

        design = cmxlFindObject(REDS_DESIGN_OBJ)
        when(design
            res = errset(cmsk_runAutomations(design configInfo reportFile))
			unless(res
				fprintf(reportFile "\n\n Error %L" errset.errset)
			)
        )
        fprintf(reportFile "\n\n*** End Report")

        close(reportFile)
        retList
    )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Name: _readCMSKConfigFile
;;
;; Purpose:
;;    Read CMSK configuration file.
;; 
;; Parameters;
;;    configFileName - File containing all information
;;
;; Returns:
;;    list(
;;      list('DIRECTIVE1 list(<params>) )
;;      list('DIRECTIVE2 list(<params>) )
;;      ...
;;    )
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(_readCMSKConfigFile(configFileName)
    let((configFile configInfoList configInfo)
        configInfoList = nil
        configInfo = nil

        when(isFile(configFileName)
            configFile = infile(configFileName)
            when(configFile
                configInfo = car(lineread(configFile)))

            while(configInfo
                when(CMSK_DEBUG>0
                    println(list(" Line read:" configInfo)))
                configInfoList = append(configInfoList, configInfo)
                configInfo = lineread(configFile)
            )
            close(configFile)
        )

        when(CMSK_DEBUG>0
            println(list(" Configuration info... "))
            foreach(configInfo configInfoList
                println(list("  Info: " configInfo))
            )
        )

        configInfoList
    )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; 
;; Name: _accessCMSKConfigInfo
;;
;; Purpose:
;;    Access the CMSK configuration information for specific information.
;; 
;; Parameters;
;;    configInfoList - Structure containing configuration information for constraint automation
;;
;; Returns:
;;    list(
;;      list('DIRECTIVE1 list(<params>) )
;;      list('DIRECTIVE2 list(<params>) )
;;      ...
;;    )
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(_accessCMSKConfigInfo(info configInfoList)
    let((retInfo configInfo found)
        retInfo = nil
        found = nil
        when(CMSK_DEBUG>0
            println(list(" Searching for directive:" info)))

        while(configInfoList && !found
            configInfo = car(configInfoList)
            configInfoList = cdr(configInfoList)

            when(CMSK_DEBUG>1
                println(list("config info search: " configInfo )))
            sym = car(configInfo)
            if(sym==info then
                retInfo = cdr(configInfo)
                found = t
            )
        )
        retInfo
    )
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Name: cmsk_runAutomations
;;
;; Purpose:
;;    Run all automations
;; 
;; Parameters;
;;    design - CMXL ID of design being processed.
;;    configInfo - Configuration information for each automation process.
;;    reportFile - File opened for writing
;;
;; Returns:
;;    None
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
procedure(cmsk_runAutomations(design configInfo reportFile)
    let((diffPairInfo netGroupInfo)

        ;;  DiffPair automation.
        ;
        diffPairInfo = _accessCMSKConfigInfo('CMSK_DIFFPAIR configInfo)
        when(diffPairInfo
            let((dpNamePrefix)
                ;  First list contains differential pair name prefix.
                ;  Second list (of lists) contains naming convention strings.
                cmsk_createDiffPairs(design diffPairInfo reportFile 1)
            )
        )

        ;;  Net Group automation.
        ;
        netGroupInfo = _accessCMSKConfigInfo('CMSK_NETGROUP configInfo)
        when(netGroupInfo
            let(()
				fprintf(reportFile "\n=========================================================\n")
				fprintf(reportFile " Net Group automation not yet implemented.\n")			
				fprintf(reportFile "\n=========================================================\n")
            )
        )
		
		;;  Insert loops for additional automation here.
    )
)
