;;; Stage I smoke helper.  All DBIDs are consumed inside one transaction RPC.
(putd '__v2DesignExtent nil)
(defun __v2DesignExtent ()
  (let ((p (axlGetParam "paramDesign")))
    (list nil
          'bBox (when p p->bBox)
          'xy (when p p->xy)
          'width (when p p->width)
          'height (when p p->height))))

(putd '__v2Point17 nil)
(defun __v2Point17 (p)
  (when p
    (list nil 'x (car p) 'y (cadr p)
          'x17 (sprintf nil "%.17g" (car p))
          'y17 (sprintf nil "%.17g" (cadr p)))))

(putd '__v2Segment17 nil)
(defun __v2Segment17 (s net)
  (let ((ends s->startEnd) arc)
    (setq arc (equal s->objType "arc"))
    (list nil
          'objType s->objType 'net net 'layer s->layer
          'start (__v2Point17 (car ends))
          'end (__v2Point17 (cadr ends))
          'width s->width 'width17 (sprintf nil "%.17g" s->width)
          'length (axlDBGetLength s)
          'length17 (sprintf nil "%.17g" (axlDBGetLength s))
          'radius (when arc s->radius)
          'radius17 (when arc (sprintf nil "%.17g" s->radius))
          'clockwise (when arc s->isClockwise)
          'center (__v2Point17 (when arc s->xy)))))

(putd '__v2Stage1Create nil)
(defun __v2Stage1Create (kind net layer padstack start end width clockwise center)
  (let ((extent (__v2DesignExtent)) created path seg via viaResult stepResult)
    (cond
      ((equal kind 'via)
       (setq viaResult (axlDBCreateVia padstack start net nil 0))
       (unless (and viaResult (car viaResult)) (error "STAGE1_VIA_CREATE_RETURN_INVALID"))
       (setq via (car viaResult))
       (unless via (error "STAGE1_VIA_CREATE_FAILED"))
       (list nil 'kind "via" 'request
             (list nil 'x17 (sprintf nil "%.17g" (car start))
                       'y17 (sprintf nil "%.17g" (cadr start)))
             'extent extent 'committed
             (list nil 'padstack via->name 'net net
                   'x (car via->xy) 'y (cadr via->xy)
                   'x17 (sprintf nil "%.17g" (car via->xy))
                   'y17 (sprintf nil "%.17g" (cadr via->xy))
                   'start_layer (car via->startEnd)
                   'end_layer (cadr via->startEnd)
                   'mirroring (if via->isMirrored then "mirrored" else "unmirrored"))))
      (t
       (when (and (equal kind 'arc) (null center))
         (error "STAGE1_ARC_CENTER_MISSING"))
       (let ((p (axlPathStart (list start) width)))
         (if (equal kind 'arc)
             (setq stepResult (axlPathArcCenter p width end clockwise center))
             (setq stepResult (axlPathLine p nil end)))
         (unless stepResult (error "STAGE1_PATH_STEP_RETURN_NIL"))
         (setq created (axlDBCreatePath p layer net)))
       (unless (and created (car created) (car (car created)))
         (error "STAGE1_ROUTE_CREATE_RETURN_INVALID"))
       (setq path (car (car created)))
       (unless (equal (length path->segments) 1)
         (error "STAGE1_ROUTE_SEGMENT_COUNT_NOT_ONE"))
       (setq seg (car path->segments))
       (unless seg (error "STAGE1_ROUTE_SEGMENT_MISSING"))
       (list nil 'kind kind 'request
             (list nil 'start (__v2Point17 start) 'end (__v2Point17 end)
                       'width17 (sprintf nil "%.17g" width)
                       'clockwise clockwise
                       'center (__v2Point17 center))
             'extent extent 'committed
             (__v2Segment17 seg
               (when (and path->net (not (stringp path->net))) path->net->name)))))))
