# spec file for php-bartlett-PHP-Reflect
#
# Copyright (c) 2011-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    0a60a3a4dafd1f867752d68f02c482b879f73612
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     llaville
%global gh_project   php-reflect

Name:           php-bartlett-PHP-Reflect
Version:        2.2.0
Release:        %{?gh_short:0.1.%{gh_short}}%{!?gh_short:1}%{?dist}
Summary:        Adds the ability to reverse-engineer PHP

Group:          Development/Libraries
License:        BSD
URL:            http://php5.laurent-laville.org/reflect/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?gh_short:-%{gh_short}}.tar.gz

# Autoloader for RPM - die composer !
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language)               >= 5.3
# to run test suite
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(phpunit/php-timer)        >= 1.0
BuildRequires:  php-composer(nikic/php-parser)         >= 1.0.0
BuildRequires:  php-composer(symfony/class-loader)     >= 2.5
BuildRequires:  php-composer(symfony/event-dispatcher) >= 2.5
BuildRequires:  php-composer(symfony/finder)           >= 2.5
BuildRequires:  php-composer(symfony/console)          >= 2.5

# From composer.json, "require"
#        "php": ">=5.3.0",
#        "ext-tokenizer": "*",
#        "ext-pcre": "*",
#        "ext-spl": "*",
#        "ext-json": "*",
#        "ext-date": "*",
#        "phpunit/php-timer": ">=1.0.0",
#        "nikic/php-parser": "1.0.0beta1",
#        "symfony/event-dispatcher": "~2.5",
#        "symfony/finder": "~2.5",
#        "symfony/console": "~2.5"
Requires:       php(language)               >= 5.3
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-composer(phpunit/php-timer)        >= 1.0.0
Requires:       php-composer(nikic/php-parser)         >= 1.0.0
Requires:       php-composer(symfony/event-dispatcher) >= 2.5
Requires:       php-composer(symfony/event-dispatcher) <  3
Requires:       php-composer(symfony/finder)           >= 2.5
Requires:       php-composer(symfony/finder)           <  3
Requires:       php-composer(symfony/console)          >= 2.5
Requires:       php-composer(symfony/console)          <  3
# From coposer.json, "suggest"
#        "doctrine/cache": "~1.3"
Requires:       php-composer(doctrine/cache)           >= 1.3
Requires:       php-composer(doctrine/cache)           <  2
# For our patch
Requires:       php-composer(symfony/class-loader)     >= 2.5
Requires:       php-composer(symfony/class-loader)     <  3

# From package.xml
Requires:       php-reflection


%description
PHP_Reflect adds the ability to reverse-engineer classes, interfaces,
functions, constants and more, by connecting php callbacks to other tokens.

Documentation: http://php5.laurent-laville.org/reflect/manual/2.0/en/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm

find . -type f -name \*.rpm -print | xargs rm

sed -e 's/@package_version@/%{version}/' \
    -i $(find src -name \*.php)


%build
# Nothing


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/Bartlett %{buildroot}%{_datadir}/php/Bartlett

install -D -p -m 755 bin/phpreflect      %{buildroot}%{_bindir}/phpreflect
install -D -p -m 644 bin/phpreflect.json %{buildroot}%{_sysconfdir}/phpreflect.json


%check
# Version 2.0.0 : OK (128 tests, 128 assertions)
%{_bindir}/phpunit \
  -d date.timezone=UTC


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
     bartlett.laurent-laville.org/PHP_Reflect >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json README.*
%config(noreplace) %{_sysconfdir}/phpreflect.json
%{_bindir}/phpreflect
%{_datadir}/php/Bartlett


%changelog
* Wed Jul 23 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- Test build of upcoming 2.2.0

* Tue Jul  8 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- fix dependencies

* Mon May 12 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0
- sources from github
- patch autoloader to not rely on composer
- drop documentation (link to online doc in description)

* Sat Oct 12 2013 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0
- raise dependency on PHP >= 5.3

* Mon Sep 23 2013 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1

* Fri Sep 20 2013 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Jun 26 2013 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Sat Apr 06 2013 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1

* Fri Feb 22 2013 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- Version 1.6.0 (stable) - API 1.6.0 (stable)
- html documentation is now provided by upstream

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-2
- generate documentation using asciidoc, without phing

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Version 1.5.0 (stable) - API 1.5.0 (stable)
- drop documentation build

* Tue Oct 30 2012 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- Version 1.4.3 (stable) - API 1.4.0 (stable)

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-2
- rebuildt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Version 1.4.2 (stable) - API 1.4.0 (stable)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.0-2
- bump release

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Version 1.3.0 (stable) - API 1.3.0 (stable)

* Sun Feb 05 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Mon Sep 19 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-2
- remove unused .js and improve installation of generated doc
- use buildroot macro

* Mon Jul 18 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Thu Jun 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Thu Jun 02 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-1
- Version 1.0.0 (stable) - API 1.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.RC1
- Version 1.0.0RC1 (beta) - API 1.0.0 (beta)

* Sun Apr 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-1
- Version 0.7.0 (beta) - API 0.7.0 (beta)

* Mon Apr 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.6.0-1
- Version 0.6.0 (beta) - API 0.6.0 (beta)

* Wed Apr 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.1-1
- Version 0.5.1 (beta) - API 0.5.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.0-1
- Version 0.5.0 (beta) - API 0.5.0 (beta)

* Fri Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.4.0-1
- Version 0.4.0 (beta)
- Initial RPM package

