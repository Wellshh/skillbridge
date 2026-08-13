### Allegro User Guide: SKILL Reference Product Version 17.2-2016 April 2016

12
==

Simple Graphics Drawing Functions
=================================

This chapter describes the AXL-SKILL functions related to Simple Graphics Drawing. You use these drawing utilities for drawing into bitmap areas such as thumbnails within the UIF forms package.

`axlGRP` is the AXL interface to a Simple Graphics Drawing utility.

You can simplify application drawing into thumbnails within forms as follows:

* Specify the thumbnail field within the form file. This should not have a bitmap associated with it.

* Call the`axlGRPDrwInit` function with the form, field name, and a callback function. Keep the handle returned by this function so you can use it in later processing.

* Using the functions provided, redraw the image. The callback function is invoked with the graphics handle as the parameter.

* Use the`axlGRPDrwUpdate` function to trigger the callback function.

**Note:** The application*cannot* set bitmaps or graphics callbacks using the facilities outlined in the Thumbnail documentation while using this package.

Simple Graphics Drawing package supports the following:

* Rectangles (Filled and unfilled)

* Polygons (Filled and unfilled)

* Circles (Filled and unfilled)

* Simple Lines

* Poly Lines

* Bitmaps

* Text

This package supports a mappable coordinate system. With the`GRPDrwMapWindow` function, you can specify a rectangle that gets mapped to the actual drawing area. An aspect ratio of 1 to 1 is maintained.

The zero point of the drawing area is the upper left point of the drawing:

**Note:** Objects drawn earlier are overlapped by objects drawn later. The application must manage this.

**Setting Option Properties on the r\_graphics Handle**

You can set option properties on the`r_graphics` handle before calling the drawing functions. These properties, if applicable, are used by the drawing properties.

****Table 12-1****
**r\_graphics Option Properties**

| **Option** | **Default** | **Description** | **Available Settings**
| color | black | Applies to all elements. | black, white, red, green, yellow, blue, lightblue, rose, purple, teal, darkpink, darkmagenta, aqua, gray, olive, orange, pink, beige, navy, violet, silver, rust, lime, brown, mauve, magenta, lightpink, cyan, salmon, peach, darkgray, button (represents the current button color)
| fill | unfilled | Applies only to rectangles and polygons. | filled, filled\_solid, unfilled
| width | 0 | Applies only when geometric elements are unfilled. |
| text\_align | left | Text justification. Applies only to text. | left, center, right
| text\_bkmode | transparent | Text background display mode. Applies only to text. | transparent, opaque
**Examples**

See`<``cdsroot``>/share/pcb/examples/skill/form/basic/axlform.il` for a complete example.

Functions
---------

### axlGRPDrwBitmap

`axlGRPDrwBitmap(r_graphicst_bitmap)⇒ t/nil`

#### Description

Loads a bitmap into a form draw window (drawing area in the graphics field). More drawing can take place on top of the bitmap.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
| `t_bitmap` | Name of bitmap file. File must be on the`BMPPATH`, with `.bmp` as the extension.
#### Value Returned

|  |
| --- | ---
| `t` | Bitmap loaded into drawing area in the graphics field.
| `nil` | No bitmap loaded into the drawing area in the graphics field due to invalid arguments.
### axlGRPDrwCircle

`axlGRPDrwCircle(r_graphicsl_originx_radius)⇒ t/nil`

#### Description

Draws a circle into the area identified by the`r_graphics` handle, at the origin specified, and with the specified radius. Option properties attached to the `r_graphics` handle are applied when drawing the circle.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
| `l_origin` | List noting the`x` and `y` coordinates of the origin.
| `x_radius` | Integer noting the radius of the circle.
#### Value Returned

|  |
| --- | ---
| `t` | Circle drawn.
| `nil` | No circle drawn due to invalid arguments.
### axlGRPDrwInit

`axlGRPDrwInit(r_formt_fieldt_func)⇒ r_graphics/nil`

#### Description

Use this command to set graphics callback in a form field. It sets up necessary data structures for triggering the graphics callback into the graphics field.

#### Arguments

|  |
| --- | ---
| `r_form` | Handle of the form.
| `t_field` | Name of field into which the package should draw. (Only`THUMBNAIL` fields are supported.)
| `t_func` | Name of the drawing callback function. Callback function is invoked with the graphics handle as the parameter.
#### Value Returned

|  |
| --- | ---
| `r_graphics` | Graphics package handle.
| `nil` | Failed to set up necessary data structures for triggering the graphics callback due to invalid arguments.
### axlGRPDrwLine

`axlGRPDrwLine(r_graphicsl_vertices)⇒ t/nil`

#### Description

Draws a line into the area identified by the`r_graphics` handle and the list of coordinates. Option properties attached to the `r_graphics` handle are applied when drawing the line.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
| `l_vertices` | List of coordinates describing the line.
#### Value Returned

|  |
| --- | ---
| `t` | Line drawn.
| `nil` | No line drawn due to invalid arguments.
### axlGRPDrwMapWindow

`axlGRPDrwMapWindow(r_graphicsx_hgtx_width)⇒ t/nil`

#### Description

Forces a draw in a form draw field. Allows the application to denote the coordinate system that is mapped into the drawing area of the graphics field.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
| `x_hgt` | Height of drawing window.
| `x_width` | Width of drawing window.
#### Value Returned

|  |
| --- | ---
| `t` | Successful
| `nil` | Error occurred due to invalid arguments.
### axlGRPDrwPoly

`axlGRPDrwPoly(r_graphicsl_vertices)⇒ t/nil`

#### Description

Draws a polygon (multi-segment line) into the area identified by the`r_graphics` handle and the list of coordinates. Option properties attached to the `r_graphics` handle are applied when drawing the polygon. If the coordinates do not form a closed polygon, the first and last coordinates in the list are connected by a straight line.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
| `l_vertices` | List of coordinates describing the line.
#### Value Returned

|  |
| --- | ---
| `t` | Polygon or line drawn.
| `nil` | No polygon or line drawn due to invalid arguments.
### axlGRPDrwRectangle

`axlGRPDrwRectangle(r_graphicsl_upper_leftl_lower_right)⇒ t/nil`

#### Description

Draws a rectangle into the area identified by the`r_graphics` handle and the `upper_left` and `lower_right` coordinates. Option properties attached to the `r_graphics` handle are applied when drawing the rectangle.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
| `l_upper_left` | List noting the coordinate of the upper left point of the rectangle.
| `l_lower_right` | List noting the coordinate of the lower right point of the rectangle.
#### Value Returned

|  |
| --- | ---
| `t` | Rectangle drawn.
| `nil` | No rectangle drawn due to incorrect arguments.
### axlGRPDrwText

`axlGRPDrwText(r_graphicsl_origint_text)⇒ t/nil`

#### Description

Draws text into the area identified by the`r_graphics` handle at the origin specified. Option properties attached to the `r_graphics` handle are applied when drawing the text.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
| `l_origin` | List noting the`x` and `y` coordinate of the origin.
| `t_text` | Text string to be drawn.
#### Value Returned

|  |
| --- | ---
| `t` | Text drawn.
| `nil` | No text drawn due to incorrect arguments.
### axlGRPDrwUpdate

`axlGRPDrwUpdate(r_graphics)⇒ t/nil`

#### Description

Force call to register callback function for a draw window. Triggers calling of the application supplied callback function.

#### Arguments

|  |
| --- | ---
| `r_graphics` | Graphics handle.
#### Value Returned

|  |
| --- | ---
| `t` | Application supplied callback function called.
| `nil` | No callback function called due to an incorrect argument.
####




For support, see [Cadence Online Support](http://support.cadence.com) service.



*Copyright © 2017, [Cadence Design Systems, Inc.](http://www.cadence.com)*


All rights reserved.
