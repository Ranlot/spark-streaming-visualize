#!/usr/bin/env bash

fileName="pointsGenerator/points.csv"
outRoot="dataDir"

numbOfLines=60

function selectLines { 
cat $1 | head -$2 | tail -$numbOfLines
}

var=0
while true
do
	var=$((var+$numbOfLines))
	selectLines $fileName $var | hadoop fs -fs local -put - $outRoot/streamData.$var
	echo -e "\e[92m$(date)\e[0m"
	sleep 0.5
done
