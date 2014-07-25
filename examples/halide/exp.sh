#!/bin/bash
date > expLog.txt
for t in PSO GA DE PSO_GA_DE Random
do 
	./halidetuner.py apps/bilateral_grid.cpp -t $t --stop-after 3600 --seed-config cfgs/apps/bilateral_grid062301.pk  
	for d in Permutation PowerOfTwo Boolean
	do
		./halidetuner.py apps/bilateral_grid.cpp -t $t-$d --stop-after 3600 --seed-config cfgs/apps/bilateral_grid062301.pk 
	done
done	
echo $i >> expLog.txt
