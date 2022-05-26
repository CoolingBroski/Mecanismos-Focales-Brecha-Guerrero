#!/bin/bash

cd Datos

cat ../catalogSSN.dat | while read line
do
	date=$(echo $line | awk '{print $2}')
	time=$(echo $line | awk '{print $3}')
	
	datetime=$(date -d "$date $time 10 seconds ago" +%Y/%m/%d,%H:%M:%S)

	cat ../station_list.txt | while read sta
	do
		echo "WIN IG $sta HH_ $datetime +370s" | ~/SSNstp
	done
done
