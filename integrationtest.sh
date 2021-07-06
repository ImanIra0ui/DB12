#!/bin/bash

result1=$(cat result_python3.6.txt)
result2=$(cat result_python3.9.txt)
result3=$(cat result_python2.7.txt)

threshold=$(awk '{print $1/$2}' <<< "20 100")
product=$(awk '{print $1*$2}' <<< "$result3 $threshold")

difference1=$(awk '{print $1-$2}' <<< "$result1 $result3")
difference2=$(awk '{print $1-$2}' <<< "$result2 $result3")

if (( $(echo $difference1#- $product | awk '{if ($1 > $2) print 1;}') )); 
  then echo "The results provided by python 2.7 and python 3.6 are not the same"; 
else echo "The results provided by python 2.7 and python 3.6 are the same within the threshold"; 
  fi

if (( $(echo $difference2#- $product | awk '{if ($1 > $2) print 1;}') )); 
  then echo "The results provided by python 2.7 and python 3.9 are not the same"; 
else echo "The results provided by python 2.7 and python 3.9 are the same within the threshold"; 
  fi
