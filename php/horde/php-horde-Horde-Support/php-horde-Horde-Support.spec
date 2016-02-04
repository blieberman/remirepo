# remirepo/fedora spec file for php-horde-Horde-Support
#
# Copyright (c) 2012-2016 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global bootstrap    0
%global pear_name    Horde_Support
%global pear_channel pear.horde.org
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-horde-Horde-Support
Version:        2.1.5
Release:        1%{?dist}
Summary:        Horde support package

Group:          Development/Libraries
License:        BSD
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Wrapper) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Wrapper) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-support) = %{version}


%description
Support classes not tied to Horde but is used by it. These classes can be
used outside of Horde as well.

Optional dependencies:
- uuid-php or php-pecl-uuid


%prep
%setup -q -c

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%{_bindir}/phpunit .

if which php70; then
   php70 %{_bindir}/phpunit .
fi
%else
: Test disabled, missing '--with tests' option.
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Support
%{pear_testdir}/%{pear_name}


%changelog
* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4 (no change)

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3
- add dependency on Horde_Util

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2
- add provides php-composer(horde/horde-support)
- enable test suite

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 09 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Tue Jan 29 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.3-1
- Update to 2.0.3 for remi repo

* Mon Nov 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.2-1
- Update to 2.0.2 for remi repo

* Wed Nov  7 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-3
- Update to 2.0.1 for remi repo
- drop our patch, merged upstream

* Tue Nov  6 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-3
- add patch to allow uuid-php or php-pecl-uuid

* Sun Nov  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-2
- conflicts with uuid-php
- add optional %%check

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- rebuilt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-2
- backport for remi repo

* Thu Jul 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-2
- Fix packaging issues

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-1
- Upgrade to 1.0.2

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
