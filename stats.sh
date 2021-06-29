#!/usr/bin/env bash

workdir=/tmp/github-stats
repo=https://github.com/milvus-io/milvus.git
branch=master

mkdir -p ${workdir}
pushd ${workdir} || exit
git clone ${repo} repo
pushd repo || exit
git checkout ${branch}
git ls-files | xargs -n1 git blame --line-porcelain | sed -n 's/^author-mail //p' | sort -f | uniq -ic | sort -nr \
    > ../lines.txt
popd || exit
cat lines.txt
popd || exit

