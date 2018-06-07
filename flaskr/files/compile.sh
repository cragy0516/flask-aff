#!/bin/bash

if [ "$1" == "" -o "$2" == "" ];then
	echo "Usage: $0 <id>_<username> <id>"
	exit
fi

cd "${0%/*}"

docker run -it --rm \
-v "$PWD"/src/$1.c:/usr/src/myapp/$1.c \
-v "$PWD"/cases/check.sh:/usr/src/myapp/check.sh \
-v "$PWD"/cases/case_$2.txt:/usr/src/myapp/case_tmp.txt \
-w /usr/src/myapp gcc:4.9 \
timeout 10s \
/bin/bash -c "gcc -o $1 $1.c && ./check.sh $1" \
> results/result_$1.txt
