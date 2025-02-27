%define		realname   libxml2
Summary:	libXML library - cross MinGW32 version
Summary(pl.UTF-8):	Biblioteka libXML wersja 2 - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	2.13.6
Release:	2
License:	MIT
Group:		Development/Libraries
#Source0:	ftp://xmlsoft.org/libxml2/%{realname}-%{version}.tar.gz
Source0:	https://download.gnome.org/sources/libxml2/2.13/%{realname}-%{version}.tar.xz
# Source0-md5:	85dffa2387ff756bdf8b3b247594914a
Patch0:		%{realname}-open.gz.patch
Patch1:		%{realname}-largefile.patch
Patch2:		%{realname}-mingw32.patch
URL:		http://xmlsoft.org/
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.16.3
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-zlib >= 1.2.4-3
BuildRequires:	crossmingw32-xz
BuildRequires:	libtool >= 2:2.0
BuildRequires:	sed >= 4.0
Requires:	crossmingw32-zlib >= 1.2.4-3
Requires:	crossmingw32-xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,--as-needed -Wl,-z,relro -Wl,-z,combreloc
%define		filterout_c	-f[-a-z0-9=]*

%description
This library allows you to manipulate XML files.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Biblioteka libxml2 umożliwia manipulowanie zawartością plików XML.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static libxml2 library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libxml2 (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libxml2 library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libxml2 (wersja skrośna MinGW32).

%package dll
Summary:	DLL libxml2 library for Windows
Summary(pl.UTF-8):	Biblioteka DLL libxml2 dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-zlib-dll >= 1.2.4-3
Requires:	crossmingw32-xz-dll
Requires:	wine

%description dll
DLL libxml2 library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL libxml2 dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# require at least WINXP for getaddrinfo interface
CPPFLAGS="%{rpmcppflags} -DWINVER=0x0501"
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-silent-rules \
	--enable-static \
	--with-http \
	--with-legacy \
	--with-lzma \
	--without-python \
	--with-tls \
	--with-zlib

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{*.exe,xml2-config}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{aclocal,doc,gtk-doc,man}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Copyright NEWS README.md
%dir %{_docdir}
%{_libdir}/libxml2.dll.a
%{_libdir}/libxml2.la
%{_includedir}/libxml2
%{_pkgconfigdir}/libxml-2.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libxml2.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libxml2-*.dll
