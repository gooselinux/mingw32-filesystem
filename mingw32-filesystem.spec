%define debug_package %{nil}

Name:           mingw32-filesystem
Version:        63
Release:        4%{?dist}
Summary:        MinGW base filesystem and environment

Group:          Development/Libraries
License:        GPLv2+
URL:            http://hg.et.redhat.com/misc/fedora-mingw--devel/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Source0:        COPYING
Source1:        macros.mingw32
Source2:        mingw32.sh
#Source3:        mingw32.csh
Source4:        mingw32-find-requires.sh
Source5:        mingw32-find-provides.sh
Source6:        mingw32-scripts.sh
Source7:        mingw32-rpmlint.config
Source8:        Toolchain-mingw32.cmake
Source9:        mingw32-find-debuginfo.sh

Requires:       pkgconfig

# Note about 'Provides: mingw32(foo.dll)'
# ------------------------------------------------------------
#
# We want to be able to build & install mingw32 libraries without
# necessarily needing to install wine.  (And certainly not needing to
# install Windows!)  There is no requirement to have wine installed in
# order to use the mingw toolchain to develop software (ie. to
# compile more stuff on top of it), so why require that?
#
# So for expediency, this base package provides the "missing" DLLs
# from Windows.  Another way to do it would be to exclude these
# proprietary DLLs in our find-requires checking script - essentially
# it comes out the same either way.
#
Provides:       mingw32(gdi32.dll)
Provides:       mingw32(kernel32.dll)
Provides:       mingw32(ole32.dll)
Provides:       mingw32(mscoree.dll)
Provides:       mingw32(msvcrt.dll)
Provides:       mingw32(user32.dll)
Provides:       mingw32(wldap32.dll)
Provides:       mingw32(glut32.dll)
Provides:       mingw32(secur32.dll)
Provides:       mingw32(version.dll)
Provides:       mingw32(cfgmgr32.dll)
Provides:       mingw32(setupapi.dll)
Provides:       mingw32(rpcrt4.dll)
Provides:       mingw32(ws2_32.dll)
Provides:       mingw32(gdiplus.dll)
Provides:       mingw32(odbc32.dll)


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING
sed 's/@VERSION@/%{version}/' < %{SOURCE4} > mingw32-find-requires.sh


%build
# nothing


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/mingw32-scripts

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
install -m 755 %{SOURCE7} $RPM_BUILD_ROOT%{_mingw32_bindir}/

mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
for i in mingw32-configure mingw32-make mingw32-pkg-config i686-pc-mingw32-pkg-config mingw32-cmake mingw32-qmake-qt4; do
  ln -s %{_libexecdir}/mingw32-scripts $i
done
popd

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
#install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.mingw32

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/rpmlint/

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32

# GCC requires these directories, even though they contain links
# to binaries which are also installed in /usr/bin etc.  These
# contain Fedora native binaries.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/lib

# The MinGW system root which will contain Windows native binaries
# and Windows-specific header files, pkgconfig, etc.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/include
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/sys
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/pkgconfig

mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal

# We don't normally package manual pages and info files, except
# where those are not supplied by a Fedora native package.  So we
# need to create the directories.
#
# Note that some packages try to install stuff in
#   /usr/i686-pc-mingw32/sys-root/mingw/man and
#   /usr/i686-pc-mingw32/sys-root/mingw/doc
# but those are both packaging bugs.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man
mkdir -p $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man{1,2,3,4,5,6,7,8,l,n}

# NB. NOT _libdir
mkdir -p $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 mingw32-find-requires.sh $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/usr/lib/rpm
install -m 0755 %{SOURCE9} $RPM_BUILD_ROOT/usr/lib/rpm

mkdir -p $RPM_BUILD_ROOT%{_datadir}/mingw32
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_datadir}/mingw32

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/rpm/macros.mingw32
%config(noreplace) %{_sysconfdir}/profile.d/mingw32.sh
#%config(noreplace) %{_sysconfdir}/profile.d/mingw32.csh
%dir %{_sysconfdir}/rpmlint
%config(noreplace) %{_sysconfdir}/rpmlint/mingw32-rpmlint.config
%{_bindir}/mingw32-configure
%{_bindir}/mingw32-make
%{_bindir}/mingw32-pkg-config
%{_bindir}/i686-pc-mingw32-pkg-config
%{_bindir}/mingw32-cmake
%{_bindir}/mingw32-qmake-qt4
%{_libexecdir}/mingw32-scripts
%{_prefix}/i686-pc-mingw32/
%{_datadir}/mingw32
/usr/lib/rpm/mingw32-*


%changelog
* Mon Jan 03 2011 Andrew Beekhof <abeekhof@redhat.com> - 63-4
- Drop mingw32(libstdc++-6.dll) again now that everything is rebuilt
  Related: rhbz#658833

* Mon Dec 27 2010 Andrew Beekhof <abeekhof@redhat.com> - 63-3
- Temporarily provide mingw32(libstdc++-6.dll) so that we can install
  mingw32-pthreads so we can install mingw32-gcc so we can recompile 
  mingw32-pthreads to no longer require mingw32(libstdc++-6.dll).
- Drop the ExclusiveArch tag, its incompatible with noarch
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 63-2.1
- Only build mingw packages on x86_64
  Related: rhbz#658833

* Wed Dec 22 2010 Andrew Beekhof <abeekhof@redhat.com> - 63-2
- Bump the revision to avoid tag collision
  Related: rhbz#658833

* Thu Nov 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 63-1
- Set the CMAKE_RC_COMPILER variable in the CMake toolchain file (RHBZ #652435)

* Tue Oct 19 2010 Ivan Romanov <drizt@land.ru> - 62-2
- Added mingw32-qmake-qt4

* Mon Oct 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 62-1
- Provide mingw32(odbc32.dll) for Qt

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 61-1
- Provide mingw32(gdiplus.dll) for gdk-pixbuf

* Thu Sep  9 2010 Richard W.M. Jones <rjones@redhat.com> - 60-1
- Provide virtual mingw32(ws2_32.dll) for libvirt.

* Mon Sep 06 2010 Kalev Lember <kalev@smartlink.ee> - 59-1
- Own /etc/rpmlint/ dir instead of depending on rpmlint package (RHBZ#629791)

* Fri Sep  3 2010 Richard W.M. Jones <rjones@redhat.com> - 58-1
- Remove requires setup and rpm (RHBZ#629791).

* Tue Jun  8 2010 Richard W.M. Jones <rjones@redhat.com> - 57-1
- Add provides mingw32(rpcrt4.dll) (RHBZ#594581).

* Mon May 24 2010 Kalev Lember <kalev@smartlink.ee> - 56-2
- Work around cmake's Qt detection in the toolchain file

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org. - 56-1
- Prevented a circular dependency which caused the i686-pc-mingw32-pkg-config
  script to be broken. Thanks to Kalev Lember for spotting this bug

* Tue Sep  1 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 55-1
- The wrapper scripts i686-pc-mingw32-pkg-config, mingw32-pkg-config,
  mingw32-configure, mingw32-make and mingw32-cmake had a bug where
  quoted arguments could get interpreted incorrect.
  Thanks to Michael Ploujnikov for helping out with this issue

* Sat Aug 29 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 54-1
- Added the file /usr/bin/i686-pc-mingw32-pkg-config which is a wrapper script
  which calls pkg-config with the right environment variables set (BZ #513825)

* Sun Aug 23 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 53-1
- Fixed a small rpmlint warning caused by the debuginfo generation macro
  Thanks to Kalev Lember for spotting this

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 52-2
- Updated ChangeLog comment from previous version as the RPM variable
  __debug_install_post needs to be overridden instead of __os_install_post
  for -debuginfo subpackage generation

* Mon Jun 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 52-1
- Add script to create -debuginfo subpackages
  This script was created by Fridrich Strba
- All mingw32 packages now need to add these lines to their .spec files:
  %%define __debug_install_post %%{_mingw32_debug_install_post}
  %%{_mingw32_debug_package}

* Thu Jun  4 2009 Adam Goode <adam@spicenitz.org> - 51-1
- Add CMake rules

* Tue Apr 21 2009 Richard W.M. Jones <rjones@redhat.com> - 50-4
- Fix dependency problem with + in DLL name (Thomas Sailer).

* Fri Mar 27 2009 Richard W.M. Jones <rjones@redhat.com> - 50-3
- Fix up and test mingw32-pkg-config changes.

* Thu Mar 26 2009 Levente Farkas <lfarkas@lfarkas.org> - 50-1
- Add mingw32-pkg-config.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 49-2
- Rebuild for mingw32-gcc 4.4

* Thu Feb 19 2009 Richard W.M. Jones <rjones@redhat.com> - 49-1
- Added virtual provides for mingw32(cfgmgr32.dll) and mingw32(setupapi.dll).

* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 48-1
- Fix _mingw32_configure.

* Tue Feb 17 2009 Richard W.M. Jones <rjones@redhat.com> - 47-1
- Rename mingw32-COPYING to COPYING.
- Rename mingw32-macros.mingw32 to macros.mingw32.
- _mingw32_configure looks for configure in "." and ".." dirs.
- Added _mingw32_description.
- Added mingw32(version.dll) virtual provides (rhbz#485842).

* Sun Feb  1 2009 Richard W.M. Jones <rjones@redhat.com> - 46-1
- Unset PKG_CONFIG_PATH because /usr/lib/rpm/macros sets it (Erik van
  Pienbroek).

* Wed Jan 28 2009 Richard W.M. Jones <rjones@redhat.com> - 45-1
- Use PKG_CONFIG_LIBDIR instead of PKG_CONFIG_PATH so that native pkgconfig
  is never searched.

* Mon Jan 26 2009 Richard W.M. Jones <rjones@redhat.com> - 44-1
- Install rpmlint overrides file to suppress some rpmlint warnings.

* Sat Jan 24 2009 Richard W.M. Jones <rjones@redhat.com> - 43-6
- Don't claim C++ compiler exists if it's not installed, as this
  breaks autoconf and (in particular) libtool.

* Wed Jan 14 2009 Richard W.M. Jones <rjones@redhat.com> - 42-1
- Add pseudo-provides secur32.dll

* Wed Dec 17 2008 Levente Farkas <lfarkas@lfarkas.org> - 41-1
- Re-add mingw32-make

* Sat Dec  6 2008 Levente Farkas <lfarkas@lfarkas.org> - 40-2
- Rewrite mingw32-scripts to run in the current shell
- (Re-add mingw32-make) - Removed by RWMJ.
- Add mingw32-env to mingw32.sh

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 39-3
- Unify mingw32-filesystem packages from all three branches again, and test.
- Fix mingw32-scripts so it can handle extra parameters correctly.
- Remove mingw32-env & mingw32-make since neither of them actually work.

* Sun Nov 23 2008 Richard Jones <rjones@redhat.com> - 38-1
- Added mingw32(glut32.dll).

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 37-1
- Revert part of the 36-1 patch.  --build option to configure was wrong.

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 36-1
- Greatly improved macros (Levente Farkas).
- Added -mms-bitfields.

* Thu Nov 13 2008 Richard Jones <rjones@redhat.com> - 35-1
- Added mingw32(wldap32.dll) pseudo-provides.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 34-1
- Set --prefix correctly.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 33-1
- Remove mingw32.{sh,csh} which are unused.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 32-1
- Add mingw32-configure script.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 31-1
- Update the spec file with explanation of the 'Provides: mingw32(...)'
  lines for Windows system DLLs.

* Mon Oct  6 2008 Richard Jones <rjones@redhat.com> - 30-1
- Added _mingw32_cxx.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 29-1
- Added _mingw32_as, _mingw32_dlltool, _mingw32_windres.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 27-1
- Begin the grand renaming of mingw -> mingw32.
- Added mingw32(mscoree.dll).

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 25-1
- Add shared aclocal directory.

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 24-1
- Remove mingw-defs, since no longer used.
- Add _mingw_infodir.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 23-1
- Add macros for find-provides/requires scripts

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 22-1
- Windows provides OLE32.DLL.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 21-1
- Allow '.' in dll names for find-requires
- Windows provides GDI32.DLL.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 20-1
- On 64 bit install in /usr/lib/rpm always.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 19-1
- 'user32.dll' is provided by Windows.
- Allow '-' in DLL names.
- More accurate detection of DLLs in requires/provides scripts.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 17-1
- Automatically add mingw-filesystem and mingw-runtime requires.
- Add --prefix to _mingw_configure macro.
- Three backslashes required on each continuation line in RPM macros.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 14-1
- Fix path to mingw-find-requires/provides scripts.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 12-1
- Put CFLAGS on a single line to avoid problems in some configure scripts.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 10-1
- Provides certain base Windows DLLs (not literally).

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 9-1
- Include RPM dependency generators and definitions.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4-1
- Add _mingw_cc/cflags/etc. and _mingw_configure macros.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3-1
- Add _mingw_host macro.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2-1
- Add _mingw_sysroot macro.
- Add _mingw_target macro.

* Mon Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1-1
- Basic filesystem layout.
