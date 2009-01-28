%define	rev r1144

Summary:	ODBC driver for MySQL
Name:		mysql-connector-odbc
Version:	5.1.5
Release:	%mkrel 0.%{rev}.1
# exceptions allow library to be linked with most open source SW,
# not only GPL code.
License: GPLv2 with exceptions
Group:		System/Libraries
URL:		http://www.mysql.com/downloads/api-myodbc.html
Source0:	http://ftp.sunet.se/pub/unix/databases/relational/mysql/Downloads/MyODBC3/mysql-connector-odbc-%{version}%{rev}.tar.gz
Source1:	dsn-editor.pro
Patch1:		myodbc-shutdown.patch
Patch3:		mysql-connector-odbc-no_windoze.diff
Patch4:		myodbc-my-bool.patch
Patch5:		mysql-connector-odbc-5.1.5-fix-str-fmt.patch
Requires:	unixODBC
BuildRequires:	mysql-devel
BuildRequires:	unixODBC-devel
BuildRequires:	openssl-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	qt3-devel
Obsoletes:	MyODBC < %version-%release
Provides:	MyODBC = %version-%release
Obsoletes:	%{mklibname myodbc 1} < %version
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mysql-connector-odbc is an ODBC (3.50) level 0 (with level 1 and level 2
features) driver for connecting an ODBC-aware application to MySQL.
mysql-connector-odbc works on Windows NT/2000/XP, and most Unix platforms
(incl. OSX and Linux).

mysql-connector-odbc 3.51 is an enhanced version of MyODBC 2.50 to meet
ODBC 3.5 specification. The driver is commonly referred to as 'MySQL ODBC 3.51
Driver'.

%package 	devel
Summary:	Development library for ODBC driver for MySQL
Group:		Development/C
Provides:	lib%{name}-devel %{name}-devel libmyodbc-devel
Obsoletes:	lib%{name}-devel %{name}-devel libmyodbc-devel
Requires:	%{name} = %{version}
Obsoletes:	%{mklibname -d myodbc 1} < %version
Obsoletes:	%{mklibname -d mydobc} < %version

%description devel
mysql-connector-odbc is an ODBC (3.50) level 0 (with level 1 and level 2
features) driver for connecting an ODBC-aware application to MySQL.
mysql-connector-odbc works on Windows NT/2000/XP, and most Unix platforms
(incl. OSX and Linux).

mysql-connector-odbc 3.51 is an enhanced version of MyODBC 2.50 to meet
ODBC 3.5 specification. The driver is commonly referred to as 'MySQL ODBC 3.51
Driver'.

%prep
%setup -q -n mysql-connector-odbc-%{version}%{rev}
%patch1 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p0

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"

%configure2_5x \
    --enable-shared \
    --enable-static \
    --enable-gui \
    --with-qt-dir=%{qt3dir} \
    --with-qt-includes=%{qt3include} \
    --with-qt-libraries=%{qt3lib} \
    --enable-dmlink \
    --enable-myodbc-installer \
    --enable-odbcinstlink \
    --with-odbc-ini=%{_sysconfdir}/odbc.ini
%make

%install
rm -rf %{buildroot}

%makeinstall_std 

%if 0
# setup links for consolehelpper support to allow root System DSN config
install -d %{buildroot}%{_sbindir}
pushd %{buildroot}%{_bindir}
ln -sf myodbc-installer MyODBC
ln -sf consolehelper MyODBC-root
cd %{buildroot}%{_sbindir}
ln -s ../bin/MyODBC MyODBC-root
popd

# MYODBCConfig
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/MyODBC.desktop << EOF
[Desktop Entry]
Name=MyODBC
Comment=MyODBC Configuration
Exec=MyODBC
Terminal=false
Type=Application
Icon=databases_section
Categories=X-MandrivaLinux-MoreApplications-Databases;GTK;Database;Development;Application;
EOF

cat > %{buildroot}%{_datadir}/applications/MyODBC-root.desktop << EOF
[Desktop Entry]
Name=MyODBC-root
Comment=MyODBC Configuration (root user)
Exec=MyODBC-root
Terminal=false
Type=Application
Icon=databases_section
Categories=X-MandrivaLinux-MoreApplications-Databases;GTK;Database;Development;Application;
EOF

%endif
# cleanup
rm -rf %{buildroot}%{_datadir}/mysql-connector-odbc

cat > README.Mandriva << EOF

Please run this command when register:
%{_bindir}/myodbc-installer -d -a -n "MySQL ODBC 5.1 Driver" -t "DRIVER=%_libdir/libmyodbc5-%version.so;SETUP=%_libdir/libmyodbc3S-%version.so"

Please run this command when unregister:

%{_bindir}/myodbc-installer -d -r -n "MySQL ODBC 5.1 Driver"
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog LICENSE.exceptions LICENSE.gpl README README.debug README.Mandriva
%{_bindir}/*
%{_libdir}/libmyodbc3S-%version.so
%{_libdir}/libmyodbc5-%version.so

%files devel
%defattr(-,root,root)
%{_libdir}/libmyodbc3S.so
%{_libdir}/libmyodbc5.so
%{_libdir}/*.a
%{_libdir}/*.la
