#!/bin/sh
set -e
url=git://sourceware.org/git/glibc.git
package=glibc
tag=glibc-2.39
branch=release/2.39/master
out=$package-git.patch
repo=$package.git

# use filterdiff, etc to exclude bad chunks from diff
filter() {
	cat
}

if [ ! -d $repo ]; then
	git clone --bare $url -b $branch $repo
fi

cd $repo
	git fetch origin +$branch:$branch +refs/tags/$tag:refs/tags/$tag
	git log -p --date=default --reverse $tag..$branch | filter > ../$out.tmp
cd ..

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}

../md5 $package.spec
../dropin $out
