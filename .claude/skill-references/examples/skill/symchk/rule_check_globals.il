/*
------------------------------------------------------------------------
    Allegro Symbol Library Footprint Check

    Author: Edward B. Acheson
    Date: May 1, 2001
	File: rule_check_globals.il
    Revision: 1.1 (release version 14.2)
	

    Command name:  symbol check

	This is a  customer accessable file.

    Description: This is a globals variable file where a user may modify
	specific rules, messages and set error types. These global variables
	are called by the "symbol check" command.

	The current variables defined in this may be changed but should not
	be deleted. New User Global Variables may be added to allow for new
	or custom rules. If the standard set of rules supplied is used, 
	removal of any of these current global variables will result in
	run time errors.

------------------------------------------------------------------------
*/

defun( _PAC_SetUserGlobals ()
prog(()

/* it is Strongly reccommended that these values do not change */
    ERROR = 40
    WARNING = 30
    INFO = 20

/* Assembly Drawing Gemoetry */
	ASSEMBLY_GEOMETRY_SHORT = "No Assembly Geometry in Symbol."
	ASSEMBLY_GEOMETRY_LONG = "No Assembly Geometry in Symbol\n Assembly Graphical Data Will Not Exist" 
	ASSEMBLY_GEOMETRY_ERROR = ERROR
/* End of Assembly Geometry Check */

/* Silkscreen Drawing Geometry */
	SILKSCREEN_GEOMETRY_SHORT = "No Silk Screen Geometry in Symbol."
	SILKSCREEN_GEOMETRY_LONG = "No Silk Screen Geometry in Symbol\n Silk Screen Graphical Data Will Not Exist" 
	SILKSCREEN_GEOMETRY_ERROR = ERROR
/* End of Silkscreen Geometry Check */

/* Text Check */
	TEXT_REFDES_SHORT = "No REFDES Text in Symbol."
	TEXT_REFDES_LONG = "No REFDES Text in Symbol\n REFDES Text Has Not Been Defined in This Symbol." 
	TEXT_REFDES_SIZE_SHORT = "Incorrect Text Size For REFDES Text."
	TEXT_REFDES_SIZE_LONG = "Text Size For REFDES is Incorrect."
	TEXT_REFDES_SUBCLASS_SHORT = "Incorrect REFDES Text Subclass Assignment."
	TEXT_REFDES_SUBCLASS_LONG = "Subclass Assignment For REFDES Text Not\non an Allowed Layer."
	TEXT_REFDES_SUBCLASS_MISSING = "REFDES Text Missing Subclass Definition"
	TEXT_REFDES_ERROR = ERROR
	TEXT_REFDES_BLOCK_ERROR = ERROR
	TEXT_REFDES_SUBCLASS_ERROR = ERROR

	TEXT_COMP_VALUE_SHORT = "No PART VALUE Text in Symbol."
	TEXT_COMP_VALUE_LONG = "No PART VALUE Text in Symbol\n COMPONENT VALUE Text Has Not Been Defined in This Symbol." 
	TEXT_COMP_VALUE_SIZE_SHORT = "Incorrect Text Size For COMPONENT VALUE Text."
	TEXT_COMP_VALUE_SIZE_LONG = "Text Size For COMPONENT VALUE is Incorrect."
	TEXT_COMP_VALUE_SUBCLASS_SHORT = "Incorrect Subclass Assignment For COMPONENT VALUE Text."
	TEXT_COMP_VALUE_SUBCLASS_LONG = "Subclass Assignment For Component Value Text Not\non an Allowed Layer."
	TEXT_COMP_VALUE_SUBCLASS_MISSING = "COMPONENT VALUE Text Missing Subclass Definition"
	TEXT_COMP_VALUE_ERROR = WARNING
	TEXT_COMP_VALUE_BLOCK_ERROR = WARNING
	TEXT_COMP_VALUE_SUBCLASS_ERROR = WARNING

	TEXT_DEVICE_SHORT = "No DEVICE Text in Symbol."
	TEXT_DEVICE_LONG = "No DEVICE Text in Symbol\n DEVICE Text Has Not Been Defined in This Symbol."
	TEXT_DEVICE_SIZE_SHORT = "Incorrect Text Size For DEVICE Text."
	TEXT_DEVICE_SIZE_LONG = "Text Size For DEVICE is Incorrect."
	TEXT_DEVICE_SUBCLASS_SHORT = "Incorrect Subclass Assignment For DEVICE Text."
	TEXT_DEVICE_SUBCLASS_LONG = "Subclass Assignment For DEVICE Text Not\non an Allowed Layer."
	TEXT_DEVICE_SUBCLASS_MISSING = "DEVICE Text Missing Subclass Definition"
	TEXT_DEVICE_ERROR = WARNING
	TEXT_DEVICE_BLOCK_ERROR = WARNING
	TEXT_DEVICE_SUBCLASS_ERROR = WARNING

	TEXT_PART_NUMBER_SHORT = "No PART NUMBER Text in Symbol."
	TEXT_PART_NUMBER_LONG = "No PART NUMBER Text in Symbol\n PART NUMBER Text Has Not Been Defined in This Symbol."
	TEXT_PART_NUMBER_SIZE_SHORT = "Incorrect Text Size For PART NUMBER Text."
	TEXT_PART_NUMBER_SIZE_LONG = "Text Size For PART NUMBER is Incorrect."
	TEXT_PART_NUMBER_SUBCLASS_SHORT = "Incorrect Subclass Assignment For PART NUMBER Text."
	TEXT_PART_NUMBER_SUBCLASS_LONG = "Subclass Assignment For PART NUMBER Text Not\non an Allowed Layer."
	TEXT_PART_NUMBER_SUBCLASS_MISSING = "PART NUMBER Text Missing Subclass Definition"
	TEXT_PART_NUMBER_ERROR = ERROR
	TEXT_PART_NUMBER_BLOCK_ERROR = ERROR
	TEXT_PART_NUMBER_SUBCLASS_ERROR = ERROR

	TEXT_PART_TOL_SHORT = "No PART TOLERANCE Text in Symbol."
	TEXT_PART_TOL_LONG = "No PART TOLERANCE Text in Symbol\n PART TOLERANCE Text Has Not Been Defined in This Symbol."
	TEXT_PART_TOL_SIZE_SHORT = "Incorrect Text Size For PART TOLERANCE Text."
	TEXT_PART_TOL_SIZE_LONG = "Text Size For PART TOLERANCE is Incorrect."
	TEXT_PART_TOL_SUBCLASS_SHORT = "Incorrect Subclass Assignment For PART TOLERANCE Text."
	TEXT_PART_TOL_SUBCLASS_LONG = "Subclass Assignment For TOLERANCE Text Not\non an Allowed Layer."
	TEXT_PART_TOL_SUBCLASS_MISSING = "TOLERANCE Text Missing Subclass Definition"
	TEXT_PART_TOL_ERROR = WARNING
	TEXT_PART_TOL_BLOCK_ERROR = WARNING
	TEXT_PART_TOL_SUBCLASS_ERROR = WARNING

	/* Legal Text Layers */
	TEXT_REFDES_SUBCLASS = list( "REF DES/ASSEMBLY_TOP" "REF DES/SILKSCREEN_TOP")
	TEXT_COMP_VALUE_SUBCLASS = list( "COMPONENT VALUE/ASSEMBLY_TOP")
	TEXT_DEVICE_SUBCLASS = list( "DEVICE TYPE/ASSEMBLY_TOP") 
	TEXT_PART_TOL_SUBCLASS = list( "TOLERANCE/ASSEMBLY_TOP")
	TEXT_PART_NUMBER_SUBCLASS = list( "USER PART NUMBER/ASSEMBLY_TOP")

	TEXT_REFDES_TEXT_BLOCK = "3"
	TEXT_COMP_VALUE_TEXT_BLOCK = "3"
	TEXT_DEVICE_TEXT_BLOCK = "3"
	TEXT_PART_NUMBER_TEXT_BLOCK = "3"
	TEXT_PART_TOL_TEXT_BLOCK = "3"

/* End of Text Check */

	return()
))

