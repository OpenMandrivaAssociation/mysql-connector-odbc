%define	rev r1127
%define	major 1
%define libname	%mklibname myodbc %{major}
%define develname %mklibname mydobc -d

Summary:	ODBC driver for MySQL
Name:		mysql-connector-odbc
Version:	3.51.26
Release:	%mkrel 0.%{rev}.1
License:	Public Domain
Group:		System/Libraries
URL:		http://www.mysql.com/downloads/api-myodbc.html
Source0:	http://ftp.sunet.se/pub/unix/databases/relational/mysql/Downloads/MyODBC3/mysql-connector-odbc-%{version}%{rev}.tar.gz
Source1:	dsn-editor.pro
Patch0:		MyODBC-libname.diff
Patch1:		myodbc-shutdown.patch
Patch2:		mysql-connector-odbc-linkage_fix.diff
Patch3:		mysql-connector-odbc-no_windoze.diff
Requires:	unixODBC
Requires:	usermode-consoleonly
Requires:	%{libname} = %{version}
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mysql-connector-odbc is an ODBC (3.50) level 0 (with level 1 and level 2
features) driver for connecting an ODBC-aware application to MySQL.
mysql-connector-odbc works on Windows NT/2000/XP, and most Unix platforms
(incl. OSX and Linux).

mysql-connector-odbc 3.51 is an enhanced version of MyODBC 2.50 to meet
ODBC 3.5 specification. The driver is commonly referred to as 'MySQL ODBC 3.51
Driver'.

%package -n	%{libname}
Summary:	ODBC driver for MySQL
Group:		System/Libraries 

%description -n	%{libname}
mysql-connector-odbc is an ODBC (3.50) level 0 (with level 1 and level 2
features) driver for connecting an ODBC-aware application to MySQL.
mysql-connector-odbc works on Windows NT/2000/XP, and most Unix platforms
(incl. OSX and Linux).

mysql-connector-odbc 3.51 is an enhanced version of MyODBC 2.50 to meet
ODBC 3.5 specification. The driver is commonly referred to as 'MySQL ODBC 3.51
Driver'.

%package -n	%{develname}
Summary:	Development library for ODBC driver for MySQL
Group:		Development/C
Provides:	lib%{name}-devel %{name}-devel libmyodbc-devel
Obsoletes:	lib%{name}-devel %{name}-devel libmyodbc-devel
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname -d myodbc 1}

%description -n	%{develname}
mysql-connector-odbc is an ODBC (3.50) level 0 (with level 1 and level 2
features) driver for connecting an ODBC-aware application to MySQL.
mysql-connector-odbc works on Windows NT/2000/XP, and most Unix platforms
(incl. OSX and Linux).

mysql-connector-odbc 3.51 is an enhanced version of MyODBC 2.50 to meet
ODBC 3.5 specification. The driver is commonly referred to as 'MySQL ODBC 3.51
Driver'.

%prep

%setup -q -n mysql-connector-odbc-%{version}%{rev}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0

cp %{SOURCE1} dsn-editor/dsn-editor.pro
# lib64 fixes
find -type f -name "*.c*" -o -type f -name "*.h" | xargs perl -pi -e "s|/usr/lib|%{_libdir}|g"

perl -pi -e "s|/usr/lib|%{_libdir}|g; \
	    s|/lib\b|/%{_lib}|g;
	    s|/lib/|/%{_lib}/|g" configure.in

# not so pretty dlname fix, but..., it works, so what more do you want?
find -type f -name "*.c*" -o -type f -name "*.h" | xargs perl -pi -e "s|libmyodbc3\.so|libmyodbc3\.so\.%{major}|g"
find -type f -name "*.c*" -o -type f -name "*.h" | xargs perl -pi -e "s|libmyodbc3S\.so|libmyodbc3S\.so\.%{major}|g"
find -type f -name "*.c*" -o -type f -name "*.h" | xargs perl -pi -e "s|libmyodbc3_r\.so|libmyodbc3_r\.so\.%{major}|g"

%build
export WANT_AUTOCONF_2_5=1
rm -f ./configure
libtoolize --copy --force; aclocal; automake --foreign --add-missing --copy --force-missing; autoconf

%configure2_5x \
    --enable-shared \
    --enable-static \
    --enable-thread-safe \
    --with-qt-dir=%{qt3dir} \
    --with-qt-includes=%{qt3include} \
    --with-qt-libraries=%{qt3lib} \
    --enable-dmlink \
    --enable-myodbcinst \
    --enable-imyodbc \
    --with-separate-debug-driver \
    --with-mysql-path=%{_prefix} \
    --with-unixODBC=%{_prefix} \
    --with-unixODBC-includes=%{_includedir} \
    --with-unixODBC-libs=%{_libdir} \
    --with-odbc-ini=%{_sysconfdir}/odbc.ini

%make

pushd dsn-editor
    %{qt3dir}/bin/qmake dsn-editor.pro -o Makefile.qt
    %make -f Makefile.qt
popd

%install
rm -rf %{buildroot}

%makeinstall_std

# install it as just "MyODBC"
install -m0755 bin/myodbc3c %{buildroot}%{_bindir}/myodbc3c

# Menu entries

# setup links for consolehelpper support to allow root System DSN config
install -d %{buildroot}%{_sbindir}
pushd %{buildroot}%{_bindir}
ln -sf myodbc3c MyODBC
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

# cleanup
rm -rf %{buildroot}%{_datadir}/mysql-connector-odbc

cat > README.Mandriva << EOF

Please run this command when register:

%{_bindir}/myodbc3i -w0 -a -d -t"MySQL ODBC 3.51 Driver;DRIVER=%{_libdir}/libmyodbc3.so.%{major};SETUP=%{_libdir}/libmyodbc3S.so.%{major}"

Please run this command when unregister:

%{_bindir}/myodbc3i -w0 -r -d -n"MySQL ODBC 3.51 Driver"
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
%{_bindir}/myodbc3i
%{_bindir}/myodbc3m
%{_bindir}/myodbc3c
%{_bindir}/MyODBC*
%{_sbindir}/MyODBC*
%{_datadir}/applications/*.desktop

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la

