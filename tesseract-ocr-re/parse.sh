#!/bin/bash
for f in $1/*/*.jpg;  
	do {
		if [ ! -f "$f.txt" ];
			then {
				echo $f
				tesseract "${f}" "${f}" --dpi 150 
			}
		fi
	} done
