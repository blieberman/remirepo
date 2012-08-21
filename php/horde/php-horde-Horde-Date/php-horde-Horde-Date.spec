%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Date
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Date
Version:        1.0.11
Release:        3%{?dist}
Summary:        Horde Date package

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

BuildRequires:  php-pear >= 1:1.4.9-1.2
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(%{pear_channel}/Horde_Nls) < 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) < 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) < 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) < 2.0.0
Requires:       php-common >= 5.2.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Package for creating and manipulating dates.

%prep
%setup -q -c

cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%if 0%{?fedora} > 13
%find_lang %{pear_name}
%else
sh %{SOURCE1} $RPM_BUILD_ROOT %{pear_name}
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi

%files -f %{pear_name}-%{version}/%{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Date
%{pear_phpdir}/Horde/Date.php
%{pear_testdir}/%{pear_name}
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%dir %{pear_datadir}/%{pear_name}/locale/*
%dir %{pear_datadir}/%{pear_name}/locale/*/LC_MESSAGES


%changelog
* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.11-3
- rebuilt for new pear_datadir

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.0.11-2
- rebuilt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.11-1
- backport for remi repo

* Thu Jul 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.11-1
- Update to 1.0.11, fix packaging issues

* Thu Jun 14 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10, fix packaging issues

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.9-1
- Initial package
