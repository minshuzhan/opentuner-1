#!/bin/bash
for i in {1..1}
do 
	echo $i >> expLog.txt
	for t in PSO GA DE PSO_GA_DE Random
	do 
		./halidetuner.py apps/bilateral_grid.cpp -t $t --stop-after 3600 --seed-config cfgs/apps/bilateral_grid062301.pk --label $t
		for d in Permutation PowerOfTwo Boolean
		do
			./halidetuner.py apps/bilateral_grid.cpp -t $t-$d --stop-after 3600 --seed-config cfgs/apps/bilateral_grid062301.pk --label $t-$d
		done
	done	
done
