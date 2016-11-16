# blieberman spec file for blieberman-php70
# with customizations for blieberman, adapted from
#
# remirepo spec file for php 7.0
# with backport stuff, adapted from
#
# Fedora spec file for php
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
# API/ABI check
%global apiver      20151012
%global zendver     20151012
%global pdover      20150127
# Extension version
%global fileinfover 1.0.5
%global zipver      1.13.0
%global jsonver     1.4.0

# Adds -z now to the linker flags
%global _hardened_build 1

# version used for php embedded library soname
%global embed_version 7.0

%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

%ifarch ppc ppc64
%global oraclever 10.2.0.2
%else
%global oraclever 12.1
%endif

# Build for LiteSpeed Web Server (LSAPI)
%global with_lsws     1

# Regression tests take a long time, you can skip 'em with this
#global runselftest 0
%{!?runselftest: %global runselftest 1}

# Use the arch-specific mysql_config binary to avoid mismatch with the
# arch detection heuristic used by bindir/mysql_config.
%global mysql_config %{_libdir}/mysql/mysql_config

%if 0%{?rhel} >= 7
%global with_libpcre  1
%else
%global with_libpcre  0
%endif

%if 0%{?rhel} >= 6
%global with_sqlite3  1
%else
%global with_sqlite3  0
%endif

# Build ZTS extension or only NTS
%global with_zts      1

# Debuild build
%global with_debug    %{?_with_debug:1}%{!?_with_debug:0}

%if 0%{?__isa_bits:1}
%global isasuffix -%{__isa_bits}
%else
%global isasuffix %nil
%endif

# /usr/sbin/apsx with httpd < 2.4 and defined as /usr/bin/apxs with httpd >= 2.4
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir     %%{_libdir}/httpd/modules}}
%{!?_httpd_contentdir: %{expand: %%global _httpd_contentdir /var/www}}

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# systemd to manage the service, with notify mode, with additional service config
%if 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif
# httpd 2.4.10 with httpd-filesystem and sethandler support
%global with_httpd2410 0
# nginx 1.6 with nginx-filesystem
%global with_nginx     0

%global with_dtrace 1
%global with_libzip  1
%global with_zip     0
%global db_devel  db4-devel

%global rpmrel        1

Summary: blieberman PHP70
Name: blieberman-php70
Version: %{_iv_pkg_version}
Release: %{_iv_pkg_min_version}
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM is licensed under BSD
License: PHP and Zend and BSD
Group: Development/Languages
URL: http://www.php.net/

Source0: https://source.build.blieberman.me/%{name}-%{version}.tar.gz
Source1: php.conf
Source2: php.ini
Source3: macros.php
Source4: php-fpm.conf
Source5: php-fpm-www.conf
Source6: php-fpm.service
Source7: php-fpm.logrotate
Source8: php-fpm.sysconfig
Source9: php.modconf
Source10: php.ztsmodconf
Source12: php.conf2
Source13: nginx-fpm.conf
Source14: nginx-php.conf
# Configuration files for some extensions
Source50: 10-opcache.ini
Source51: opcache-default.blacklist
Source99: php-fpm.init

# Build fixes
Patch5: php-7.0.0-includedir.patch
Patch6: php-5.6.3-embed.patch
Patch7: php-5.3.0-recode.patch
Patch8: php-7.0.2-libdb.patch
Patch9: php-7.0.7-curl.patch g

# Functional changes
Patch40: php-7.0.0-dlopen.patch
Patch42: php-7.0.0-systzdata-v14.patch
# See http://bugs.php.net/53436
Patch43: php-5.4.0-phpize.patch
# Use -lldap_r for OpenLDAP
Patch45: php-5.6.3-ldap_r.patch
# Make php_config.h constant across builds
Patch46: php-7.0.0-fixheader.patch
# drop "Configure command" from phpinfo output
Patch47: php-5.6.3-phpinfo.patch

# Upstream fixes (100+)

# Security fixes (200+)

# Fixes for tests (300+)
# Factory is droped from system tzdata
Patch300: php-7.0.10-datetests.patch
# Revert changes for pcre < 8.34
Patch301: php-7.0.0-oldpcre.patch

# WIP

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: bzip2-devel, curl-devel >= 7.9
BuildRequires: httpd-devel >= 2.0.46-1, pam-devel
%if %{with_httpd2410}
# to ensure we are using httpd with filesystem feature (see #1081453)
BuildRequires: httpd-filesystem
%endif
%if %{with_nginx}
# to ensure we are using nginx with filesystem feature (see #1142298)
BuildRequires: nginx-filesystem
%endif
BuildRequires: libstdc++-devel, openssl-devel
%if %{with_sqlite3}
# For Sqlite3 extension
BuildRequires: sqlite-devel >= 3.6.0
%else
BuildRequires: sqlite-devel >= 3.0.0
%endif
BuildRequires: zlib-devel, smtpdaemon, libedit-devel
%if %{with_libpcre}
BuildRequires: pcre-devel >= 8.20
%endif
BuildRequires: bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires: libtool-ltdl-devel
%if %{with_dtrace}
BuildRequires: systemtap-sdt-devel
%endif
#BuildRequires: bison

Obsoletes: stm-php, stm-php-backend, php53, php53u, php54w, php55u, php55w, php56u, php56w, php70u, php70w, mod_php70u
# Avoid obsoleting php54 from RHSCL
Obsoletes: php54 > 5.4
%if %{with_zts}
Obsoletes: php-zts < 5.3.7
# blieberman custom name
Provides: %{name}-zts = %{version}-%{release}
Provides: %{name}-zts%{?_isa} = %{version}-%{release}
%endif

Requires: httpd-mmn = %{_httpd_mmn}
Provides: mod_php = %{version}-%{release}
Requires: %{name}-common%{?_isa} = %{version}-%{release}
# For backwards-compatibility, require php-cli for the time being:
Requires: %{name}-cli%{?_isa} = %{version}-%{release}
# To ensure correct /var/lib/php/session ownership:
%if %{with_httpd2410}
Requires(pre): httpd-filesystem
%else
Requires(pre): httpd
%endif
# php engine for Apache httpd webserver
# blieberman custom name
Provides: %{name}(httpd)

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.


%package cli
Group: Development/Languages
Summary: Command-line interface for PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
# blieberman custom name
Provides: %{name}-cgi = %{version}-%{release}, %{name}%{?_isa} = %{version}-%{release}
Provides: %{name}-pcntl, %{name}-pcntl%{?_isa}
Provides: %{name}-readline, %{name}-readline%{?_isa}
Obsoletes: php53-cli, php53u-cli, php54-cli, php54w-cli, php55u-cli, php55w-cli, php56u-cli, php56w-cli, php70u-cli, php70w-cli

%description cli
The php-cli package contains the command-line interface
executing PHP scripts, /usr/bin/php, and the CGI interface.


%package dbg
Group: Development/Languages
Summary: The interactive PHP debugger
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php56u-dbg, php56w-dbg, php70u-dbg, php70w-phpdbg

%description dbg
The php-dbg package contains the interactive PHP debugger.


%package fpm
Group: Development/Languages
Summary: PHP FastCGI Process Manager
# All files licensed under PHP version 3.01, except
# Zend is licensed under Zend
# TSRM and fpm are licensed under BSD
License: PHP and Zend and BSD
BuildRequires: libacl-devel
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
%if %{with_systemd}
BuildRequires: systemd-devel
BuildRequires: systemd-units
Requires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
%else
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts
%endif
%if %{with_httpd2410}
# To ensure correct /var/lib/php/session ownership:
Requires(pre): httpd-filesystem
# For php.conf in /etc/httpd/conf.d
# and version 2.4.10 for proxy support in SetHandler
Requires: httpd-filesystem >= 2.4.10
# php engine for Apache httpd webserver
# blieberman custom name
Provides: %{name}(httpd)

%endif
%if %{with_nginx}
# for /etc/nginx ownership
Requires: nginx-filesystem
%endif
Obsoletes: php53-fpm, php53u-fpm, php54-fpm, php54w-fpm, php55u-fpm, php55w-fpm, php56u-fpm, php56w-fpm, php70u-fpm, php70w-fpm

%description fpm
PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI
implementation with some additional features useful for sites of
any size, especially busier sites.

%if %{with_lsws}
%package litespeed
Summary: LiteSpeed Web Server PHP support
Group: Development/Languages
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php53-litespeed, php53u-litespeed, php54-litespeed, php54w-litespeed, php55u-litespeed, php55w-litespeed, php56u-litespeed, php56w-litespeed, php70u-litespeed, php70w-litespeed

%description litespeed
The php-litespeed package provides the %{_bindir}/lsphp command
used by the LiteSpeed Web Server (LSAPI enabled PHP).
%endif


%package common
Group: Development/Languages
Summary: Common files for PHP
# All files licensed under PHP version 3.01, except
# fileinfo is licensed under PHP version 3.0
# regex, libmagic are licensed under BSD
# main/snprintf.c, main/spprintf.c and main/rfc1867.c are ASL 1.0
License: PHP and BSD and ASL 1.0
# ABI/API check - Arch specific
# blieberman custom name
Provides: %{name}(api) = %{apiver}%{isasuffix}
Provides: %{name}(zend-abi) = %{zendver}%{isasuffix}
Provides: %{name}(language) = %{version}, %{name}(language)%{?_isa} = %{version}

# Provides for all builtin/shared modules:
# blieberman custom name
Provides: %{name}-bz2, %{name}-bz2%{?_isa}
Provides: %{name}-calendar, %{name}-calendar%{?_isa}
Provides: %{name}-core = %{version}, %{name}-core%{?_isa} = %{version}
Provides: %{name}-ctype, %{name}-ctype%{?_isa}
Provides: %{name}-curl, %{name}-curl%{?_isa}
Provides: %{name}-date, %{name}-date%{?_isa}
Provides: %{name}-exif, %{name}-exif%{?_isa}
Provides: %{name}-fileinfo, %{name}-fileinfo%{?_isa}
Provides: %{name}-filter, %{name}-filter%{?_isa}
Provides: %{name}-ftp, %{name}-ftp%{?_isa}
Provides: %{name}-gettext, %{name}-gettext%{?_isa}
Provides: %{name}-hash, %{name}-hash%{?_isa}
Provides: %{name}-mhash = %{version}, %{name}-mhash%{?_isa} = %{version}
Provides: %{name}-iconv, %{name}-iconv%{?_isa}
Provides: %{name}-libxml, %{name}-libxml%{?_isa}
Provides: %{name}-openssl, %{name}-openssl%{?_isa}
Provides: %{name}-phar, %{name}-phar%{?_isa}
Provides: %{name}-pcre, %{name}-pcre%{?_isa}
Provides: %{name}-reflection, %{name}-reflection%{?_isa}
Provides: %{name}-session, %{name}-session%{?_isa}
Provides: %{name}-sockets, %{name}-sockets%{?_isa}
Provides: %{name}-spl, %{name}-spl%{?_isa}
Provides: %{name}-standard = %{version}, %{name}-standard%{?_isa} = %{version}
Provides: %{name}-tokenizer, %{name}-tokenizer%{?_isa}
Provides: %{name}-zlib, %{name}-zlib%{?_isa}

Obsoletes: php-pecl-phar < 1.2.4
Obsoletes: php-pecl-Fileinfo < 1.0.5

# blieberman custom name
Provides:  %{name}-pecl-Fileinfo = %{fileinfover}, %{name}-pecl-Fileinfo%{?_isa} = %{fileinfover}
Provides:  %{name}-pecl(Fileinfo) = %{fileinfover}, %{name}-pecl(Fileinfo)%{?_isa} = %{fileinfover}

Obsoletes: php-mhash < 5.3.0
Obsoletes: php53-mhash, php53u-mhash
Obsoletes: php53-common, php53u-common, php54-common, php54w-common, php55u-common, php55w-common, php56u-common, php56w-common, php70u-common, php70w-common

%description common
The php-common package contains files used by both the php
package and the php-cli package.


%package devel
Group: Development/Libraries
Summary: Files needed for building PHP extensions
Requires: %{name}-cli%{?_isa} = %{version}-%{release}, autoconf, automake
%if %{with_libpcre}
Requires: pcre-devel%{?_isa}
%endif
Obsoletes: php-pecl-pdo-devel
Obsoletes: php-pecl-json-devel  < %{jsonver}
Obsoletes: php-pecl-jsonc-devel < %{jsonver}
%if %{with_zts}
# blieberman custom name
Provides: %{name}-zts-devel = %{version}-%{release}
Provides: %{name}-zts-devel = %{version}-%{release}
%endif

Obsoletes: php53-devel, php53u-devel, php54-devel, php54w-devel, php55u-devel, php55w-devel, php56u-devel, php56w-devel, php70u-devel, php70w-devel

%description devel
The php-devel package contains the files needed for building PHP
extensions. If you need to compile your own PHP extensions, you will
need to install this package.


%package opcache
Summary: The Zend OPcache
Group: Development/Languages
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zendopcache
# blieberman custom name
Provides:  %{name}-pecl-zendopcache = %{version}
Provides:  %{name}-pecl-zendopcache%{?_isa} = %{version}
Provides:  %{name}-pecl(opcache) = %{version}
Provides:  %{name}-pecl(opcache)%{?_isa} = %{version}

Obsoletes: php55u-opcache, php55w-opcache, php56u-opcache, php56w-opcache, php70u-opcache, php70w-opcache

%description opcache
The Zend OPcache provides faster PHP execution through opcode caching and
optimization. It improves PHP performance by storing precompiled script
bytecode in the shared memory. This eliminates the stages of reading code from
the disk and compiling it on future access. In addition, it applies a few
bytecode optimization patterns that make code execution faster.


%package imap
Summary: A module for PHP applications that use IMAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: mod_php3-imap, stronghold-php-imap
BuildRequires: krb5-devel, openssl-devel, libc-client-devel
Obsoletes: php53-imap, php53u-imap, php54-imap, php54w-imap, php55u-imap, php55w-imap, php56u-imap, php56w-imap, php70u-imap, php70w-imap

%description imap
The php-imap module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail
messages on mail servers. PHP is an HTML-embedded scripting language.


%package ldap
Summary: A module for PHP applications that use LDAP
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: cyrus-sasl-devel, openldap-devel, openssl-devel
Obsoletes: php53-ldap, php53u-ldap, php54-ldap, php54w-ldap, php55u-ldap, php55w-ldap, php56u-ldap, php56w-ldap, php70u-ldap, php70w-ldap

%description ldap
The php-ldap adds Lightweight Directory Access Protocol (LDAP)
support to PHP. LDAP is a set of protocols for accessing directory
services over the Internet. PHP is an HTML-embedded scripting
language.


%package pdo
Summary: A database access abstraction module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
# ABI/API check - Arch specific
# blieberman custom name
Provides: %{name}-pdo-abi  = %{pdover}%{isasuffix}
Provides: %{name}(pdo-abi) = %{pdover}%{isasuffix}

%if %{with_sqlite3}
# blieberman custom name
Provides: %{name}-sqlite3, php-sqlite3%{?_isa}
%endif
# blieberman custom name
Provides: %{name}-pdo_sqlite, php-pdo_sqlite%{?_isa}
Obsoletes: php53-pdo, php53u-pdo, php54-pdo, php54w-pdo, php55u-pdo, php55w-pdo, php56u-pdo, php56w-pdo, php70u-pdo, php70w-pdo

%description pdo
The php-pdo package contains a dynamic shared object that will add
a database access abstraction layer to PHP.  This module provides
a common interface for accessing MySQL, PostgreSQL or other
databases.


%package mysqlnd
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
# blieberman custom name
Provides: %{name}_database
Provides: %{name}-mysqli = %{version}-%{release}
Provides: %{name}-mysqli%{?_isa} = %{version}-%{release}
Provides: %{name}-pdo_mysql, %{name}-pdo_mysql%{?_isa}

Obsoletes: php-mysql < %{version}-%{release}
Obsoletes: php53-mysqlnd, php53u-mysqlnd, php54-mysqlnd, php54w-mysqlnd, php55u-mysqlnd, php55w-mysqlnd, php56u-mysqlnd, php56w-mysqlnd, php70u-mysqlnd, php70w-mysqlnd
Obsoletes: php53-mysql, php53u-mysql, php54-mysql, php54w-mysql, php55u-mysql, php55w-mysql, php56u-mysql, php56w-mysql, php70u-mysql, php70w-mysql

%description mysqlnd
The php-mysqlnd package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the php package.

This package use the MySQL Native Driver


%package process
Summary: Modules for PHP script using system process interfaces
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Provides: %{name}-posix, %{name}-posix%{?_isa}
Provides: %{name}-shmop, %{name}-shmop%{?_isa}
Provides: %{name}-sysvsem, %{name}-sysvsem%{?_isa}
Provides: %{name}-sysvshm, %{name}-sysvshm%{?_isa}
Provides: %{name}-sysvmsg, %{name}-sysvmsg%{?_isa}
Obsoletes: php53-process, php53u-process, php54-process, php54w-process, php55u-process, php55w-process, php56u-process, php56w-process, php70u-process, php70w-process

%description process
The php-process package contains dynamic shared objects which add
support to PHP using system interfaces for inter-process
communication.


%package odbc
Summary: A module for PHP applications that use ODBC databases
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# pdo_odbc is licensed under PHP version 3.0
License: PHP
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
Provides:  %{name}_database
Provides:  %{name}-pdo_odbc, %{name}-pdo_odbc%{?_isa}
BuildRequires: unixODBC-devel
Obsoletes: php53-odbc, php53u-odbc, php54-odbc, php54w-odbc, php55u-odbc, php55w-odbc, php56u-odbc, php56w-odbc, php70u-odbc, php70w-odbc

%description odbc
The php-odbc package contains a dynamic shared object that will add
database support through ODBC to PHP. ODBC is an open specification
which provides a consistent API for developers to use for accessing
data sources (which are often, but not always, databases). PHP is an
HTML-embeddable scripting language. If you need ODBC support for PHP
applications, you will need to install this package and the php
package.


%package soap
Summary: A module for PHP applications that use the SOAP protocol
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: libxml2-devel
Obsoletes: php53-soap, php53u-soap, php54-soap, php54w-soap, php55u-soap, php55w-soap, php56u-soap, php56w-soap, php70u-soap, php70w-soap

%description soap
The php-soap package contains a dynamic shared object that will add
support to PHP for using the SOAP web services protocol.


%package interbase
Summary: A module for PHP applications that use Interbase/Firebird databases
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires:  firebird-devel
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
Provides:  %{name}_database
Provides:  %{name}-firebird, %{name}-firebird%{?_isa}
Provides:  %{name}-pdo_firebird, %{name}-pdo_firebird%{?_isa}
Obsoletes: php53-interbase, php53u-interbase, php54-interbase, php54w-interbase, php55u-interbase, php55w-interbase, php56u-interbase, php56w-interbase, php70u-interbase, php70w-interbase

%description interbase
The php-interbase package contains a dynamic shared object that will add
database support through Interbase/Firebird to PHP.

InterBase is the name of the closed-source variant of this RDBMS that was
developed by Borland/Inprise.

Firebird is a commercially independent project of C and C++ programmers,
technical advisors and supporters developing and enhancing a multi-platform
relational database management system based on the source code released by
Inprise Corp (now known as Borland Software Corp) under the InterBase Public
License.


%package xml
Summary: A module for PHP applications which use XML
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Provides:  %{name}-dom, %{name}-dom%{?_isa}
Provides:  %{name}-domxml, %{name}-domxml%{?_isa}
Provides:  %{name}-simplexml, %{name}-simplexml%{?_isa}
Provides:  %{name}-wddx, %{name}-wddx%{?_isa}
Provides:  %{name}-xmlreader, %{name}xmlreader%{?_isa}
Provides:  %{name}-xmlwriter, %{name}-xmlwriter%{?_isa}
Provides:  %{name}-xsl, %{name}-xsl%{?_isa}
BuildRequires: libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1
Obsoletes: php53-xml, php53u-xml, php54-xml, php54w-xml, php55u-xml, php55w-xml, php56u-xml, php56w-xml, php70u-xml, php70w-xml

%description xml
The php-xml package contains dynamic shared objects which add support
to PHP for manipulating XML documents using the DOM tree,
and performing XSL transformations on XML documents.


%package xmlrpc
Summary: A module for PHP applications which use the XML-RPC protocol
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libXMLRPC is licensed under BSD
License: PHP and BSD
Requires: %{name}-xml%{?_isa} = %{version}-%{release}
Obsoletes: php53-xmlrpc, php53u-xmlrpc, php54-xmlrpc, php54w-xmlrpc, php55u-xmlrpc, php55w-xmlrpc, php56u-xmlrpc, php56w-xmlrpc, php70u-xmlrpc, php70w-xmlrpc

%description xmlrpc
The php-xmlrpc package contains a dynamic shared object that will add
support for the XML-RPC protocol to PHP.


%package mbstring
Summary: A module for PHP applications which need multi-byte string handling
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libmbfl is licensed under LGPLv2
# onigurama is licensed under BSD
# ucgendat is licensed under OpenLDAP
License: PHP and LGPLv2 and BSD and OpenLDAP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php53-mbstring, php53u-mbstring, php54-mbstring, php54w-mbstring, php55u-mbstring, php55w-mbstring, php56u-mbstring, php56w-mbstring, php70u-mbstring, php70w-mbstring

%description mbstring
The php-mbstring package contains a dynamic shared object that will add
support for multi-byte string handling to PHP.


%package bcmath
Summary: A module for PHP applications for using the bcmath library
Group: Development/Languages
# All files licensed under PHP version 3.01, except
# libbcmath is licensed under LGPLv2+
License: PHP and LGPLv2+
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php53-bcmath, php53u-bcmath, php54-bcmath, php54w-bcmath, php55u-bcmath, php55w-bcmath, php56u-bcmath, php56w-bcmath, php70u-bcmath, php70w-bcmath

%description bcmath
The php-bcmath package contains a dynamic shared object that will add
support for using the bcmath library to PHP.


%package gmp
Summary: A module for PHP applications for using the GNU MP library
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: gmp-devel
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php53-gmp, php53u-gmp, php54-gmp, php54w-gmp, php55u-gmp, php55w-gmp, php56u-gmp, php56w-gmp, php70u-gmp, php70w-gmp

%description gmp
These functions allow you to work with arbitrary-length integers
using the GNU MP library.


%package dba
Summary: A database abstraction layer module for PHP applications
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
BuildRequires: %{db_devel}, gdbm-devel, tokyocabinet-devel
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php53-dba, php53u-dba, php54-dba, php54w-dba, php55u-dba, php55w-dba, php56u-dba, php56w-dba, php70u-dba, php70w-dba

%description dba
The php-dba package contains a dynamic shared object that will add
support for using the DBA database abstraction layer to PHP.


%package mcrypt
Summary: Standard PHP module provides mcrypt library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: libmcrypt-devel
Obsoletes: php53-mcrypt, php53u-mcrypt, php54-mcrypt, php54w-mcrypt, php55u-mcrypt, php55w-mcrypt, php56u-mcrypt, php56w-mcrypt, php70u-mcrypt, php70w-mcrypt

%description mcrypt
The php-mcrypt package contains a dynamic shared object that will add
support for using the mcrypt library to PHP.


%package tidy
Summary: Standard PHP module provides tidy library support
Group: Development/Languages
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: libtidy-devel
Obsoletes: php53-tidy, php53u-tidy, php54-tidy, php54w-tidy, php55u-tidy, php55w-tidy, php56u-tidy, php56w-tidy, php70u-tidy, php70w-tidy

%description tidy
The php-tidy package contains a dynamic shared object that will add
support for using the tidy library to PHP.


%package pdo-dblib
Summary: PDO driver Microsoft SQL Server and Sybase databases
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-pdo%{?_isa} = %{version}-%{release}
BuildRequires: freetds-devel >= 0.91
Provides:  %{name}-pdo_dblib, %{name}-pdo_dblib%{?_isa}
Obsoletes: %{name}-mssql < %{version}-%{release}
Obsoletes: php53-mssql, php53u-mssql, php54-mssql, php54w-mssql, php55u-mssql, php55w-mssql, php56u-mssql, php56w-mssql, php70u-pdo-dblib, php70w-pdo_dblib

%description pdo-dblib
The php-pdo-dblib package contains a dynamic shared object
that implements the PHP Data Objects (PDO) interface to enable access from
PHP to Microsoft SQL Server and Sybase databases through the FreeTDS libary.


%package embedded
Summary: PHP library for embedding in applications
Group: System Environment/Libraries
Requires: %{name}-common%{?_isa} = %{version}-%{release}
# doing a real -devel package for just the .so symlink is a bit overkill
Provides:  %{name}-embedded-devel = %{version}-%{release}
Provides:  %{name}-embedded-devel%{?_isa} = %{version}-%{release}
Obsoletes: php53-embedded, php53u-embedded, php54-embedded, php54w-embedded, php55u-embedded, php55w-embedded, php56u-embedded, php56w-embedded, php70u-embedded, php70w-embedded

%description embedded
The php-embedded package contains a library which can be embedded
into applications to provide PHP scripting language support.


%package pspell
Summary: A module for PHP applications for using pspell interfaces
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: aspell-devel >= 0.50.0
Obsoletes: php53-pspell, php53u-pspell, php54-pspell, php54w-pspell, php55u-pspell, php55w-pspell, php56u-pspell, php56w-pspell, php70u-pspell, php70w-pspell

%description pspell
The php-pspell package contains a dynamic shared object that will add
support for using the pspell library to PHP.


%package recode
Summary: A module for PHP applications for using the recode library
Group: System Environment/Libraries
# All files licensed under PHP version 3.01
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: recode-devel
Obsoletes: php53-recode, php53u-recode, php54-recode, php54w-recode, php55u-recode, php55w-recode, php56u-recode, php56w-recode, php70u-recode, php70w-recode

%description recode
The php-recode package contains a dynamic shared object that will add
support for using the recode library to PHP.


%package enchant
Summary: Enchant spelling extension for PHP applications
Group: System Environment/Libraries
# All files licensed under PHP version 3.0
License: PHP
Requires: %{name}-common%{?_isa} = %{version}-%{release}
BuildRequires: enchant-devel >= 1.2.4
Obsoletes: php53-enchant, php53u-enchant, php54-enchant, php54w-enchant, php55u-enchant, php55w-enchant, php56u-enchant, php56w-enchant, php70u-enchant, php70w-enchant

%description enchant
The php-enchant package contains a dynamic shared object that will add
support for using the enchant library to PHP.

%if %{with_zip}
%package zip
Summary: ZIP archive management extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-zip          < %{zipver}
Provides:  php-pecl(zip)         = %{zipver}
Provides:  php-pecl(zip)%{?_isa} = %{zipver}
Provides:  php-pecl-zip          = %{zipver}
Provides:  php-pecl-zip%{?_isa}  = %{zipver}
Obsoletes: php53-zip, php53u-zip, php54-zip, php54w-zip, php55u-zip, php55w-zip, php56u-zip, php56w-zip, php70u-zip, php70w-zip
%if %{with_libzip}
# 0.11.1 required, but 1.0.1 is bundled
BuildRequires: pkgconfig(libzip) >= 1.0.1
%endif

%description zip
The php-zip package provides an extension that will add
support for ZIP archive management to PHP.
%endif


%package json
Summary: JavaScript Object Notation extension for PHP
# All files licensed under PHP version 3.0.1
License: PHP
Group: System Environment/Libraries
Requires: %{name}-common%{?_isa} = %{version}-%{release}
Obsoletes: php-pecl-json          < %{jsonver}
Obsoletes: php-pecl-jsonc         < %{jsonver}
Provides:  php-pecl(json)         = %{jsonver}
Provides:  php-pecl(json)%{?_isa} = %{jsonver}
Provides:  php-pecl-json          = %{jsonver}
Provides:  php-pecl-json%{?_isa}  = %{jsonver}
Obsoletes: php53-json, php53u-json, php54-json, php54w-json, php55u-json, php55w-json, php56u-json, php56w-json, php70u-json, php70w-json

%description json
The php-json package provides an extension that will add
support for JavaScript Object Notation (JSON) to PHP.



%prep
echo CIBLE = %{name}-%{version}-%{release} libzip=%{with_libzip}

# ensure than current httpd use prefork MPM.
httpd -V  | grep -q 'threaded:.*yes' && exit 1

%setup -q -n php-%{version}%{?rcver}

%patch5 -p1 -b .includedir
%patch6 -p1 -b .embed
%patch7 -p1 -b .recode
%patch8 -p1 -b .libdb
%if 0%{?rhel}
%patch9 -p1 -b .curltls
%endif

%patch40 -p1 -b .dlopen
%if 0%{?rhel} >= 5
%patch42 -p1 -b .systzdata
%endif
%patch43 -p1 -b .headers
%if 0%{?rhel} >= 7
%patch45 -p1 -b .ldap_r
%endif
%patch46 -p1 -b .fixheader
%patch47 -p1 -b .phpinfo

# upstream patches

# security patches

# Fixes for tests
%if 0%{?rhel} >= 5
%patch300 -p1 -b .datetests
%endif
%if %{with_libpcre}
if ! pkg-config libpcre --atleast-version 8.34 ; then
# Only apply when system libpcre < 8.34
%patch301 -p1 -b .pcre834
fi
%endif

# WIP patch

# Prevent %%doc confusion over LICENSE files
cp Zend/LICENSE Zend/ZEND_LICENSE
cp TSRM/LICENSE TSRM_LICENSE
cp sapi/fpm/LICENSE fpm_LICENSE
cp ext/mbstring/libmbfl/LICENSE libmbfl_LICENSE
cp ext/mbstring/oniguruma/COPYING oniguruma_COPYING
cp ext/mbstring/ucgendat/OPENLDAP_LICENSE ucgendat_LICENSE
cp ext/fileinfo/libmagic/LICENSE libmagic_LICENSE
cp ext/phar/LICENSE phar_LICENSE
cp ext/bcmath/libbcmath/COPYING.LIB libbcmath_COPYING

# Multiple builds for multiple SAPIs
mkdir build-cgi build-apache build-embedded \
%if %{with_zts}
    build-zts build-ztscli \
%endif
    build-fpm

# ----- Manage known as failed test -------
# affected by systzdata patch
rm ext/date/tests/timezone_location_get.phpt
rm ext/date/tests/timezone_version_get.phpt
rm ext/date/tests/timezone_version_get_basic1.phpt
# Should be skipped but fails sometime
rm ext/standard/tests/file/file_get_contents_error001.phpt
# fails sometime
rm ext/sockets/tests/mcast_ipv?_recv.phpt
# cause stack exhausion
rm Zend/tests/bug54268.phpt
rm Zend/tests/bug68412.phpt
# avoid issue when 2 builds run simultaneously
%ifarch x86_64
sed -e 's/64321/64322/' -i ext/openssl/tests/*.phpt
%endif

# Safety check for API version change.
pver=$(sed -n '/#define PHP_VERSION /{s/.* "//;s/".*$//;p}' main/php_version.h)
if test "x${pver}" != "x%{version}%{?rcver}"; then
   : Error: Upstream PHP version is now ${pver}, expecting %{version}%{?rcver}.
   : Update the version/rcver macros and rebuild.
   exit 1
fi

vapi=$(sed -n '/#define PHP_API_VERSION/{s/.* //;p}' main/php.h)
if test "x${vapi}" != "x%{apiver}"; then
   : Error: Upstream API version is now ${vapi}, expecting %{apiver}.
   : Update the apiver macro and rebuild.
   exit 1
fi

vzend=$(sed -n '/#define ZEND_MODULE_API_NO/{s/^[^0-9]*//;p;}' Zend/zend_modules.h)
if test "x${vzend}" != "x%{zendver}"; then
   : Error: Upstream Zend ABI version is now ${vzend}, expecting %{zendver}.
   : Update the zendver macro and rebuild.
   exit 1
fi

%if %{with_zip}
ver=$(sed -n '/#define PHP_ZIP_VERSION /{s/.* "//;s/".*$//;p}' ext/zip/php_zip.h)
if test "$ver" != "%{zipver}"; then
   : Error: Upstream ZIP version is now ${ver}, expecting %{zipver}.
   : Update the %{zipver} macro and rebuild.
   exit 1
fi
%endif

ver=$(sed -n '/#define PHP_JSON_VERSION /{s/.* "//;s/".*$//;p}' ext/json/php_json.h)
if test "$ver" != "%{jsonver}"; then
   : Error: Upstream JSON version is now ${ver}, expecting %{jsonver}.
   : Update the %{jsonver} macro and rebuild.
   exit 1
fi

# https://bugs.php.net/63362 - Not needed but installed headers.
# Drop some Windows specific headers to avoid installation,
# before build to ensure they are really not needed.
rm -f TSRM/tsrm_win32.h \
      TSRM/tsrm_config.w32.h \
      Zend/zend_config.w32.h \
      ext/mysqlnd/config-win.h \
      ext/standard/winver.h \
      main/win32_internal_function_disabled.h \
      main/win95nt.h

# Fix some bogus permissions
find . -name \*.[ch] -exec chmod 644 {} \;
chmod 644 README.*

# php-fpm configuration files for tmpfiles.d
echo "d /run/php-fpm 755 root root" >php-fpm.tmpfiles

# Some extensions have their own configuration file
cp %{SOURCE50} 10-opcache.ini
%if 0%{?rhel} != 6
cat << EOF >>10-opcache.ini

; Enables or disables copying of PHP code (text segment) into HUGE PAGES.
; This should improve performance, but requires appropriate OS configuration.
opcache.huge_code_pages=0
EOF
%ifarch x86_64
sed -e '/opcache.huge_code_pages/s/0/1/' -i 10-opcache.ini
%endif
%endif

# Regenerated bison files
# to force, rm Zend/zend_{language,ini}_parser.[ch]
if [ ! -f Zend/zend_language_parser.c ]; then
  ./genfiles
fi


%build
%if 0%{?rhel} >= 6
# aclocal workaround - to be improved
cat $(aclocal --print-ac-dir)/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >>aclocal.m4
%endif

# Force use of system libtool:
libtoolize --force --copy
%if 0%{?rhel} >= 6
cat $(aclocal --print-ac-dir)/{libtool,ltoptions,ltsugar,ltversion,lt~obsolete}.m4 >build/libtool.m4
%else
cat $(aclocal --print-ac-dir)/libtool.m4 > build/libtool.m4
%endif

# Regenerate configure scripts (patches change config.m4's)
touch configure.in
./buildconf --force
%if %{with_debug}
LDFLAGS="-fsanitize=address"
export LDFLAGS
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign -fsanitize=address -ggdb"
%else
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
%endif
export CFLAGS

# Install extension modules in %{_libdir}/php/modules.
EXTENSION_DIR=%{_libdir}/php/modules; export EXTENSION_DIR

# Set PEAR_INSTALLDIR to ensure that the hard-coded include_path
# includes the PEAR directory even though pear is packaged
# separately.
PEAR_INSTALLDIR=%{_datadir}/pear; export PEAR_INSTALLDIR

# Shell function to configure and build a PHP tree.
build() {
# Old/recent bison version seems to produce a broken parser;
# upstream uses GNU Bison 2.3. Workaround:
# Only provided in official tarball (not in snapshot)
if [ -f ../Zend/zend_language_parser.c ]; then
mkdir Zend && cp ../Zend/zend_{language,ini}_{parser,scanner}.[ch] Zend
fi

# Always static:
# date, filter, libxml, reflection, spl: not supported
# hash: for PHAR_SIG_SHA256 and PHAR_SIG_SHA512
# session: dep on hash, used by soap and wddx
# pcre: used by filter, zip
# pcntl, readline: only used by CLI sapi
# openssl: for PHAR_SIG_OPENSSL
# zlib: used by image

ln -sf ../configure
%configure \
    --cache-file=../config.cache \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --without-pear \
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_prefix} \
    --with-png-dir=%{_prefix} \
    --with-xpm-dir=%{_prefix} \
    --without-gdbm \
    --with-jpeg-dir=%{_prefix} \
    --with-openssl \
    --with-system-ciphers \
%if %{with_libpcre}
    --with-pcre-regex=%{_prefix} \
%endif
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_prefix} \
%if 0%{?rhel} >= 5
    --with-system-tzdata \
%endif
    --with-mhash \
%if %{with_dtrace}
    --enable-dtrace \
%endif
%if %{with_debug}
    --enable-debug \
%endif
    $*
if test $? != 0; then
  tail -500 config.log
  : configure failed
  exit 1
fi

make %{?_smp_mflags}
}

# Build /usr/bin/php-cgi with the CGI SAPI, and most shared extensions
pushd build-cgi

build --libdir=%{_libdir}/php \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
%if 0%{?rhel} == 6
      --disable-huge-code-pages \
%endif
      --enable-phpdbg \
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-webp-dir=%{_prefix} \
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-gdbm=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --with-interbase=shared,%{_libdir}/firebird \
      --with-pdo-firebird=shared,%{_libdir}/firebird \
      --enable-dom=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
%if %{with_sqlite3}
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

without_shared="--without-gd \
      --disable-dom --disable-dba --without-unixODBC \
      --disable-opcache \
      --disable-json \
      --disable-xmlreader --disable-xmlwriter \
      --without-sqlite3 --disable-phar --disable-fileinfo \
      --without-pspell --disable-wddx \
      --without-curl --disable-posix --disable-xml \
      --disable-simplexml --disable-exif --without-gettext \
      --without-iconv --disable-ftp --without-bz2 --disable-ctype \
      --disable-shmop --disable-sockets --disable-tokenizer \
      --disable-sysvmsg --disable-sysvshm --disable-sysvsem"

# Build Apache module, and the CLI SAPI, /usr/bin/php
pushd build-apache
build --with-apxs2=%{_httpd_apxs} \
      --libdir=%{_libdir}/php \
%if %{with_lsws}
      --with-litespeed \
%endif
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build php-fpm
pushd build-fpm
build --enable-fpm \
%if %{with_systemd}
      --with-fpm-systemd \
%endif
      --with-fpm-acl \
      --libdir=%{_libdir}/php \
      --without-mysqli \
      --disable-pdo \
      ${without_shared}
popd

# Build for inclusion as embedded script language into applications,
# /usr/lib[64]/libphp7.so
pushd build-embedded
build --enable-embed \
      --without-mysqli --disable-pdo \
      ${without_shared}
popd

%if %{with_zts}
# Build a special thread-safe (mainly for modules)
pushd build-ztscli

EXTENSION_DIR=%{_libdir}/php-zts/modules
build --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --program-prefix=zts- \
      --disable-cgi \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --enable-pcntl \
      --enable-opcache \
      --enable-opcache-file \
%if 0%{?rhel} == 6
      --disable-huge-code-pages \
%endif
      --with-imap=shared --with-imap-ssl \
      --enable-mbstring=shared \
      --enable-mbregex \
      --with-webp-dir=%{_prefix} \
%endif
      --with-gmp=shared \
      --enable-calendar=shared \
      --enable-bcmath=shared \
      --with-bz2=shared \
      --enable-ctype=shared \
      --enable-dba=shared --with-db4=%{_prefix} \
                          --with-gdbm=%{_prefix} \
                          --with-tcadb=%{_prefix} \
      --with-gettext=shared \
      --with-iconv=shared \
      --enable-sockets=shared \
      --enable-tokenizer=shared \
      --enable-exif=shared \
      --enable-ftp=shared \
      --with-xmlrpc=shared \
      --with-ldap=shared --with-ldap-sasl \
      --enable-mysqlnd=shared \
      --with-mysqli=shared,mysqlnd \
      --with-mysql-sock=%{mysql_sock} \
      --enable-mysqlnd-threading \
      --with-interbase=shared,%{_libdir}/firebird \
      --with-pdo-firebird=shared,%{_libdir}/firebird \
      --enable-dom=shared \
      --enable-simplexml=shared \
      --enable-xml=shared \
      --enable-wddx=shared \
      --enable-soap=shared \
      --with-xsl=shared,%{_prefix} \
      --enable-xmlreader=shared --enable-xmlwriter=shared \
      --with-curl=shared,%{_prefix} \
      --enable-pdo=shared \
      --with-pdo-odbc=shared,unixODBC,%{_prefix} \
      --with-pdo-mysql=shared,mysqlnd \
      --with-pdo-sqlite=shared,%{_prefix} \
      --with-pdo-dblib=shared,%{_prefix} \
%if %{with_sqlite3}
      --with-sqlite3=shared,%{_prefix} \
%else
      --without-sqlite3 \
%endif
      --enable-json=shared \
%if %{with_zip}
      --enable-zip=shared \
%if %{with_libzip}
      --with-libzip \
%endif
%endif
      --without-readline \
      --with-libedit \
      --with-pspell=shared \
      --enable-phar=shared \
      --with-mcrypt=shared,%{_prefix} \
      --with-tidy=shared,%{_prefix} \
      --enable-sysvmsg=shared --enable-sysvshm=shared --enable-sysvsem=shared \
      --enable-shmop=shared \
      --enable-posix=shared \
      --with-unixODBC=shared,%{_prefix} \
      --enable-fileinfo=shared \
      --with-icu-dir=%{_prefix} \
      --with-enchant=shared,%{_prefix} \
      --with-recode=shared,%{_prefix}
popd

# Build a special thread-safe Apache SAPI
pushd build-zts
build --with-apxs2=%{_httpd_apxs} \
      --includedir=%{_includedir}/php-zts \
      --libdir=%{_libdir}/php-zts \
      --enable-maintainer-zts \
      --with-config-file-scan-dir=%{_sysconfdir}/php-zts.d \
      --without-mysql \
      --disable-pdo \
      ${without_shared}
popd

### NOTE!!! EXTENSION_DIR was changed for the -zts build, so it must remain
### the last SAPI to be built.

%check
%if %runselftest
cd build-apache

# Run tests, using the CLI SAPI
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
export SKIP_ONLINE_TESTS=1
unset TZ LANG LC_ALL
if ! make test; then
  set +x
  for f in $(find .. -name \*.diff -type f -print); do
    if ! grep -q XFAIL "${f/.diff/.phpt}"
    then
      echo "TEST FAILURE: $f --"
      head -n 100 "$f"
      echo -e "\n-- $f result ends."
    fi
  done
  set -x
  #exit 1
fi
unset NO_INTERACTION REPORT_EXIT_STATUS MALLOC_CHECK_
%endif


%install
%if %{with_zts}
# Install the extensions for the ZTS version
make -C build-ztscli install \
     INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# Install the version for embedded script language in applications + php_embed.h
make -C build-embedded install-sapi install-headers \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the php-fpm binary
make -C build-fpm install-fpm \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install everything from the CGI SAPI build
make -C build-cgi install \
     INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the default configuration file and icons
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_contentdir}/icons
install -m 644 php.gif $RPM_BUILD_ROOT%{_httpd_contentdir}/icons/php.gif

%if %{with_libpcre}
if ! pkg-config libpcre --atleast-version 8.38 ; then
   sed -e 's/;pcre.jit=1/pcre.jit=0/' -i $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
fi
%endif

# For third-party packaging:
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/php

# install the DSO
install -m 755 -d $RPM_BUILD_ROOT%{_httpd_moddir}
install -m 755 build-apache/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp7.so

%if %{with_zts}
# install the ZTS DSO
install -m 755 build-zts/libs/libphp7.so $RPM_BUILD_ROOT%{_httpd_moddir}/libphp7-zts.so
%endif

# Apache config fragment
%if "%{_httpd_modconfdir}" == "%{_httpd_confdir}"
# Single config file with httpd < 2.4
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif
cat %{SOURCE1} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%else
# Dual config file with httpd >= 2.4
install -D -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%if %{with_zts}
cat %{SOURCE10} >>$RPM_BUILD_ROOT%{_httpd_modconfdir}/15-php.conf
%endif
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif
%if %{with_httpd2410}
cat %{SOURCE12} >>$RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
%if %{with_zts}
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d
%endif
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/wsdlcache
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/opcache

%if %{with_lsws}
install -m 755 build-apache/sapi/litespeed/php $RPM_BUILD_ROOT%{_bindir}/lsphp
%endif

# PHP-FPM stuff
# Log
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
# Config
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf.default .
mv $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf.default .
# LogRotate
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# Environment file
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
%if %{with_systemd}
install -m 755 -d $RPM_BUILD_ROOT/run/php-fpm
# tmpfiles.d
install -m 755 -d $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
install -m 644 php-fpm.tmpfiles $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/php-fpm.conf
# install systemd unit files and scripts for handling server startup
# this folder requires systemd >= 204
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/php-fpm.service.d
install -m 755 -d $RPM_BUILD_ROOT%{_unitdir}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/
%else
sed  -ne '1,2p' -i $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php-fpm
sed -i -e 's:/run:/var/run:' $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.conf
sed -i -e 's:/run:/var/run:' $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm
# Service
install -m 755 -d $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE99} $RPM_BUILD_ROOT%{_initrddir}/php-fpm
%endif
%if %{with_nginx}
# Nginx configuration
install -D -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
install -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/nginx/default.d/php.conf

# Switch to UDS
# FPM
sed -e 's@127.0.0.1:9000@/run/php-fpm/www.sock@' \
    -e 's@^;listen.acl_users@listen.acl_users@' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-fpm.d/www.conf
# Nginx
sed -e 's@127.0.0.1:9000@unix:/run/php-fpm/www.sock@' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/nginx/conf.d/php-fpm.conf
# Apache
sed -e 's@proxy:fcgi://127.0.0.1:9000@proxy:unix:/run/php-fpm/www.sock|fcgi://localhost@' \
    -i $RPM_BUILD_ROOT%{_httpd_confdir}/php.conf
%endif

# Generate files lists and stub .ini files for each subpackage
for mod in odbc ldap xmlrpc imap json \
    mysqlnd mysqli pdo_mysql \
    mbstring dom xsl soap bcmath dba xmlreader xmlwriter \
    simplexml bz2 calendar ctype exif ftp gettext gmp iconv \
    sockets tokenizer opcache \
    pdo pdo_odbc pdo_sqlite \
%if %{with_zip}
    zip \
%endif
    interbase pdo_firebird \
%if %{with_sqlite3}
    sqlite3 \
%endif
    enchant phar fileinfo \
    mcrypt tidy pdo_dblib pspell curl wddx \
    posix shmop sysvshm sysvsem sysvmsg recode xml \
    ; do
    case $mod in
      opcache)
        # Zend extensions
        ini=10-${mod}.ini;;
      pdo_*|mysqli|wddx|xmlreader|xmlrpc)
        # Extensions with dependencies on 20-*
        ini=30-${mod}.ini;;
      *)
        # Extensions with no dependency
        ini=20-${mod}.ini;;
    esac
    # some extensions have their own config file
    if [ -f ${ini} ]; then
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini}
      cp -p ${ini} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini}
    else
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%if %{with_zts}
      cat > $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/${ini} <<EOF
; Enable ${mod} extension module
extension=${mod}.so
EOF
%endif
    fi
    cat > files.${mod} <<EOF
%attr(755,root,root) %{_libdir}/php/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php.d/${ini}
%if %{with_zts}
%attr(755,root,root) %{_libdir}/php-zts/modules/${mod}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/php-zts.d/${ini}
%endif
EOF
done

# The dom, xsl and xml* modules are all packaged in php-xml
cat files.dom files.xsl files.xml{reader,writer} files.wddx \
    files.simplexml >> files.xml

# mysqlnd
cat files.mysqli \
    files.pdo_mysql \
    >> files.mysqlnd

# Split out the PDO modules
cat files.pdo_odbc >> files.odbc
cat files.pdo_firebird >> files.interbase

# sysv* and posix in packaged in php-process
cat files.shmop files.sysv* files.posix > files.process

# Package sqlite3 and pdo_sqlite with pdo; isolating the sqlite dependency
# isn't useful at this time since rpm itself requires sqlite.
cat files.pdo_sqlite >> files.pdo
%if %{with_sqlite3}
cat files.sqlite3 >> files.pdo
%endif

# Package curl, phar and fileinfo in -common.
cat files.curl files.phar files.fileinfo \
    files.exif files.gettext files.iconv files.calendar \
    files.ftp files.bz2 files.ctype files.sockets \
    files.tokenizer > files.common

# The default Zend OPcache blacklist file
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache-default.blacklist
install -m 644 %{SOURCE51} $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/opcache-default.blacklist
sed -e '/blacklist_filename/s/php.d/php-zts.d/' \
    -i $RPM_BUILD_ROOT%{_sysconfdir}/php-zts.d/10-opcache.ini

# Install the macros file:
sed -e "s/@PHP_APIVER@/%{apiver}%{isasuffix}/" \
    -e "s/@PHP_ZENDVER@/%{zendver}%{isasuffix}/" \
    -e "s/@PHP_PDOVER@/%{pdover}%{isasuffix}/" \
    -e "s/@PHP_VERSION@/%{version}/" \
%if ! %{with_zts}
    -e "/zts/d" \
%endif
    < %{SOURCE3} > macros.php

install -m 644 -D macros.php \
           $RPM_BUILD_ROOT%{macrosdir}/macros.php

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_libdir}/php/modules/*.a \
       $RPM_BUILD_ROOT%{_libdir}/php-zts/modules/*.a \
       $RPM_BUILD_ROOT%{_bindir}/{phptar} \
       $RPM_BUILD_ROOT%{_datadir}/pear \
       $RPM_BUILD_ROOT%{_libdir}/libphp7.la

# Remove irrelevant docs
rm -f README.{Zeus,QNX,CVS-RULES}


%if ! %{with_httpd2410}
%pre fpm
# Add the "apache" user as we don't require httpd
getent group  apache >/dev/null || \
  groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{_httpd_contentdir} -c "Apache" apache
exit 0
%endif

%post fpm
%if %{with_systemd}
%systemd_post php-fpm.service
%else
if [ $1 = 1 ]; then
    # Initial installation
    /sbin/chkconfig --add php-fpm
fi
%endif

%preun fpm
%if %{with_systemd}
%systemd_preun php-fpm.service
%else
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /sbin/service php-fpm stop >/dev/null 2>&1
    /sbin/chkconfig --del php-fpm
fi
%endif

%postun fpm
%if %{with_systemd}
%systemd_postun_with_restart php-fpm.service
%else
if [ $1 -ge 1 ]; then
    /sbin/service php-fpm condrestart >/dev/null 2>&1 || :
fi
%endif

%post embedded -p /sbin/ldconfig
%postun embedded -p /sbin/ldconfig


%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root)
%{_httpd_moddir}/libphp7.so
%if %{with_zts}
%{_httpd_moddir}/libphp7-zts.so
%endif
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%config(noreplace) %{_httpd_confdir}/php.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/15-php.conf
%endif
%{_httpd_contentdir}/icons/php.gif

%files common -f files.common
%defattr(-,root,root)
%doc CODING_STANDARDS CREDITS EXTENSIONS NEWS README*
%license LICENSE Zend/ZEND_* TSRM_LICENSE
%license libmagic_LICENSE
%license phar_LICENSE
%doc php.ini-*
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/modules
%if %{with_zts}
%dir %{_sysconfdir}/php-zts.d
%dir %{_libdir}/php-zts
%dir %{_libdir}/php-zts/modules
%endif
%dir %{_localstatedir}/lib/php

%dir %{_datadir}/php

%files cli
%defattr(-,root,root)
%{_bindir}/php
%{_bindir}/zts-php
%{_bindir}/php-cgi
%{_bindir}/phar.phar
%{_bindir}/phar
# provides phpize here (not in -devel) for pecl command
%{_bindir}/phpize
%{_mandir}/man1/php.1*
%{_mandir}/man1/zts-php.1*
%{_mandir}/man1/php-cgi.1*
%{_mandir}/man1/phar.1*
%{_mandir}/man1/phar.phar.1*
%{_mandir}/man1/phpize.1*
%{_mandir}/man1/zts-phpize.1*
%doc sapi/cgi/README* sapi/cli/README

%files dbg
%defattr(-,root,root)
%{_bindir}/phpdbg
%{_mandir}/man1/phpdbg.1*
%if %{with_zts}
%{_bindir}/zts-phpdbg
%{_mandir}/man1/zts-phpdbg.1*
%endif
%doc sapi/phpdbg/{README.md,CREDITS}

%files fpm
%defattr(-,root,root)
%doc php-fpm.conf.default www.conf.default
%license fpm_LICENSE
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/wsdlcache
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/opcache
%if %{with_httpd2410}
%config(noreplace) %{_httpd_confdir}/php.conf
%endif
%config(noreplace) %{_sysconfdir}/php-fpm.conf
%config(noreplace) %{_sysconfdir}/php-fpm.d/www.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/php-fpm
%config(noreplace) %{_sysconfdir}/sysconfig/php-fpm
%if %{with_nginx}
%config(noreplace) %{_sysconfdir}/nginx/conf.d/php-fpm.conf
%config(noreplace) %{_sysconfdir}/nginx/default.d/php.conf
%endif
%if %{with_systemd}
%{_prefix}/lib/tmpfiles.d/php-fpm.conf
%{_unitdir}/php-fpm.service
%dir %{_sysconfdir}/systemd/system/php-fpm.service.d
%dir /run/php-fpm
%else
%{_initrddir}/php-fpm
%dir %{_localstatedir}/run/php-fpm
%endif
%{_sbindir}/php-fpm
%dir %{_sysconfdir}/php-fpm.d
# log owned by apache for log
%attr(770,apache,root) %dir %{_localstatedir}/log/php-fpm
%{_mandir}/man8/php-fpm.8*
%dir %{_datadir}/fpm
%{_datadir}/fpm/status.html

%if %{with_lsws}
%files litespeed
%defattr(-,root,root)
%{_bindir}/lsphp
%endif

%files devel
%defattr(-,root,root)
%{_bindir}/php-config
%{_includedir}/php
%{_libdir}/php/build
%if %{with_zts}
%{_bindir}/zts-php-config
%{_includedir}/php-zts
%{_bindir}/zts-phpize
%{_libdir}/php-zts/build
%endif
%{_mandir}/man1/php-config.1*
%{_mandir}/man1/zts-php-config.1*
%{macrosdir}/macros.php

%files embedded
%defattr(-,root,root,-)
%{_libdir}/libphp7.so
%{_libdir}/libphp7-%{embed_version}.so

%files odbc -f files.odbc
%files imap -f files.imap
%files ldap -f files.ldap
%files xml -f files.xml
%files xmlrpc -f files.xmlrpc
%files mbstring -f files.mbstring
%license libmbfl_LICENSE
%license oniguruma_COPYING
%license ucgendat_LICENSE
%defattr(-,root,root,-)
%files soap -f files.soap
%files bcmath -f files.bcmath
%license libbcmath_COPYING
%files gmp -f files.gmp
%files dba -f files.dba
%files pdo -f files.pdo
%files mcrypt -f files.mcrypt
%files tidy -f files.tidy
%files pdo-dblib -f files.pdo_dblib
%files pspell -f files.pspell
%files process -f files.process
%files recode -f files.recode
%files interbase -f files.interbase
%files enchant -f files.enchant
%files mysqlnd -f files.mysqlnd
%files opcache -f files.opcache
%config(noreplace) %{_sysconfdir}/php.d/opcache-default.blacklist
%config(noreplace) %{_sysconfdir}/php-zts.d/opcache-default.blacklist
%if %{with_zip}
%files zip -f files.zip
%endif
%files json -f files.json


%changelog
* Mon Nov 14 2016 Ben Lieberman <ben.lieberman@gmail.com> 7.0.13-2
- Porting to use custom blieberman names and paths
- removing gd, pgsql, snmp, internationalization, osi8 package builds
- using tar.gz instead of tar.xz for primary source, changing source tarball path
- removing safety check for pdo api version
- removing any references to fedorda os

* Tue Nov  8 2016 Remi Collet <remi@fedoraproject.org> 7.0.13-1
- Update to 7.0.13 - http://www.php.net/releases/7_0_13.php
