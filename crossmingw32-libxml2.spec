#
%define		_realname   libxml2
Summary:	libXML library - cross Mingw32 version
Summary(es.UTF-8):Biblioteca libXML version 2
Summary(pl.UTF-8):Biblioteka libXML wersja 2 - wersja skrośna dla Mingw32
Summary(pt_BR.UTF-8):Biblioteca libXML versão 2
Name:		crossmingw32-%{_realname}
Version:	2.6.27
Release:	1
License:	MIT
Group:		Libraries
#Source0:	http://ftp.gnome.org/pub/GNOME/sources/libxml2/2.6/%{name}-%{version}.tar.bz2
Source0:	ftp://xmlsoft.org/libxml2/%{_realname}-%{version}.tar.gz
# Source0-md5:	f5806f5059ef7bd4d3fcf36cf116d1ef
Patch0:		%{name}-noexamples.patch
Patch1:		%{_realname}-man_fixes.patch
Patch2:		%{_realname}-open.gz.patch
Patch3:		%{_realname}-DESTDIR.patch
URL:		http://xmlsoft.org/
BuildRequires:	autoconf >= 2.2
BuildRequires:	automake
BuildRequires:	crossmingw32-zlib
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	sed >= 4.0
Obsoletes:	xml-common
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
This library allows you to manipulate XML files.

%description -l es.UTF-8
Esta biblioteca permite manipulación de archivos XML.

%description -l pl.UTF-8
Biblioteka libxml2 umożliwia manipulowanie zawartością plików XML.

%description -l pt_BR.UTF-8
Esta biblioteca permite a manipulação de arquivos XML.

%prep
%setup -q -n %{_realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e 's,-L/usr/lib64,-L/usr/%{_lib},' xml2-config.in

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	m4datadir=%{_aclocaldir} \
	pkgconfigdir=%{_pkgconfigdir}

# install catalog file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog Copyright NEWS README TODO
%{_libdir}/lib*.la
%{_libdir}/lib*.a
%{_bindir}/*.dll

#%dir %{_prefix}/%{_sysconfdir}/xml
#%config(noreplace) %verify(not md5 mtime) %{_sysconfdir}/xml/catalog

%attr(755,root,root) %{_bindir}/xml2-config
%{_pkgconfigdir}/*
%{_aclocaldir}/*.m4
%{_includedir}/libxml2
