/*
------------------------------------------------------------------------
    Allegro Symbol Library Footprint Check

    Author: Edward B. Acheson
    Date: May 15, 2001
    File: rule_check_tables.il
    Revision: 1.1 (release version 14.2)


    Command name:  symbol check

	This file is user accessable to allow for the addition of and removal
	of new or current checks.

    Description: These Allegro SKILL Functions were developed to allow
    			an Allegro Library the capability of verification of
				an Allegro Footprint against a Foorprint Library Standard.


    Requirements: This is one two file that may be modified by the user
				to cuztomize  rules in the Symbol check environment.
------------------------------------------------------------------------
*/

/*
================================================================================
NAME: _PAC_setUserTreeDefault

SYNOPSYS: _PAC_setUserFormTreeData( ) 

DESCRIPTION:
    This function returns a list of rule set groups and rules sets to be displayed
	in the Symbol check form rules tree. The format is critical for this function.


	list(
			list( ["group name1"]
				list( list(["check name1"] ["function call"])
					  list(["check name2"] ["function call"])
					)
				)

			list( ["group name1"]
				list( list(["check name1"] ["function call"])
					  list(["check name2"] ["function call"])
					)
				)
		)

		All list input is to be of type string.
INPUT:
    none   

OUTPUT:
    	The list of rule groups, rule names, and rule function calls 

================================================================================
*/
defun( _PAC_setUserFormTreeData ()
prog( ()

return(

	list( 
		list( "REFDES Checks"
			list( '("REFDES Exist" "check_refdes_exist(file_ptr)")
				  '("REFDES Text Size" "check_refdes_blocksize(file_ptr)")
				  '("REFDES Subclass" "check_refdes_subclass(file_ptr)")
			)
		)
		list( "COMPONENT VALUE Checks"
			list( '("COMPONENT VALUE Exist" "check_compvalue_exist(file_ptr)")
				  '("COMPONENT VALUE Text Size" "check_compval_blocksize(file_ptr)")
				  '("COMPONENT VALUE Subclass" "check_compval_subclass(file_ptr)")
			)
		)
		list( "DEVICE TYPE Checks"
			list( '("DEVICE TYPE Exist" "check_device_exist(file_ptr)")
				  '("DEVICE TYPE Text Size" "check_device_blocksize(file_ptr)")
				  '("DEVICE TYPE Subclass" "check_device_subclass(file_ptr)")
			)
		)
		list( "TOLERANCE Checks"
			list( '("TOLERANCE Exist" "check_prttol_exist(file_ptr)")
				  '("TOLERANCE Text Size" "check_prttol_blocksize(file_ptr)")
				  '("TOLERANCE Subclass" "check_prttol_subclass(file_ptr)")
			)
		)
		list( "PART NUMBER Checks"
			list( '("PART NUMBER Exist" "check_prtnum_exist(file_ptr)")
				  '("PART NUMBER Text Size" "check_prtnum_blocksize(file_ptr)")
				  '("PART NUMBER Subclass" "check_prtnum_subclass(file_ptr)")
			)
		)
		list( "GEOMETRY Checks"
			list( '("SILK SCREEN Geometry" "check_silkscreen_geometry(file_ptr)")
				  '("ASSEMBLY Geometry" "check_assembly_geometry(file_ptr)")
			)
		)
		list( "Reports"
			list( '("PIN Location Report" "report_pin_location(file_ptr log_file)")
			)
		)
	)
)
))

