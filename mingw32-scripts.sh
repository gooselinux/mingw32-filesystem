#!/bin/sh -

# mingw32-scripts
# Copyright (C) 2008 Red Hat Inc., Richard W.M. Jones.
# Copyright (C) 2008 Levente Farkas
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# This is a useful command-line script through which one can use the
# macros from mingw32-macros.mingw32 cross-compilation. 

if [ "`basename $0`" = "i686-pc-mingw32-pkg-config" ] ; then
    NAME="_mingw32_pkg_config"
else
    NAME="_`basename $0|tr -- - _`"
fi

# NOTE: The use of 'eval' in combination with '$@' is a potential security risk
#       We should find a more safe replacement for this command
#       Suggestions are welcome at the Fedora MinGW mailing list
eval "`rpm --eval "%{$NAME}"`" '"$@"'
