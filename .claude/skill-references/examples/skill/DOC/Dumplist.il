
(defun DumpAxlFuncs (filename)
   (let (x file)
	sprintf(filename "%s/%s" getWorkingDir() filename)
	file = outfile(filename "w")
	mapcar(
	   lambda( ( x ) 
		fprintf(file "%s\n" x)
		 ) _lfn("axl")
		)
	close(file)
	t
   )
)

