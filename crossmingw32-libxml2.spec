%define		realname   libxml2
Summary:	libXML library - cross MinGW32 version
Summary(pl.UTF-8):	Biblioteka libXML wersja 2 - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	2.7.8
Release:	1
License:	MIT
Group:		Development/Libraries
#Source0:	http://ftp.gnome.org/pub/GNOME/sources/libxml2/2.6/%{name}-%{version}.tar.bz2
Source0:	ftp://xmlsoft.org/libxml2/%{realname}-%{version}.tar.gz
# Source0-md5:	8127a65e8c3b08856093099b52599c86
Patch0:		%{realname}-amfix.patch
Patch1:		%{realname}-man_fixes.patch
Patch2:		%{realname}-open.gz.patch
Patch3:		%{realname}-largefile.patch
Patch4:		%{realname}-version-script.patch
URL:		http://xmlsoft.org/
BuildRequires:	autoconf >= 2.2
BuildRequires:	automake >= 1.4
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-zlib >= 1.2.4-3
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	sed >= 4.0
Requires:	crossmingw32-zlib >= 1.2.4-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		filterout_ld		-Wl,--as-needed -Wl,-z,relro -Wl,-z,combreloc

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
Requires:	wine

%description dll
DLL libxml2 library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL libxml2 dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--without-python

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/{aclocal,doc,gtk-doc,man}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog Copyright NEWS README TODO
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
