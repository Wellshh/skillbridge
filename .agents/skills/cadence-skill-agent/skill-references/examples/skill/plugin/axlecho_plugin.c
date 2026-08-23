/*INDENT OFF*/
/*------------------------------------------------------------------------*/
/*-
 *	Cadence Design Systems
 * (c) 2006 Cadence Design Systems, Inc. All rights reserved.
 * This work may not be copied, modified, re-published, uploaded, 
 * executed, or distributed in any way, in any medium, whether in 
 * whole or in part, without prior written permission from Cadence 
 * Design Systems, Inc.
 *
 */
/*------------------------------------------------------------------------*/

/*-
  This is an example of an axl skill plugin with three exported APIs
     1) an echo
     2) a data return
     3) calculate a distance between 2 points

  See axlDllDoc in Axl Reference manual for programming documentation.
 */
/*INDENT ON*/



#ifdef _WINDOWS
#include <windows.h>
#endif

// to see stdout on Windows, TELCONSOLE must be defined as a OS level 
// variable 

#include <stdio.h>
#include <string.h>
#include <math.h>
#include "axlplugin.h"

#ifdef _WINDOWS
#define AXL_DLL_DECLARE __declspec(dllexport)
#else
#define AXL_DLL_DECLARE
#endif

/*-
   This demostrates the different types of arguments
   support by axlPlugin interface. It echoes what was passed plus
   it adds the one data type only supported on output
 */

AXL_DLL_DECLARE
int
ashEcho(AXLPluginArgs *out, AXLPluginArgs *in)
{
    int i;
    AXLPluginEntry *entry;

    printf("Input data -- flag=%d count=%d\n", in->flag, in->count);
    for(i=0; i<in->count; i++) {
	entry = &in->argv[i];
	out->argv[i].type = entry->type;
    	switch(entry->type) {
    	case AP_BOOL:
            printf("\tint     %d\n", entry->data.b_value);
	    out->argv[i].data.b_value = entry->data.b_value;
	    break;
    	case AP_LONG:
            printf("\tlong     %d\n", entry->data.l_value);
	    out->argv[i].data.l_value = entry->data.l_value;
	    break;
        case AP_DOUBLE:
            printf("\tdouble  %f\n", entry->data.d_value);
	    out->argv[i].data.d_value = entry->data.d_value;
	    break;
    	case AP_CONST_STRING:
            printf("\tcchar * '%s'\n", entry->data.cs_value);
	    out->argv[i].data.cs_value = entry->data.cs_value;
	    break;
    	case AP_XY:
            printf("\txy      (%f %f)\n", entry->data.xy_value.x , entry->data.xy_value.y);
	    out->argv[i].data.xy_value = entry->data.xy_value;
	    break;
    	default:
            printf("BAD DATA  -- noargs --\n");
	    return -1;
	}
    }
    if (i < out->maxEntries) {
    	out->argv[i].type = AP_STRING;
    	out->argv[i].data.s_value = strdup("Hello from the dll!");
    	i++;
    }
    out->count = i;
    return 0;
}

/*-
   This demostrates the return value method. It returns the number
   of arguments present on input
 */
 
AXL_DLL_DECLARE
int
ashReturn(AXLPluginArgs *out, AXLPluginArgs *in)
{
    return in->count;
}


/*-
   Calculates the distance between two points
 */
 
#ifndef ABS
#   define ABS(a) ((a) >= 0 ? (a) : -(a))
#endif

AXL_DLL_DECLARE
int
ashDistance(AXLPluginArgs *out, AXLPluginArgs *in)
{
    AXLXY *xy1, *xy2;
    double dx, dy, length;

    // errors in input data
    if (in->count != 2)
	return -1;
    if ((in->argv[0].type != AP_XY) && (in->argv[1].type != AP_XY))
	return -1;

    // do the real work
    xy1 = &in->argv[0].data.xy_value;
    xy2 = &in->argv[1].data.xy_value;

    dx = (xy1->x - xy2->x);
    dy = (xy1->y - xy2->y);
    dx = ABS(dx);
    dy = ABS(dy);
    if (dx==0.0)
        length = dy;
    else if (dy==0.0)
        length = dx;
    else
        length = sqrt(dx * dx + dy * dy);

    // format data for return
    out->count = 1;
    out->argv[0].type = AP_DOUBLE;
    out->argv[0].data.d_value = length;

    return 0;
}
