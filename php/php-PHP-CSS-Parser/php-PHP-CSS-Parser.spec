# spec file for php-PHP-CSS-Parser
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit  4c4ab985e372113dbfd0a8192fbd8629bface9bb
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   sabberworm
%global gh_project PHP-CSS-Parser

Name:           php-%{gh_project}
Summary:        A Parser for CSS Files
Version:        5.1.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# For tests
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl


%description
PHP CSS Parser: a Parser for CSS Files written in PHP.
Allows extraction of CSS files into a data structure, manipulation
of said structure and output as (optimized) CSS.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr lib/Sabberworm %{buildroot}%{_datadir}/php/Sabberworm


%check
cd tests
phpunit --bootstrap bootstrap.php .


%files
%defattr(-,root,root,-)
# LICENSE is in the README.md file
%doc *md
%{_datadir}/php/Sabberworm


%changelog
* Mon Apr 28 2014 Remi Collet <remi@fedoraproject.org> - 5.1.2-1
- update to 5.1.2

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 5.1.1-2
- add upstream patch (required by Horde_Css_Parser)

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 5.1.1-1
- update to 5.1.1 (no change, only documentation)

* Sun Oct 27 2013 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- update to 5.1.0

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 5.0.8-1
- update to 5.0.8

* Wed Jun 19 2013 Remi Collet <remi@fedoraproject.org> - 5.0.6-1
- update to 5.0.6

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 5.0.5-1
- Initial packaging
