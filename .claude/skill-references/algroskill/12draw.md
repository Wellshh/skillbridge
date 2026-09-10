### axlGRPDrwBitmap

`axlGRPDrwBitmap( r_graphics t_bitmap ) => t/nil`

#### Description

Loads a bitmap into a form draw window (drawing area in the graphics field). More drawing can take place on top of the bitmap.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |
| `t_bitmap` | Name of bitmap file. File must be on the `BMPPATH`, with `.bmp` as the extension. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Bitmap loaded into drawing area in the graphics field. |
| `nil` | No bitmap loaded into the drawing area in the graphics field due to invalid arguments. |

### axlGRPDrwCircle

`axlGRPDrwCircle( r_graphics l_origin x_radius ) => t/nil`

#### Description

Draws a circle into the area identified by the `r_graphics` handle, at the origin specified, and with the specified radius. Option properties attached to the `r_graphics` handle are applied when drawing the circle.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |
| `l_origin` | List noting the `x` and `y` coordinates of the origin. |
| `x_radius` | Integer noting the radius of the circle. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Circle drawn. |
| `nil` | No circle drawn due to invalid arguments. |

### axlGRPDrwInit

`axlGRPDrwInit( r_form t_field t_func ) => r_graphics/nil`

#### Description

Use this command to set graphics callback in a form field. It sets up necessary data structures for triggering the graphics callback into the graphics field.

#### Arguments

| Name | Description |
|---|---|
| `r_form` | Handle of the form. |
| `t_field` | Name of field into which the package should draw. (Only `THUMBNAIL` fields are supported.) |
| `t_func` | Name of the drawing callback function. Callback function is invoked with the graphics handle as the parameter. |

#### Value Returns

| Name | Description |
|---|---|
| `r_graphics` | Graphics package handle. |
| `nil` | Failed to set up necessary data structures for triggering the graphics callback due to invalid arguments. |

### axlGRPDrwLine

`axlGRPDrwLine( r_graphics l_vertices ) => t/nil`

#### Description

Draws a line into the area identified by the `r_graphics` handle and the list of coordinates. Option properties attached to the `r_graphics` handle are applied when drawing the line.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |
| `l_vertices` | List of coordinates describing the line. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Line drawn. |
| `nil` | No line drawn due to invalid arguments. |

### axlGRPDrwMapWindow

`axlGRPDrwMapWindow( r_graphics x_hgt x_width ) => t/nil`

#### Description

Forces a draw in a form draw field. Allows the application to denote the coordinate system that is mapped into the drawing area of the graphics field.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |
| `x_hgt` | Height of drawing window. |
| `x_width` | Width of drawing window. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Successful |
| `nil` | Error occurred due to invalid arguments. |

### axlGRPDrwPoly

`axlGRPDrwPoly( r_graphics l_vertices ) => t/nil`

#### Description

Draws a polygon (multi-segment line) into the area identified by the `r_graphics` handle and the list of coordinates. Option properties attached to the `r_graphics` handle are applied when drawing the polygon. If the coordinates do not form a closed polygon, the first and last coordinates in the list are connected by a straight line.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |
| `l_vertices` | List of coordinates describing the line. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Polygon or line drawn. |
| `nil` | No polygon or line drawn due to invalid arguments. |

### axlGRPDrwRectangle

`axlGRPDrwRectangle( r_graphics l_upper_left l_lower_right ) => t/nil`

#### Description

Draws a rectangle into the area identified by the `r_graphics` handle and the `upper_left` and `lower_right` coordinates. Option properties attached to the `r_graphics` handle are applied when drawing the rectangle.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |
| `l_upper_left` | List noting the coordinate of the upper left point of the rectangle. |
| `l_lower_right` | List noting the coordinate of the lower right point of the rectangle. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Rectangle drawn. |
| `nil` | No rectangle drawn due to incorrect arguments. |

### axlGRPDrwText

`axlGRPDrwText( r_graphics l_origin t_text ) => t/nil`

#### Description

Draws text into the area identified by the `r_graphics` handle at the origin specified. Option properties attached to the `r_graphics` handle are applied when drawing the text.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |
| `l_origin` | List noting the `x` and `y` coordinate of the origin. |
| `t_text` | Text string to be drawn. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Text drawn. |
| `nil` | No text drawn due to incorrect arguments. |

### axlGRPDrwUpdate

`axlGRPDrwUpdate( r_graphics ) => t/nil`

#### Description

Force call to register callback function for a draw window. Triggers calling of the application supplied callback function.

#### Arguments

| Name | Description |
|---|---|
| `r_graphics` | Graphics handle. |

#### Value Returns

| Name | Description |
|---|---|
| `t` | Application supplied callback function called. |
| `nil` | No callback function called due to an incorrect argument. |

Return to top of page
 
 
 
 
 
 



 
 
 
 
 
 
 
 
 
 
 
 
 
For support, see Cadence Online Support service.
 
 
 
 Copyright © 2017, Cadence Design Systems, Inc.
 
 
 
All rights reserved.

