(putd '__abp_probe_project nil)
(defun __abp_probe_project ()
  (__abProjectComponents nil t))

(putd '__abp_probe_move nil)
(defun __abp_probe_move (refdes x y rotation)
  (__abMoveComponent refdes x y rotation))
