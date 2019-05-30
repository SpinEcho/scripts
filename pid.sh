#!/bin/bash
proc=$( top -b -n 1 | grep $1 | awk '{print $1}' )
str=$'har följande ID:\n'
echo $1 "$str" $proc
