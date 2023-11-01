Name:           graphite2
Version:        1.3.10
Release:        10%{?dist}
Summary:        Font rendering capabilities for complex non-Roman writing systems
Group:          Development/Tools

License:        (LGPLv2+ or GPLv2+ or MPL) and (Netscape or GPLv2+ or LGPLv2+)
URL:            https://sourceforge.net/projects/silgraphite/
Source0:        https://downloads.sourceforge.net/project/silgraphite/graphite2//%{name}-%{version}.tgz
Patch0:         graphite-arm-nodefaultlibs.patch
Patch1:         graphite2-1.2.0-cmakepath.patch
# backports for warnings
Patch2:         0001-Fix-stricter-gcc-warnings.patch
Patch3:         0001-Fix-memory-leaks-on-realloc-failure.patch
# https://github.com/caolanm/graphite/commits/covscan_warning_1 fix/silence covscan warnings
Patch4:         0001-Related-rhbz-1602527-CTOR_DTOR_LEAK-coverity-warning.patch
Patch5:         0001-Related-rhbz-1602527-resourceLeak-cppcheck-warning.patch
Patch6:         0001-Related-rhbz-1602527-add-comment-to-silence-leaked_s.patch
Patch7:         0001-WaE-misleading-indentation.patch
Patch8:         graphite2.stack-protect.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  freetype-devel
BuildRequires:  doxygen asciidoc
BuildRequires:  texlive-helvetic texlive-sectsty texlive-tocloft texlive-xtab texlive-multirow

Obsoletes:      silgraphite < 2.3.1-5

%description
Graphite2 is a project within SIL’s Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create “smart fonts” capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Files for developing with graphite2
Group: Development/Libraries

Obsoletes: silgraphite-devel < 2.3.1-5

%description devel
Includes and definitions for developing with graphite2.

%prep
%setup -q
%patch0 -p1 -b .arm
%patch1 -p1 -b .cmake
%patch2 -p1 -b .warnings
%patch3 -p1 -b .resourceLeak
%patch4 -p1 -b .CTOR_DTOR_LEAK
%patch5 -p1 -b .leaked_storage
%patch6 -p1 -b .silence_leak
%patch7 -p1 -b .misleading-indentation
%patch8 -p1 -b .stack-protect

%build
%cmake -DGRAPHITE2_COMPARE_RENDERER=OFF  .
make %{?_smp_mflags}
make docs
sed -i -e 's!<a id="id[a-z]*[0-9]*"></a>!!g' doc/manual.html

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

# rhbz#1595710 can renable this in the next release of graphite2 where python3 is supported
#%check
#ctest

%ldconfig_scriptlets

%files
%license LICENSE COPYING
%doc ChangeLog README.md
%{_bindir}/gr2fonttest
%{_libdir}/libgraphite2.so.3
%{_libdir}/libgraphite2.so.3.0.1

%files devel
%doc doc/manual.html
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/graphite2-release.cmake
%{_libdir}/%{name}/graphite2.cmake
%{_includedir}/%{name}
%{_libdir}/libgraphite2.so
%{_libdir}/pkgconfig/graphite2.pc

%changelog
* Wed Sep 05 2018 Caolán McNamara <caolanm@redhat.com> - 1.3.10-10
- Resolves: rhbz#1624116 backport upstream stack-protect enabling

* Mon Jul 23 2018 Caolán McNamara <caolanm@redhat.com> - 1.3.10-9
- rhbz#1602527 try harder on covscan warnings

* Mon Jul 23 2018 Caolán McNamara <caolanm@redhat.com> - 1.3.10-8
- rhbz#1602527 covscan warnings

* Tue Jul 17 2018 Caolán McNamara <caolanm@redhat.com> - 1.3.10-7
- Resolves: rhbz#1595710 drop python2-fonttools buildrequire

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.10-4
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Michael Cronenworth <mike@cchtml.com> - 1.3.10-1
- New upstream release
- Resolves CVE-2017-7778

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 29 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.6-1
- update to latest release

* Wed Feb 17 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.5-1
- Resolves: rhbz#1305806 CVE-2016-1521 CVE-2016-1522 CVE-2016-1523 CVE-2016-1526

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.2.4-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.4-1
- New upstream release

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-5
- Move *.so.major symlink to main package.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Caolán McNamara <caolanm@redhat.com> - 1.2.2-3
- clarify licenses

* Wed Jun 19 2013 Karsten Hopp <karsten@redhat.com> 1.2.2-2
- use minimum texlive buildrequires, Than Ngo, rhbz#975843 

* Thu May 30 2013 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.2-1
- New upstream release

* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-4
- Drop refman.pdf as its same as manual.html
- patch install path for cmake files as they are arch dependent

* Tue Jan 29 2013 Kalev Lember <kalevlember@gmail.com> - 1.2.0-3
- Move manual.html to -devel subpackage

* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-2
- revert the wrongly committed f18 spec to f19
- spec file cleanup
- thanks to jnovy for finding me minimum texlive BR
- partial multilib fix for manual.html

* Fri Nov 9 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.0-1
- New upstream release
* Wed Oct 3 2012 Caolán McNamara <caolanm@redhat.com> - 1.1.1-4
- expand license field to cover tri-licenced GrUtfTextSrc test
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.1-2
- Fix FTBFS on ARM
* Mon Feb 27 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.1-1
- New upstream release
* Wed Feb 8 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.0-1
- New upstream release
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Fri Sep 23 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.3-1
- New upstream release
* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-3
- Obsolete silgraphite
* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-2
- Removed dependency on silgraphite-devel
- Stopped building comparerenderer - the only thing that depended on silgraphite
* Fri Aug 19 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-1
- Rebase to new release
- SPEC Cleanup
- Documentation is now properly installed
* Wed Aug 17 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-2
- Added some necessary requires
* Wed Aug 10 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-1
- Initial build of graphite2
