#!/bin/sh
#mingw32_find-debuginfo.sh - automagically generate debug info and file list
#for inclusion in an rpm spec file for mingw32-* packages.

if [ -z "$1" ] ; then BUILDDIR="."
else BUILDDIR=$1
fi

for f in `find $RPM_BUILD_ROOT -type f -name "*.exe" -or -name "*.dll"`
do
	case $(i686-pc-mingw32-objdump -h $f 2>/dev/null | egrep -o '(debug[\.a-z_]*|gnu.version)') in
	    *debuglink*) continue ;;
	    *debug*) ;;
	    *gnu.version*)
		echo "WARNING: "`echo $f | sed -e "s,^$RPM_BUILD_ROOT/*,/,"`" is already stripped!"
		continue
		;;
	    *) continue ;;
	esac

	echo extracting debug info from $f
	i686-pc-mingw32-objcopy --only-keep-debug $f $f.debug || :
	pushd `dirname $f`
	i686-pc-mingw32-objcopy --add-gnu-debuglink=`basename $f.debug` --strip-unneeded `basename $f` || :
	popd
done

find $RPM_BUILD_ROOT -type f -name "*.exe.debug" -or -name "*.dll.debug" |
    sed -n -e "s#^$RPM_BUILD_ROOT##p" > $BUILDDIR/debugfiles.list


