# enable_by_default: Toggle if pipewire should be enabled by default and/or replace PulseAudio.
#      0 = no
#      1 = yes
%define enable_by_default 0


%ifarch %{ix86}
%define _disable_ld_no_undefined 1
%define _disable_lto 1
%endif

%define spa_api	0.2
%define api	0.3
%define major	0
%define libname	%mklibname %{name} %{api} %{major}
%define devname	%mklibname %{name} -d

Name:		pipewire
Summary:	Media Sharing Server
Version:	0.3.29
Release:	1
License:	LGPLv2+
Group:		System/Servers
URL:		https://pipewire.org/
Source0:	https://github.com/PipeWire/pipewire/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:		0001-conf-start-media-session-through-pipewire.patch

BuildRequires:	doxygen
BuildRequires:  gettext
BuildRequires:	gcc
BuildRequires:	graphviz
BuildRequires:	meson
#BuildRequires:	xmltoman
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:  pkgconfig(bluez)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(glib-2.0) >= 2.32
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:	pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-net-1.0) >= 1.10.0
BuildRequires:	pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(ldacBT-enc)
BuildRequires:	pkgconfig(ldacBT-abr)
BuildRequires:	pkgconfig(libopenaptx)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libv4l2)
BuildRequires:	pkgconfig(sbc)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	vulkan-headers
BuildRequires:	xmltoman
BuildRequires:  llvm-devel

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
%package alsa
Summary:        PipeWire media server ALSA support
License:        MIT
Recommends:     %{name} = %{version}-%{release}

%description alsa
This package contains an ALSA plugin for the PipeWire media server.

#------------------------------------------------

%package libjack
Summary:        PipeWire libjack library
License:        MIT
Recommends:     %{name} = %{version}-%{release}
Obsoletes:      pipewire-jack < 0.2.96-2

%description libjack
This package contains a PipeWire replacement for JACK audio connection kit
"libjack" library.

#------------------------------------------------

%package plugin-jack
Summary:        PipeWire media server JACK support
License:        MIT
Recommends:     %{name} = %{version}-%{release}

%description plugin-jack
This package contains the PipeWire spa plugin to connect to a JACK server.

#------------------------------------------------

%prep
%autosetup -T -b0 -p1

%build
# Build failing on i686 with Clang with error:
#ld: error: undefined symbol: __atomic_store_8
#>>> referenced by pipewire-jack.c:3977 (../pipewire-jack/src/pipewire-jack.c:3977)
#lto.tmp:(jack_set_sync_timeout)

%ifarch %{ix86}
export CC=gcc
export CXX=g++
%endif
%meson -D docs=enabled -D man=enabled -D gstreamer=enabled -D systemd=enabled -D pipewire-pulseaudio=enabled -D jack=enabled -D pipewire-jack=enabled -D pipewire-pulseaudio=enabled -D vulkan=enabled -D pipewire-alsa=enabled -D bluez5-codec-aac=disabled -D bluez5-codec-aptx=disabled -D libcamera=disabled -D ffmpeg=enabled --buildtype=release
%meson_build

%install
%meson_install

# upstream should use udev.pc
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pipewire-alsa.rules %{buildroot}%{_prefix}/lib/udev/rules.d

# Test fail on ARMv7hnl
%ifnarch %{arm}
%check
%meson_test
%endif

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d /var/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0



#              Attention! Achtung! Uwaga! Attenzione!                     #
###########################################################################
# PipeWire can replace (and probably will) PulseAudio and become default  #
#        It is currently disabled, to activate it togle ON switch         #
#             Don't do this without consulting with OMV Team.             #
###########################################################################

%if %enable_by_default
%post
%systemd_user_post pipewire.service
%systemd_user_post pipewire.socket
	
%systemd_user_post pipewire-pulse.service
%systemd_user_post pipewire-pulse.socket
%endif


%files
%license LICENSE
%doc README.md
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}.conf
%{_datadir}/pipewire/client.conf
%{_datadir}/pipewire/client-rt.conf
%{_datadir}/pipewire/jack.conf
%{_datadir}/pipewire/pipewire-pulse.conf
%{_datadir}/pipewire/media-session.d/*
%{_userunitdir}/%{name}.*
%{_bindir}/%{name}
%{_bindir}/%{name}-media-session
%{_bindir}/pipewire-pulse
%dir %{_libdir}/%{name}-%{api}/
%{_libdir}/%{name}-%{api}/libpipewire-module-*.so
%{_libdir}/spa-%{spa_api}
%{_mandir}/man5/*.5*
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%{_datadir}/alsa-card-profile/mixer/paths/*
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%{_datadir}/locale/*/LC_MESSAGES/pipewire.mo
%{_userunitdir}/pipewire-pulse.*
%{_userunitdir}/pipewire-media-session.service
%{_prefix}/lib/udev/rules.d/90-pipewire-alsa.rules
%{_datadir}/pipewire/filter-chain/*.conf

%files -n %{libname}
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}-%{api}.so.%{major}{,.*}

%files -n %{devname}
%{_includedir}/%{name}-%{api}/%{name}*
%{_includedir}/spa-%{spa_api}
%{_libdir}/lib%{name}-%{api}.so
%{_libdir}/pkgconfig/lib%{name}-%{api}.pc
%{_libdir}/pkgconfig/libspa-%{spa_api}.pc

%files doc
%{_docdir}/%{name}/html/

%files utils
%{_bindir}/spa-monitor
%{_bindir}/spa-inspect
%{_bindir}/spa-json-dump
%{_bindir}/pw-mon
%{_bindir}/pw-cat
%{_bindir}/pw-cli
%{_bindir}/pw-dot
%{_bindir}/pw-link
%{_bindir}/pw-loopback
%{_bindir}/pw-metadata
%{_bindir}/pw-mididump
%{_bindir}/pw-midiplay
%{_bindir}/pw-midirecord
%{_bindir}/pw-play
%{_bindir}/pw-record
%{_bindir}/pw-profiler
%{_bindir}/pw-reserve
%{_bindir}/pw-top
%{_bindir}/pw-dump
%{_bindir}/spa-acp-tool
%{_bindir}/spa-resample
%{_mandir}/man1/*.1*

%files -n gstreamer1.0-%{name}
%{_libdir}/gstreamer-1.0/libgst%{name}.so

%files alsa
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so

%files libjack
%{_bindir}/pw-jack
%{_libdir}/pipewire-%{api}/jack

%files plugin-jack
%{_libdir}/spa-%{spa_api}/jack/
