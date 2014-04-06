# Spec file for php-sabre-vobject
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    dd1dd19b6601cdc99408b70ec260052825f70b8f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     fruux
%global gh_project   sabre-vobject
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-%{gh_project}
Summary:        Library to parse and manipulate iCalendar and vCard objects
Version:        3.2.0
Release:        1%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz
License:        BSD
Group:          Development/Libraries

# replace composer autloader by PSR-O trivial one
Patch0:         %{gh_project}-bin.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
%endif

# From composer.json
Requires:       php(language) >= 5.3.1
Requires:       php-mbstring
# From phpcompatinfo report for version 3.2.0
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xml


%description
The VObject library allows you to easily parse and manipulate iCalendar
and vCard objects using PHP. The goal of the VObject library is to create
a very complete library, with an easy to use API.

This project is a spin-off from SabreDAV, where it has been used for several
years. The VObject library has 100% unittest coverage.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .psr0

: Create trivial PSR0 autoloader for tests
cat <<EOF | tee psr0.php
<?php
spl_autoload_register(function (\$class) {
    \$file = str_replace('\\\\', '/', \$class).'.php';
    @include \$file;
});
define('SABRE_TEMPDIR', __DIR__ . '/temp/');
mkdir(SABRE_TEMPDIR);
EOF


%build
# nothing to build


%install
# Install as a PSR-0 library
mkdir -p %{buildroot}%{_datadir}/php
cp -pr lib/Sabre %{buildroot}%{_datadir}/php/Sabre

# Install the command
install -Dpm 0755 bin/vobject \
         %{buildroot}/%{_bindir}/vobject


%check
%if %{with_tests}
sed -e s/testGetDateTime/SKIP_testGetDateTime/ \
    -i tests/Sabre/VObject/Property/VCard/DateAndOrTimeTest.php

: Run upstream test suite against installed library
cd tests
phpunit \
  --bootstrap=../psr0.php \
  --include-path=%{buildroot}%{_datadir}/php \
  -d date.timezone=UTC
%else
: Skip upstream test suite
%endif


%files
%defattr(-,root,root,-)
%doc ChangeLog.md composer.json LICENSE README.md
%{_datadir}/php/Sabre
%{_bindir}/vobject


%changelog
* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 3.2.0-1
- update to 3.2.0

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 3.1.3-1
- update to 3.1.3

* Tue Dec 31 2013 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Initial packaging