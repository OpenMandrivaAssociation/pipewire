%define spa_api	0.1
%define api	0.2
%define major	1
%define libname	%mklibname %{name} %{api} %{major}
%define devname	%mklibname %{name} -d

Name:		pipewire
Summary:	Media Sharing Server
Version:	0.2.3
Release:	
License:	LGPLv2+
Group:		System/Servers
URL:		https://pipewire.org/
Source0:	https://github.com/PipeWire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz
## upstream patches

BuildRequires:	doxygen
BuildRequires:	gcc
BuildRequires:	graphviz
BuildRequires:	meson >= 0.35.0
BuildRequires:	xmltoman
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(glib-2.0) >= 2.32
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:	pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-net-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
BuildRequires:	pkgconfig(systemd) >= 184
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(sbc)
BuildRequires:	pkgconfig(sdl2)

Requires:	systemd >= 184
Requires:	rtkit
Requires(pre):	shadow-utils

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

#------------------------------------------------

%package -n	%{libname}
Summary:        Libraries for PipeWire clients
Group:		System/Libraries

%description -n	%{libname}
This package contains the runtime libraries for any application that
wishes to interface with a PipeWire media server.

#------------------------------------------------

%package -n	%{devname}
Summary:        Headers and libraries for PipeWire client development
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	spa-devel = %{version}-%{release}

%description -n	%{devname}
Headers and libraries for developing applications that can communicate
with a PipeWire media server.

#------------------------------------------------

%package	doc
Summary:	PipeWire media server documentation
Group:		Documentation
BuildArch:	noarch
Requires:	%{name} >= %{version}-%{release}

%description	doc
This package contains documentation for the PipeWire media server.

#------------------------------------------------

%package	utils
Summary:	PipeWire media server utilities
Group:		System/Servers

%description	utils
This package contains command line utilities for the PipeWire
media server.

#------------------------------------------------

%package -n	gstreamer1.0-%{name}
Summary:	GStreamer 1.0 plugin for the PipeWire multimedia server
Group:		System/Servers

%description -n	gstreamer1.0-%{name}
GStreamer 1.0 plugin for the PipeWire multimedia server.

#------------------------------------------------

%prep
%setup -q -T -b0

%build
%meson -D docs=true -D man=true -D gstreamer=true -D systemd=true
%meson_build

%install
%meson_install

%check
%meson_test

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d /var/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%files
%license LICENSE GPL LGPL
%doc README
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/%{name}.conf
%{_userunitdir}/%{name}.*
%{_bindir}/%{name}
%{_libdir}/%{name}-%{api}/
%{_libdir}/spa/
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%license LICENSE GPL LGPL
%doc README
%{_libdir}/lib%{name}-%{api}.so.%{major}{,.*}

%files -n %{devname}
%{_includedir}/%{name}/
%{_includedir}/spa/
%{_libdir}/lib%{name}-%{api}.so
%{_libdir}/pkgconfig/lib%{name}-%{api}.pc
%{_libdir}/pkgconfig/libspa-%{spa_api}.pc

%files doc
%{_docdir}/%{name}/html/

%files utils
%{_bindir}/%{name}-monitor
%{_bindir}/%{name}-cli
%{_mandir}/man1/%{name}.conf.5*
%{_mandir}/man1/%{name}-monitor.1*
%{_mandir}/man1/%{name}-cli.1*
%{_bindir}/spa-monitor
%{_bindir}/spa-inspect

%files -n gstreamer1.0-%{name}
%{_libdir}/gstreamer-1.0/libgst%{name}.so
