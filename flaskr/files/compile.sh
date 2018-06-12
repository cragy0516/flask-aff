#!/bin/bash

if [ "$1" == "" -o "$2" == "" ];then
	echo "Usage: $0 <id>_<username> <id>"
	exit
fi

cd "${0%/*}"

if [ ! -e "$PWD"/src/$1.c ] || [ ! -e "$PWD"/cases/check.sh ] || [ ! -e "$PWD"/cases/case_$2.txt ] || [ ! -e "$PWD"/cases/programs/case_$2 ]; then
	echo "error"
	exit 1 
fi

docker run -it --rm \
-v "$PWD"/src/$1.c:/usr/src/myapp/$1.c \
-v "$PWD"/cases/check.sh:/usr/src/myapp/check.sh \
-v "$PWD"/cases/case_$2.txt:/usr/src/myapp/case_tmp.txt \
-v "$PWD"/cases/programs/case_$2:/usr/src/myapp/programs/solution \
-w /usr/src/myapp gcc:4.9 \
timeout 5s \
/bin/bash -c "gcc -std=c99 -w -o $1 $1.c && ./check.sh $1" \
> results/result_$1.txt
