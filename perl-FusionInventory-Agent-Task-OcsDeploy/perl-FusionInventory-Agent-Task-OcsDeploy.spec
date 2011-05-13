Name:           perl-FusionInventory-Agent-Task-OcsDeploy
Version:        1.1.0
Release:        2%{?dist}
Summary:        OCS Inventory NG Software deployment support for FusionInventory Agent
Summary(fr):    Gestion du déploiement logiciel OCS Inventory NG avec FusionInventory
License:        GPLv2+
Group:          Development/Libraries

URL:            http://forge.fusioninventory.org/projects/fusioninventory-agent-task-ocsdeploy
Source0:        http://search.cpan.org/CPAN/authors/id/F/FU/FUSINV/FusionInventory-Agent-Task-OcsDeploy-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(Archive::Extract)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy::Recursive)
# For tests
BuildRequires:  perl(FusionInventory::Agent) >= 2.1.5
BuildRequires:  perl(Time::HiRes) perl(XML::Simple) perl(Test::More)

Requires:       perl(Archive::Extract)
Requires:       perl(FusionInventory::Agent) >= 2.1.5
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%if 0%{?fedora} >= 6 || 0%{?rhel} >= 5
Requires:       perl(POE::Component::Client::HTTP)
%endif


%if 0%{?fedora} >= 11 || 0%{?rhel} >= 6
# This work only on recent fedora - But only lates rpm detect this
%{?filter_setup:
%filter_from_requires /perl(Win32/d
%?perl_default_filter
}
%else
%{?perl_default_filter}
%endif


%description
With this module, FusionInventory Agent can accept software deployment
request from an OCS Inventory server NG.


%description -l fr
Avec ce module, l'agent FusionInventory peut traiter les ordres de
déploiement de logiciel envoyés par un serveur OCS Inventory NG.


%prep
%setup -q -n FusionInventory-Agent-Task-OcsDeploy-%{version}

# Filtering auto Requires detection
cat <<EOF | tee %{name}-req
#!/bin/sh
%{__perl_requires} $* | \
sed -e '/perl(Win32::/d'
EOF

%global __perl_requires %{_builddir}/FusionInventory-Agent-Task-OcsDeploy-%{version}/%{name}-req
chmod +x %{__perl_requires}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS Changes LICENSE README THANKS
%{perl_vendorlib}/FusionInventory/Agent/Task/OcsDeploy.pm
%if 0%{?rhel} == 4
# this optional module requires perl(POE::Component::Client::HTTP)
%exclude %{perl_vendorlib}/FusionInventory/Agent/Task/OcsDeploy/P2P.pm
%else
%{perl_vendorlib}/FusionInventory/Agent/Task/OcsDeploy/P2P.pm
%endif
%{_mandir}/man3/Fusion*


%changelog
* Fri May 13 2011 Remi Collet <Fedora@famillecollet.com> - 1.1.0-2
- fix f15 build (filter perl(Win32::OLE) dependency)

* Mon Dec 13 2010 Remi Collet <Fedora@famillecollet.com> - 1.1.0-1
- update to 1.1.0
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-Task-OcsDeploy-1.1.0/Changes

* Fri Sep 10 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.8-2
- fix %%check

* Thu Sep 09 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.8-1
- update to 1.0.8
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-Task-OcsDeploy-1.0.8/Changes

* Tue Sep 07 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.7-1
- update to 1.0.7
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-Task-OcsDeploy-1.0.7/Changes

* Sun Sep 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.6-1
- update to 1.0.6

* Sun Aug 15 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.5-1
- update to 1.0.5

* Sat May 29 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.3-1
- update to 1.0.3
- add filter for Win32 component
- switch URL to forge

* Fri May 07 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Specfile autogenerated by cpanspec 1.78.
- spec cleanup + translation

