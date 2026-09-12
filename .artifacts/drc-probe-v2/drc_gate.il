;;; Independent checker gate helper. Native lookup and axlDRCItem occur in one RPC.
(putd '__v2DrcItemCount nil)
(defun __v2DrcItemCount
  (kind primary secondary @optional layer objType start end width radius isClockwise center)
  (let ((target (__abFindDrcItem kind primary secondary layer objType start end width radius isClockwise center)))
    (if target then
      (let ((items (axlDRCItem t target)) projected)
        (foreach item items
          (setq projected (cons (__abProjectDrc item) projected)))
        (list t (axlDRCItem nil target) (reverse projected)))
      (list nil nil nil))))
