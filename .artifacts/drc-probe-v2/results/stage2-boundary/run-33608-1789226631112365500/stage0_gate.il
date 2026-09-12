;;; Stage0 direct DRC evidence helper
(putd '__v2DrcItemCount nil)
(defun __v2DrcItemCount (kind primary secondary @optional layer objType start end width radius isClockwise center)
  (let ((start2 (if (and start (listp start)) start start))
        (end2 (if (and end (listp end)) end end))
        (center2 (if (and center (listp center)) center center))
        target projected items count)
    (setq target (__abFindDrcItem kind primary secondary layer objType start2 end2 width radius isClockwise center2))
    (if target then
      (progn (setq count (axlDRCItem nil target)) (setq items (axlDRCItem t target))
        (foreach item items (setq projected (cons (list nil 'data (__abProjectDrc item) 'waived item->waived 'allegro_generated item->fixed) projected)))
        (list nil 'resolved t 'count count 'markers (reverse projected)
          'args (list nil 'kind kind 'primary primary 'layer layer 'objType objType 'start start 'end end 'width width 'radius radius 'clockwise isClockwise 'center center)
          'canonical (list nil 'start start2 'end end2 'center center2)))
      else (list nil 'resolved nil 'count nil 'markers nil
        'args (list nil 'kind kind 'primary primary 'layer layer 'objType objType 'start start 'end end 'width width 'radius radius 'clockwise isClockwise 'center center)
        'canonical (list nil 'start start2 'end end2 'center center2)))))
(putd '__v2DrcSnapshot nil)
(defun __v2DrcSnapshot ()
  (let ((items axlDBGetDesign()->drcs) projected)
    (foreach item items (setq projected (cons (list nil 'data (__abProjectDrc item) 'waived item->waived 'allegro_generated item->fixed) projected)))
    (list nil 'count (axlDRCGetCount) 'markers (reverse projected))))


