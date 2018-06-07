#!/bin/bash

while read sol_in sol_out
do
	res_out=`echo ${sol_in} | ./$1`
	if [ "${res_out}" != "${sol_out}" ];then
		# it means result is different.
		# otherwise, it will echo 'error' to file.
		echo "fail : must ${sol_out} but give ${res_out}"
		exit
	fi
done < case_tmp.txt

echo "correct"
